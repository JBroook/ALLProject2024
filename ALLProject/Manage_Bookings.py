from tkinter import ttk
import ctk
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

self.master = ctk.CTk()
self.master.title("Manage Booking")
self.master.geometry('1536x800')

#Background Image
background_image = ctk.CTkImage(img.open("Manage_Booking.png"),
                                          size=(self.width, self.height-64))
background_image_label = ctk.CTkLabel(master=self.master.master, image=background_image, text="")
background_image_label.place(relx=0, rely=0)

#Left Box

#Booking ID
book_entry = ctk.CTkEntry(self.master, width=217/1280*self.width,
                                    height=34/720*self.height, bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
book_entry.place(x=351/1280*self.width,y=75/720*self.height)

#Customer Name
name_entry = ctk.CTkEntry(self.master, width=217/1280*self.width,
                                    height=34/720*self.height, bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
name_entry.place(x=351/1280*self.width,y=115/720*self.height)

#Customer Contact
contact_entry = ctk.CTkEntry(self.master, width=217/1280*self.width,
                                    height=34/720*self.height, bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
contact_entry.place(x=351/1280*self.width,y=154/720*self.height)

#Start Date
start_entry = ctk.CTkEntry(self.master, width=217/1280*self.width,
                                    height=34/720*self.height, bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
start_entry.place(x=351/1280*self.width,y=193/720*self.height)

#End Date
end_entry = ctk.CTkEntry(self.master, width=217/1280*self.width,
                                    height=34/720*self.height, bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
end_entry.place(x=351/1280*self.width,y=233/720*self.height)

#Approved Button
app_button = ctk.CTkButton(self.master,text = "Approve" ,bg_color= "white", fg_color="#1572D3",text_color="white",
            border_color="#1572D3", width=87/1280*self.width, height=32/588*self.height,
                                      font=("Poppins Medium",18))
app_button.place(x=541/1280*self.width,y=328/720*self.height)


#Right Box

#Model
model_entry = ctk.CTkEntry(self.master, width=217/1280*self.width,
                                    height=34/720*self.height, bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
model_entry.place(x=972/1280*self.width,y=75/720*self.height)

#Capacity
capacity_entry = ctk.CTkEntry(self.master, width=217/1280*self.width,
                                    height=34/720*self.height, bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
capacity_entry.place(x=972/1280*self.width,y=115/720*self.height)

#Transmission
mission_entry = ctk.CTkEntry(self.master, width=217/1280*self.width,
                                    height=34/720*self.height, bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
mission_entry.place(x=972/1280*self.width,y=154/720*self.height)

#Price
price_entry = ctk.CTkEntry(self.master, width=217/1280*self.width,
                                    height=34/720*self.height, bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
price_entry.place(x=972/1280*self.width,y=193/720*self.height)

#Status
status_entry = ctk.CTkEntry(self.master, width=217/1280*self.width,
                                    height=34/720*self.height, bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
status_entry.place(x=972/1280*self.width,y=233/720*self.height)

#Reject Button
reject_button = ctk.CTkButton(self.master,text = "Reject" ,bg_color= "white", fg_color="#1572D3",text_color="white",
            border_color="#1572D3", width=87/1280*self.width, height=32/588*self.height,
                                      font=("Poppins Medium",18))
reject_button.place(x=669/1280*self.width,y=328/720*self.height)


#Back Button
back_button = ctk.CTkButton(self.master,text = "Back" ,bg_color= "white", fg_color="#1572D3",text_color="white",
            border_color="#1572D3", width=87/1280*self.width, height=32/588*self.height,
                                      font=("Poppins Medium",18))
back_button.place(x=46/1280*self.width,y=588/720*self.height)

#Treeview

def on_tree_select(event):
    selected_item = treeview.selection()
    if selected_item:
        item_values = treeview.item(selected_item, "values")
        print("Selected Booking:", item_values)

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=("Poppins Medium",18),rowheight=100/720*self.height)
style.configure("Treeview", font=("Poppins", 16),rowheight=40/720*self.height)
treeview = ttk.Treeview(self.master, columns=("ID","Customer Name","Customer Contact","Model",
                                        "Price", "Start Date","End Date", "Status"),
                        show="headings")

treeview.heading("ID", text="ID")
treeview.column("ID", width=round(8), anchor="center")

treeview.heading("Customer Name", text="Customer Name")
treeview.column("Customer Name", width=round(80), anchor="center")

treeview.heading("Customer Contact", text="Customer Contact")
treeview.column("Customer Contact", width=round(93), anchor="center")

treeview.heading("Model", text="Model")
treeview.column("Model", width=round(10), anchor="center")

treeview.heading("Price", text="Price")
treeview.column("Price", width=round(10), anchor="center")

treeview.heading("Start Date", text="End Date")
treeview.column("Start Date", width=round(50), anchor="center")

treeview.heading("End Date", text="End Date")
treeview.column("End Date", width=round(50), anchor="center")

treeview.heading("Status", text="Status")
treeview.column("Status", width=round(20), anchor="center")

treeview.place(x=310, y=578,width=1453, height=365)
# Binding the select event to a callback function
treeview.bind("<<TreeviewSelect>>", on_tree_select)


self.master.mainloop()