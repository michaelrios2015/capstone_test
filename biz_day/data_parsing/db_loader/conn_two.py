import psycopg2

# connects to database, right now test database
connTwo = psycopg2.connect(
    database="copy_cmos",
    user="postgres",
    password="JerryPine",
    host="localhost",
    port="5432",
)
