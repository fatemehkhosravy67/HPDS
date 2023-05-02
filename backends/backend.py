import psutil
import time
import sqlite3

# Connect to the database
with sqlite3.connect('hpds.db') as conn:
    c = conn.cursor()

    # Create the RAM usage table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS ram_usage
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  total REAL,
                  free REAL,
                  used REAL,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

    # Loop indefinitely
    while True:
        # Get the system memory usage
        memory = psutil.virtual_memory()

        # Convert memory units to MB
        total_memory = round(memory.total / (1024 ** 2), 2)
        free_memory = round(memory.free / (1024 ** 2), 2)
        used_memory = round(memory.used / (1024 ** 2), 2)

        # Insert the data into the RAM usage table
        c.execute("INSERT INTO ram_usage (total, free, used) VALUES (?, ?, ?)",
                  (total_memory, free_memory, used_memory))
        conn.commit()

        # Wait for one minute before checking again
        time.sleep(60)
