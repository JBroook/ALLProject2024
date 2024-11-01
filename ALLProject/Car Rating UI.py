import ctk
from PIL import Image

self.master=ctk.CTk()
self.master.geometry("1200x800")

rate_booking_ui=ctk.CTkImage(light_image=img.open("Project Images/Rate Car Booking.png"),size=(self.width,self.height-68))
rate_booking_ui_label=ctk.CTkLabel(self.master,image=rate_booking_ui,text="")
rate_booking_ui_label.place(x=0,y=0,anchor="nw")

booking=[0,"20-10-2024","25-10-2024","George Town","Perodua Axia","Project Images/PeroduaAxia.jpg"]

car_name=ctk.CTkLabel(self.master,fg_color="#FFFFFF",bg_color="#FFFFFF",text=booking[4],text_color="#000000",font=("Poppins",56))
car_name.place(x=317/1707*self.width,y=203/1067*self.height,anchor="nw")

car_picture=ctk.CTkImage(light_image=img.open(booking[5]),size=(580.22/1707*self.width,307.49/1067*self.height))
car_picture_label=ctk.CTkLabel(self.master,image=car_picture,text="")
car_picture_label.place(x=261/1707*self.width,y=331.09/1067*self.height,anchor="nw")

start_date=ctk.CTkLabel(self.master,fg_color="#FFFFFF",bg_color="#FFFFFF",anchor="w",text=booking[1],text_color="#747474",font=("Poppins",26/1067*self.height))
start_date.place(x=352/1707*self.width,y=692/1067*self.height,anchor="nw")

end_date=ctk.CTkLabel(self.master,fg_color="#FFFFFF",bg_color="#FFFFFF",anchor="w",text=booking[2],text_color="#747474",font=("Poppins",26/1067*self.height))
end_date.place(x=352/1707*self.width,y=738/1067*self.height,anchor="nw")

location=ctk.CTkLabel(self.master,fg_color="#FFFFFF",bg_color="#FFFFFF",anchor="w",text=booking[3],text_color="#747474",font=("Poppins",26/1067*self.height))
location.place(x=668/1707*self.width,y=693/1067*self.height,anchor="nw")

comment_entry=ctk.CTkTextbox(self.master,width=492/1707*self.width,
                                        height=449/1067*self.height,
                                        bg_color="white",
                                        fg_color="#D9D9D9",
                                        border_color="#D9D9D9",
                                        corner_radius=8,
                                        wrap="word",
                                        scrollbar_button_color="#000000",
                                        text_color="black",
                                        font=("Poppins Light",32))
comment_entry.place(x=1068/1707*self.width,y=306/1067*self.height,anchor="nw")

btn1=ctk.CTkButton(self.master,width=79/1707*self.width,height=75/1067*self.height,bg_color="white",fg_color="#EFBF14",text="☆",text_color="#000000",font=("Poppins",32))
btn1.place(x=1084/1707*self.width,y=182/1067*self.height,anchor="nw")

btn2=ctk.CTkButton(self.master,width=79/1707*self.width,height=75/1067*self.height,bg_color="white",fg_color="#EFBF14",text="☆",text_color="#000000",font=("Poppins",32))
btn2.place(x=1179/1707*self.width,y=182/1067*self.height,anchor="nw")

btn3=ctk.CTkButton(self.master,width=79/1707*self.width,height=75/1067*self.height,bg_color="white",fg_color="#EFBF14",text="☆",text_color="#000000",font=("Poppins",32))
btn3.place(x=1274/1707*self.width,y=182/1067*self.height,anchor="nw")

btn4=ctk.CTkButton(self.master,width=79/1707*self.width,height=75/1067*self.height,bg_color="white",fg_color="#EFBF14",text="☆",text_color="#000000",font=("Poppins",32))
btn4.place(x=1369/1707*self.width,y=182/1067*self.height,anchor="nw")

btn5=ctk.CTkButton(self.master,width=79/1707*self.width,height=75/1067*self.height,bg_color="white",fg_color="#EFBF14",text="☆",text_color="#000000",font=("Poppins",32))
btn5.place(x=1464/1707*self.width,y=182/1067*self.height,anchor="nw")

bck_btn=ctk.CTkButton(self.master,width=171/1707*self.width,height=69/1067*self.height,bg_color="white",fg_color="#1572D3",text="Back",text_color="white",font=("Poppins",24))
bck_btn.place(x=72/1707*self.width,y=878/1067*self.height,anchor="nw")

confirm_btn=ctk.CTkButton(self.master,width=171/1707*self.width,height=69/1067*self.height,bg_color="white",fg_color="#1572D3",text="Confirm",text_color="white",font=("Poppins",24))
confirm_btn.place(x=1389/1707*self.width,y=786/1067*self.height,anchor="nw")

self.master.mainloop()