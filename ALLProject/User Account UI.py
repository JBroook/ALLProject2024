import customtkinter
from customtkinter import CTkImage
from PIL import Image

root=customtkinter.CTk()
root.geometry("1200x800")

user_account_ui=customtkinter.CTkImage(light_image=Image.open("Project Images/DriveEaseUI.png"),size=(root.winfo_screenwidth(),root.winfo_screenheight()-68))
user_account_ui_label=customtkinter.CTkLabel(root,image=user_account_ui,text="")
user_account_ui_label.place(x=0,y=0,anchor="nw")

first_name_entry=customtkinter.CTkEntry(root,
                                        width=357.85/1707*root.winfo_screenwidth(),
                                        height=56.69/1067*root.winfo_screenheight(),
                                        bg_color="white",
                                        fg_color="#D9D9D9",
                                        border_color="#D9D9D9",
                                        text_color="black",
                                        font=("Poppins Light",24))
first_name_entry.place(x=704.58/1707*root.winfo_screenwidth(),y=362.58/1067*root.winfo_screenheight(),anchor="nw")

last_name_entry=customtkinter.CTkEntry(root,width=357.85/1707*root.winfo_screenwidth(),
                                        height=56.69/1067*root.winfo_screenheight(),
                                        bg_color="white",
                                        fg_color="#D9D9D9",
                                        border_color="#D9D9D9",
                                        text_color="black",
                                        font=("Poppins Light",24))
last_name_entry.place(x=1122.44/1707*root.winfo_screenwidth(),y=362.58/1067*root.winfo_screenheight(),anchor="nw")

username_entry=customtkinter.CTkEntry(root,width=357.85/1707*root.winfo_screenwidth(),
                                        height=56.69/1067*root.winfo_screenheight(),
                                        bg_color="white",
                                        fg_color="#D9D9D9",
                                        border_color="#D9D9D9",
                                        text_color="black",
                                        font=("Poppins Light",24))
username_entry.place(x=704.58/1707*root.winfo_screenwidth(),y=500.77/1067*root.winfo_screenheight(),anchor="nw")

email_entry=customtkinter.CTkEntry(root,width=357.85/1707*root.winfo_screenwidth(),
                                        height=56.69/1067*root.winfo_screenheight(),
                                        bg_color="white",
                                        fg_color="#D9D9D9",
                                        border_color="#D9D9D9",
                                        text_color="black",
                                        font=("Poppins Light",24))
email_entry.place(x=704.58/1707*root.winfo_screenwidth(),y=638.95/1067*root.winfo_screenheight(),anchor="nw")

back_btn=customtkinter.CTkButton(root,width=176.7/1707*root.winfo_screenwidth(),height=75/1067*root.winfo_screenheight(),bg_color="white",fg_color="#1572D3",text="Back",text_color="white",font=("Poppins Light",24))
back_btn.place(x=81.13/1707*root.winfo_screenwidth(),y=891.25/1067*root.winfo_screenheight(),anchor="nw")

edit_btn=customtkinter.CTkButton(root,width=176.7/1707*root.winfo_screenwidth(),height=75/1067*root.winfo_screenheight(),bg_color="white",fg_color="#1572D3",text="Edit",text_color="white",font=("Poppins Light",24))
edit_btn.place(x=1350/1707*root.winfo_screenwidth(),y=720/1067*root.winfo_screenheight(),anchor="nw")

root.mainloop()