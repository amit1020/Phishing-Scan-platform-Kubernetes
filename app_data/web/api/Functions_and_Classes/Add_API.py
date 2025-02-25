import sys,os,mysql.connector,time,configparser
from mysql.connector import Error
from dotenv import load_dotenv
from functools import wraps
from pathlib import Path

#Encryption and Decryption modules
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from binascii import hexlify
import base64

sys.stdout.reconfigure(encoding='utf-8')


API_LIST = ['virustotal','urlscan']


def encrypt_message(message: str) -> str:
    public_key_path = Path(__file__).parent.parent.parent.parent / "keys" / "Public.pem"
    
    with open(public_key_path, "rb") as file:  # Open the public key file
        public_key = RSA.import_key(file.read())

    cipher_rsa = PKCS1_OAEP.new(public_key)  # Create a new PKCS1_OAEP object
    encrypted_data = cipher_rsa.encrypt(message.encode("utf-8"))  # Convert message to bytes and encrypt

    return base64.b64encode(encrypted_data).decode("utf-8")  # Properly encode to Base64

    




def connect_with_retry(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        delay=5
        retries=10
        for attempt in range(retries):
            try:
                env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.env_user_db"))
                load_dotenv(env_path)
                    #print(f" Attempting MySQL connection (Try {attempt + 1}/{retries})...")
                    #creates the connection var 
                connection = mysql.connector.connect(
                    host=os.getenv("MYSQL_HOST"),
                    user="root",
                    password=os.getenv("MYSQL_ROOT_PASSWORD"),
                    database=os.getenv("MYSQL_DATABASE"),
                    port=int(os.getenv("MYSQL_PORT", "3306")),
                    charset="utf8mb4"
                )
                    
                if connection.is_connected():
                    #?If the connection is success, create the cursor and build the database
                    func(connection)
                    return 
                   
                    
            except mysql.connector.Error as err:
                time.sleep(delay)
        #If the connection is unable to connect after multiple retries, raise an exception 
        raise Exception("MySQL is not available after multiple retries.")
    return wrapper






@connect_with_retry
def add_api_values(connection_):
    
    #*Get the data from the env file
    api_env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.env_api"))
    load_dotenv(api_env_path)

    mycursor = connection_.cursor()
    
    for _ in API_LIST:
        try:
            mycursor = connection_.cursor()
            sql = "INSERT INTO API_Table (api_website_name, value) VALUES (%s, %s)"
            
            print(_,os.getenv(_),flush=True)
            en_data = encrypt_message(os.getenv(_))#Encrypt the API key
            val = (_,en_data)
            mycursor.execute(sql, val)
            connection_.commit()
        except Error as e:
            print(f"Error: '{e}'")
            pass
    
    
    
#add_api_values()        

    








