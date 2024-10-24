from tkinter import messagebox
import customtkinter
from PIL import Image
import sqlite3

root = customtkinter.CTk()
root.title("Payment Page")
root.geometry('1536x800')

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
    root.destroy()  # Close the Payment Page

    conn.close()

background_image = customtkinter.CTkImage(Image.open("Payment_Page.png"), size=(root.winfo_screenwidth(), root.winfo_screenheight()-64))
background_image_label = customtkinter.CTkLabel(master=root.master, image=background_image, text="")
background_image_label.place(relx=0, rely=0)

#Cardholder's Name
name_entry = customtkinter.CTkEntry(root, placeholder_text="Alice Tan Wong", width=320/1280*root.winfo_screenwidth(),
                                    height=34/720*root.winfo_screenheight(), bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
name_entry.place(x=451/1280*root.winfo_screenwidth(),y=240/720*root.winfo_screenheight())

#Card Number
number_entry = customtkinter.CTkEntry(root, placeholder_text="1234 5678 9012 3456", width=320/1280*root.winfo_screenwidth(),
                                      height=34/720*root.winfo_screenheight(), bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
number_entry.place(x=451/1280*root.winfo_screenwidth(),y=320/720*root.winfo_screenheight())

#Expiry Date
expiry_entry = customtkinter.CTkEntry(root, placeholder_text="01/24", width=159/1280*root.winfo_screenwidth(),
                                      height=34/720*root.winfo_screenheight(), bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
expiry_entry.place(x=451/1280*root.winfo_screenwidth(),y=400/720*root.winfo_screenheight())

#CVC
cvc_entry = customtkinter.CTkEntry(root, placeholder_text="* * *", width=122/1280*root.winfo_screenwidth(),
                                   height=34/720*root.winfo_screenheight(), bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
cvc_entry.place(x=650/1280*root.winfo_screenwidth(),y=400/720*root.winfo_screenheight())

#Pay Button
confirm_button = customtkinter.CTkButton(root,text = "Pay" ,bg_color= "white", fg_color="Green",text_color="white",
            border_color="#1572D3", width=89/1280*root.winfo_screenwidth(),
                                         height=39/720*root.winfo_screenheight(), font=("Poppins Medium",18), command = lambda:pay())
confirm_button.place(x=450/1280*root.winfo_screenwidth(),y=512/720*root.winfo_screenheight())

#Destroy Window
def destroy():
    messagebox.showinfo("Payment Interrupted", "Are You Sure, You Want To Cancel The Process!")
    root.destroy()

#Back Button
back_button = customtkinter.CTkButton(root,text = "Back" ,bg_color= "white", fg_color="#1572D3",text_color="white",
            border_color="#1572D3", width=89/1280*root.winfo_screenwidth(),
                                      height=39/720*root.winfo_screenheight(), font=("Poppins Medium",18), command = destroy)
back_button.place(x=45/1280*root.winfo_screenwidth(),y=588/720*root.winfo_screenheight())

root.mainloop()