from tkinter import messagebox
import ctk
from PIL import Image
import sqlite3

self.master = ctk.CTk()
self.master.title("Registration Page")
self.master.geometry('1536x800')

background_image = ctk.CTkImage(Image.open("main/assets/registration page.png"), size=(self.width, self.height - 71))
background_image_label = ctk.CTkLabel(master=self.master.master, image=background_image, text="")
background_image_label.place(relx=0, rely=0)

#Connecting To Database

# Database setup
conn = sqlite3.connect('DriveEase.db')
c = conn.cursor()

# Create a table for Card Details
c.execute('''CREATE TABLE IF NOT EXISTS REGISTRATION
             (REGISTRATION_ID INTEGER PRIMARY KEY AUTOINCREMENT,
              FIRST_NAME VARCHAR(255) NOT NULL, 
              LAST_NAME VARCHAR(255) NOT NULL,
              DATE_OF_BIRTH VARCHAR(255) NOT NULL,
              EMAIL VARCHAR(255) NOT NULL,
              USERNAME VARCHAR(255) NOT NULL, 
              PASSWORD VARCHAR(255) NOT NULL
              )''')
conn.commit()

def register():

    first = first_entry.get().strip()
    last = last_entry.get().strip()
    date = date_entry.get().strip()
    email = email_entry.get().strip()
    user = user_entry.get().strip()
    password = password_entry.get().strip()
    confirm = confirm_entry

    # Validate input
    if not first or not last or not date or not email or not user or not password or not confirm:
        messagebox.showerror("Interrupted", "All fields are required!")

        return

    c.execute("INSERT INTO REGISTRATION ( FIRST_NAME, LAST_NAME, DATE_OF_BIRTH, EMAIL, USERNAME, PASSWORD) "
              "VALUES(?, ?, ?, ?, ?, ?)", (first, last, date, email, user, password))
    conn.commit()
    messagebox.showinfo("Success", "Registration Successful!")
    self.master.destroy()  # Close the Invoice Page

#First Name
first_entry = ctk.CTkEntry(self.master, placeholder_text="Alice", width=215, height=34, bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
first_entry.place(x=142/1280*self.width,y=194/720*self.height)

#Last Name
last_entry = ctk.CTkEntry(self.master, placeholder_text="Tan", width=215, height=34, bg_color="white",
                                    fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
last_entry.place(x=142/1280*self.width,y=262/720*self.height)

#Date Of Birth
date_entry = ctk.CTkEntry(self.master, placeholder_text="YYYY-MM-DD", width=215, height=34,
                                    bg_color="white",fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
date_entry.place(x=142/1280*self.width,y=342/720*self.height)

#Email
email_entry = ctk.CTkEntry(self.master, placeholder_text="alicetan@yahoo.com", width=215, height=34,
                                     bg_color="white",fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
email_entry.place(x=142/1280*self.width,y=412/720*self.height)

#Username
user_entry = ctk.CTkEntry(self.master, placeholder_text="Alicewonderland", width=215, height=34, bg_color="white",
                                    fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
user_entry.place(x=410/1280*self.width,y=194/720*self.height)

#Password
password_entry = ctk.CTkEntry(self.master, placeholder_text="******", width=215, height=34, bg_color="white",
                                        fg_color="#D9D9D9", border_color="#D9D9D9",text_color="black")
password_entry.place(x=410/1280*self.width,y=262/720*self.height)

#Confirm Password
confirm_entry = ctk.CTkEntry(self.master, placeholder_text="******", width=215, height=34, bg_color="white",
                                       fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
confirm_entry.place(x=410/1280*self.width,y=343/720*self.height)

#Login Button
back_button = ctk.CTkButton(self.master,text = "Back to Login" ,bg_color= "white", fg_color="#1572D3",text_color="white",
            border_color="#1572D3", width=135, height=41, font=("Poppins Medium",18))
back_button.place(x=246/1280*self.width,y=500/720*self.height)

#Confirm Button
confirm_button = ctk.CTkButton(self.master,text = "Continue" ,bg_color= "white", fg_color="#1572D3",text_color="white",
            border_color="#1572D3", width=135, height=41, font=("Poppins Medium",18), command=register)
confirm_button.place(x=402/1280*self.width,y=500/720*self.height)

self.master.mainloop()