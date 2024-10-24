import customtkinter
from PIL import Image

root2=customtkinter.CTk()
root2.geometry("1200x800")

rate_booking_ui=customtkinter.CTkImage(light_image=Image.open("Project Images/Rate car.png"),size=(root2.winfo_screenwidth(),root2.winfo_screenheight()-68))
rate_booking_ui_label=customtkinter.CTkLabel(root2,image=rate_booking_ui,text="")
rate_booking_ui_label.place(x=0,y=0,anchor="nw")

booking=[0,"20-10-2024","25-10-2024","George Town","Perodua Axia","Project Images/PeroduaAxia.jpg"]

car_name=customtkinter.CTkLabel(root2,width=333/1707*root2.winfo_screenwidth(),height=49.66/1067*root2.winfo_screenheight(),fg_color="#FFFFFF",bg_color="#FFFFFF",text=booking[4],text_color="#000000",font=("Poppins",48))
car_name.place(x=380/1707*root2.winfo_screenwidth(),y=250.6/1067*root2.winfo_screenheight(),anchor="nw")

car_picture=customtkinter.CTkImage(light_image=Image.open(booking[5]),size=(580.22/1707*root2.winfo_screenwidth(),307.49/1067*root2.winfo_screenheight()))
car_picture_label=customtkinter.CTkLabel(root2,image=car_picture,text="")
car_picture_label.place(x=261/1707*root2.winfo_screenwidth(),y=331.09/1067*root2.winfo_screenheight(),anchor="nw")

start_date=customtkinter.CTkLabel(root2,width=234/1707*root2.winfo_screenwidth(),height=37/1067*root2.winfo_screenheight(),fg_color="#FFFFFF",bg_color="#FFFFFF",text=booking[1],text_color="#747474",font=("Poppins",32))
start_date.place(x=352/1707*root2.winfo_screenwidth(),y=695/1067*root2.winfo_screenheight(),anchor="nw")

end_date=customtkinter.CTkLabel(root2,width=234/1707*root2.winfo_screenwidth(),height=37/1067*root2.winfo_screenheight(),fg_color="#FFFFFF",bg_color="#FFFFFF",text=booking[2],text_color="#747474",font=("Poppins",32))
end_date.place(x=344/1707*root2.winfo_screenwidth(),y=738.81/1067*root2.winfo_screenheight(),anchor="nw")

location=customtkinter.CTkLabel(root2,width=234/1707*root2.winfo_screenwidth(),height=37/1067*root2.winfo_screenheight(),fg_color="#FFFFFF",bg_color="#FFFFFF",text=booking[3],text_color="#747474",font=("Poppins",32))
location.place(x=647/1707*root2.winfo_screenwidth(),y=718/1067*root2.winfo_screenheight(),anchor="nw")

comment_entry=customtkinter.CTkTextbox(root2,width=492/1707*root2.winfo_screenwidth(),
                                        height=449/1067*root2.winfo_screenheight(),
                                        fg_color="#D9D9D9",
                                        border_color="#D9D9D9",
                                        corner_radius=8,
                                        wrap="word",
                                        scrollbar_button_color="#000000",
                                        text_color="black",
                                        font=("Poppins Light",32))
comment_entry.place(x=1068/1707*root2.winfo_screenwidth(),y=306/1067*root2.winfo_screenheight(),anchor="nw")

btn1=customtkinter.CTkButton(root2,width=79/1707*root2.winfo_screenwidth(),height=75/1067*root2.winfo_screenheight(),fg_color="#EFBF14",text="1",text_color="#000000",font=("Poppins Light",32))
btn1.place(x=1084/1707*root2.winfo_screenwidth(),y=182/1067*root2.winfo_screenheight(),anchor="nw")

btn2=customtkinter.CTkButton(root2,width=79/1707*root2.winfo_screenwidth(),height=75/1067*root2.winfo_screenheight(),bg_color="white",fg_color="#EFBF14",text="2",text_color="#000000",font=("Poppins Light",32))
btn2.place(x=1179/1707*root2.winfo_screenwidth(),y=182/1067*root2.winfo_screenheight(),anchor="nw")

btn3=customtkinter.CTkButton(root2,width=79/1707*root2.winfo_screenwidth(),height=75/1067*root2.winfo_screenheight(),bg_color="white",fg_color="#EFBF14",text="3",text_color="#000000",font=("Poppins Light",32))
btn3.place(x=1274/1707*root2.winfo_screenwidth(),y=182/1067*root2.winfo_screenheight(),anchor="nw")

btn4=customtkinter.CTkButton(root2,width=79/1707*root2.winfo_screenwidth(),height=75/1067*root2.winfo_screenheight(),bg_color="white",fg_color="#EFBF14",text="4",text_color="#000000",font=("Poppins Light",32))
btn4.place(x=1369/1707*root2.winfo_screenwidth(),y=182/1067*root2.winfo_screenheight(),anchor="nw")

btn5=customtkinter.CTkButton(root2,width=79/1707*root2.winfo_screenwidth(),height=75/1067*root2.winfo_screenheight(),bg_color="white",fg_color="#EFBF14",text="5",text_color="#000000",font=("Poppins Light",32))
btn5.place(x=1464/1707*root2.winfo_screenwidth(),y=182/1067*root2.winfo_screenheight(),anchor="nw")

bck_btn=customtkinter.CTkButton(root2,width=171/1707*root2.winfo_screenwidth(),height=69/1067*root2.winfo_screenheight(),fg_color="#1572D3",text="Back",text_color="white",font=("Poppins Light",24))
bck_btn.place(x=72/1707*root2.winfo_screenwidth(),y=881/1067*root2.winfo_screenheight(),anchor="nw")

confirm_btn=customtkinter.CTkButton(root2,width=171/1707*root2.winfo_screenwidth(),height=69/1067*root2.winfo_screenheight(),fg_color="#1572D3",text="Confirm",text_color="white",font=("Poppins Light",24))
confirm_btn.place(x=1389/1707*root2.winfo_screenwidth(),y=788/1067*root2.winfo_screenheight(),anchor="nw")

root2.mainloop()