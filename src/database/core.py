import os

from dotenv import load_dotenv

# load `.env` file
load_dotenv()

# URL to connect to the database
DATABASE_URL = os.getenv("DATABASE_URL")
