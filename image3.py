#!/Users/CFDA_BOLOGNA/opt/anaconda3/bin/python
import binascii, struct
import dfuexec, utilities

class Image3:
    def __init__(self, data):
        # Ensure data is bytes
        if isinstance(data, str):
            data = data.encode('latin-1')
            
        (self.magic, self.totalSize, self.dataSize, self.signedSize, self.type) = struct.unpack('4s3I4s', data[0:20])
        self.tags = []
        pos = 20
        while pos < 20 + self.dataSize:
            if pos + 12 > len(data):
                break
            (tagMagic, tagTotalSize, tagDataSize) = struct.unpack('4s2I', data[pos:pos+12])
            if tagTotalSize == 0 or pos + tagTotalSize > len(data):
                break
            self.tags.append((tagMagic, tagTotalSize, tagDataSize, data[pos+12:pos+tagTotalSize]))
            pos += tagTotalSize

    @staticmethod
    def createImage3FromTags(type, tags):
        dataSize = 0
        signedSize = 0
        for (tagMagic, tagTotalSize, tagDataSize, tagData) in tags:
            dataSize += 12 + len(tagData)
            if tagMagic[::-1] not in [b'CERT', b'SHSH']:
                signedSize += 12 + len(tagData)

        # totalSize must be rounded up to 64-byte boundary
        totalSize = 20 + dataSize
        remainder = totalSize % 64
        if remainder != 0:
            totalSize += 64 - remainder

        # Ensure type is bytes
        if isinstance(type, str):
            type = type.encode('ascii')

        bytes_data = struct.pack('4s3I4s', b'Img3'[::-1], totalSize, dataSize, signedSize, type)
        for (tagMagic, tagTotalSize, tagDataSize, tagData) in tags:
            bytes_data += struct.pack('4s2I', tagMagic, tagTotalSize, tagDataSize) + tagData
        return bytes_data + b'\x00' * (totalSize - len(bytes_data))

    def getTags(self, magic):
        # Ensure magic is bytes
        if isinstance(magic, str):
            magic = magic.encode('ascii')
            
        matches = []
        for tag in self.tags:
            if tag[0] == magic:
                matches.append(tag)
        return matches

    def getKeybag(self):
        keybags = self.getTags(b'KBAG'[::-1])
        for (tagMagic, tagTotalSize, tagDataSize, tagData) in keybags:
            if len(tagData) >= 8:
                (kbag_type, aes_type) = struct.unpack('<2I', tagData[:8])
                if kbag_type == 1:
                    return tagData[8:8+48]
        return None

    def getPayload(self):
        data = self.getTags(b'DATA'[::-1])
        if len(data) == 1:
            return data[0][3]

    def getDecryptedPayload(self):
        try:
            keybag = self.getKeybag()
            if keybag is None:
                return None
                
            device = dfuexec.PwnedDFUDevice()
            decrypted_keybag = device.decrypt_keybag(keybag)
            
            payload = self.getPayload()
            if payload is None:
                return None
                
            iv_hex = binascii.hexlify(decrypted_keybag[:16]).decode('ascii')
            key_hex = binascii.hexlify(decrypted_keybag[16:]).decode('ascii')
            
            return utilities.aes_decrypt(payload, iv_hex, key_hex)
        except Exception:
            return None

    def shrink24KpwnCertificate(self):
        for i in range(len(self.tags)):
            tag = self.tags[i]
            if tag[0] == b'CERT'[::-1] and len(tag[3]) >= 3072:
                data = tag[3][:3072]
                # Handle bytes properly for Python 3
                if isinstance(data, bytes):
                    # Find the last non-null byte
                    data = data.rstrip(b'\x00')
                else:
                    data = data.rstrip('\x00').encode('latin-1')
                self.tags[i] = (b'CERT'[::-1], 12 + len(data), len(data), data)
                break

    def newImage3(self, decrypted=True):
        typeTag = self.getTags(b'TYPE'[::-1])
        assert len(typeTag) == 1
        versTag = self.getTags(b'VERS'[::-1])
        assert len(versTag) <= 1
        dataTag = self.getTags(b'DATA'[::-1])
        assert len(dataTag) == 1
        sepoTag = self.getTags(b'SEPO'[::-1])
        assert len(sepoTag) <= 2
        bordTag = self.getTags(b'BORD'[::-1])
        assert len(bordTag) <= 2
        kbagTag = self.getTags(b'KBAG'[::-1])
        assert len(kbagTag) <= 2
        shshTag = self.getTags(b'SHSH'[::-1])
        assert len(shshTag) <= 1
        certTag = self.getTags(b'CERT'[::-1])
        assert len(certTag) <= 1

        (tagMagic, tagTotalSize, tagDataSize, tagData) = dataTag[0]
        if len(kbagTag) > 0 and decrypted:
            newTagData = self.getDecryptedPayload()
            if newTagData is None:
                newTagData = tagData
            kbagTag = []
        else:
            newTagData = tagData
        
        # Ensure lengths match
        if len(newTagData) != len(tagData):
            # Pad or truncate as needed
            if len(newTagData) < len(tagData):
                newTagData += b'\x00' * (len(tagData) - len(newTagData))
            else:
                newTagData = newTagData[:len(tagData)]

        return Image3.createImage3FromTags(self.type, typeTag + [(tagMagic, tagTotalSize, tagDataSize, newTagData)] + versTag + sepoTag + bordTag + kbagTag + shshTag + certTag)
