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
 
    def update(self, old_name, new_name):
        try:
            query = "UPDATE FishStat SET Name = ? WHERE Name = ?;"
            query = "UPDATE FishStat SET Color = ? WHERE Color = ?;"
            query = "UPDATE FishStat SET Habitat = ? WHERE Habitat = ?;"
            query = "UPDATE FishStat SET Pounds = ? WHERE Pounds = ?;"
            query = "UPDATE FishStat SET MaxAge = ? WHERE MaxAge = ?;"
            self.cursor.execute(query, (new_name, old_name))
            self.Fishconnect.commit()
            self.select()
        except sqlite3.Error as error:
            return "Update Error", error

    # Deleting
    def delete(self):
        try:
            query = "DELETE FROM FishStat WHERE Name = ?;"
            self.cursor.execute(query, (self.deleteRec[0],))  # Ensure the parameter is passed as a tuple
            self.Fishconnect.commit()
        except sqlite3.Error as error:
            print(error)
            return "Delete Error", error
