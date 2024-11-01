import ctk
from PIL import Image

self.master=ctk.CTk()
self.master.geometry("1200x800")

current_booking_ui=ctk.CTkImage(light_image=img.open("Project Images/Current Booking.png"),size=(self.width,self.height-68))
current_booking_ui_label=ctk.CTkLabel(self.master,image=current_booking_ui,text="")
current_booking_ui_label.place(x=0,y=0,anchor="nw")

booking_page=[0,"Perodua Axia","Project Images/PeroduaAxia.jpg","5 people","Auto","20-10-2024","25-10-2024","George Town","RM98/day","Pending"]

car_image_ph=ctk.CTkImage(light_image=img.open(booking_page[2]),size=(563/1707*self.width,327/1069*self.height))
car_image_ph_label=ctk.CTkLabel(self.master,image=car_image_ph,text="")
car_image_ph_label.place(x=333/1707*self.width,y=310/1067*self.height,anchor="nw")

car_name=ctk.CTkLabel(self.master,width=442/1707*self.width,height=61/1067*self.height,fg_color="#FFFFFF",bg_color="#FFFFFF",text=booking_page[1],text_color="#000000",font=("Poppins",32))
car_name.place(x=1030/1707*self.width,y=240/1067*self.height,anchor="nw")

capacity=ctk.CTkLabel(self.master,width=125/1707*self.width,height=39/1067*self.height,fg_color="#FFFFFF",bg_color="#FFFFFF",text=booking_page[3],anchor="w",text_color="#747474",font=("Poppins Light",24))
capacity.place(x=1100/1707*self.width,y=333/1067*self.height,anchor="nw")

type=ctk.CTkLabel(self.master,width=115/1707*self.width,height=39/1067*self.height,fg_color="#FFFFFF",bg_color="#FFFFFF",text=booking_page[4],anchor="w",text_color="#747474",font=("Poppins Light",24))
type.place(x=1350/1707*self.width,y=333/1067*self.height,anchor="nw")

start_date=ctk.CTkLabel(self.master,width=242/1707*self.width,height=35/1067*self.height,fg_color="#FFFFFF",bg_color="#FFFFFF",text=booking_page[5],anchor="w",text_color="#747474",font=("Poppins Light",22))
start_date.place(x=1171/1707*self.width,y=395/1067*self.height,anchor="nw")

end_date=ctk.CTkLabel(self.master,width=251/1707*self.width,height=35/1067*self.height,fg_color="#FFFFFF",bg_color="#FFFFFF",text=booking_page[6],anchor="w",text_color="#747474",font=("Poppins Light",22))
end_date.place(x=1171/1707*self.width,y=431/1067*self.height,anchor="nw")

location=ctk.CTkLabel(self.master,width=305/1707*self.width,height=39/1067*self.height,fg_color="#FFFFFF",bg_color="#FFFFFF",text=booking_page[7],anchor="w",text_color="#747474",font=("Poppins Light",24))
location.place(x=1098/1707*self.width,y=484/1067*self.height,anchor="nw")

price=ctk.CTkLabel(self.master,width=264/1707*self.width,height=39/1067*self.height,fg_color="#FFFFFF",bg_color="#FFFFFF",text=booking_page[8],anchor="w",text_color="#9C9C9C",font=("Poppins",24))
price.place(x=1157/1707*self.width,y=552/1067*self.height,anchor="nw")

status_label=ctk.CTkLabel(self.master,width=150/1707*self.width,height=54.4/1067*self.height,fg_color="#FFFFFF",bg_color="#FFFFFF",text="Status:",text_color="#000000",font=("Poppins",36))
status_label.place(x=400/1707*self.width,y=809/1067*self.height,anchor="nw")

status=ctk.CTkLabel(self.master,width=307.46/1707*self.width,height=54/1067*self.height,fg_color="#FFFFFF",bg_color="#FFFFFF",text=booking_page[9],text_color="#000000",font=("Poppins",30))
status.place(x=566/1707*self.width,y=809/1067*self.height,anchor="nw")

bck_btn=ctk.CTkButton(self.master,width=171/1707*self.width,height=69/1067*self.height,bg_color="white",fg_color="#1572D3",text="Back",text_color="#FFFFFF",font=("Poppins",24))
bck_btn.place(x=61/1707*self.width,y=879/1067*self.height,anchor="nw")

update_btn=ctk.CTkButton(self.master,width=171/1707*self.width,height=60.4/1067*self.height,bg_color="white",fg_color="#1572D3",text="Update",text_color="#FFFFFF",font=("Poppins",24))
update_btn.place(x=1071/1707*self.width,y=621.08/1067*self.height,anchor="nw")

cancel_btn=ctk.CTkButton(self.master,width=171/1707*self.width,height=60.4/1067*self.height,bg_color="white",fg_color="#1572D3",text="Cancel",text_color="#FFFFFF",font=("Poppins",24))
cancel_btn.place(x=1273/1707*self.width,y=621.08/1067*self.height,anchor="nw")

pay_btn=ctk.CTkButton(self.master,width=153/1707*self.width,height=54.4/1067*self.height,bg_color="white",fg_color="#1572D3",text="Pay",text_color="#FFFFFF",font=("Poppins",24))
pay_btn.place(x=1098/1707*self.width,y=809/1067*self.height,anchor="nw")

self.master.mainloop()