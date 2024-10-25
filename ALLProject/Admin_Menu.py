import customtkinter
from PIL import Image

root = customtkinter.CTk()
root.title("Menu")
root.geometry('1536x800')

#Background Image
background_image = customtkinter.CTkImage(Image.open("Admin_Menu.png"), size=(root.winfo_screenwidth(), root.winfo_screenheight()-64))
background_image_label = customtkinter.CTkLabel(master=root.master, image=background_image, text="")
background_image_label.place(relx=0, rely=0)

#Logout Button
out_button = customtkinter.CTkButton(root,text = "Logout" ,bg_color= "white", fg_color="#1572D3",text_color="white",
            border_color="#1572D3", width=89/1280*root.winfo_screenwidth(),
                                      height=39/720*root.winfo_screenheight(), font=("Poppins Medium",18))
out_button.place(x=1148/1280*root.winfo_screenwidth(),y=586/720*root.winfo_screenheight())

#Manage Cars Button
cars_button = customtkinter.CTkButton(root,text = "Go" ,bg_color= "white", fg_color="#1572D3",text_color="white",
            border_color="#1572D3", width=89/1280*root.winfo_screenwidth(),
                                      height=39/720*root.winfo_screenheight(), font=("Poppins Medium",18))
cars_button.place(x=999/1280*root.winfo_screenwidth(),y=280/720*root.winfo_screenheight())

#Manage Bookings Button
booking_button = customtkinter.CTkButton(root,text = "Go" ,bg_color= "white", fg_color="#1572D3",text_color="white",
            border_color="#1572D3", width=89/1280*root.winfo_screenwidth(),
                                      height=39/720*root.winfo_screenheight(), font=("Poppins Medium",18))
booking_button.place(x=999/1280*root.winfo_screenwidth(),y=280/720*root.winfo_screenheight())

#Manage Cars Button
cars_button = customtkinter.CTkButton(root,text = "Go" ,bg_color= "white", fg_color="#1572D3",text_color="white",
            border_color="#1572D3", width=89/1280*root.winfo_screenwidth(),
                                      height=39/720*root.winfo_screenheight(), font=("Poppins Medium",18))
cars_button.place(x=380/1280*root.winfo_screenwidth(),y=280/720*root.winfo_screenheight())

#Performance Report Button
performance_button = customtkinter.CTkButton(root,text = "Go" ,bg_color= "white", fg_color="#1572D3",text_color="white",
            border_color="#1572D3", width=89/1280*root.winfo_screenwidth(),
                                      height=39/720*root.winfo_screenheight(), font=("Poppins Medium",18))
performance_button.place(x=729/1280*root.winfo_screenwidth(),y=506/720*root.winfo_screenheight())

root.mainloop()