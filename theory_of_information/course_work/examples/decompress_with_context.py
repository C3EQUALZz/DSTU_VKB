import py7zr

with py7zr.SevenZipFile('sample.7z', mode='r') as z:
    z.extractall()

with py7zr.SevenZipFile('target.7z', 'w') as z:
    z.writeall('./base_dir')
