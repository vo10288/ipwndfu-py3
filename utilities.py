#!/Users/CFDA_BOLOGNA/opt/anaconda3/bin/python
import subprocess, sys

def apply_patches(binary, patches):
    """Apply binary patches to data"""
    for (offset, data) in patches:
        # Ensure data is bytes
        if isinstance(data, str):
            data = data.encode('latin-1')
        if isinstance(binary, str):
            binary = binary.encode('latin-1')
        
        binary = binary[:offset] + data + binary[offset + len(data):]
    return binary

def aes_decrypt(data, iv, key):
    """Decrypt data using AES with OpenSSL"""
    # Convert to bytes if needed
    if isinstance(data, str):
        data = data.encode('latin-1')
    if isinstance(iv, str):
        iv = iv.encode('ascii')
    if isinstance(key, str):
        key = key.encode('ascii')
    
    if len(key) == 32:  # 32 hex chars = 128 bits
        aes = 128
    elif len(key) == 64:  # 64 hex chars = 256 bits
        aes = 256
    else:
        print('ERROR: Bad AES key given to aes_decrypt. Exiting.')
        sys.exit(1)

    # Convert iv and key to string for command line
    iv_str = iv.decode('ascii') if isinstance(iv, bytes) else iv
    key_str = key.decode('ascii') if isinstance(key, bytes) else key

    p = subprocess.Popen(['openssl', 'enc', '-aes-%s-cbc' % aes, '-d', '-nopad', '-iv', iv_str, '-K', key_str],
                       stdout=subprocess.PIPE,
                       stdin=subprocess.PIPE,
                       stderr=subprocess.PIPE)
    (stdout, stderr) = p.communicate(input=data)

    if p.returncode != 0 or len(stderr) > 0:
        error_msg = stderr.decode('utf-8', errors='ignore') if isinstance(stderr, bytes) else stderr
        print('ERROR: openssl failed: %s' % error_msg)
        sys.exit(1)

    return stdout

def hex_dump(data, address):
    """Create hex dump of binary data using xxd"""
    # Ensure data is bytes
    if isinstance(data, str):
        data = data.encode('latin-1')
    
    p = subprocess.Popen(['xxd', '-o', str(address)], 
                        stdin=subprocess.PIPE, 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
    (stdout, stderr) = p.communicate(input=data)

    if p.returncode != 0 or len(stderr) > 0:
        error_msg = stderr.decode('utf-8', errors='ignore') if isinstance(stderr, bytes) else stderr
        print('ERROR: xxd failed: %s' % error_msg)
        sys.exit(1)

    # Return as string for compatibility
    return stdout.decode('utf-8', errors='ignore') if isinstance(stdout, bytes) else stdout

def hex_to_bytes(hex_str):
    """Convert hex string to bytes (Python 3 helper)"""
    if isinstance(hex_str, str):
        return bytes.fromhex(hex_str)
    return hex_str

def bytes_to_hex(data):
    """Convert bytes to hex string (Python 3 helper)"""
    if isinstance(data, bytes):
        return data.hex()
    return data
