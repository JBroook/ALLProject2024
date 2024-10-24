import customtkinter
from PIL import Image
import sqlite3

self.master = customtkinter.CTk()
self.master.title("Booking Status")
self.master.geometry('1536x800')

#Background Image
background_image = customtkinter.CTkImage(Image.open("main/assets/Booking_Status.png"), size=(self.width, self.height - 64))
background_image_label = customtkinter.CTkLabel(master=self.master.master, image=background_image, text="")
background_image_label.place(relx=0, rely=0)

#Current Booking
current_button = customtkinter.CTkButton(self.master,text = "Current Booking" ,bg_color= "white", fg_color="#1572D3",text_color="white",
            border_color="#1572D3", width=775/1280*self.width,
                                         height=88/720*self.height, font=("Poppins Medium",18))
current_button.place(x=230/1280*self.width,y=240/720*self.height)

#Past Booking
past_button = customtkinter.CTkButton(self.master,text = "Past Booking" ,bg_color= "white", fg_color="#1572D3",text_color="white",
            border_color="#1572D3", width=775/1280*self.width,
                                      height=88/720*self.height, font=("Poppins Medium",18))
past_button.place(x=230/1280*self.width,y=387/720*self.height)

#Back Button
back_button = customtkinter.CTkButton(self.master,text = "Back" ,bg_color= "white", fg_color="#1572D3",text_color="white",
            border_color="#1572D3", width=89/1280*self.width,
                                      height=39/720*self.height, font=("Poppins Medium",18))
back_button.place(x=45/1280*self.width,y=588/720*self.height)

self.master.mainloop()