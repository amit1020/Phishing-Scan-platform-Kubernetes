import sys,os,configparser,mysql.connector,time
from mysql.connector import Error
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from web.api.Functions_and_Classes.Add_API import add_api_values
from web.api.Functions_and_Classes.General_Functions import verify_otp

HTTP_METHODS = ["GET","POST","PUT","DELETE","PATCH","HEAD","OPTIONS","CONNECT","TRACE"]



sys.stdout.reconfigure(encoding='utf-8')



            
class Database_Connection_Class:
    def __init__(self):
        
        self.database_code_path = Path(__file__).parent / "Users_DB.sql"#local path
        # Load .env file correctly
        env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.env_user_db"))
        load_dotenv(env_path)
        


        self.host = os.getenv("MYSQL_HOST", "-----").split(":")[0]
        print(self.host)
        self.user = os.getenv("MYSQL_USER", "------")
        print(self.user)
        self.password = os.getenv("MYSQL_PASSWORD", "------")
        print(self.password)
        self.port = int(os.getenv("MYSQL_PORT", "3306"))
        self.database = os.getenv("MYSQL_DATABASE", "------")
        self.connection = None
        self.mycursor = None

        self.connect_with_retry()
        
        _virustotal_exist = self.check_or_get_data(table_name="API_Table",columns="api_website_name",condition="api_website_name",value="virustotal",message_type="condition")
        _urlscan_exist = self.check_or_get_data(table_name="API_Table",columns="api_website_name",value="urlscan",condition="api_website_name",message_type="condition")
        sys.stdout.flush()
        
        if _virustotal_exist is None or _urlscan_exist is None:            
            add_api_values(self.connection)
            print("APIs added",flush=True)


    #Try to connects the dayabase with multiple retries
    def connect_with_retry(self, retries=10, delay=5):
            """Attempts to connect to MySQL with retries and ensures the database exists."""
            for attempt in range(1, retries + 1):
                try:
                    print(f"🔄 Attempt {attempt}/{retries}: Connecting to MySQL...")

                    # Step 1: First, connect WITHOUT specifying a database
                    temp_connection = mysql.connector.connect(
                        host=self.host,
                        user=self.user,
                        password=self.password,
                        port=self.port,
                        charset="utf8mb4"
                    )

                    temp_cursor = temp_connection.cursor()

                    # Step 2: Check if the database exists
                    temp_cursor.execute("SHOW DATABASES;")
                    databases = [db[0] for db in temp_cursor.fetchall()]

                    if self.database not in databases:
                        print(f"⚠️ Database '{self.database}' not found. Creating it now...")
                        temp_cursor.execute(f"CREATE DATABASE {self.database};")
                        print(f"✅ Database '{self.database}' created successfully.")

                    # Close temporary connection
                    temp_cursor.close()
                    temp_connection.close()

                    # Step 3: Reconnect with the newly created database
                    self.connection = mysql.connector.connect(
                        host=self.host,
                        user=self.user,
                        password=self.password,
                        database=self.database,
                        port=self.port,
                        charset="utf8mb4"
                    )

                    if self.connection.is_connected():
                        print(f"✅ Successfully connected to '{self.database}'!")

                        # Create cursor AFTER successful connection
                        self.mycursor = self.connection.cursor()

                        # Step 4: Run any required setup
                        self.Build_database()  # Ensure this function exists
                        
                        return  # Exit function after successful connection

                except mysql.connector.Error as err:
                    print(f"⚠️ Connection attempt {attempt} failed: {err}")
                    time.sleep(delay)  # Wait before retrying

            # If all retries fail, raise an exception
            raise Exception("❌ MySQL is not available after multiple retries.")
    
    #!Test function 
    def Get_Connection_Status(self):
        return self.connection.is_connected()
    
    
    
    def VertifyOTP(self,Name:str,OTP) -> bool:
            try:
                print(Name,flush=True)
                self.mycursor.execute('SELECT 2FA_key FROM Users_Table WHERE name="%s"', (Name.strip(),))# get from the database all names of clients
                result = self.mycursor.fetchone()  # Use fetchone() since we expect a single result

                print(result,flush=True)
                
                if result is None:
                    print("No matching user found.", flush=True)
                    return False  # No user found with the given name
                print(f"{result[0][0]} + {verify_otp(secret_key=result[0][0],otp=OTP)}" ,flush=True)
                return verify_otp(secret_key=result[0][0],otp=OTP)
                
                #return results[0][0]
            except mysql.connector.Error as e:
                print(f"Database Error: {e}", flush=True)
                return False
            except Exception as e:
                print(e)
                return False
    
    
    
    
    def insert_data(self,table_name:str,columns:str,values:str) -> bool:
        if self.mycursor is None or table_name is None or columns is None or values is None:
            return None
        
        try:
            self.mycursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({values})")
            self.connection.commit()
            return True
        except Exception as e:
            #print(e)
            return False
        
    


   

    
    
    
    def check_or_get_data(self,table_name:str,columns:str,condition:str=None,value:str=None,message_type:str=None):
        if self.mycursor is not None:
            if table_name is  None or columns is  None or message_type is  None:#Check if the table_name is not None
                return None
            
            match message_type: #Check the message type
                case "condition":   #E.g check if the user is exist
                    if condition is  None or value is  None:#Check if the condition is not None
                        return None
                    self.mycursor.execute(f"SELECT {columns} FROM {table_name} WHERE {condition}='{value}'")# get from the database all names of clients
                        
                case "Get-data": #E.g get the user data
                    self.mycursor.execute(f"SELECT {columns} FROM {table_name}")# get from the database all names of clients
                
                case "Specific-data": #E.g get the user data
                    if value is None:
                        return None
                    
                    self.mycursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {columns}='{value}';")# get from the database all names of clients
                    exists = self.mycursor.fetchone()[0]
                    return bool(exists) #return the result as a list of dict
                case _:
                    #! Invlid message_type
                    return None             
            try:
                results = self.mycursor.fetchall()
                if results is None or len(results) == 0:
                    return None
                rows = []
                for row in results:
                    rows.append(row)
                return rows
            
            except Exception as e:
                print(e)
                return None
        return None
    
    
    
    #*-------------------------------Create user----------------------------------------------------------------------------
    def Create_Client(self,Data:dict,twoFA_key_var:str) -> bool:
        if Data is not None:
            try:
                sql = "INSERT INTO Users_Table (name, password, email, 2FA_key, phone_number) VALUES (%s, %s, %s, %s, %s)"
                vals = (Data['name'],Data['password'],Data['email'], twoFA_key_var, Data['phone_number'])
                            
                self.mycursor.execute(sql,vals)
                self.connection.commit()
                                
                #return f"Success to add new client - {Data['name']}"
                
                return True

            except Exception as error:
                print(f"{error}")
                #return f"Error to add new client - {Data['name']} code problem:\n[!] {error}"
        
                return False


    
    
    
    #*-------------------------------Add_Links----------------------------------------------------------------------------
    def Add_Links(self,Data:dict) -> tuple[bool,str]:
        if Data is not None: #check if the data is not empty
            for item in Data.values():
                if item == "" or item == None: #check if there is an empty field, if there is return False
                    return (False,"There is an empty field")
            try:
                sql = "INSERT INTO Links_Table (purpose, website_name, link, request_type, description, headers) VALUES (%s, %s, %s, %s, %s, %s)"
                if Data['request_type'] not in HTTP_METHODS:
                    return (False,"The request type is not valid")
                
                vals = (Data['purpose'],Data['website_Name'],Data['link'],Data['request_type'],Data['description'],Data['headers'])
                
                self.mycursor.execute(sql,vals)
                self.connection.commit()
                
                return (True,f'Success to add new Link - {Data["link"]}')

            except Exception as error:
                return (False,f"Error to add new Link - {Data['link']} code problem:\n[!] {error}")
     #*-----------------------------------------------------------------------------------------------------------
     
     
     
     
     
     
    #*if the database isnt exist, the python will  Build the database from the sql file 
    def Build_database(self):
        #print("Running database setup...")
        with open(self.database_code_path, 'r', encoding='utf-8') as file:
            sql_commands = file.read()

        for command in sql_commands.split(';'):
            if command.strip():
                try:
                    self.mycursor.execute(command)
                    self.connection.commit()
                except mysql.connector.Error as err:
                    #print(f"Error executing SQL: {err}")
                    self.connection.rollback()
    #*-----------------------------------------------------------------------------------------------------------                
                    
                    
                    
    #?NEED TO UNDERSTANT MORE                
    def close_connections(self):
        if hasattr(self, 'mycursor') and self.mycursor:
            self.mycursor.close()
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()
            print("The connection is closed")
    #?NEED TO UNDERSTANT MORE
    def __enter__(self):
        return self
    #?NEED TO UNDERSTANT MORE
    def __exit__(self, exc_type, exc_value, traceback:bool):
        self.close_connections()
        
    
        

        
      
      








"""
    def Get_data_from_database(self,table_name:str,columns:str,condition:str=None,value:str=None,function_call_name:str=None):#Value is the value of the condition
        if self.mycursor is not None:
            if condition is not None and value is not None:
                try:
                    self.mycursor.execute(f"SELECT {columns} FROM {table_name} WHERE {condition}='{value}'")# get from the database all names of clients
                    results = self.mycursor.fetchall()
                    rows = []
                    for row in results:
                        rows.append(row)
                    Write_Database_Log(f"User get all columns: {columns} from {table_name} Table", "INFO")
                    
                    #FP = Fitness_perimetersTable, C = ClientsTable
                    if function_call_name is not None and (function_call_name == "Get_Data_About_Client_From_App_Page_C" or function_call_name == "Get_Data_About_Client_From_App_Page_FP"):
                        if function_call_name == "Get_Data_About_Client_From_App_Page_C": 
                            return dict(zip(PARAMS_FOR_GET_DATA_RETURN_ClientTable, rows[0])) 
                        
                        else: #function_call_name == "Get_Data_About_Client_From_App_Page_FP"
                            #TODO improve the code of all the function 
                            self.mycursor.execute(f"SELECT {columns} FROM {table_name} WHERE {condition}='{value}' ORDER BY Check_Date DESC LIMIT 1;")# get from the database all names of clients
                            results = self.mycursor.fetchall()
                            rows = []
                            for row in results:
                                rows.append(row)  
                            return dict(zip(PARAMS_FOR_GET_DATA_RETURN_Fitness_perimetersTable, rows[0]))
                    return rows
                except Exception as e:
                    print(e)
                    Write_Database_Log(f"{e}", "WARNING")
                    return None
            else:
                try:
                    self.mycursor.execute(f"SELECT {columns} FROM {table_name}")# get from the database all names of clients
                    results = self.mycursor.fetchall()
                    rows = []
                    for row in results:
                        rows.append(row)
                    #Write_Database_Log(f"User get all columns: {columns} from {table_name} Table", "INFO")
                    return rows
                except Exception as e:
                    #Write_Database_Log(f"{e}", "WARNING")
                    return None
        else:
            Write_Database_Log("The Curser not connect, Function Get_data_from_database ", "WARNING")
            print("cursor is not connect")

    
    
    def Searching_user(self,Phone_Number:str):
        if self.mycursor is not None:
            try:
                self.mycursor.execute(f"SELECT Phone_Number From ClientsTable WHERE Phone_Number={Phone_Number}")
                
                if len(self.mycursor.fetchall()) == 0: #result list
                    Write_Database_Log(f"There is not user - {Phone_Number}","WARNING")
                    return None
                else:
                    return True
            except Exception as e:
                Write_Database_Log(f"Problen to search user: {e}","ERROR")
                
            

    
    def Create_Client(self,Data:dict) -> bool:
        if Data is not None:
            try:
                sql = "INSERT INTO ClientsTable (FullName, Phone_Number, Address, Age, Gender, Begining_Date, Email, HEALTH_DECLARATION) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                vals = (Data['FullName'],Data['Phone_Number'],Data['Address'],Data['Age'],Data['Gender'],Data['Begining_Date'],Data['Email'],Data['HEALTH_DECLARATION'])
                self.mycursor.execute(sql,vals)
                self.connection.commit()
                Write_Database_Log(f"Success to add new client - {Data['FullName']}", "INFO")
                self.Create_Fitness_perimeters(Data=Data)
                print(f"Success to add new client - {Data['FullName']}")
                return True

            except Exception as error:
                print(f"Error to add new client - {Data['FullName']} code problem:\n[!] {error}")
                Write_Database_Log(f"Error to add new client - {Data['FullName']} code problem:\n[!] {error}", "ERROR")
                return False






   

#TODO Check why __del__ not work here
    def close_connections(self):
        try:
            if hasattr(self, 'mycursor') and self.mycursor:
                self.mycursor.close()
            if hasattr(self, 'connection') and self.connection:
                self.connection.close()
        except Exception as e:
            pass
"""




