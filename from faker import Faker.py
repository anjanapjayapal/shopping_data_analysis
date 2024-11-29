from faker import Faker
import random
import mysql.connector

# Initialize Faker
fake = Faker()

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost", user="root", password="root", database="RetailDB"
)
cursor = conn.cursor()


# Function to insert customers
def insert_customers(num_customers):
    for _ in range(num_customers):
        name = fake.name()
        email = fake.email()
        join_date = fake.date_this_decade()
        cursor.execute(
            "INSERT INTO Customers (Name, Email, JoinDate) VALUES (%s, %s, %s)",
            (name, email, join_date),
        )
    conn.commit()


# Function to insert purchases
def insert_purchases(num_purchases):
    cursor.execute("SELECT CustomerID FROM Customers")
    customer_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(num_purchases):
        customer_id = random.choice(customer_ids)
        product = fake.word()
        amount = round(random.uniform(5.0, 500.0), 2)
        purchase_date = fake.date_this_year()
        cursor.execute(
            "INSERT INTO Purchases (CustomerID, Product, Amount, PurchaseDate) VALUES (%s, %s, %s, %s)",
            (customer_id, product, amount, purchase_date),
        )
    conn.commit()


# Insert data
insert_customers(10000)  # Insert 10,000 customers
insert_purchases(100000)  # Insert 100,000 purchases

# Close connection
cursor.close()
conn.close()