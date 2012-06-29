import magic

def read_file(filename):
    m = magic.open(magic.MIME)
    m.load()
    mm = m.file(filename)
    m.close()
    return mm
