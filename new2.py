import sqlite3
import random
import time


categories = ["Shopping", "Groceries", "Electronics", "Gaming", "Travel", "Entertainment"]


def create_table():
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            acc_id INTEGER,
            acc_num INTEGER,
            category TEXT,
            amount REAL,
            processed INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


def generate_transaction():
    acc_id = random.randint(10000, 99999)  
    acc_num = random.randint(100000, 999999) 
    category = random.choice(categories) 
    amount = round(random.uniform(10, 5000), 2)  

    return (acc_id, acc_num, category, amount)


def store_transaction(transaction):
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (acc_id, acc_num, category, amount) VALUES (?, ?, ?, ?)", transaction)
    conn.commit()
    conn.close()


def add_processed_column():
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()


    cursor.execute("PRAGMA table_info(transactions)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'processed' not in columns:
        cursor.execute("""
            ALTER TABLE transactions ADD COLUMN processed INTEGER DEFAULT 0
        """)
        conn.commit()

    conn.close()


def generate_real_time_transactions():
    create_table() 
    transaction_count = 0
    try:
        while True:
            transaction = generate_transaction()
            store_transaction(transaction)
            transaction_count += 1
            print(f"Generated Transaction {transaction_count}: {transaction}")
            time.sleep(5)
    except KeyboardInterrupt:
        print("Transaction generation stopped.")


add_processed_column()

generate_real_time_transactions()
