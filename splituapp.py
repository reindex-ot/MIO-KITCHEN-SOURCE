#!/usr/bin/env python

# split_app for Python2/3 by SuperR. @XDA
#
# For extracting img files from UPDATE.APP

# Based on the app_structure file in split_up_data.pl by McSpoon


from os import makedirs, sep, path
from string import printable
from struct import unpack


def extract(source, out_dir: str, flist: list):
    byte_num = 4
    img_files = []

    try:
        makedirs(out_dir, exist_ok=True)
    finally:
        ...
    if not path.exists(source):
        print('The File Not Exist!')
        return 
    with open(source, 'rb') as f:
        while True:
            i = f.read(byte_num)

            if not i:
                break
            elif i != b'\x55\xAA\x5A\xA5':
                continue

            header_size = list(unpack('<L', f.read(byte_num)))[0]
            f.seek(16, 1)
            file_size = list(unpack('<L', f.read(byte_num)))[0]
            f.seek(32, 1)

            try:
                filename = str(f.read(16).decode())
                filename = ''.join(f for f in filename if f in printable).lower()
            except Exception or BaseException:
                filename = ''

            f.seek(22, 1)
            # Its Crc_data
            f.read(header_size - 98)

            if not flist or filename in flist:
                if filename in img_files:
                    filename = filename + '_2'

                print(f'Extracting {filename}.img ...')

                chunk = 10240

                try:
                    with open(out_dir + sep + filename + '.img', 'wb') as o:
                        while file_size > 0:
                            chunk = min(chunk, file_size)

                            o.write(f.read(chunk))
                            file_size -= chunk
                except Exception as e:
                    print(f'ERROR: Failed to create {filename}.img:%s\n' % e)
                    return

                img_files.append(filename)
            else:
                f.seek(file_size, 1)

            x_bytes = byte_num - f.tell() % byte_num
            if x_bytes < byte_num:
                f.seek(x_bytes, 1)

    print('Extraction complete')


def get_parts(source):
    byte_num = 4

    with open(source, 'rb') as f:
        while True:
            i = f.read(byte_num)

            if not i:
                break
            elif i != b'\x55\xAA\x5A\xA5':
                continue

            header_size = list(unpack('<L', f.read(byte_num)))[0]
            f.seek(16, 1)
            file_size = list(unpack('<L', f.read(byte_num)))[0]
            f.seek(32, 1)

            try:
                filename = str(f.read(16).decode())
                filename = ''.join(f for f in filename if f in printable).lower()
            except Exception or BaseException:
                filename = ''

            f.seek(22, 1)
            # Its Crc_data
            f.read(header_size - 98)
            f.seek(file_size, 1)

            x_bytes = byte_num - f.tell() % byte_num
            if x_bytes < byte_num:
                f.seek(x_bytes, 1)
            if filename:
                yield filename
