import customtkinter
from PIL import Image

self.master = customtkinter.CTk()
self.master.title("Menu")
self.master.geometry('1536x800')

#Background Image
background_image = customtkinter.CTkImage(Image.open("Admin_Menu.png"), size=(self.master.self.width, self.master.self.height-64))
background_image_label = customtkinter.CTkLabel(master=self.master.master, image=background_image, text="")
background_image_label.place(relx=0, rely=0)

#Logout Button
out_button = customtkinter.CTkButton(self.master,text = "Logout" ,bg_color= "white", fg_color="#1572D3",text_color="white",
            border_color="#1572D3", width=89/1280*self.master.self.width,
                                      height=39/720*self.master.self.height, font=("Poppins Medium",18))
out_button.place(x=1148/1280*self.master.self.width,y=586/720*self.master.self.height)

#Manage Cars Button
cars_button = customtkinter.CTkButton(self.master,text = "Go" ,bg_color= "white", fg_color="#1572D3",text_color="white",
            border_color="#1572D3", width=89/1280*self.master.self.width,
                                      height=39/720*self.master.self.height, font=("Poppins Medium",18))
cars_button.place(x=999/1280*self.master.self.width,y=280/720*self.master.self.height)

#Manage Bookings Button
booking_button = customtkinter.CTkButton(self.master,text = "Go" ,bg_color= "white", fg_color="#1572D3",text_color="white",
            border_color="#1572D3", width=89/1280*self.master.self.width,
                                      height=39/720*self.master.self.height, font=("Poppins Medium",18))
booking_button.place(x=999/1280*self.master.self.width,y=280/720*self.master.self.height)

#Manage Cars Button
cars_button = customtkinter.CTkButton(self.master,text = "Go" ,bg_color= "white", fg_color="#1572D3",text_color="white",
            border_color="#1572D3", width=89/1280*self.master.self.width,
                                      height=39/720*self.master.self.height, font=("Poppins Medium",18))
cars_button.place(x=380/1280*self.master.self.width,y=280/720*self.master.self.height)

#Performance Report Button
performance_button = customtkinter.CTkButton(self.master,text = "Go" ,bg_color= "white", fg_color="#1572D3",text_color="white",
            border_color="#1572D3", width=89/1280*self.master.self.width,
                                      height=39/720*self.master.self.height, font=("Poppins Medium",18))
performance_button.place(x=729/1280*self.master.self.width,y=506/720*self.master.self.height)

self.master.mainloop()