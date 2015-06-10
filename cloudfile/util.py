from hashlib import md5

def gen_md5(p):
    '''
    Return the MD5 checksum for the file at pathname p
    '''
    BSIZE = 2**20
    hasher = md5()
    with open(p) as f:
        chunk = f.read(BSIZE)
        while len(chunk) > 0:
            hasher.update(chunk)
            chunk = f.read(BSIZE)
    return hasher.hexdigest()
