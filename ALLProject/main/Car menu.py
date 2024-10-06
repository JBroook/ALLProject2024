import tkinter as tk
from doctest import master
from tkinter import ttk, PhotoImage, Toplevel
import customtkinter as ctk, customtkinter
from PIL import Image,ImageTk
from customtkinter import CTkLabel

page=customtkinter.CTk()
page.geometry("1200x1000")
page.title("Car Menu")

options_frame=customtkinter.CTkFrame(page,fg_color="#393E46",corner_radius=0)
options_frame.pack(side="left",fill="both")
options_frame.configure(width=150,height=500)

def indicate(page):
    delete_pages()
    page()

def delete_pages():
    for frame in main_frame.winfo_children():
        frame.destroy()

car_type_one_button=tk.Button(options_frame,text="Small",bg="#222831",fg="white",font=("Times new roman",20,"bold"),bd=0,command=lambda:indicate(car_type_one))
car_type_one_button.place(x=15,y=10)

def car_type_one():
    photo_myvi=ctk.CTkImage(light_image=Image.open('../../../PycharmProjects/GroupProject/Project Images/Project Images/perodua myvi.png'), dark_image=Image.open(
        '../../../PycharmProjects/GroupProject/Project Images/Project Images/perodua myvi.png'), size=(250, 200))
    Button_myvi=customtkinter.CTkButton(main_frame,image=photo_myvi,fg_color="#EEEEEE",text_color="black",text="Perodua Myvi",compound="top",font=("Arial",20,"bold"),command=lambda:indicate(myvi_window))
    Button_myvi.configure(width=300,height=150)
    Button_myvi.place(x=10,y=20)

    def myvi_window():
        mv_window=Toplevel(master)
        mv_window.title("Perodua Myvi")
        mv_window.geometry("1000x800")
        mv_window.configure(bg="#00ADB5")
        photo_mv=ctk.CTkImage(light_image=Image.open('../../../PycharmProjects/GroupProject/Project Images/Project Images/perodua myvi.png'), dark_image=Image.open(
            '../../../PycharmProjects/GroupProject/Project Images/Project Images/perodua myvi.png'), size=(350, 300))
        label_mv=ctk.CTkLabel(mv_window,image=photo_mv,text="Perodua Myvi",compound="top",font=("Arial",25,"bold"))
        label_mv.place(x=10,y=10)
        label_mv_capacity=ctk.CTkLabel(mv_window,text="Capacity: 5 people",font=("Arial",25,"normal"))
        label_mv_capacity.place(x=350,y=60)
        label_mv_luggage=ctk.CTkLabel(mv_window, text="Luggage: 2 luggages", font=("Arial", 25, "normal"))
        label_mv_luggage.place(x=350, y=90)
        label_mv_type=ctk.CTkLabel(mv_window, text="Type: Auto", font=("Arial", 25, "normal"))
        label_mv_type.place(x=350, y=120)
        label_mv_price=ctk.CTkLabel(mv_window, text="Price: RM76/day", font=("Arial", 25, "normal"))
        label_mv_price.place(x=350, y=150)
        choose_mv=customtkinter.CTkButton(mv_window,text="Choose this car",fg_color="#393E46",font=("Helvetica",30,"bold"))
        choose_mv.place(x=200,y=370)
        back_mv=customtkinter.CTkButton(mv_window,text="Back",font=("Helvetica",25,"bold"),fg_color="#393E46",command=mv_window.destroy)
        back_mv.place(x=10,y=470)

    photo_axia = ctk.CTkImage(light_image=Image.open('../../../PycharmProjects/GroupProject/Project Images/Project Images/PeroduaAxia.jpg'), dark_image=Image.open('../../../PycharmProjects/GroupProject/Project Images/Project Images/PeroduaAxia.jpg'),
                              size=(250, 200))
    Button_axia = customtkinter.CTkButton(main_frame, image=photo_axia, fg_color="#EEEEEE", text_color="black",
                                          text="Perodua Axia", compound="top", font=("Arial", 20, "bold"),
                                          command=lambda: indicate(axia_window))
    Button_axia.configure(width=300, height=150)
    Button_axia.place(x=350, y=20)

    def axia_window():
        ax_window = Toplevel(master)
        ax_window.title("Perodua Axia")
        ax_window.geometry("1000x1000")
        ax_window.configure(bg="#00ADB5")
        photo_ax = ctk.CTkImage(light_image=Image.open('../../../PycharmProjects/GroupProject/Project Images/Project Images/PeroduaAxia.jpg'), dark_image=Image.open('../../../PycharmProjects/GroupProject/Project Images/Project Images/PeroduaAxia.jpg'),
                                size=(320, 250))
        label_ax = ctk.CTkLabel(ax_window, image=photo_ax, text="Perodua Axia", compound="top",
                                font=("Arial", 20, "bold"))
        label_ax.place(x=10, y=10)
        label_ax_capacity = ctk.CTkLabel(ax_window, text="Capacity: 5 people", font=("Arial", 25, "normal"))
        label_ax_capacity.place(x=350, y=60)
        label_ax_luggage = ctk.CTkLabel(ax_window, text="Luggage: 2 luggages", font=("Arial", 25, "normal"))
        label_ax_luggage.place(x=350, y=90)
        label_ax_type = ctk.CTkLabel(ax_window, text="Type: Auto", font=("Arial", 25, "normal"))
        label_ax_type.place(x=350, y=120)
        label_ax_price = ctk.CTkLabel(ax_window, text="Price: RM94/day", font=("Arial", 25, "normal"))
        label_ax_price.place(x=350, y=150)
        choose_ax = customtkinter.CTkButton(ax_window, text="Choose this car",fg_color= "#393E46",font=("Helvetica", 30, "bold"))
        choose_ax.place(x=200, y=370)
        back_ax = customtkinter.CTkButton(ax_window, text="Back", font=("Helvetica", 25, "bold"), fg_color="#393E46",command=ax_window.destroy)
        back_ax.place(x=10, y=470)

car_type_two_button=tk.Button(options_frame,text="Medium",bg="#222831",fg="white",font=("Times new roman",20,"bold"),bd=0,command=lambda:indicate(car_type_two))
car_type_two_button.place(x=15,y=80)

def car_type_two():
    photo_civic = ctk.CTkImage(light_image=Image.open('../../../PycharmProjects/GroupProject/Project Images/Project Images/hondacivic.jpeg'), dark_image=Image.open(
        '../../../PycharmProjects/GroupProject/Project Images/Project Images/hondacivic.jpeg'),
                              size=(250, 200))
    Button_civic = customtkinter.CTkButton(main_frame, image=photo_civic, fg_color="#EEEEEE", text_color="black",
                                          text="Honda Civic", compound="top", font=("Arial", 20, "bold"),
                                          command=lambda: indicate(civic_window))
    Button_civic.configure(width=300, height=150)
    Button_civic.place(x=10, y=20)

    def civic_window():
        cv_window = Toplevel(master)
        cv_window.title("Honda Civic")
        cv_window.geometry("1000x800")
        cv_window.configure(bg="#00ADB5")
        photo_cv = ctk.CTkImage(light_image=Image.open('../../../PycharmProjects/GroupProject/Project Images/Project Images/hondacivic.jpeg'), dark_image=Image.open('../../../PycharmProjects/GroupProject/Project Images/Project Images/hondacivic.jpeg'), size=(320, 250))
        label_cv = ctk.CTkLabel(cv_window, image=photo_cv, text="Honda Civic", compound="top",font=("Arial", 25, "bold"))
        label_cv.place(x=10, y=10)
        label_cv_capacity = ctk.CTkLabel(cv_window, text="Capacity: 5 people", font=("Arial", 25, "normal"))
        label_cv_capacity.place(x=350, y=60)
        label_cv_luggage = ctk.CTkLabel(cv_window, text="Luggage: 2 luggages", font=("Arial", 25, "normal"))
        label_cv_luggage.place(x=350, y=90)
        label_cv_type = ctk.CTkLabel(cv_window, text="Type: Auto", font=("Arial", 25, "normal"))
        label_cv_type.place(x=350, y=120)
        label_cv_price = ctk.CTkLabel(cv_window, text="Price: RM103/day", font=("Arial", 25, "normal"))
        label_cv_price.place(x=350, y=150)
        choose_cv = customtkinter.CTkButton(cv_window, text="Choose this car", fg_color="#393E46",font=("Helvetica", 30, "bold"))
        choose_cv.place(x=200, y=370)
        back_cv = customtkinter.CTkButton(cv_window, text="Back", font=("Helvetica", 25, "bold"), fg_color="#393E46",command=cv_window.destroy)
        back_cv.place(x=10, y=470)

car_type_three_button=tk.Button(options_frame,text="Large",bg="#222831",fg="white",font=("Times new roman",20,"bold"),bd=0,command=lambda:indicate(car_type_three))
car_type_three_button.place(x=15,y=150)

def car_type_three():
    photo_bezza=ctk.CTkImage(light_image=Image.open('../../../PycharmProjects/GroupProject/Project Images/Project Images/PeroduaBezza.jpg'),dark_image=Image.open(
        '../../../PycharmProjects/GroupProject/Project Images/Project Images/PeroduaBezza.jpg'),size=(250, 200))
    Button_bezza = customtkinter.CTkButton(main_frame,image=photo_bezza,fg_color="#EEEEEE",text_color="black",
                                          text="Perodua Bezza",compound="top",font=("Arial",20,"bold"),
                                          command=lambda:indicate(bezza_window))
    Button_bezza.configure(width=300,height=150)
    Button_bezza.place(x=10,y=20)

    def bezza_window():
        bz_window=Toplevel(master)
        bz_window.title("Perodua Bezza")
        bz_window.geometry("1000x800")
        bz_window.configure(bg="#00ADB5")
        photo_bz=ctk.CTkImage(light_image=Image.open('../../../PycharmProjects/GroupProject/Project Images/Project Images/PeroduaBezza.jpg'),dark_image=Image.open(
            '../../../PycharmProjects/GroupProject/Project Images/Project Images/PeroduaBezza.jpg'),size=(320,280))
        label_bz=ctk.CTkLabel(bz_window,image=photo_bz,text="Perodua Bezza",compound="top",font=("Arial",25,"bold"))
        label_bz.place(x=10,y=10)
        label_bz_capacity=ctk.CTkLabel(bz_window,text="Capacity: 5 people",font=("Arial",25,"normal"))
        label_bz_capacity.place(x=350,y=60)
        label_bz_luggage=ctk.CTkLabel(bz_window,text="Luggage: 2 luggages",font=("Arial",25,"normal"))
        label_bz_luggage.place(x=350,y=90)
        label_bz_type=ctk.CTkLabel(bz_window,text="Type: Auto",font=("Arial",25,"normal"))
        label_bz_type.place(x=350,y=120)
        label_bz_price=ctk.CTkLabel(bz_window,text="Price: RM82/day",font=("Arial",25,"normal"))
        label_bz_price.place(x=350,y=150)
        choose_bz=customtkinter.CTkButton(bz_window,text="Choose this car",fg_color="#393E46",font=("Helvetica",30,"bold"))
        choose_bz.place(x=200,y=370)
        back_bz=customtkinter.CTkButton(bz_window,text="Back",font=("Helvetica", 25, "bold"),fg_color="#393E46",command=bz_window.destroy)
        back_bz.place(x=10,y=470)

car_type_four_button=tk.Button(options_frame,text="Van",bg="#222831",fg="white",font=("Times new roman",20,"bold"),bd=0,command=lambda:indicate(car_type_four))
car_type_four_button.place(x=15,y=220)

def car_type_four():
    photo_urvan = ctk.CTkImage(light_image=Image.open('../../../PycharmProjects/GroupProject/Project Images/Project Images/nissanurvan.jpg'), dark_image=Image.open(
        '../../../PycharmProjects/GroupProject/Project Images/Project Images/nissanurvan.jpg'),size=(320, 200))
    Button_urvan = customtkinter.CTkButton(main_frame, image=photo_urvan, fg_color="#EEEEEE", text_color="black",
                                          text="Nissan Urvan", compound="top", font=("Arial", 20, "bold"),
                                          command=lambda: indicate(urvan_window))
    Button_urvan.configure(width=350, height=250)
    Button_urvan.place(x=10, y=20)

    def urvan_window():
        ur_window = Toplevel(master)
        ur_window.title("Nissan Urvan")
        ur_window.geometry("1000x800")
        ur_window.configure(bg="#00ADB5")
        photo_ur = ctk.CTkImage(light_image=Image.open('../../../PycharmProjects/GroupProject/Project Images/Project Images/nissanurvan.jpg'), dark_image=Image.open(
            '../../../PycharmProjects/GroupProject/Project Images/Project Images/nissanurvan.jpg'), size=(350, 250))
        label_ur = ctk.CTkLabel(ur_window, image=photo_ur, text="Nissan Urvan", compound="top",
                                font=("Arial", 25, "bold"))
        label_ur.place(x=10, y=10)
        label_ur_capacity = ctk.CTkLabel(ur_window, text="Capacity: 5 people", font=("Arial", 25, "normal"))
        label_ur_capacity.place(x=380, y=60)
        label_ur_luggage = ctk.CTkLabel(ur_window, text="Luggage: 2 luggages", font=("Arial", 25, "normal"))
        label_ur_luggage.place(x=380, y=90)
        label_ur_type = ctk.CTkLabel(ur_window, text="Type: Auto", font=("Arial", 25, "normal"))
        label_ur_type.place(x=380, y=120)
        label_ur_price = ctk.CTkLabel(ur_window, text="Price: RM76/day", font=("Arial", 25, "normal"))
        label_ur_price.place(x=380, y=150)
        choose_ur = customtkinter.CTkButton(ur_window, text="Choose this car", fg_color="#393E46",
                                            font=("Helvetica", 30, "bold"),command=ur_window.destroy)
        choose_ur.place(x=200, y=370)
        back_ur = customtkinter.CTkButton(ur_window, text="Back", font=("Helvetica", 25, "bold"), fg_color="#393E46")
        back_ur.place(x=10, y=470)

car_type_five_button=tk.Button(options_frame,text="SUV",bg="#222831",fg="white",font=("Times new roman",20,"bold"),bd=0,command=lambda:indicate(car_type_five))
car_type_five_button.place(x=15,y=290)

def car_type_five():
    photo_nissan_x = ctk.CTkImage(light_image=Image.open('../../../PycharmProjects/GroupProject/Project Images/Project Images/nissanxtrail.png'), dark_image=Image.open('../../../PycharmProjects/GroupProject/Project Images/Project Images/nissanxtrail.png'),
                              size=(350, 200))
    Button_nissan_x = customtkinter.CTkButton(main_frame, image=photo_nissan_x, fg_color="#EEEEEE", text_color="black",
                                          text="Nissan X-Trail", compound="top", font=("Arial", 20, "bold"),
                                          command=lambda: indicate(nissan_x_window))
    Button_nissan_x.configure(width=300, height=150)
    Button_nissan_x.place(x=10, y=20)

    def nissan_x_window():
        nx_window = Toplevel(master)
        nx_window.title("Nissan X-Trail")
        nx_window.geometry("1000x1000")
        nx_window.configure(bg="#00ADB5")
        photo_nx = ctk.CTkImage(light_image=Image.open('../../../PycharmProjects/GroupProject/Project Images/Project Images/nissanxtrail.png'), dark_image=Image.open('../../../PycharmProjects/GroupProject/Project Images/Project Images/nissanxtrail.png'),
                                size=(350, 200))
        label_nx = ctk.CTkLabel(nx_window, image=photo_nx, text="Nissan X-Trail", compound="top",
                                font=("Arial", 20, "bold"))
        label_nx.place(x=10, y=10)
        label_nx_capacity = ctk.CTkLabel(nx_window, text="Capacity: 7 people", font=("Arial", 25, "normal"))
        label_nx_capacity.place(x=350, y=60)
        label_nx_luggage = ctk.CTkLabel(nx_window, text="Luggage: 2 luggages", font=("Arial", 25, "normal"))
        label_nx_luggage.place(x=350, y=90)
        label_nx_type = ctk.CTkLabel(nx_window, text="Type: Auto", font=("Arial", 25, "normal"))
        label_nx_type.place(x=350, y=120)
        label_nx_price = ctk.CTkLabel(nx_window, text="Price: RM254/day", font=("Arial", 25, "normal"))
        label_nx_price.place(x=350, y=150)
        choose_nx = customtkinter.CTkButton(nx_window, text="Choose this car", fg_color="#393E46",
                                            font=("Helvetica", 30, "bold"),command=nx_window.destroy)
        choose_nx.place(x=200, y=270)
        back_nx = customtkinter.CTkButton(nx_window, text="Back", font=("Helvetica", 25, "bold"), fg_color="#393E46")
        back_nx.place(x=10, y=370)

main_frame=customtkinter.CTkFrame(page,fg_color="#00ADB5",corner_radius=0)
main_frame.pack(expand="true",fill="both")



page.mainloop()
