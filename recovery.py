#!/Users/CFDA_BOLOGNA/opt/anaconda3/bin/python
import sys, time
import usb # pyusb: use 'pip install pyusb' to install this module
import usb.backend.libusb1
import libusbfinder

MAX_PACKET_SIZE = 0x4000

def acquire_device(timeout=10):
    backend = usb.backend.libusb1.get_backend(find_library=lambda x:libusbfinder.libusb1_path())
    #print('Acquiring device handle')
    start = time.time()
    # Keep retrying for up to timeout seconds if device is not found.
    while time.time() - start < timeout:
        device = usb.core.find(idVendor=0x5AC, idProduct=0x1281, backend=backend)
        if device is not None:
            return device
        sys.stdout.flush()
        time.sleep(0.1)
    print('ERROR: No Apple device in Recovery Mode 0x1281 detected. Exiting.')
    sys.exit(1)

def release_device(device):
    #print('Releasing device handle.')
    usb.util.dispose_resources(device)

def send_command(device, command):
    # Convert command to bytes if it's a string
    if isinstance(command, str):
        command = command.encode('utf-8')
    
    # TODO: Add assert?
    device.ctrl_transfer(0x40, 0, 0, 0, command + b'\x00', 30000)

def send_data(device, data):
    #print('Sending 0x%x of data to device.' % len(data))
    
    # Ensure data is bytes
    if isinstance(data, str):
        data = data.encode('latin-1')
    
    assert device.ctrl_transfer(0x41, 0, 0, 0, 0, 1000) == 0
    index = 0
    while index < len(data):
        amount = min(len(data) - index, MAX_PACKET_SIZE)
        chunk = data[index:index + amount]
        assert device.write(0x04, chunk, 1000) == amount
        index += amount
