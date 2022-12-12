import os
import time

device_code = os.popen("wmic cpu get processorid | findstr -v ProcessorId").read().strip()
print(device_code)
time.sleep(30)