from . import *
import os
import sqlite3



def start():
    print("Started")

    # Check if database exists
    if "database.db" not in os.listdir():
        print("[+] Database does not exist. Creating...")

        # Create the database file
        with open("database.db", "w+") as db:
            pass

        # Connect to the database file
        con = sqlite3.connect("database.db")
        cur = con.cursor()

        # Create Users table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Users(uid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            surname TEXT NOT NULL,
                            phone TEXT NOT NULL 
                            )
            """
        )

        # Create EmergencyContact table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS EmergencyContact(cid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            phone TEXT NOT NULL,
                            relation TEXT NOT NULL,
                            email TEXT,
                            belongsTo INT NOT NULL,
                            FOREIGN KEY(belongsTo) REFERENCES users(uid)
                            )
            """
        )
        print("[+] Created all tables")

        # Commits the changes to the database
        con.commit()
        cur.close()
        con.close()


    # Run the actual program
    print("[+] Starting backend server.")
    from server.main import main
    main()


