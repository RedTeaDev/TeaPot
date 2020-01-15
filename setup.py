import getpass
from configparser import ConfigParser

from redtea import redtea

# Declare default configuration
input_mysql_host = "localhost"
input_mysql_schema = "teapot"
input_mysql_user = "root"
input_mysql_password = ""

print("""

  _____                      _      ____             __ _                       _             
 |_   _|__  __ _ _ __   ___ | |_   / ___|___  _ __  / _(_) __ _ _   _ _ __ __ _| |_ ___  _ __ 
   | |/ _ \/ _` | '_ \ / _ \| __| | |   / _ \| '_ \| |_| |/ _` | | | | '__/ _` | __/ _ \| '__|
   | |  __/ (_| | |_) | (_) | |_  | |__| (_) | | | |  _| | (_| | |_| | | | (_| | || (_) | |   
   |_|\___|\__,_| .__/ \___/ \__|  \____\___/|_| |_|_| |_|\__, |\__,_|_|  \__,_|\__\___/|_|   
                |_|         by RedTea and ColaIan         |___/                               
                           
                  NOTE: You can change the settings later in config.ini :3
     
""")

input_token = input("Discord bot token: ")
input_storage_type = input("Use MySQL? [Y/n] ")
if input_storage_type.lower() == "y":
    input_storage_type = "mysql"
    input_mysql_host = input("Database Host: ")
    input_mysql_schema = input("Database Schema: ")
    input_mysql_user = input("Database User: ")
    input_mysql_password = getpass.getpass(prompt="Database Password: ")
elif input_storage_type.lower() == "n":
    input_storage_type = "flatfile"
else:
    input_storage_type = "flatfile"
    print("[!] Your input was not valid, and has been automagically set to flatfile storage.")

try:
    config = ConfigParser()

    config['Main'] = {
        'version': '0.1',
        'token': input_token,
        'storage_type': input_storage_type
    }

    config['MySQL'] = {
        'host': input_mysql_host,
        'database': input_mysql_schema,
        'user': input_mysql_user,
        'password': input_mysql_password
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
