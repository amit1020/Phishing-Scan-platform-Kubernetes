import pyotp,qrcode,PIL, bcrypt,phonenumbers,re,requests
from email_validator import validate_email, EmailNotValidError
from functools import lru_cache
import dns.resolver
#Encryption and Decryption modules
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

#This module converts binary data to Hexadecimal
from binascii import hexlify








#! ------------------ Encryption and Decryption functions --------------

"""
def generate_key():
    PrivateKey = RSA.generate(2048) #Generate an RSA key of length 2048 bits
    PublicKey = PrivateKey.publickey() #Extract the public key from the private key
    with open("./Public.pem", "wb") as file: #Open a file to write the private key
        file.write(PublicKey.export_key())
    return PrivateKey,PublicKey
    
    
private,public = generate_key()
data = encrypt_message(public,"Hello World")
time.sleep(2)
Decrypt_(private,data)


"""

def encrypt_message(public_key,message:str):
    message = message.encode("utf-8") #Convert the message to bytes
    cipher_rsa = PKCS1_OAEP.new(public_key) #Create a new PKCS1_OAEP object with the public key
    
    encrypted_data = cipher_rsa.encrypt(message) #Encrypt the message
    print(f"Encrypted: {hexlify(encrypted_data)}") #Print the encrypted message
    
    return encrypted_data
    
    
    
    
def Decrypt_(private_key,encrypted_data):
    cipher_rsa = PKCS1_OAEP.new(private_key) #Create a new PKCS1_OAEP object with the private key
    decrypted_data = cipher_rsa.decrypt(encrypted_data) #Decrypt the message
    print(f"Decrypted: {decrypted_data.decode('utf-8')}") #Print the decrypted message



#! ------------------ Hashing functions --------------

def HashPassword(pass_:str):
    _ = pass_.encode('utf-8')  # Convert password to bytes
    hashed = bcrypt.hashpw( _ , bcrypt.gensalt())
    return hashed



def VertifyPassword(pass_:str,hashed_pass:str):
    _ = pass_.encode('utf-8')  # Convert password to bytes
    return bcrypt.checkpw(_, hashed_pass)







#! ------------------ 2FA functions --------------

# Generate a 2FA secret
def generate_2fa_secret():
    totp = pyotp.TOTP(pyotp.random_base32())
    return totp.secret #! This is the secret key that be stored in the database


def Create_QR(key:str,name:str) -> bool:
    if key == None or name == None:
        return False
    try:
        uri = pyotp.totp.TOTP(key).provisioning_uri(name=name, 
                                                issuer_name="Phishing_Scan_Platform")#create the uri - URL identification of the 2FA 
        
        QRC = qrcode.make(uri).save(f"{name}.png") #Create the QR code and save it to the file
        return True
    except Exception as e:
        print(e)#!Remove this line
        return False
    
    

#Vertify the OTP
def verify_otp(secret_key, otp):
    return pyotp.TOTP(secret_key).verify(otp,valid_window=0) #! This is the secret key that be stored in the database






#*------------------------Validate data functions------------------------
  
# Convert phone number to E.164 format
def format_without_extension(phone_number, region="IL"):
    """Formats a phone number to E.164 format."""
    try:
        parsed_number = phonenumbers.parse(phone_number, region)
        return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
    except phonenumbers.NumberParseException:
        return None  # Return None for invalid numbers

class ValidData:
    def __init__(self, data: dict):
        if data is None:
            raise ValueError("Data is missing")
        
        self.email = data.get("email")
        self.phone_number = data.get("phone_number")
        self.password = data.get("password")

        if not self.email or not self.phone_number or not self.password:
            raise ValueError("Missing required fields: email, phone_number, password")

    def __call__(self, region="IL") -> tuple[bool, str]:
        """Main function to validate user email, phone, and password."""
        #Validate email
        email_valid, email_message = self.validate_user_email()
        if not email_valid:
            return False, email_message

        #Validate phone number
        phone_valid, phone_message = self.validate_user_phone(region)
        if not phone_valid:
            return False, phone_message

        #Validate password
        password_valid, password_message = self.validate_password()
        if not password_valid:
            return False, password_message

        return True, "All data is valid"

    #*---------- Phone Validation ----------------
    def validate_user_phone(self, region) -> tuple[bool, str]:
        """Validates user phone number."""
        formatted_number = format_without_extension(self.phone_number, region)
        if not formatted_number:
            return False, "Invalid phone number"
        
        try:
            parsed_number = phonenumbers.parse(formatted_number, region)
            if phonenumbers.is_valid_number(parsed_number) and phonenumbers.is_possible_number(parsed_number):
                return True, "Valid phone number"
            return False, "Invalid phone number"
        except phonenumbers.NumberParseException:
            return False, "Invalid phone number"

    #*---------- Email Validation ----------------
    def validate_user_email(self) -> tuple[bool, str]:
        """Validates email format and checks if domain has valid MX records."""
        try:
            valid_email = validate_email(self.email, check_deliverability=True).normalized
            
            #Extra MX record check for more accuracy
            if not self.domain_has_mx_record():
                return False, "Invalid email: No mail server found"

            return True, f"Valid email: {valid_email}"

        except EmailNotValidError:
            return False, "Invalid email address"

    def domain_has_mx_record(self) -> bool:
        """Checks if the domain has valid MX records."""
        try:
            domain = self.email.split('@')[-1]  # Extract domain
            mx_records = dns.resolver.resolve(domain, 'MX')
            return bool(mx_records)  # Returns True if MX records exist
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout):
            return False  # No mail server found

    #*---------- Password Validation ----------------
    def validate_password(self) -> tuple[bool, str]:
        """Checks password strength based on predefined security rules."""
        if len(self.password) < 8:
            return False, "Password must be at least 8 characters long"
        if not re.search(r"[A-Z]", self.password) or not re.search(r"[a-z]", self.password):
            return False, "Password must contain both uppercase and lowercase letters"
        if not re.search(r"\d", self.password):
            return False, "Password must contain at least one number"
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", self.password):
            return False, "Password must contain at least one special character"
        if self.is_common_password():
            return False, "Password is too common"

        return True, "Strong password"


    @staticmethod
    @lru_cache(maxsize=1)
    def get_common_passwords() -> list:
        """Fetches and caches the common password list from GitHub."""
        url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10k-most-common.txt"
        try:
            response = requests.get(url, timeout=5)  # Added timeout for reliability
            response.raise_for_status()  # Raise an error for bad responses (4xx/5xx)
            return response.text.strip().lower().split("\n")
        except requests.RequestException:
            return []  # Return an empty list if request fails

    def is_common_password(self) -> bool:
        """Checks if the password is in the list of commonly used passwords."""
        return self.password.lower() in self.get_common_passwords()


