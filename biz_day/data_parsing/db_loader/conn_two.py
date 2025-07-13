import psycopg2
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from secret import passwords

# connects to database, right now test database
connTwo = psycopg2.connect(
    database="cmos",
    user="postgres",
    password=passwords.dbPassword,
    host="localhost",
    port="5432",
)
