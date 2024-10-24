from ftplib import all_errors
from tkinter import messagebox
import sqlite3 as sql

import customtkinter as ctk
from PIL import Image as img
import re
import smtplib,ssl
from email.message import EmailMessage
import string, random
import pyglet
from tkcalendar import Calendar

pyglet.font.add_file("assets/fonts/Poppins-SemiBold.ttf")
pyglet.font.add_file("assets/fonts/Poppins-Light.ttf")
pyglet.font.add_file("assets/fonts/Poppins-Medium.ttf")

def check_filter_options(dictionary, array):
    i = 0
    for option in dictionary:
        if dictionary[option]=="any":
            continue
        match option:
            case "capacity":
                if dictionary[option]!=array[5]:
                    return False
            case "manufacturer year":
                if dictionary[option] != str(array[1]):
                    return False
            case "transmission":
                if dictionary[option] != array[7]:
                    return False
            case "price":
                if dictionary[option]==1:
                    if array[3] >=100: return False
                elif dictionary[option] == 2:
                    if array[3] >= 200 or array[3]<100: return False
                else:
                    if array[3] < 200: return False

        i += 1
    return True

class App:
    def __init__(self, master):
        #app settings
        self.master = master
        self.master.title("Car Rental App")
        self.master.geometry("800x500")
        self.master._state_before_windows_set_titlebar_color = 'zoomed'
        self.width = self.master.winfo_screenwidth()
        self.height = self.master.winfo_screenheight()

        # ui definitions
        self.pickup_location_list = ["Pantai Jerejak","Batu Ferringhi","Georgetown","Bayan Lepas","Bayan Baru","Gelugor","Air Itam"]
        self.manu_year = ctk.StringVar()
        self.user_info = {
            "first name" : "Default",
            "last name" : "User",
            "username" : "Unknown",
            "email" : "Unknown",
            "id" : 0
        }
        self.search_options = {
            "capacity": "any",
            "manufacturer year": "any",
            "transmission": "any",
            "price": "any"
        }
        self.current_calendar = "pickup"

        #database stuff
        self.sqliteConnection = sql.connect("DriveEase.db")
        self.cursor = self.sqliteConnection.cursor()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS USERS (
            USER_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            USERNAME VARCHAR(255) NOT NULL,
            EMAIL VARCHAR(255) NOT NULL,
            USER_PASSWORD VARCHAR(255) NOT NULL,
            FIRST_NAME VARCHAR(255) NOT NULL,
            LAST_NAME VARCHAR(255) NOT NULL,
            DATE_OF_BIRTH VARCHAR(100) NOT NULL
        )
        ''')
        #check if admin account exists, if no, create one
        self.cursor.execute("SELECT * FROM USERS WHERE USERNAME = 'Admin';")
        result = self.cursor.fetchall()
        if len(result)==0:
            self.cursor.execute('''
            INSERT INTO USERS (USERNAME, EMAIL, USER_PASSWORD, FIRST_NAME, LAST_NAME, DATE_OF_BIRTH)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', ("Admin","jeremiahboey@gmail.com","Admin@1234","Admin","Account","2000-01-01"))

        self.sqliteConnection.commit()
        self.master.bind("<KeyRelease>", self.login_enter)
        self.master.bind("<<CalendarSelected>>",lambda x : self.set_calendar("change",x))
        # self.cursor.execute("SELECT * FROM CARS WHERE CAR_ID = 1")
        # self.rental_details(self.cursor.fetchall()[0])
        self.login()

    def login(self):
        for i in self.master.winfo_children():
            i.destroy()
        # bg image
        login_ui = ctk.CTkImage(light_image=img.open("assets/login ui.png"), size=(self.width, self.height-64))
        login_ui_label = ctk.CTkLabel(master=self.master, image=login_ui, text="")
        login_ui_label.place(relx=0, rely=0, anchor="nw")

        # # username stuff
        self.username = ctk.StringVar()
        usernameEntry = ctk.CTkEntry(
            self.master,
            textvariable=self.username,
            width=402/1536*self.width,
            height=54/864*self.height,
            bg_color="white",
            fg_color="#D9D9D9",
            border_color="#D9D9D9",
            text_color="black",
            font=("Poppins Light",24)
        )
        usernameEntry.place(x=186/1536*self.width,y=375/864*self.height,anchor="nw")

        # # password stuff
        self.password = ctk.StringVar()
        passwordEntry = ctk.CTkEntry(self.master,
            textvariable=self.password,
            width=402/1536*self.width,
            height=54/864*self.height,
            bg_color="white",
            fg_color="#D9D9D9",
            border_color="#D9D9D9",
            text_color="black",
            font=("Poppins Light",24),
            show="*"
        )
        passwordEntry.place(x=186/1536*self.width,y=484/864*self.height,anchor="nw")

        # login/register frame
        loginButton = ctk.CTkButton(
            self.master,
            text="Login",
            command=self.test_credentials,
                bg_color="white",
            fg_color="#1572D3",
            text_color="white",
            border_color="#1572D3",
            width=187/1536*self.width,
            height=57/864*self.height,
            font=("Poppins Medium",18)
        )
        loginButton.place(x=185/1536*self.width,y=583/864*self.height,anchor="nw")

        registerButton = ctk.CTkButton(
            self.master,
            text="Register",
            command=self.register,
            bg_color="white",
            fg_color="#1572D3",
            text_color="white",
            border_color="#1572D3",
            width=187/1536*self.width,
            height=57/864*self.height,
            font=("Poppins Medium",18)
        )
        registerButton.place(x=401/1536*self.width,y=583/864*self.height,anchor="nw")


    def register(self):
        for i in self.master.winfo_children():
            i.destroy()

        background_image = ctk.CTkImage(img.open("assets/registration page.png"), size=(self.width, self.height - 71))
        background_image_label = ctk.CTkLabel(master=self.master.master, image=background_image, text="")
        background_image_label.place(relx=0, rely=0)

        # First Name
        self.newFirstName = ctk.StringVar()
        first_entry = ctk.CTkEntry(self.master, placeholder_text="Alice", width=215/1536*self.width, height=34/864*self.height, bg_color="white",
                                   fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black", textvariable=self.newFirstName)
        first_entry.place(x=120 / 1280 * self.width, y=194 / 720 * self.height)

        # Last Name
        self.newLastName = ctk.StringVar()
        last_entry = ctk.CTkEntry(self.master, placeholder_text="Tan", width=215/1536*self.width, height=34/864*self.height, bg_color="white",
                                  fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black", textvariable=self.newLastName)
        last_entry.place(x=120 / 1280 * self.width, y=262 / 720 * self.height)

        # Date Of Birth
        self.newDOB = ctk.StringVar()
        date_entry = ctk.CTkEntry(self.master, placeholder_text="YYYY-MM-DD", width=215/1536*self.width, height=34/864*self.height,
                                  bg_color="white", fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black",textvariable=self.newDOB)
        date_entry.place(x=120 / 1280 * self.width, y=342 / 720 * self.height)

        # Email
        self.newEmail = ctk.StringVar()
        email_entry = ctk.CTkEntry(self.master, placeholder_text="alicetan@yahoo.com", width=215/1536*self.width, height=34/864*self.height,
                                   bg_color="white", fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black",textvariable=self.newEmail)
        email_entry.place(x=120 / 1280 * self.width, y=412 / 720 * self.height)

        # Username
        self.newUsername = ctk.StringVar()
        user_entry = ctk.CTkEntry(self.master, placeholder_text="Alicewonderland", width=215/1536*self.width, height=34/864*self.height,
                                  bg_color="white",
                                  fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black",textvariable=self.newUsername)
        user_entry.place(x=390 / 1280 * self.width, y=194 / 720 * self.height)

        # Password
        self.newPassword = ctk.StringVar()
        password_entry = ctk.CTkEntry(self.master, placeholder_text="******", width=215/1536*self.width, height=34/864*self.height, bg_color="white",
                                      fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black",textvariable=self.newPassword)
        password_entry.place(x=390 / 1280 * self.width, y=262 / 720 * self.height)

        # Confirm Password
        self.confirmPassword = ctk.StringVar()
        confirm_entry = ctk.CTkEntry(self.master, placeholder_text="******", width=215/1536*self.width, height=34/864*self.height, bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black",textvariable=self.confirmPassword)
        confirm_entry.place(x=390 / 1280 * self.width, y=343 / 720 * self.height)

        # Login Button
        back_button = ctk.CTkButton(self.master, text="Back to Login", bg_color="white", fg_color="#1572D3",
                                    text_color="white",
                                    border_color="#1572D3", width=135/1536*self.width, height=41/864*self.height, font=("Poppins Medium", 18), command=self.login)
        back_button.place(x=226 / 1280 * self.width, y=500 / 720 * self.height)

        # Confirm Button
        self.confirm_button = ctk.CTkButton(self.master, text="Continue", bg_color="white", fg_color="#1572D3",
                                       text_color="white",
                                       border_color="#1572D3", width=135/1536*self.width, height=41/864*self.height, font=("Poppins Medium", 18),
                                       command=self.confirm_registration)
        self.confirm_button.place(x=382 / 1280 * self.width, y=500 / 720 * self.height)

    def test_credentials(self):
        query = f"SELECT * FROM USERS WHERE USERNAME = \'{self.username.get()}\';"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        if len(result):
            user = result[0]
            if user[3] == self.password.get():
                self.user_info["first name"] = user[4]
                self.user_info["last name"] = user[5]
                self.user_info["username"] = user[1]
                self.user_info["email"] = user[2]
                self.user_info["id"] = user[0]
                self.home_page()
            else:
                messagebox.showerror("Error", "Password is wrong")
        else:
            messagebox.showerror("Error", "Username doesn't exist")

    def db_find_user(self, _username):
        query = f"SELECT * FROM USERS WHERE USERNAME = \'{_username}\';"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    #register button
    def confirm_registration(self):
        #check if all the details entered are valid or not
        error = ""
        result = self.db_find_user(self.newUsername.get())

        valid_email = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.newEmail.get())
        if len(self.newUsername.get())<8:
            error = "Username must be 8 characters minimum"
        elif len(result):
            error = "Username taken"
        elif not valid_email:
            error = "Email is invalid"
        elif len(self.newPassword.get())<8:
            error = "Password must be 8 characters minimum"
        elif not any(i.isdigit() for i in self.newPassword.get()):
            error = "Password must contain at least one digit"
        elif self.newPassword.get()!=self.confirmPassword.get():
            error = "Passwords do not match"

        if error :messagebox.showerror("Error", error)
        else:
            self.confirm_button.configure(state="disabled")
            #send verification code email
            msg = EmailMessage()
            self.random_code = ''.join(random.choices(string.ascii_letters,k=6))
            print(self.random_code)
            msg.set_content("Thank you for registering with DriveEase.\nYour verification code is: "+self.random_code)
            msg['Subject'] = 'DriveEase Verification Code'
            msg['From'] = "skelliesaintscary@gmail.com"
            msg['To'] = self.newEmail.get()

            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("jeremiahboey@gmail.com","kqlv jfry sdet zszi")
            s.send_message(msg)
            s.quit()

            self.newWindow = ctk.CTkToplevel(self.master)

            # sets the title of the
            # Toplevel widget
            self.newWindow.title("Verify your email")

            # sets the geometry of toplevel
            self.newWindow.geometry("400x200")

            # A Label widget to show in toplevel
            ctk.CTkLabel(self.newWindow,text="Enter your verification code").pack()
            self.verification_code = ctk.StringVar()
            ctk.CTkEntry(self.newWindow,textvariable=self.verification_code).pack()
            ctk.CTkButton(self.newWindow,text="Submit",command=self.check_verification).pack()

    def login_enter(self, event):
        if event.keysym == "Return":
            self.test_credentials()

    def home_page(self):
        for i in self.master.winfo_children():
            i.destroy()

        homepage_ui = ctk.CTkImage(light_image=img.open("assets/home page ui.png"), size=(self.width, self.height-64))
        homepage_ui_label = ctk.CTkLabel(self.master,image=homepage_ui,text="")
        homepage_ui_label.place(relx=0,rely=0,anchor="nw")

        rent_button = ctk.CTkButton(
            master=self.master,
            text="Go",
            width=158/1536*self.width,
            height=40/864*self.height,
            font=("Poppins Medium",14),
            bg_color="#FFFFFF",
            fg_color="#1572D3",
            text_color="white",
            command=self.rental_page
        )
        rent_button.place(x=1210/1536*self.width  ,y=204/864*self.height,anchor="nw")

        account_button = ctk.CTkButton(
            master=self.master,
            text="Go",
            width=158/1536*self.width,
            height=42/864*self.height,
            font=("Poppins Medium", 14),
            bg_color="#FFFFFF",
            fg_color="#1572D3",
            text_color="white",
            command=self.user_account
        )
        account_button.place(x=1210/1536*self.width, y=441/864*self.height, anchor="nw")

        book_button = ctk.CTkButton(
            master=self.master,
            text="Go",
            width=158/1536*self.width,
            height=42/864*self.height,
            font=("Poppins Medium", 14),
            bg_color="#FFFFFF",
            fg_color="#1572D3",
            text_color="white"
        )
        book_button.place(x=1210/1536*self.width, y=673/864*self.height, anchor="nw")

    def check_verification(self):
        if self.verification_code.get()==self.random_code:
            self.cursor.execute('''
                INSERT INTO USERS (USERNAME, EMAIL, USER_PASSWORD, FIRST_NAME, LAST_NAME, DATE_OF_BIRTH)
                VALUES(?, ?, ?, ?, ?, ?)''',
                (self.newUsername.get(), self.newEmail.get(), self.newPassword.get(),
                 self.newFirstName.get(), self.newLastName.get(), self.newDOB.get())
            )
            self.sqliteConnection.commit()
            self.newWindow.destroy()
            self.login()
        else:
            messagebox.showerror("Wrong code","Wrong code: Try again")

    def rental_page(self, option_filter={"capacity": "any", "manufacturer year": "any", "transmission": "any", "price": "any"}):
        for i in self.master.winfo_children():
            i.destroy()

        rental_ui = ctk.CTkImage(light_image=img.open("assets/car rental ui.png"), size=(self.width, self.height-64))
        rental_ui_label = ctk.CTkLabel(master=self.master, image=rental_ui, text="")
        rental_ui_label.place(x=0,y=0,anchor="nw")

        #search option buttons
        five_passenger = ctk.CTkButton(
            self.master,
            text="5 Passengers",
            bg_color="white",
            fg_color="#f0f4fc",
            text_color="#1572D3",
            border_color="#f0f4fc",
            width=159/1536*self.width,
            height=42/864*self.height,
            font=("Poppins Medium", 18),
            command=lambda : self.set_search_option("5 Passengers")
        )
        five_passenger.place(x=53/1536*self.width, y=170/864*self.height, anchor="nw")

        seven_passenger = ctk.CTkButton(
            self.master,
            text="7 Passengers",
            bg_color="white",
            fg_color="#f0f4fc",
            text_color="#1572D3",
            border_color="#f0f4fc",
            width=159/1536*self.width,
            height=42/864*self.height,
            font=("Poppins Medium", 18),
            command=lambda : self.set_search_option("7 Passengers")
        )
        seven_passenger.place(x=263/1536*self.width, y=170/864*self.height, anchor="nw")

        self.manu_year.trace("w", lambda name, index, mode, sv=self.manu_year: self.set_search_option("Manufacturer Year"))
        manufacturer_year_entry = ctk.CTkEntry(
            self.master,
            bg_color="white",
            fg_color="#f0f4fc",
            text_color="#1572D3",
            border_color="#f0f4fc",
            width=167/1536*self.width,
            height=38/864*self.height,
            font=("Poppins Medium", 20),
            textvariable=self.manu_year
        )
        manufacturer_year_entry.place(x=53/1536*self.width,y=287/864*self.height)

        auto_button = ctk.CTkButton(
            self.master,
            text="Auto",
            bg_color="white",
            fg_color="#f0f4fc",
            text_color="#1572D3",
            border_color="#f0f4fc",
            width=97/1536*self.width,
            height=42/864*self.height,
            font=("Poppins Medium", 18),
            command=lambda : self.set_search_option("Auto")
        )
        auto_button.place(x=53/1536*self.width, y=403/864*self.height, anchor="nw")

        manual_button = ctk.CTkButton(
            self.master,
            text="Manual",
            bg_color="white",
            fg_color="#f0f4fc",
            text_color="#1572D3",
            border_color="#f0f4fc",
            width=118/1536*self.width,
            height=42/864*self.height,
            font=("Poppins Medium", 18),
            command=lambda : self.set_search_option("Manual")
        )
        manual_button.place(x=187/1536*self.width, y=403/864*self.height, anchor="nw")

        price_1 = ctk.CTkButton(
            self.master,
            text="$",
            bg_color="white",
            fg_color="#f0f4fc",
            text_color="#1572D3",
            border_color="#f0f4fc",
            width=74/1536*self.width,
            height=42/864*self.height,
            font=("Poppins Medium", 18),
            command=lambda : self.set_search_option("Price 1")
        )
        price_1.place(x=53/1536*self.width, y=518/864*self.height, anchor="nw")

        price_2 = ctk.CTkButton(
            self.master,
            text="$$",
            bg_color="white",
            fg_color="#f0f4fc",
            text_color="#1572D3",
            border_color="#f0f4fc",
            width=83/1536*self.width,
            height=42/864*self.height,
            font=("Poppins Medium", 18),
            command=lambda : self.set_search_option("Price 2")
        )
        price_2.place(x=178/1536*self.width, y=518/864*self.height, anchor="nw")

        price_3 = ctk.CTkButton(
            self.master,
            text="$$$",
            bg_color="white",
            fg_color="#f0f4fc",
            text_color="#1572D3",
            border_color="#f0f4fc",
            width=92/1536*self.width,
            height=42/864*self.height,
            font=("Poppins Medium", 18),
            command=lambda : self.set_search_option("Price 3")
        )
        price_3.place(x=309/1536*self.width, y=518/864*self.height, anchor="nw")

        reset_button = ctk.CTkButton(
            self.master,
            text="Reset",
            bg_color="white",
            fg_color="#1572D3",
            text_color="white",
            border_color="#1572D3",
            width=137/1536*self.width,
            height=38/864*self.height,
            font=("Poppins Medium", 18),
            command=lambda : self.set_search_option("Reset")
        )
        reset_button.place(x=151/1536*self.width, y=600/864*self.height, anchor="nw")

        back_button = ctk.CTkButton(
            self.master,
            text="Back",
            bg_color="white",
            fg_color="#1572D3",
            text_color="white",
            border_color="#1572D3",
            width=107/1536*self.width,
            height=48/864*self.height,
            font=("Poppins Medium", 18),
            command=self.home_page
        )
        back_button.place(x=31/1536*self.width, y=725/864*self.height, anchor="nw")

        car_frame = ctk.CTkScrollableFrame(
            master=self.master,
            width=1026/1536*self.width,
            height=760/864*self.height,
            bg_color="white",
            fg_color="white"
        )
        car_frame.place(x=480/1536*self.width,y=10/864*self.height,anchor="nw")
        self.cursor.execute('SELECT * FROM CARS')
        results = self.cursor.fetchall()
        i = 0
        for car in results:
            if not check_filter_options(option_filter,car):
                continue

            car_slot_frame = ctk.CTkFrame(master=car_frame,bg_color="white",fg_color="white")
            slot_image = ctk.CTkImage(light_image=img.open('assets/car slot frame.png'),size=(903,248))
            slot_image_label = ctk.CTkLabel(master=car_slot_frame,image=slot_image, text="")
            slot_image_label.pack()

            #car image
            pil_image = img.open("assets/cars/" + car[4])
            car_image = ctk.CTkImage(light_image=img.open("assets/cars/" + car[4]), size=(272,round(272*pil_image.size[1]/pil_image.size[0])))
            car_image_label = ctk.CTkLabel(master=car_slot_frame, image=car_image, text="")
            car_image_label.place(x=50,y=56,anchor="nw")
            car_slot_frame.pack()

            #car name
            car_name = ctk.CTkLabel(master=car_slot_frame,text=car[2],font=("Poppins Medium",32),text_color="black")
            car_name.place(x=380,y=20)
            #rating
            car_rating = ctk.CTkLabel(master=car_slot_frame, text=car[6], font=("Poppins Regular", 20), text_color="black")
            car_rating.place(x=410, y=70)
            #capacity
            car_capacity = ctk.CTkLabel(master=car_slot_frame, text=str(car[5])+" Passengers", font=("Poppins Regular", 20),
                                      text_color="#959595")
            car_capacity.place(x=416, y=120)
            # year
            car_manufacturer_year = ctk.CTkLabel(master=car_slot_frame, text=car[1],
                                        font=("Poppins Regular", 20),
                                        text_color="#959595")
            car_manufacturer_year.place(x=595, y=120)
            # price
            car_price = ctk.CTkLabel(master=car_slot_frame, text="RM"+str(car[3]),
                                        font=("Poppins Semibold", 18),
                                        text_color="black")
            car_price.place(x=502, y=171)
            #rent button
            rentButton = ctk.CTkButton(
                master=car_slot_frame,
                text="Rent",
                bg_color="white",
                fg_color="#1572D3",
                text_color="white",
                border_color="#1572D3",
                width=137,
                height=38,
                font=("Poppins Medium", 14),
                command=lambda car_deets=car : self.rental_details(car_deets)
            )

            rentButton.place(x=708, y=166, anchor="nw")
            i+=1

    def set_search_option(self,option):
        disable = False
        match option:
            case "5 Passengers":
                self.search_options["capacity"] = 5
            case "7 Passengers":
                self.search_options["capacity"] = 7
            case "Manufacturer Year":
                self.search_options["manufacturer year"] = self.manu_year.get()
                if len(self.manu_year.get())!=4:
                    disable = True
            case "Auto":
                self.search_options["transmission"]  = "auto"
            case "Manual":
                self.search_options["transmission"] = "manual"
            case "Price 1":
                self.search_options["price"] = 1
            case "Price 2":
                self.search_options["price"] = 2
            case "Price 3":
                self.search_options["price"] = 3
            case "Reset":
                self.search_options = {"capacity": "any", "manufacturer year": "any", "transmission": "any", "price": "any"}

        if not disable: self.rental_page(self.search_options)

    def user_account(self):
        for i in self.master.winfo_children():
            i.destroy()

        user_account_ui = ctk.CTkImage(light_image=img.open("assets/user account ui.png"),
                                         size=(self.width, self.height - 68))
        user_account_ui_label = ctk.CTkLabel(self.master, image=user_account_ui, text="")
        user_account_ui_label.place(x=0, y=0, anchor="nw")

        #welcome message
        name_label = ctk.CTkLabel(
            self.master,text=self.user_info["first name"]+" "+self.user_info["last name"],
            font=("Poppins Regular",36),
            bg_color="white",fg_color="white",text_color="#1572D3"
        )
        name_label.place(x=200,y=550)

        self.first_name = ctk.StringVar()
        self.first_name.set(self.user_info["first name"])
        self.first_name_entry = ctk.CTkEntry(
            self.master,
            width=357.85 / 1707 * self.width,
            height=56.69 / 1067 * self.height,
            bg_color="white",
            fg_color="#D9D9D9",
            border_color="#D9D9D9",
            text_color="black",
            font=("Poppins Light", 24),
            textvariable=self.first_name
        )
        self.first_name_entry.place(x=704.58 / 1707 * self.width, y=362.58 / 1067 * self.height,
                               anchor="nw")
        self.first_name_entry.configure(state="readonly")

        self.last_name = ctk.StringVar()
        self.last_name.set(self.user_info["last name"])
        self.last_name_entry = ctk.CTkEntry(self.master, width=357.85 / 1707 * self.width,
                                                 height=56.69 / 1067 * self.height,
                                                 bg_color="white",
                                                 fg_color="#D9D9D9",
                                                 border_color="#D9D9D9",
                                                 text_color="black",
                                                 font=("Poppins Light", 24),
                                                 textvariable=self.last_name
                                       )
        self.last_name_entry.place(x=1122.44 / 1707 * self.width, y=362.58 / 1067 * self.height,
                              anchor="nw")
        self.last_name_entry.configure(state="readonly")

        self.account_username = ctk.StringVar()
        self.account_username.set(self.user_info["username"])
        self.username_entry = ctk.CTkEntry(self.master, width=357.85 / 1707 * self.width,
                                                height=56.69 / 1067 * self.height,
                                                bg_color="white",
                                                fg_color="#D9D9D9",
                                                border_color="#D9D9D9",
                                                text_color="black",
                                                font=("Poppins Light", 24),
                                                textvariable=self.account_username
                                                )
        self.username_entry.place(x=704.58 / 1707 * self.width, y=500.77 / 1067 * self.height,
                             anchor="nw")
        self.username_entry.configure(state="readonly")

        self.email = ctk.StringVar()
        self.email.set(self.user_info["email"])
        self.email_entry = ctk.CTkEntry(self.master, width=357.85 / 1707 * self.width,
                                             height=56.69 / 1067 * self.height,
                                             bg_color="white",
                                             fg_color="#D9D9D9",
                                             border_color="#D9D9D9",
                                             text_color="black",
                                             font=("Poppins Light", 24),
                                             textvariable=self.email
                                             )
        self.email_entry.place(x=704.58 / 1707 * self.width, y=638.95 / 1067 * self.height,
                          anchor="nw")

        self.email_entry.configure(state="readonly")

        back_btn = ctk.CTkButton(self.master, width=176.7 / 1707 * self.width,
                                           height=75 / 1067 * self.height, bg_color="white",
                                           fg_color="#1572D3", text="Back", text_color="white",
                                           font=("Poppins Light", 24),
                                            command=self.home_page)
        back_btn.place(x=81.13 / 1707 * self.width, y=891.25 / 1067 * self.height,
                       anchor="nw")

        edit_btn = ctk.CTkButton(self.master, width=176.7 / 1707 * self.width,
                                           height=75 / 1067 * self.height, bg_color="white",
                                           fg_color="#1572D3", text="Edit", text_color="white",
                                           font=("Poppins Light", 24),command=self.enable_edit)
        edit_btn.place(x=1340 / 1707 * self.width, y=690 / 1067 * self.height, anchor="nw")



    def enable_edit(self):
        self.first_name_entry.configure(state="normal")
        self.last_name_entry.configure(state="normal")
        self.username_entry.configure(state="normal")
        self.email_entry.configure(state="normal")

        self.finish_btn = ctk.CTkButton(self.master, width=176.7 / 1707 * self.width,
                                 height=75 / 1067 * self.height, bg_color="white",
                                 fg_color="#1572D3", text="Done", text_color="white",
                                 font=("Poppins Light", 24), command=self.disable_edit)
        self.finish_btn.place(x=1150 / 1707 * self.width, y=690 / 1067 * self.height, anchor="nw")

    def disable_edit(self):
        self.user_info["first name"] = self.first_name.get()
        self.user_info["last name"] = self.last_name.get()
        self.user_info["email"] = self.email.get()

        result = self.db_find_user(self.account_username.get())
        username_changed = self.user_info["username"]!=self.account_username.get()
        self.user_info["username"] = self.account_username.get()
        # check if all the details entered are valid or not
        error = ""

        valid_email = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.user_info["email"])
        if len(self.user_info["username"]) < 8:
            error = "Username must be 8 characters minimum"
        elif len(result) and username_changed:
            error = "Username taken"
        elif not valid_email:
            error = "Email is invalid"

        if error:
            messagebox.showerror("Error", error)
        else:
            self.first_name_entry.configure(state="readonly")
            self.last_name_entry.configure(state="readonly")
            self.username_entry.configure(state="readonly")
            self.email_entry.configure(state="readonly")

            self.finish_btn.destroy()
            self.cursor.execute(
                '''
                UPDATE USERS
                SET FIRST_NAME = ?, LAST_NAME = ?, USERNAME = ?, EMAIL = ?
                WHERE USER_ID =  ?;
                ''',
                (self.user_info["first name"],
                 self.user_info["last name"],
                 self.user_info["username"],
                 self.user_info["email"],
                 self.user_info["id"]
                 ))
            self.sqliteConnection.commit()

    def rental_details(self, car_array):
        for i in self.master.winfo_children():
            i.destroy()

        rental_details_ui = ctk.CTkImage(light_image=img.open("assets/rental details ui.png"),
                                       size=(self.width, self.height - 68))
        rental_details_ui_label = ctk.CTkLabel(self.master, image=rental_details_ui, text="")
        rental_details_ui_label.place(x=0, y=0, anchor="nw")

        pil_image = img.open("assets/cars/"+car_array[4])
        car_image = ctk.CTkImage(light_image=pil_image,
                                         size=(600, round(600*pil_image.size[1]/pil_image.size[0])))
        car_image_label = ctk.CTkLabel(self.master, image=car_image, text="",fg_color="white")
        car_image_label.place(x=55, y=300, anchor="nw")

        #car details
        #capacity
        capacity_label = ctk.CTkLabel(
            master=self.master,
            text=str(car_array[5])+" Passengers",
            font=("Poppins Regular",32),
            text_color="#959595",
            fg_color="white"
        )
        capacity_label.place(x=897,y=162,anchor="nw")
        # transmission
        transmission_label = ctk.CTkLabel(
            master=self.master,
            text=car_array[7],
            font=("Poppins Regular", 32),
            text_color="#959595",
            fg_color="white"
        )
        transmission_label.place(x=1212, y=162, anchor="nw")
        # manufacturer year
        manu_year_label = ctk.CTkLabel(
            master=self.master,
            text=car_array[1],
            font=("Poppins Regular", 32),
            text_color="#959595",
            fg_color="white"
        )
        manu_year_label.place(x=897, y=222, anchor="nw")
        # price
        price_label = ctk.CTkLabel(
            master=self.master,
            text="$"+str(car_array[3]),
            font=("Poppins Semibold", 32),
            text_color="black",
            fg_color="white"
        )
        price_label.place(x=1290, y=222, anchor="nw")
        #name
        name_label = ctk.CTkLabel(
            master=self.master,
            text=car_array[2],
            font=("Poppins Medium", 64),
            text_color="black",
            fg_color="white"
        )
        name_label.place(x=858, y=60, anchor="nw")

        #pick up location
        pickup_location = ctk.CTkComboBox(
            self.master,
            width=263,height=41,
            values=self.pickup_location_list,
            bg_color="white",
            fg_color="#D9D9D9",
            border_color="white",
            button_color="#D9D9D9",
            text_color="black",
            font=("Poppins Medium",16),
            dropdown_font=("Poppins Medium",16)
        )
        pickup_location.place(x=1026,y=358,anchor="nw")

        #pick up date
        self.pickup_date = ctk.CTkButton(
            self.master,text="",
            bg_color="white",fg_color="#D9D9D9",hover_color="#B6B6B6",text_color="black",
            font=("Poppins Medium",16),
            anchor="w",
            width=263,height=41,
            command=lambda : self.set_calendar("create pickup")
        )
        self.pickup_date.place(x=1028,y=451,anchor="nw")

        # return date
        self.return_date = ctk.CTkButton(
            self.master, text="",
            bg_color="white", fg_color="#D9D9D9", hover_color="#B6B6B6", text_color="black",
            font=("Poppins Medium", 16),
            anchor="w",
            width=263, height=41,
            command=lambda: self.set_calendar("create return")
        )
        self.return_date.place(x=1028, y=550, anchor="nw")


        #confirm button
        confirm_btn = ctk.CTkButton(self.master, width=170 / 1536 * self.width,
                                 height=54 / 864 * self.height, bg_color="white",
                                 fg_color="#1572D3", text="Confirm", text_color="white",
                                 font=("Poppins Light", 24),
                                 command=lambda : messagebox.showinfo("Booking made","Your booking is made\nPlease await approval"))
        confirm_btn.place(x=1065 / 1536 * self.width, y=642 / 864 * self.height,
                       anchor="nw")
        #back button
        back_btn = ctk.CTkButton(self.master, width=105 / 1536 * self.width,
                                 height=47 / 864 * self.height, bg_color="white",
                                 fg_color="#1572D3", text="Back", text_color="white",
                                 font=("Poppins Light", 24),
                                 command=self.rental_page)
        back_btn.place(x=55 / 1536 * self.width, y=717 / 864 * self.height,
                       anchor="nw")

    def set_calendar(self, code, event=None):
        match code:
            case "create pickup":
                self.return_date.configure(state="disabled")
                self.current_calendar = "pickup"
                self.pickup_date_calendar = Calendar(
                    self.master, selectmode='day',
                    showweeknumbers=False, cursor="hand2", date_pattern='dd-mm-y',
                    borderwidth=0, bordercolor='white',
                    font="Poppins 16"
                )
                self.pickup_date_calendar.place(x=1300, y=600, anchor="nw")
            case "create return":
                self.pickup_date.configure(state="disabled")
                self.current_calendar = "return"
                self.return_date_calendar = Calendar(
                    self.master, selectmode='day',
                    showweeknumbers=False, cursor="hand2", date_pattern='dd-mm-y',
                    borderwidth=0, bordercolor='white',
                    font="Poppins 16"
                )
                self.return_date_calendar.place(x=1300, y=700, anchor="nw")
            case "change":
                if self.current_calendar=="pickup":
                    self.pickup_date.configure(text=self.pickup_date_calendar.get_date())
                    self.pickup_date_calendar.destroy()
                    self.return_date.configure(state="normal")
                else:
                    self.return_date.configure(text=self.return_date_calendar.get_date())
                    self.return_date_calendar.destroy()
                    self.pickup_date.configure(state="normal")

    def past_rentals(self):
        for i in self.master.winfo_children():
            i.destroy()
        # bg image
        past_rentals_ui = ctk.CTkImage(light_image=img.open("assets/past booking ui.png"), size=(self.width, self.height-71))
        past_rentals_ui_label = ctk.CTkLabel(master=self.master, image=past_rentals_ui, text="")
        past_rentals_ui_label.place(relx=0, rely=0, anchor="nw")

        rentals_frame = ctk.CTkScrollableFrame(
            self.master,
            bg_color="white",fg_color="white",
            width=900,height=550
        )
        rentals_frame.place(x=298,y=149,anchor="nw")

        #back button
        back_btn = ctk.CTkButton(self.master, width=105 / 1536 * self.width,
                                 height=47 / 864 * self.height, bg_color="white",
                                 fg_color="#1572D3", text="Back", text_color="white",
                                 font=("Poppins Medium", 24),
                                 command=self.rental_page)
        back_btn.place(x=55 / 1536 * self.width, y=717 / 864 * self.height,
                       anchor="nw")

        self.cursor.execute("SELECT * FROM BOOKINGS INNER JOIN CARS ON BOOKINGS.CAR_ID = CARS.CAR_ID")
        booking_list = self.cursor.fetchall()

        for all_details in booking_list:
            booking = all_details[0:6]
            car = all_details[6:14]

            slot_frame = ctk.CTkFrame(
                rentals_frame,width=895,height=240,
                bg_color="white",fg_color="white"
            )
            #image
            img_string = "assets/past booking slot frame rated.png" if booking[4]!=-1 else "assets/past booking slot frame.png"
            slot_image = ctk.CTkImage(light_image=img.open(img_string),
                                           size=(895,240))
            slot_image_label = ctk.CTkLabel(
                master=slot_frame, image=slot_image, text="",
                bg_color="white"
            )
            slot_image_label.place(x=0, y=0, anchor="nw")

            # car image
            pil_image = img.open("assets/cars/" + car[4])
            car_image = ctk.CTkImage(light_image=img.open("assets/cars/" + car[4]),
                                     size=(272, round(272 * pil_image.size[1] / pil_image.size[0])))
            car_image_label = ctk.CTkLabel(master=slot_frame, image=car_image, text="")
            car_image_label.place(x=30, y=56, anchor="nw")
            #start and end date
            start_label = ctk.CTkLabel(
                master=slot_frame,text=booking[1],
                bg_color="white",fg_color="white",text_color="#747474",
                font=("Poppins Regular",20)
            )
            start_label.place(x=432,y=70)
            end_label = ctk.CTkLabel(
                master=slot_frame, text=booking[2],
                bg_color="white", fg_color="white", text_color="#747474",
                font=("Poppins Regular", 20)
            )
            end_label.place(x=432, y=97)
            #location
            location_label = ctk.CTkLabel(
                master=slot_frame, text=booking[3],
                bg_color="white", fg_color="white", text_color="#747474",
                font=("Poppins Regular", 20)
            )
            location_label.place(x=370, y=138)

            # car name
            car_name = ctk.CTkLabel(master=slot_frame, text=car[2], font=("Poppins Medium", 32), text_color="black")
            car_name.place(x=325, y=20)

            #rating/ratings button
            if booking[4]==-1:
                rate_button = ctk.CTkButton(
                    slot_frame,text="Rate",width=105,height=47,
                    font=("Poppins Medium",16),
                    bg_color="white",fg_color="#1572D3",text_color="white"
                )
                rate_button.place(x=705,y=120)
            else:
                rating_label = ctk.CTkLabel(
                    slot_frame,text=booking[4],
                    font=("Poppins Medium",64),
                    bg_color="white",fg_color="white",text_color="black"
                )
                rating_label.place(x=715,y=60)
                view_button = ctk.CTkButton(
                    slot_frame,text="View",
                    bg_color="white",fg_color="#1572D3",text_color="white",
                    width=105,height=47,font=("Poppins Medium",16)
                )
                view_button.place(x=715,y=145)

            slot_frame.pack()

    # def bookings_page(self):
        