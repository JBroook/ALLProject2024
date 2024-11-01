import customtkinter
from tkinter import messagebox, ttk, filedialog
from PIL import Image
import sqlite3

root3=customtkinter.CTk()
root3.geometry("1200x900")

manage_car_ui=customtkinter.CTkImage(light_image=Image.open("Project Images/manage car details.png"),
                                       size=(root3.winfo_screenwidth(),root3.winfo_screenheight()-68))
manage_car_ui_label=customtkinter.CTkLabel(root3,image=manage_car_ui,text="")
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
        img=customtkinter.CTkImage(light_image=Image.open(image_path),size=(450/1707*root3.winfo_screenwidth(),300/1067*root3.winfo_screenheight()))
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

registration_number_entry=customtkinter.CTkEntry(root3,width=363/1707*root3.winfo_screenwidth(),
                                                 height=34/1067*root3.winfo_screenheight(),
                                                 bg_color="#F0F4FC",
                                                 fg_color="#D9D9D9",
                                                 border_color="#D9D9D9",
                                                 text_color="black",
                                                 font=("Poppins Light",24))
registration_number_entry.place(x=1041/1707*root3.winfo_screenwidth(),y=143/1067*root3.winfo_screenheight(),anchor="nw")

model_entry=customtkinter.CTkEntry(root3,width=363/1707*root3.winfo_screenwidth(),
                                   height=34/1067*root3.winfo_screenheight(),
                                   bg_color="#F0F4FC",
                                   fg_color="#D9D9D9",
                                   border_color="#D9D9D9",
                                   text_color="black",
                                   font=("Poppins Light",24))
model_entry.place(x=1041/1707*root3.winfo_screenwidth(),y=189/1067*root3.winfo_screenheight(),anchor="nw")

capacity_entry=customtkinter.CTkEntry(root3,width=363/1707*root3.winfo_screenwidth(),
                                      height=34/1067*root3.winfo_screenheight(),
                                      bg_color="#F0F4FC",
                                      fg_color="#D9D9D9",
                                      border_color="#D9D9D9",
                                      text_color="black",
                                      font=("Poppins Light",24))
capacity_entry.place(x=1041/1707*root3.winfo_screenwidth(),y=234/1067*root3.winfo_screenheight(),anchor="nw")

transmission_entry=customtkinter.CTkEntry(root3,width=363/1707*root3.winfo_screenwidth(),
                                          height=34/1067*root3.winfo_screenheight(),
                                          bg_color="#F0F4FC",
                                          fg_color="#D9D9D9",
                                          border_color="#D9D9D9",
                                          text_color="black",
                                          font=("Poppins Light",24))
transmission_entry.place(x=1041/1707*root3.winfo_screenwidth(),y=279/1067*root3.winfo_screenheight(),anchor="nw")

manufacture_year_entry=customtkinter.CTkEntry(root3,width=363/1707*root3.winfo_screenwidth(),
                                              height=34/1067*root3.winfo_screenheight(),
                                              bg_color="#F0F4FC",
                                              fg_color="#D9D9D9",
                                              border_color="#D9D9D9",
                                              text_color="black",
                                              font=("Poppins Light",24))
manufacture_year_entry.place(x=1041/1707*root3.winfo_screenwidth(),y=325/1067*root3.winfo_screenheight(),anchor="nw")

price_entry=customtkinter.CTkEntry(root3,width=363/1707*root3.winfo_screenwidth(),
                                   height=34/1067*root3.winfo_screenheight(),
                                   bg_color="#F0F4FC",
                                   fg_color="#D9D9D9",
                                   border_color="#D9D9D9",
                                   text_color="black",
                                   font=("Poppins Light",24))
price_entry.place(x=1041/1707*root3.winfo_screenwidth(),y=371/1067*root3.winfo_screenheight(),anchor="nw")

image_display=customtkinter.CTkLabel(root3,width=494/1707*root3.winfo_screenwidth(),
                                     height=358/1067*root3.winfo_screenheight(),
                                     text="",
                                     bg_color="#F0F4FC",
                                     fg_color="#FFFFFF",
                                     corner_radius=9)
image_display.place(x=208/1707*root3.winfo_screenwidth(),y=144/1067*root3.winfo_screenheight(),anchor="nw")

insert_image_btn=customtkinter.CTkButton(root3,width=208/1707*root3.winfo_screenwidth(),
                                         height=45.39/1067*root3.winfo_screenheight(),
                                         bg_color="#F0F4FC",
                                         fg_color="#1572D3",
                                         text="Insert Image",
                                         text_color="#FFFFFF",
                                         font=("Poppins",24),
                                         command=browse_image)
insert_image_btn.place(x=783/1707*root3.winfo_screenwidth(),y=417/1067*root3.winfo_screenheight(),anchor="nw")

save_btn=customtkinter.CTkButton(root3,width=150/1707*root3.winfo_screenwidth(),
                                 height=58/1067*root3.winfo_screenheight(),
                                 bg_color="#F0F4FC",
                                 fg_color="#1572D3",
                                 text="Save",
                                 text_color="#FFFFFF",
                                 font=("Poppins",24),
                                 command=save_data)
save_btn.place(x=783/1707*root3.winfo_screenwidth(),y=488/1067*root3.winfo_screenheight(),anchor="nw")

update_btn=customtkinter.CTkButton(root3,width=150/1707*root3.winfo_screenwidth(),
                                   height=58/1067*root3.winfo_screenheight(),
                                   bg_color="#F0F4FC",
                                   fg_color="#1572D3",
                                   text="Update",
                                   text_color="#FFFFFF",
                                   font=("Poppins",24),
                                   command=update_data)
update_btn.place(x=955/1707*root3.winfo_screenwidth(),y=488/1067*root3.winfo_screenheight(),anchor="nw")

delete_btn=customtkinter.CTkButton(root3,width=150/1707*root3.winfo_screenwidth(),
                                 height=58/1067*root3.winfo_screenheight(),
                                 bg_color="#F0F4FC",
                                 fg_color="#1572D3",
                                 text="Delete",
                                 text_color="#FFFFFF",
                                 font=("Poppins",24),
                                 command=delete_data)
delete_btn.place(x=1127/1707*root3.winfo_screenwidth(),y=488/1067*root3.winfo_screenheight(),anchor="nw")

clear_btn=customtkinter.CTkButton(root3,width=150/1707*root3.winfo_screenwidth(),
                                 height=58/1067*root3.winfo_screenheight(),
                                 bg_color="#F0F4FC",
                                 fg_color="#1572D3",
                                 text="Clear",
                                 text_color="#FFFFFF",
                                 font=("Poppins",24),
                                 command=clear_selection)
clear_btn.place(x=1299/1707*root3.winfo_screenwidth(),y=488/1067*root3.winfo_screenheight(),anchor="nw")

back_btn=customtkinter.CTkButton(root3,width=150/1707*root3.winfo_screenwidth(),
                                 height=58/1067*root3.winfo_screenheight(),
                                 bg_color="#F0F4FC",
                                 fg_color="#1572D3",
                                 text="Back",
                                 text_color="#FFFFFF",
                                 font=("Poppins",24))
back_btn.place(x=58/1707*root3.winfo_screenwidth(),y=908/1067*root3.winfo_screenheight(),anchor="nw")

style = ttk.Style()
style.configure("Treeview.Heading",font=("Poppins Medium",26),rowheight=30,background="#FFFFFF")
treeview = ttk.Treeview(root3, columns=("ID", "Registration Number", "Model", "Capacity", "Transmission", "Manufacture Year", "Price"), show="headings")
treeview.place(x=260,y=850,
               width=2000/1707*root3.winfo_screenwidth(),
               height=450/1067*root3.winfo_screenheight())
treeview.bind("<<TreeviewSelect>>",select_item)

treeview.heading("ID", text="ID")
treeview.column("ID", width=100, anchor="center")
treeview.heading("Registration Number", text="Registration Number")
treeview.column("Registration Number", width=350, anchor="center")
treeview.heading("Model", text="Model")
treeview.column("Model", width=300, anchor="center")
treeview.heading("Capacity", text="Capacity")
treeview.column("Capacity", width=300, anchor="center")
treeview.heading("Transmission", text="Transmission")
treeview.column("Transmission", width=300, anchor="center")
treeview.heading("Manufacture Year", text="Manufacture Year")
treeview.column("Manufacture Year", width=300, anchor="center")
treeview.heading("Price",text="Price (RM)")
treeview.column("Price", width=250, anchor="center")

refresh_treeview()

root3.mainloop()