# coding=utf-8

import hashlib

if __name__=="__main__":
    timestamp = "1695606508"
    nonce = "1037502139"
    token = "voyagerke"
    list = [token, timestamp, nonce]
    list.sort()

    sha1 = hashlib.sha1()
    # map(sha1.update, list)
    sha1.update("".join(list).encode('utf-8')) 
    hashcode = sha1.hexdigest()
    print(f'hashcode: {hashcode}')
