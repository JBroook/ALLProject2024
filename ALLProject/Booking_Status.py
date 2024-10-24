import customtkinter
from PIL import Image
import sqlite3

root = customtkinter.CTk()
root.title("Booking Status")
root.geometry('1536x800')

#Background Image
background_image = customtkinter.CTkImage(Image.open("Booking_Status.png"), size=(root.winfo_screenwidth(), root.winfo_screenheight()-64))
background_image_label = customtkinter.CTkLabel(master=root.master, image=background_image, text="")
background_image_label.place(relx=0, rely=0)

#Current Booking
current_button = customtkinter.CTkButton(root,text = "Current Booking" ,bg_color= "white", fg_color="#1572D3",text_color="white",
            border_color="#1572D3", width=775, height=88, font=("Poppins Medium",18))
current_button.place(x=230/1280*root.winfo_screenwidth(),y=240/720*root.winfo_screenheight())

#Past Booking
past_button = customtkinter.CTkButton(root,text = "Past Booking" ,bg_color= "white", fg_color="#1572D3",text_color="white",
            border_color="#1572D3", width=775, height=88, font=("Poppins Medium",18))
past_button.place(x=230/1280*root.winfo_screenwidth(),y=387/720*root.winfo_screenheight())

#Back Button
back_button = customtkinter.CTkButton(root,text = "Back" ,bg_color= "white", fg_color="#1572D3",text_color="white",
            border_color="#1572D3", width=89, height=39, font=("Poppins Medium",18))
back_button.place(x=45/1280*root.winfo_screenwidth(),y=588/720*root.winfo_screenheight())

root.mainloop()