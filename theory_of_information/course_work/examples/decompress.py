import py7zr

archive = py7zr.SevenZipFile('sample.7z', mode='r')
archive.extractall(path="/tmp")
archive.close()