import customtkinter
from PIL import Image

root1=customtkinter.CTk()
root1.geometry("1200x800")

current_booking_ui=customtkinter.CTkImage(light_image=Image.open("Project Images/Current Booking.png"),size=(root1.winfo_screenwidth(),root1.winfo_screenheight()-68))
current_booking_ui_label=customtkinter.CTkLabel(root1,image=current_booking_ui,text="")
current_booking_ui_label.place(x=0,y=0,anchor="nw")

booking_page=[0,"Perodua Axia","Project Images/PeroduaAxia.jpg","5 people","Auto","20-10-2024","25-10-2024","George Town","RM98/day","Pending"]

car_image_ph=customtkinter.CTkImage(light_image=Image.open(booking_page[2]),size=(563/1707*root1.winfo_screenwidth(),327/1069*root1.winfo_screenheight()))
car_image_ph_label=customtkinter.CTkLabel(root1,image=car_image_ph,text="")
car_image_ph_label.place(x=333/1707*root1.winfo_screenwidth(),y=310/1067*root1.winfo_screenheight(),anchor="nw")

car_name=customtkinter.CTkLabel(root1,width=442/1707*root1.winfo_screenwidth(),height=61/1067*root1.winfo_screenheight(),fg_color="#FFFFFF",bg_color="#FFFFFF",text=booking_page[1],text_color="#000000",font=("Poppins",32))
car_name.place(x=1030/1707*root1.winfo_screenwidth(),y=240/1067*root1.winfo_screenheight(),anchor="nw")

capacity=customtkinter.CTkLabel(root1,width=125/1707*root1.winfo_screenwidth(),height=39/1067*root1.winfo_screenheight(),fg_color="#FFFFFF",bg_color="#FFFFFF",text=booking_page[3],anchor="w",text_color="#747474",font=("Poppins Light",24))
capacity.place(x=1100/1707*root1.winfo_screenwidth(),y=333/1067*root1.winfo_screenheight(),anchor="nw")

type=customtkinter.CTkLabel(root1,width=115/1707*root1.winfo_screenwidth(),height=39/1067*root1.winfo_screenheight(),fg_color="#FFFFFF",bg_color="#FFFFFF",text=booking_page[4],anchor="w",text_color="#747474",font=("Poppins Light",24))
type.place(x=1350/1707*root1.winfo_screenwidth(),y=333/1067*root1.winfo_screenheight(),anchor="nw")

start_date=customtkinter.CTkLabel(root1,width=242/1707*root1.winfo_screenwidth(),height=35/1067*root1.winfo_screenheight(),fg_color="#FFFFFF",bg_color="#FFFFFF",text=booking_page[5],anchor="w",text_color="#747474",font=("Poppins Light",22))
start_date.place(x=1171/1707*root1.winfo_screenwidth(),y=395/1067*root1.winfo_screenheight(),anchor="nw")

end_date=customtkinter.CTkLabel(root1,width=251/1707*root1.winfo_screenwidth(),height=35/1067*root1.winfo_screenheight(),fg_color="#FFFFFF",bg_color="#FFFFFF",text=booking_page[6],anchor="w",text_color="#747474",font=("Poppins Light",22))
end_date.place(x=1171/1707*root1.winfo_screenwidth(),y=431/1067*root1.winfo_screenheight(),anchor="nw")

location=customtkinter.CTkLabel(root1,width=305/1707*root1.winfo_screenwidth(),height=39/1067*root1.winfo_screenheight(),fg_color="#FFFFFF",bg_color="#FFFFFF",text=booking_page[7],anchor="w",text_color="#747474",font=("Poppins Light",24))
location.place(x=1098/1707*root1.winfo_screenwidth(),y=484/1067*root1.winfo_screenheight(),anchor="nw")

price=customtkinter.CTkLabel(root1,width=264/1707*root1.winfo_screenwidth(),height=39/1067*root1.winfo_screenheight(),fg_color="#FFFFFF",bg_color="#FFFFFF",text=booking_page[8],anchor="w",text_color="#9C9C9C",font=("Poppins",24))
price.place(x=1157/1707*root1.winfo_screenwidth(),y=552/1067*root1.winfo_screenheight(),anchor="nw")

status_label=customtkinter.CTkLabel(root1,width=150/1707*root1.winfo_screenwidth(),height=54.4/1067*root1.winfo_screenheight(),fg_color="#FFFFFF",bg_color="#FFFFFF",text="Status:",text_color="#000000",font=("Poppins",36))
status_label.place(x=400/1707*root1.winfo_screenwidth(),y=809/1067*root1.winfo_screenheight(),anchor="nw")

status=customtkinter.CTkLabel(root1,width=307.46/1707*root1.winfo_screenwidth(),height=54/1067*root1.winfo_screenheight(),fg_color="#FFFFFF",bg_color="#FFFFFF",text=booking_page[9],text_color="#000000",font=("Poppins",30))
status.place(x=566/1707*root1.winfo_screenwidth(),y=809/1067*root1.winfo_screenheight(),anchor="nw")

bck_btn=customtkinter.CTkButton(root1,width=171/1707*root1.winfo_screenwidth(),height=69/1067*root1.winfo_screenheight(),bg_color="white",fg_color="#1572D3",text="Back",text_color="#FFFFFF",font=("Poppins",24))
bck_btn.place(x=61/1707*root1.winfo_screenwidth(),y=879/1067*root1.winfo_screenheight(),anchor="nw")

update_btn=customtkinter.CTkButton(root1,width=171/1707*root1.winfo_screenwidth(),height=60.4/1067*root1.winfo_screenheight(),bg_color="white",fg_color="#1572D3",text="Update",text_color="#FFFFFF",font=("Poppins",24))
update_btn.place(x=1071/1707*root1.winfo_screenwidth(),y=621.08/1067*root1.winfo_screenheight(),anchor="nw")

cancel_btn=customtkinter.CTkButton(root1,width=171/1707*root1.winfo_screenwidth(),height=60.4/1067*root1.winfo_screenheight(),bg_color="white",fg_color="#1572D3",text="Cancel",text_color="#FFFFFF",font=("Poppins",24))
cancel_btn.place(x=1273/1707*root1.winfo_screenwidth(),y=621.08/1067*root1.winfo_screenheight(),anchor="nw")

pay_btn=customtkinter.CTkButton(root1,width=153/1707*root1.winfo_screenwidth(),height=54.4/1067*root1.winfo_screenheight(),bg_color="white",fg_color="#1572D3",text="Pay",text_color="#FFFFFF",font=("Poppins",24))
pay_btn.place(x=1098/1707*root1.winfo_screenwidth(),y=809/1067*root1.winfo_screenheight(),anchor="nw")

root1.mainloop()