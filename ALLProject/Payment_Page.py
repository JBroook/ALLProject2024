from tkinter import messagebox
import ctk
from PIL import Image
import sqlite3

self.master = ctk.CTk()
self.master.title("Payment Page")
self.master.geometry('1536x800')

# Database setup
conn = sqlite3.connect('DriveEase.db')
c = conn.cursor()

# Create a table for Card Details
c.execute('''CREATE TABLE IF NOT EXISTS PAYMENT
             (PAYMENT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
             CARDHOLDERS_NAME VARCHAR(255) NOT NULL, 
             CARD_NUMBER VARCHAR(255) NOT NULL, 
             EXPIRY_DATE VARCHAR(255) NOT NULL, 
             CVV VARCHAR(255) NOT NULL
             )'''
          )
conn.commit()

# Function to Make Payment
def pay():

    name = name_entry.get().strip()
    number = number_entry.get().strip()
    date = expiry_entry.get().strip()
    code = cvc_entry.get().strip()

    # Validate input
    if not name or not number or not date or not code:
        messagebox.showerror("Error", "All fields are required!")

        return

    c.execute("INSERT INTO PAYMENT (CARDHOLDERS_NAME, CARD_NUMBER, EXPIRY_DATE, CVV) "
              "VALUES (?, ?, ?, ?)", (name, number, date, code))
    conn.commit()
    messagebox.showinfo("Success", "Payment successful!")
    self.master.destroy()  # Close the Payment Page

    conn.close()

background_image = ctk.CTkImage(Image.open("Payment_Page.png"), size=(self.width, self.height-64))
background_image_label = ctk.CTkLabel(master=self.master, image=background_image, text="")
background_image_label.place(relx=0, rely=0)

#Cardholder's Name
name_entry = ctk.CTkEntry(self.master, placeholder_text="Alice Tan Wong", width=320/1280*self.width,
                                    height=34/720*self.height, bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
name_entry.place(x=451/1280*self.width,y=240/720*self.height)

#Card Number
number_entry = ctk.CTkEntry(self.master, placeholder_text="1234 5678 9012 3456", width=320/1280*self.width,
                                      height=34/720*self.height, bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
number_entry.place(x=451/1280*self.width,y=320/720*self.height)

#Expiry Date
expiry_entry = ctk.CTkEntry(self.master, placeholder_text="01/24", width=159/1280*self.width,
                                      height=34/720*self.height, bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
expiry_entry.place(x=451/1280*self.width,y=400/720*self.height)

#CVC
cvc_entry = ctk.CTkEntry(self.master, placeholder_text="* * *", width=122/1280*self.width,
                                   height=34/720*self.height, bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
cvc_entry.place(x=650/1280*self.width,y=400/720*self.height)

#Pay Button
confirm_button = ctk.CTkButton(self.master,text = "Pay" ,bg_color= "white", fg_color="Green",text_color="white",
            border_color="#1572D3", width=89/1280*self.width,
                                         height=39/720*self.height, font=("Poppins Medium",18), command = lambda:pay())
confirm_button.place(x=450/1280*self.width,y=512/720*self.height)

#Destroy Window
def destroy():
    messagebox.showinfo("Payment Interrupted", "Are You Sure, You Want To Cancel The Process!")
    self.master.destroy()

#Back Button
back_button = ctk.CTkButton(self.master,text = "Back" ,bg_color= "white", fg_color="#1572D3",text_color="white",
            border_color="#1572D3", width=89/1280*self.width,
                                      height=39/720*self.height, font=("Poppins Medium",18), command = destroy)
back_button.place(x=45/1280*self.width,y=588/720*self.height)

self.master.mainloop()