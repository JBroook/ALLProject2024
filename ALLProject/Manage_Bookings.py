from tkinter import ttk
import customtkinter
from PIL import Image
import sqlite3


# Connect to the Database
def connect_db():
    conn = sqlite3.connect('DriveEase.db')
    return conn

#Retrieve from Database
def show_booking_details():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT b.BOOKING_ID, u.FIRST_NAME, u.EMAIL, 
    c.MODEL, c.TRANSMISSION, c.PRICE, 
    b.START_DATE, b.END_DATE
    FROM BOOKINGS b
    JOIN CARS c on b.BOOKING_ID
    ''')
    cursor.fetchall()
    conn.close()

root = customtkinter.CTk()
root.title("Manage Booking")
root.geometry('1536x800')

#Background Image
background_image = customtkinter.CTkImage(Image.open("Manage_Booking.png"),
                                          size=(root.winfo_screenwidth(), root.winfo_screenheight()-64))
background_image_label = customtkinter.CTkLabel(master=root.master, image=background_image, text="")
background_image_label.place(relx=0, rely=0)

#Left Box

#Booking ID
book_entry = customtkinter.CTkEntry(root, width=217/1280*root.winfo_screenwidth(),
                                    height=34/720*root.winfo_screenheight(), bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
book_entry.place(x=351/1280*root.winfo_screenwidth(),y=75/720*root.winfo_screenheight())

#Customer Name
name_entry = customtkinter.CTkEntry(root, width=217/1280*root.winfo_screenwidth(),
                                    height=34/720*root.winfo_screenheight(), bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
name_entry.place(x=351/1280*root.winfo_screenwidth(),y=115/720*root.winfo_screenheight())

#Customer Contact
contact_entry = customtkinter.CTkEntry(root, width=217/1280*root.winfo_screenwidth(),
                                    height=34/720*root.winfo_screenheight(), bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
contact_entry.place(x=351/1280*root.winfo_screenwidth(),y=154/720*root.winfo_screenheight())

#Start Date
start_entry = customtkinter.CTkEntry(root, width=217/1280*root.winfo_screenwidth(),
                                    height=34/720*root.winfo_screenheight(), bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
start_entry.place(x=351/1280*root.winfo_screenwidth(),y=193/720*root.winfo_screenheight())

#End Date
end_entry = customtkinter.CTkEntry(root, width=217/1280*root.winfo_screenwidth(),
                                    height=34/720*root.winfo_screenheight(), bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
end_entry.place(x=351/1280*root.winfo_screenwidth(),y=233/720*root.winfo_screenheight())

#Approved Button
app_button = customtkinter.CTkButton(root,text = "Approve" ,bg_color= "white", fg_color="#1572D3",text_color="white",
            border_color="#1572D3", width=87/1280*root.winfo_screenwidth(), height=32/588*root.winfo_screenheight(),
                                      font=("Poppins Medium",18))
app_button.place(x=541/1280*root.winfo_screenwidth(),y=328/720*root.winfo_screenheight())


#Right Box

#Model
model_entry = customtkinter.CTkEntry(root, width=217/1280*root.winfo_screenwidth(),
                                    height=34/720*root.winfo_screenheight(), bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
model_entry.place(x=972/1280*root.winfo_screenwidth(),y=75/720*root.winfo_screenheight())

#Capacity
capacity_entry = customtkinter.CTkEntry(root, width=217/1280*root.winfo_screenwidth(),
                                    height=34/720*root.winfo_screenheight(), bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
capacity_entry.place(x=972/1280*root.winfo_screenwidth(),y=115/720*root.winfo_screenheight())

#Transmission
mission_entry = customtkinter.CTkEntry(root, width=217/1280*root.winfo_screenwidth(),
                                    height=34/720*root.winfo_screenheight(), bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
mission_entry.place(x=972/1280*root.winfo_screenwidth(),y=154/720*root.winfo_screenheight())

#Price
price_entry = customtkinter.CTkEntry(root, width=217/1280*root.winfo_screenwidth(),
                                    height=34/720*root.winfo_screenheight(), bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
price_entry.place(x=972/1280*root.winfo_screenwidth(),y=193/720*root.winfo_screenheight())

#Status
status_entry = customtkinter.CTkEntry(root, width=217/1280*root.winfo_screenwidth(),
                                    height=34/720*root.winfo_screenheight(), bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
status_entry.place(x=972/1280*root.winfo_screenwidth(),y=233/720*root.winfo_screenheight())

#Reject Button
reject_button = customtkinter.CTkButton(root,text = "Reject" ,bg_color= "white", fg_color="#1572D3",text_color="white",
            border_color="#1572D3", width=87/1280*root.winfo_screenwidth(), height=32/588*root.winfo_screenheight(),
                                      font=("Poppins Medium",18))
reject_button.place(x=669/1280*root.winfo_screenwidth(),y=328/720*root.winfo_screenheight())


#Back Button
back_button = customtkinter.CTkButton(root,text = "Back" ,bg_color= "white", fg_color="#1572D3",text_color="white",
            border_color="#1572D3", width=87/1280*root.winfo_screenwidth(), height=32/588*root.winfo_screenheight(),
                                      font=("Poppins Medium",18))
back_button.place(x=46/1280*root.winfo_screenwidth(),y=588/720*root.winfo_screenheight())

#Treeview

def on_tree_select(event):
    selected_item = treeview.selection()
    if selected_item:
        item_values = treeview.item(selected_item, "values")
        print("Selected Booking:", item_values)

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=("Poppins Medium",18),rowheight=100)
style.configure("Treeview", font=("Poppins", 16),rowheight=40)
treeview = ttk.Treeview(root, columns=("ID","Customer Name","Customer Contact","Model",
                                        "Price", "Start Date","End Date", "Status"),
                        show="headings")

treeview.heading("ID", text="ID")
treeview.column("ID", width=8, anchor="center")

treeview.heading("Customer Name", text="Customer Name")
treeview.column("Customer Name", width=80, anchor="center")

treeview.heading("Customer Contact", text="Customer Contact")
treeview.column("Customer Contact", width=93, anchor="center")

treeview.heading("Model", text="Model")
treeview.column("Model", width=10, anchor="center")

treeview.heading("Price", text="Price")
treeview.column("Price", width=10, anchor="center")

treeview.heading("Start Date", text="End Date")
treeview.column("Start Date", width=50, anchor="center")

treeview.heading("End Date", text="End Date")
treeview.column("End Date", width=50, anchor="center")

treeview.heading("Status", text="Status")
treeview.column("Status", width=20, anchor="center")

treeview.place(x=310, y=578, width=1453/1280*root.winfo_screenwidth(), height=363/720*root.winfo_screenheight())
# Binding the select event to a callback function
treeview.bind("<<TreeviewSelect>>", on_tree_select)


root.mainloop()