'''
Brandon Ratelle
IST
6 Feb 25
Fish Db
'''
#imports section
import sqlite3
import tkinter as tk

class FishDb():
    def __init__(self):
        self.connected = False
        self.updateRec = ["","","","",""]
        self.deleteRec = [""]

    # Connection and Disconnection setup
    def connection(self):
        try:
            self.Fishconnect = sqlite3.connect('hey.sqlite')
            self.cursor = self.Fishconnect.cursor()
            self.create_table()  # Create the table if it doesn't exist
            return "Proper connection."
        except sqlite3.Error as error:
            return "Error Connecting", error

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS FishStat (
            ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            Name TEXT NOT NULL,
            Color TEXT NOT NULL,
            Habitat TEXT NOT NULL,
            Pounds REAL NOT NULL,
            MaxAge INTEGER NOT NULL
        );
        """
        self.cursor.execute(query)
        self.Fishconnect.commit()

    def disconnect(self):
        if self.Fishconnect:
            self.Fishconnect.close()
            return "Connection Closed"

    # Selecting/showing database
    def select(self):
        try:
            query = "SELECT * FROM FishStat;"
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            for o in records:
                print(o)
            return records
        except sqlite3.Error as error:
            return "Select Error", error

    # Insert values
    def insert(self, name, color, habitat, pounds, maxage):
        try:
            query = "INSERT INTO FishStat(Name, Color, Habitat, Pounds, MaxAge) VALUES(?, ?, ?, ?, ?);"
            self.cursor.execute(query, (name, color, habitat, pounds, maxage))
            self.Fishconnect.commit()
        except sqlite3.Error as error:
            return "Insert Error", error

    # Updating
 
    def update(self, old_record):
        try:
            # Fetch existing values from the database for comparison
            query = "SELECT Name, Color, Habitat, Pounds, MaxAge FROM FishStat WHERE Name = ?"
            self.cursor.execute(query, (old_record[0],))  # Use a tuple (old_record[0],)
            existing_values = self.cursor.fetchone()

            if not existing_values:
                raise ValueError("No record found with the given Name.")

            # Correct column mappings
            names = ["Name", "Color", "Habitat", "Pounds", "MaxAge"]

            # Loop through columns and update only if the value has changed
            for i in range(1, len(old_record)):  # Start at 1 to skip "Name" (or ID)
                if str(old_record[i]) != str(existing_values[i - 1]):  # Align indexes
                    # Dynamically construct the query with column names
                    query = f"UPDATE FishStat SET {names[i]} = ? WHERE Name = ?"
                    self.cursor.execute(query, (old_record[i], old_record[0]))

            # Commit all updates after the loop
            self.Fishconnect.commit()
            self.select()  # Refresh or reload UI/data

        except sqlite3.Error as error:
            self.Fishconnect.rollback()  # Roll back changes on error
            print(f"Database Error: {error}")
            return "Update Error", error

        except ValueError as ve:
            print(ve)
            return ve


    # Deleting
    def delete(self):
        try:
            query = "DELETE FROM FishStat WHERE Name = ?;"
            self.cursor.execute(query, (self.deleteRec[0],))  # Ensure the parameter is passed as a tuple
            self.Fishconnect.commit()
        except sqlite3.Error as error:
            print(error)
            return "Delete Error", error
