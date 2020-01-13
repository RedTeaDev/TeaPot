from redtea import redtea
from configparser import ConfigParser
import os
tokenget = input("Please Type Your Discord Bot Token>>>")
try:
    config = ConfigParser()

    config['Main'] = {
        'Token': tokenget,
        'SaveFile': 'false'
    }
    with open('./config.ini', 'w') as file:
       print("[*] Writing config to ./config.ini ....")
       redtea.sleep(1.55)
       config.write(file)
       print("[*] Susses build Config.ini!")
except Exception as error:
    print("[!] FAIL to build Config File,make sure you have permission to write! Error>>" + str(fail))
    redtea.sleep(10)
    exit(1)
print("Done!")
redtea.sleep(5)
exit(1)
