from dotenv import load_dotenv
import os

load_dotenv()

class Config():
    secret_key = os.getenv("SECRET_KEY")
    algorithm = os.getenv("ALGORITHM")
    
config = Config()