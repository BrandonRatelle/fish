from copyfishDb import FishDb
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import PhotoImage

class FishGui():
    def __init__(self):
        self.win = tk.Tk()
        self.win.title("My Aquarium")
        self.win.geometry("800x400")  # Adjusted height
        self.db = FishDb()
        self.connected = False  # Track connection status
        self.fishImage = tk.PhotoImage(file="R.png")
        self.fishLabel = tk.Label(self.win, image=self.fishImage)
        self.fishLabel.place(relwidth=1, relheight=1)

        #Storage for data from db queries
        self.currentIndex = 0
        self.records = []

        self.nameVar = tk.StringVar()
        self.colorVar = tk.StringVar()
        self.habitatVar = tk.StringVar()
        self.poundsVar = tk.StringVar()
        self.maxageVar = tk.StringVar()

        # Create a frame for the entry boxes and position it in the middle
        self.entryFrame = tk.Frame(self.win)
        self.entryFrame.pack(pady=20)

        tk.Label(self.entryFrame, text="Name").pack()
        self.entryName = tk.Entry(self.entryFrame, textvariable=self.nameVar)
        self.entryName.pack()

        tk.Label(self.entryFrame, text="Color").pack()
        self.entryColor = tk.Entry(self.entryFrame, textvariable=self.colorVar)
        self.entryColor.pack()

        tk.Label(self.entryFrame, text="Habitat").pack()
        self.entryHabitat = tk.Entry(self.entryFrame, textvariable=self.habitatVar)
        self.entryHabitat.pack()

        tk.Label(self.entryFrame, text="Pounds").pack()
        self.entryPounds = tk.Entry(self.entryFrame, textvariable=self.poundsVar)
        self.entryPounds.pack()

        tk.Label(self.entryFrame, text="Max Age").pack()
        self.entryMaxage = tk.Entry(self.entryFrame, textvariable=self.maxageVar)
        self.entryMaxage.pack()

        self.btnAdd = tk.Button(self.entryFrame, text="Add Fish", command=self.addFish)
        self.btnAdd.pack(side=tk.LEFT, padx=5, pady=5)

        self.btnDelete = tk.Button(self.entryFrame, text="Delete Fish", command=self.deleteFish)
        self.btnDelete.pack(side=tk.LEFT, padx=5, pady=5)

        self.btnSave = tk.Button(self.entryFrame, text="Save Changes", command=self.saveChanges)
        self.btnSave.pack(side=tk.LEFT, padx=5, pady=5)

        # Create a frame for the cassette player buttons
        self.cassetteFrame = tk.Frame(self.win)
        self.cassetteFrame.pack(pady=10)

        self.btnFirst = tk.Button(self.cassetteFrame, text="First", command=self.showFirst)
        self.btnFirst.grid(row=0, column=0, padx=5, pady=5)

        self.btnBack2 = tk.Button(self.cassetteFrame, text="Back 2", command=self.showBack2)
        self.btnBack2.grid(row=0, column=1, padx=5, pady=5)

        self.btnPrev = tk.Button(self.cassetteFrame, text="Previous", command=self.showPrevious)
        self.btnPrev.grid(row=0, column=2, padx=5, pady=5)

        self.btnNext = tk.Button(self.cassetteFrame, text="Next", command=self.showNext)
        self.btnNext.grid(row=0, column=3, padx=5, pady=5)

        self.btnForward2 = tk.Button(self.cassetteFrame, text="Forward 2", command=self.showForward2)
        self.btnForward2.grid(row=0, column=4, padx=5, pady=5)

        self.btnLast = tk.Button(self.cassetteFrame, text="Last", command=self.showLast)
        self.btnLast.grid(row=0, column=5, padx=5, pady=5)

        # Create a frame for the connect/disconnect button
        self.connectFrame = tk.Frame(self.win)
        self.connectFrame.pack(pady=10)

        self.btnConnect = tk.Button(self.connectFrame, text="Connect", command=self.toggleConnection, font=("Arial", 14), padx=20, pady=10)
        self.btnConnect.pack()

        # status bar
        self.statusBar = tk.Label(self.win, text="Disconnected, Cannot make changes to the database", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 12), padx=10, pady=5)
        self.statusBar.pack(side=tk.BOTTOM, fill=tk.X)
        # Add menu bar
        self.menuBar = tk.Menu(self.win)
        self.win.config(menu=self.menuBar)

        # Navigation menu
        self.navMenu = tk.Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label="Navigation", menu=self.navMenu)
        self.navMenu.add_command(label="First", command=self.showFirst)
        self.navMenu.add_command(label="Back 2", command=self.showBack2)
        self.navMenu.add_command(label="Previous", command=self.showPrevious)
        self.navMenu.add_command(label="Next", command=self.showNext)
        self.navMenu.add_command(label="Forward 2", command=self.showForward2)
        self.navMenu.add_command(label="Last", command=self.showLast)

        # Edit menu
        self.editMenu = tk.Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label="Edit", menu=self.editMenu)
        self.editMenu.add_command(label="Add Fish", command=self.addFish)
        self.editMenu.add_command(label="Delete Fish", command=self.deleteFish)
        self.editMenu.add_command(label="Save Changes", command=self.saveChanges)

        # Help menu
        self.helpMenu = tk.Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label="Help", menu=self.helpMenu)
        self.helpMenu.add_command(label="About", command=self.showHelp)

        self.win.mainloop()

    def toggleConnection(self):
        if self.connected:
            self.disconnect()
        else:
            self.connect()

    def connect(self):
        try:
            self.db.connection()
            self.fetchdata()
            self.connected = True
            self.btnConnect.config(text="Disconnect")
            self.statusBar.config(text="Connected")
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {e}")

    def disconnect(self):
        try:
            self.db.Fishconnect.close()
            self.connected = False
            self.btnConnect.config(text="Connect")
            self.statusBar.config(text="Disconnected")
            self.clearFields()
            messagebox.showinfo("Info", "Disconnected from database.")
        except Exception as error:
            messagebox.showerror("Database Error", f"Failed to disconnect from database: {error}")

    def fetchdata(self):
        self.records = self.db.select()
        self.currentIndex = 0
        if self.records:
            self.showRecord(self.currentIndex)

        print()

    def showRecord(self, index):
        if 0 <= index < len(self.records):
            record = self.records[index]
            self.populateEntries(record)

    def populateEntries(self, record):
        self.nameVar.set(record[1])
        self.colorVar.set(record[2])
        self.habitatVar.set(record[3])
        self.poundsVar.set(record[4])
        self.maxageVar.set(record[5])

    def showPrevious(self):
        if self.currentIndex > 0:
            self.currentIndex -= 1
            self.showRecord(self.currentIndex)

    def showNext(self):
        if self.currentIndex < len(self.records) - 1:
            self.currentIndex += 1
            self.showRecord(self.currentIndex)

    def showFirst(self):
        self.currentIndex = 0
        self.showRecord(self.currentIndex)

    def showLast(self):
        self.currentIndex = len(self.records) - 1
        self.showRecord(self.currentIndex)

    def showForward2(self):
        self.currentIndex = min(self.currentIndex + 2, len(self.records) - 1)
        self.showRecord(self.currentIndex)

    def showBack2(self):
        self.currentIndex = max(self.currentIndex - 2, 0)
        self.showRecord(self.currentIndex)

    def addFish(self):
        self.clearFields()  # Clear fields to allow new input
        self.currentIndex = len(self.records)  # Set current index to a new record

    def deleteFish(self):
        if self.currentIndex < len(self.records):
            if messagebox.askyesno(title="Confirm Delete", message=f"Are you sure you want to delete this fish, {self.entryName.get()}?"):
                try:
                    self.db.deleteRec = [self.entryName.get()]
                    self.db.delete()
                    self.records.pop(self.currentIndex)
                    self.currentIndex = max(0, self.currentIndex - 1)
                    self.fetchdata()  # Refresh the data after deletion
                    messagebox.showinfo("Success", "Fish deleted successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete fish: {e}")
    def saveChanges(self):
        try:
            self.name = self.nameVar.get()
            self.color = self.colorVar.get()
            self.habitat = self.habitatVar.get()
            self.pounds = self.poundsVar.get()
            self.maxage = self.maxageVar.get()
    

            if (self.currentIndex >= len(self.records)):  # Adding a new record
                self.db.insert(self.name, self.color, self.habitat, self.pounds, self.maxage)
                messagebox.showinfo("Success", "Fish added successfully!")
                self.fetchdata()
  
            else:  # Updating an existing record
                existing_records = []

                
                
                existing_records.append(str(self.name))
                existing_records.append(str(self.color))
                existing_records.append(str(self.habitat))
                existing_records.append(str(self.pounds))
                existing_records.append(str(self.maxage))

                
                self.db.update(existing_records)
                messagebox.showinfo("Success", "Fish updated successfully!")

                self.fetchdata()# Refresh the data after adding/updating
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save changes: {e}")

    def clearFields(self):
        if self.connected:
            self.nameVar.set("")
            self.colorVar.set("")
            self.habitatVar.set("")
            self.poundsVar.set("")
            self.maxageVar.set("")

    def showHelp(self):
        messagebox.showinfo("Help", "This is a fish tracking application for an aquarium. Use the menu or buttons to navigate, add, delete, or update fish records.")






