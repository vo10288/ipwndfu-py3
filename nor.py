#!/Users/CFDA_BOLOGNA/opt/anaconda3/bin/python
import binascii, struct

NOR_SIZE = 0x100000

class NorData():
    def __init__(self, dump):
        # Ensure dump is bytes
        if isinstance(dump, str):
            dump = dump.encode('latin-1')
        
        assert len(dump) == NOR_SIZE

        (img2_magic, self.block_size, unused, firmware_block, firmware_block_count) = struct.unpack('<4s4I', dump[:20])
        (img2_crc,) = struct.unpack('<I', dump[48:52])
        
        # Calculate CRC32 for verification
        calculated_crc = binascii.crc32(dump[:48]) & 0xffffffff
        assert img2_crc == calculated_crc

        self.firmware_offset = self.block_size * firmware_block
        self.firmware_length = self.block_size * firmware_block_count
        
        self.parts = [
            dump[0:52],
            dump[52:512],
            dump[512:self.firmware_offset],
            dump[self.firmware_offset:self.firmware_offset + self.firmware_length],
            dump[self.firmware_offset + self.firmware_length:]
        ]

        self.images = []
        offset = 0
        while True:
            if offset + 8 > len(self.parts[3]):
                break
                
            (magic, size) = struct.unpack('<4sI', self.parts[3][offset:offset+8])
            
            # Check for Img3 magic (reversed)
            if magic != b'Img3'[::-1] or size == 0:
                break
                
            if offset + size > len(self.parts[3]):
                break
                
            self.images.append(self.parts[3][offset:offset + size])
            offset += size

    def dump(self):
        """Reconstruct NOR dump from parts and images"""
        # Replace self.parts[3] with content of self.images
        all_images = b''.join(self.images)
        
        # Pad with 0xFF bytes to firmware_length
        padding_needed = self.firmware_length - len(all_images)
        if padding_needed > 0:
            all_images += b'\xff' * padding_needed
        
        # Reconstruct the full dump
        dump = self.parts[0] + self.parts[1] + self.parts[2] + all_images + self.parts[4]
        
        assert len(dump) == NOR_SIZE
        return dump

    def get_image_by_type(self, image_type):
        """Get image by type (e.g., 'illb', 'ibot')"""
        if isinstance(image_type, str):
            image_type = image_type.encode('ascii')
        
        for image in self.images:
            if len(image) >= 12:
                # Check image type at offset 8
                img_type = image[8:12]
                if img_type == image_type:
                    return image
        return None

    def replace_image(self, old_image, new_image):
        """Replace an image in the images list"""
        for i, image in enumerate(self.images):
            if image == old_image:
                self.images[i] = new_image
                return True
        return False

    def add_image(self, image_data):
        """Add a new image to the images list"""
        if isinstance(image_data, str):
            image_data = image_data.encode('latin-1')
        self.images.append(image_data)

    def remove_image(self, image_data):
        """Remove an image from the images list"""
        if image_data in self.images:
            self.images.remove(image_data)
            return True
        return False

    def get_images_info(self):
        """Get information about all images"""
        info = []
        for i, image in enumerate(self.images):
            if len(image) >= 12:
                magic = image[0:4]
                size = struct.unpack('<I', image[4:8])[0]
                img_type = image[8:12]
                info.append({
                    'index': i,
                    'magic': magic,
                    'size': size,
                    'type': img_type,
                    'data_length': len(image)
                })
        return info
