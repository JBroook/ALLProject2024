from tkinter import *
from tkinter import messagebox
import customtkinter
import sqlite3

root = customtkinter.CTk()
root.title("Payment Page")
root.geometry('500x525')
root.resizable(True, True)

# Database setup
conn = sqlite3.connect('DriveEase.db')
c = conn.cursor()

# Create a table for Card Details
c.execute('''CREATE TABLE IF NOT EXISTS Card_Details
             (Name_On_Card NUMBER, Card_Number NUMBER, 
             Expiry_Date NUMBER, Security_Code NUMBER)''')
conn.commit()

# Function to Make Payment
def submit():

    name = Name_entry.get().strip()
    number = Number_entry.get().strip()
    date = Date_entry.get().strip()
    code = Code_entry.get().strip()

    # Validate input
    if not name or not number or not date or not code:
        messagebox.showerror("Error", "All fields are required!")

        return

    c.execute("INSERT INTO Card_Details (Name_On_Card, Card_Number, Expiry_Date, Security_Code) "
              "VALUES (?, ?, ?, ?)", (name, number, date, code))
    conn.commit()
    messagebox.showinfo("Success", "Payment successful!")
    root.destroy()  # Close the Invoice Page
    #show_login_page()  # Open login page after successful registration

    conn.close()

#frame
root.checkbox_frame = customtkinter.CTkFrame(root,fg_color="#222831")
root.checkbox_frame.pack(padx=(20,0), pady=(20, 0))

#Invoice Label
Invoice_label = customtkinter.CTkLabel(root.checkbox_frame, text="Invoice",font=("Times New Roman", 20, "bold"),)
Invoice_label.pack(pady=15)

#Card Name
Name_label = customtkinter.CTkLabel(root.checkbox_frame, text="Name on Card",)
Name_label.pack(pady=5)
Name_entry = customtkinter.CTkEntry(root.checkbox_frame, width=30, placeholder_text="Ex. John Website",)
Name_entry.pack(padx=10, fill=X ,pady=5)

#Card Number
Number_label = customtkinter.CTkLabel(root.checkbox_frame, text="Card Number")
Number_label.pack(pady=5)
Number_entry = customtkinter.CTkEntry(root.checkbox_frame, width=30, placeholder_text="1234 5678 9012 3456",)
Number_entry.pack(padx=10, fill=X, pady=5)

#Expiry Date
Date_label = customtkinter.CTkLabel(root.checkbox_frame, text="Expiry Date")
Date_label.pack(pady=5)
Date_entry = customtkinter.CTkEntry(root.checkbox_frame, width=30, placeholder_text="01/24",)
Date_entry.pack(padx=10, fill=X, pady=5)

#Security Code
Code_label = customtkinter.CTkLabel(root.checkbox_frame, text="Security Code")
Code_label.pack(pady=5,)
Code_entry = customtkinter.CTkEntry(root.checkbox_frame, width=30,placeholder_text="* * *")
Code_entry.pack(padx=10, fill=X, pady=5)

#Success Command Window
def success():
    sucess = customtkinter.CTkToplevel(root)
    sucess.title("Payment Payment Successful")
    sucess.geometry("500x300")
    sucess.resizable(False,False)

#Submit Button
submit_button = customtkinter.CTkButton(root.checkbox_frame,
                                        text="Confirm",
                                        fg_color="green",
                                        corner_radius=50,
                                        command= lambda:submit())

submit_button.pack(padx=20, pady=20)
root.grid_columnconfigure(0, weight=1)

#Destroy Window
def destroy():
    messagebox.showinfo("Payment Interrupted", "Are You Sure, You Want To Cancel The Process!")
    root.destroy()

#Cancel Button
cancel_button = customtkinter.CTkButton(root.checkbox_frame,
                                        text="Cancel",
                                        fg_color="red",
                                        corner_radius=50,
                                        command=destroy)
cancel_button.pack(padx=20, pady=5)



root.mainloop()