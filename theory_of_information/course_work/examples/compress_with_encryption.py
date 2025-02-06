import py7zr

with py7zr.SevenZipFile('target.7z', 'w', password='secret') as archive:
    archive.writeall('/path/to/base_dir', 'base')