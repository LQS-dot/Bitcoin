import hashlib,base64
import time


license = input("请输入设备码:")
device_code = license + "lqs"
hash = hashlib.md5()
hash.update(base64.b64encode(device_code.encode('utf-8')))
hash_value = hash.hexdigest()
print (hash_value)
time.sleep(30)