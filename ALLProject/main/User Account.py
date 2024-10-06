import tkinter as tk
from tkinter import ttk
import customtkinter
from PIL import Image,ImageTk

my_page=customtkinter.CTk()
my_page.geometry('700x600')
my_page.title("User Account")

frame_one=customtkinter.CTkFrame(master=my_page,fg_color="#393E46",corner_radius=0)
frame_one.pack(side="left",fill="both")

my_image=Image.open("../../../PycharmProjects/GroupProject/Project Images/Project Images/Image_1.png").resize((200, 150))
image_tk=ImageTk.PhotoImage(my_image)
label=ttk.Label(my_page,image=image_tk)
label.place(x=50,y=50)

welcome=tk.Label(my_page,text="Welcome", bg="#393E46", fg="white", font=("Arial",30,"bold"))
welcome.place(x=50,y=300)
entry_username_frame_one=tk.Entry(my_page,bg="#393E46",width=10,font=("Arial",30,"normal"))
entry_username_frame_one.place(x=40,y=350)

back=tk.Button(my_page,text="Back", bg="#222831",fg="red",font=("Arial",35,"bold"))
back.place(x=10,y=800)

frame_two=customtkinter.CTkFrame(master=my_page,fg_color="#00ADB5",corner_radius=0)
frame_two.pack(expand="true",fill="both")

firstname=tk.Label(my_page,text="First Name:",bg="#00ADB5", fg="black",font=("Arial",20,"bold"))
firstname.place(x=320,y=100)
entry_firstname=tk.Entry(my_page,bg="#00ADB5",width=20,font=("Arial",20,"normal"))
entry_firstname.place(x=480,y=100)

lastname=tk.Label(my_page,text="Last Name:",bg="#00ADB5",fg="black",font=("Arial",20,"bold"))
lastname.place(x=320,y=150)
entry_lastname=tk.Entry(my_page,bg="#00ADB5",width=20,font=("Arial",20,"normal"))
entry_lastname.place(x=475,y=150)

username_frame_two=tk.Label(my_page,text="Username:",bg="#00ADB5",fg="black",font=("Arial",20,"bold"))
username_frame_two.place(x=320,y=200)
entry_username_frame_two=tk.Entry(my_page,bg="#00ADB5",width=20,font=("Arial",20,"normal"))
entry_username_frame_two.place(x=470,y=200)

email=tk.Label(my_page,text="Email:",bg="#00ADB5",fg="black",font=("Arial",20,"bold"))
email.place(x=320,y=250)
entry_email=tk.Entry(my_page,bg="#00ADB5",width=35,font=("Arial",20,"normal"))
entry_email.place(x=420,y=250)

my_page.mainloop()