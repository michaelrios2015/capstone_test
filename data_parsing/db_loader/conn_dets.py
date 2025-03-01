import psycopg2

# connects to database
conn = psycopg2.connect(
    database="test_cmo",
    user="postgres",
    password="JerryPine",
    host="localhost",
    port="5432",
)
