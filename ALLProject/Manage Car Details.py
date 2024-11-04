import ctk
from tkinter import messagebox, ttk, filedialog
from PIL import Image
import sqlite3

self.master=ctk.CTk()
self.master.geometry("1200x900")

manage_car_ui=ctk.CTkImage(light_image=img.open("Project Images/manage car details.png"),
                                       size=(self.width,self.height-68))
manage_car_ui_label=ctk.CTkLabel(self.master,image=manage_car_ui,text="")
manage_car_ui_label.place(x=0,y=0,anchor="nw")

selected_car_id=None
image_path=""

def connect_db():
    conn = sqlite3.connect('manage_car_details.db')
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_number TEXT,
            model TEXT,
            capacity TEXT,
            transmission TEXT,
            manufacture_year TEXT,
            price REAL,
            image_path TEXT
        )
    ''')
    conn.commit()
    return conn, cursor

def save_data():
    registration_number = registration_number_entry.get()
    model = model_entry.get()
    capacity = capacity_entry.get()
    transmission = transmission_entry.get()
    manufacture_year = manufacture_year_entry.get()
    price = price_entry.get()
    if not image_path:
        messagebox.showwarning("Warning", "Please upload an image.")
        return

    conn, cursor = connect_db()
    cursor.execute('SELECT COUNT(*) FROM cars WHERE registration_number = ?', (registration_number,))
    if cursor.fetchone()[0] > 0:
        messagebox.showwarning("Warning", "This registration number already exists.")
        conn.close()
        return

    cursor.execute(''' 
        INSERT INTO cars (registration_number, model, capacity, transmission, manufacture_year, price, image_path)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (registration_number, model, capacity, transmission, manufacture_year, price, image_path))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Data saved successfully!")
    refresh_treeview()

def refresh_treeview():
    for row in treeview.get_children():
        treeview.delete(row)

    conn, cursor = connect_db()
    cursor.execute('SELECT id, registration_number, model, capacity, transmission, manufacture_year, price FROM cars')
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        treeview.insert("", "end", values=row)

def browse_image():
    global image_path
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if image_path:
        upload_image()

def upload_image():
    try:
        img=ctk.CTkImage(light_image=img.open(image_path),size=(450/1707*self.width,300/1067*self.height))
        image_display.configure(image=img)
        image_display.image=img

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load image: {e}")

def delete_data():
    global selected_car_id
    if selected_car_id is not None:
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this car?")
        if confirm:
            conn, cursor = connect_db()
            cursor.execute('DELETE FROM cars WHERE id = ?', (selected_car_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Car deleted successfully!")
            refresh_treeview()
            clear_selection()
    else:
        messagebox.showwarning("Warning", "Please select a car to delete.")

def update_data():
    global selected_car_id
    if selected_car_id is not None:
        registration_number = registration_number_entry.get()
        model = model_entry.get()
        capacity = capacity_entry.get()
        transmission = transmission_entry.get()
        manufacture_year = manufacture_year_entry.get()
        price = price_entry.get()

        conn, cursor = connect_db()
        cursor.execute(''' 
            UPDATE cars 
            SET registration_number = ?, model = ?, capacity = ?, transmission = ?, manufacture_year = ?, price = ?
            WHERE id = ?
        ''', (registration_number, model, capacity, transmission, manufacture_year, price, selected_car_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Car updated successfully!")
        refresh_treeview()
        clear_selection()
    else:
        messagebox.showwarning("Warning", "Please select a car to update.")

def select_item(event):
    global selected_car_id, image_path
    selected_item = treeview.selection()
    if selected_item:
        item = treeview.item(selected_item)
        values = item['values']
        selected_car_id = values[0]

        conn, cursor = connect_db()
        cursor.execute('SELECT * FROM cars WHERE id = ?', (selected_car_id,))
        car_data = cursor.fetchone()
        conn.close()

        if car_data:
            registration_number_entry.delete(0, 'end')
            registration_number_entry.insert(0, car_data[1])
            model_entry.delete(0, 'end')
            model_entry.insert(0, car_data[2])
            capacity_entry.delete(0, 'end')
            capacity_entry.insert(0, car_data[3])
            transmission_entry.delete(0, 'end')
            transmission_entry.insert(0, car_data[4])
            manufacture_year_entry.delete(0, 'end')
            manufacture_year_entry.insert(0, car_data[5])
            price_entry.delete(0, 'end')
            price_entry.insert(0, car_data[6])

            image_path = car_data[7]
            if image_path:
                upload_image()

def clear_selection():
    global selected_car_id
    selected_car_id = None
    registration_number_entry.delete(0, 'end')
    model_entry.delete(0, 'end')
    capacity_entry.delete(0, 'end')
    transmission_entry.delete(0, 'end')
    manufacture_year_entry.delete(0, 'end')
    price_entry.delete(0, 'end')
    image_display.configure(image="")

registration_number_entry=ctk.CTkEntry(self.master,width=363/1707*self.width,
                                                 height=34/1067*self.height,
                                                 bg_color="#F0F4FC",
                                                 fg_color="#D9D9D9",
                                                 border_color="#D9D9D9",
                                                 text_color="black",
                                                 font=("Poppins Light",24))
registration_number_entry.place(x=1041/1707*self.width,y=143/1067*self.height,anchor="nw")

model_entry=ctk.CTkEntry(self.master,width=363/1707*self.width,
                                   height=34/1067*self.height,
                                   bg_color="#F0F4FC",
                                   fg_color="#D9D9D9",
                                   border_color="#D9D9D9",
                                   text_color="black",
                                   font=("Poppins Light",24))
model_entry.place(x=1041/1707*self.width,y=189/1067*self.height,anchor="nw")

capacity_entry=ctk.CTkEntry(self.master,width=363/1707*self.width,
                                      height=34/1067*self.height,
                                      bg_color="#F0F4FC",
                                      fg_color="#D9D9D9",
                                      border_color="#D9D9D9",
                                      text_color="black",
                                      font=("Poppins Light",24))
capacity_entry.place(x=1041/1707*self.width,y=234/1067*self.height,anchor="nw")

transmission_entry=ctk.CTkEntry(self.master,width=363/1707*self.width,
                                          height=34/1067*self.height,
                                          bg_color="#F0F4FC",
                                          fg_color="#D9D9D9",
                                          border_color="#D9D9D9",
                                          text_color="black",
                                          font=("Poppins Light",24))
transmission_entry.place(x=1041/1707*self.width,y=279/1067*self.height,anchor="nw")

manufacture_year_entry=ctk.CTkEntry(self.master,width=363/1707*self.width,
                                              height=34/1067*self.height,
                                              bg_color="#F0F4FC",
                                              fg_color="#D9D9D9",
                                              border_color="#D9D9D9",
                                              text_color="black",
                                              font=("Poppins Light",24))
manufacture_year_entry.place(x=1041/1707*self.width,y=325/1067*self.height,anchor="nw")

price_entry=ctk.CTkEntry(self.master,width=363/1707*self.width,
                                   height=34/1067*self.height,
                                   bg_color="#F0F4FC",
                                   fg_color="#D9D9D9",
                                   border_color="#D9D9D9",
                                   text_color="black",
                                   font=("Poppins Light",24))
price_entry.place(x=1041/1707*self.width,y=371/1067*self.height,anchor="nw")

image_display=ctk.CTkLabel(self.master,width=494/1707*self.width,
                                     height=358/1067*self.height,
                                     text="",
                                     bg_color="#F0F4FC",
                                     fg_color="#FFFFFF",
                                     corner_radius=9)
image_display.place(x=208/1707*self.width,y=144/1067*self.height,anchor="nw")

insert_image_btn=ctk.CTkButton(self.master,width=208/1707*self.width,
                                         height=45.39/1067*self.height,
                                         bg_color="#F0F4FC",
                                         fg_color="#1572D3",
                                         text="Insert Image",
                                         text_color="#FFFFFF",
                                         font=("Poppins",24),
                                         command=browse_image)
insert_image_btn.place(x=783/1707*self.width,y=417/1067*self.height,anchor="nw")

save_btn=ctk.CTkButton(self.master,width=150/1707*self.width,
                                 height=58/1067*self.height,
                                 bg_color="#F0F4FC",
                                 fg_color="#1572D3",
                                 text="Save",
                                 text_color="#FFFFFF",
                                 font=("Poppins",24),
                                 command=save_data)
save_btn.place(x=783/1707*self.width,y=488/1067*self.height,anchor="nw")

update_btn=ctk.CTkButton(self.master,width=150/1707*self.width,
                                   height=58/1067*self.height,
                                   bg_color="#F0F4FC",
                                   fg_color="#1572D3",
                                   text="Update",
                                   text_color="#FFFFFF",
                                   font=("Poppins",24),
                                   command=update_data)
update_btn.place(x=955/1707*self.width,y=488/1067*self.height,anchor="nw")

delete_btn=ctk.CTkButton(self.master,width=150/1707*self.width,
                                 height=58/1067*self.height,
                                 bg_color="#F0F4FC",
                                 fg_color="#1572D3",
                                 text="Delete",
                                 text_color="#FFFFFF",
                                 font=("Poppins",24),
                                 command=delete_data)
delete_btn.place(x=1127/1707*self.width,y=488/1067*self.height,anchor="nw")

clear_btn=ctk.CTkButton(self.master,width=150/1707*self.width,
                                 height=58/1067*self.height,
                                 bg_color="#F0F4FC",
                                 fg_color="#1572D3",
                                 text="Clear",
                                 text_color="#FFFFFF",
                                 font=("Poppins",24),
                                 command=clear_selection)
clear_btn.place(x=1299/1707*self.width,y=488/1067*self.height,anchor="nw")

back_btn=ctk.CTkButton(self.master,width=150/1707*self.width,
                                 height=58/1067*self.height,
                                 bg_color="#F0F4FC",
                                 fg_color="#1572D3",
                                 text="Back",
                                 text_color="#FFFFFF",
                                 font=("Poppins",24))
back_btn.place(x=58/1707*self.width,y=908/1067*self.height,anchor="nw")

style = ttk.Style()
style.configure("Treeview.Heading",font=("Poppins Medium",18),rowheight=30,background="#FFFFFF")
treeview = ttk.Treeview(self.master, columns=("ID", "Registration Number", "Model", "Capacity", "Transmission", "Manufacture Year", "Price"), show="headings")
treeview.place(x=260,y=600,
               width=1500,
               height=380)
treeview.bind("<<TreeviewSelect>>",select_item)

treeview.heading("ID", text="ID")
treeview.column("ID", width=100, anchor="center")
treeview.heading("Registration Number", text="Registration Number")
treeview.column("Registration Number", width=300, anchor="center")
treeview.heading("Model", text="Model")
treeview.column("Model", width=200, anchor="center")
treeview.heading("Capacity", text="Capacity")
treeview.column("Capacity", width=150, anchor="center")
treeview.heading("Transmission", text="Transmission")
treeview.column("Transmission", width=200, anchor="center")
treeview.heading("Manufacture Year", text="Manufacture Year")
treeview.column("Manufacture Year", width=200, anchor="center")
treeview.heading("Price",text="Price (RM)")
treeview.column("Price", width=150, anchor="center")

refresh_treeview()

self.master.mainloop()