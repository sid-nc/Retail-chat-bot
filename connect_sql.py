from sqlalchemy import create_engine

db_user = "root"
db_password = "Sqled@2611"  # Use the correct password
db_host = "127.0.0.1"  # Use IP instead of "localhost"
db_port = "3306"  # Ensure MySQL is running on port 3306
db_name = "atliq_tshirts"  # Replace with actual database name

try:
    engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
    connection = engine.connect()
    print("Connected successfully!")
    connection.close()
except Exception as e:
    print(f"Connection failed: {e}")
