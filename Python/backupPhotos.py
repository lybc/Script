from qiniu import Auth,BucketManager

ak = "YpnVTDmGWRunHJhW6H-xAtMXrJA8UPOUVfeHH0t2"
sk = "QKPgIouMmu-niYkzID7xzvgxrsR2f24x1FFzwpBj"
q = Auth(access_key=ak, secret_key=sk)
bucket = BucketManager(q)
ret, eof, info = bucket.list("jiaozi", limit=100)
print(info)
