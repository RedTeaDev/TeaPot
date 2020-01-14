from configparser import ConfigParser

from redtea import redtea

input = input("Type in your discord bot token >")
try:
    config = ConfigParser()

    config['Main'] = {
        'Token': input,
        'SaveFile': 'false'
    }
    with open('./config.ini', 'w') as file:
        print("[*] Writing config to ./config.ini ....")
        config.write(file)
        print("[*] Successfully created config.ini!")
except Exception as error:
    print("[!] Failed to create config file. Error>>" + str(error))
    redtea.sleep(10)
    exit(1)
print("Done!")
redtea.sleep(5)
exit(1)
