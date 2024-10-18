from tkinter import messagebox
import sqlite3 as sql
from tokenize import String

import customtkinter as ctk
from PIL import Image as img
import re
import smtplib,ssl
from email.message import EmailMessage
import string, random
import pyglet

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
        self.manu_year = ctk.StringVar()
        self.firstName = ctk.StringVar()
        self.firstName.set("Default")
        self.lastName = ctk.StringVar()
        self.lastName.set("User")
        self.search_options = {
            "capacity": "any",
            "manufacturer year": "any",
            "transmission": "any",
            "price": "any"
        }

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
            width=402,
            height=54,
            bg_color="white",
            fg_color="#D9D9D9",
            border_color="#D9D9D9",
            text_color="black",
            font=("Poppins Light",24),
            show="*"
        )
        passwordEntry.place(x=186,y=484,anchor="nw")

        # login/register frame
        loginButton = ctk.CTkButton(
            self.master,
            text="Login",
            command=self.test_credentials,
                bg_color="white",
            fg_color="#1572D3",
            text_color="white",
            border_color="#1572D3",
            width=187,
            height=57,
            font=("Poppins Medium",18)
        )
        loginButton.place(x=185,y=592-9,anchor="nw")

        registerButton = ctk.CTkButton(
            self.master,
            text="Register",
            command=self.register,
            bg_color="white",
            fg_color="#1572D3",
            text_color="white",
            border_color="#1572D3",
            width=187,
            height=57,
            font=("Poppins Medium",18)
        )
        registerButton.place(x=401,y=592-9,anchor="nw")


    def register(self):
        for i in self.master.winfo_children():
            i.destroy()
        registrationPage = ctk.CTkFrame(self.master)

        registerLabel = ctk.CTkLabel(registrationPage, text="Register an account", font=("Arial", 24))
        registerLabel.pack(anchor="center", pady="10")

        top_frame = ctk.CTkFrame(registrationPage)
        personal_info_frame = ctk.CTkFrame(top_frame)

        self.newFirstName = ctk.StringVar()
        newFirstNameFrame = ctk.CTkFrame(personal_info_frame)
        newFirstNameLabel = ctk.CTkLabel(newFirstNameFrame, text="First Name: ")
        newFirstNameLabel.pack(anchor="w")
        newFirstNameEntry = ctk.CTkEntry(newFirstNameFrame, textvariable=self.newFirstName)
        newFirstNameEntry.pack()
        newFirstNameFrame.pack()

        self.newLastName = ctk.StringVar()
        newLastNameFrame = ctk.CTkFrame(personal_info_frame)
        newLastNameLabel = ctk.CTkLabel(newLastNameFrame, text="Last Name: ")
        newLastNameLabel.pack(anchor="w")
        newLastNameEntry = ctk.CTkEntry(newLastNameFrame, textvariable=self.newLastName)
        newLastNameEntry.pack()
        newLastNameFrame.pack()

        self.newDOB = ctk.StringVar()
        newDOBFrame = ctk.CTkFrame(personal_info_frame)
        newDOBLabel = ctk.CTkLabel(newDOBFrame, text="DOB (YYYY-MM-DD): ")
        newDOBLabel.pack(anchor="w")
        newDOBEntry = ctk.CTkEntry(newDOBFrame, textvariable=self.newDOB)
        newDOBEntry.pack()
        newDOBFrame.pack()

        account_info_frame = ctk.CTkFrame(top_frame)
        self.newUsername = ctk.StringVar()
        newUsernameFrame = ctk.CTkFrame(account_info_frame)
        newUsernameLabel = ctk.CTkLabel(newUsernameFrame, text="Username: ")
        newUsernameLabel.pack(anchor="w")
        newUsernameEntry = ctk.CTkEntry(newUsernameFrame, textvariable=self.newUsername)
        newUsernameEntry.pack()
        newUsernameFrame.pack()

        self.newEmail = ctk.StringVar()
        newEmailFrame = ctk.CTkFrame(account_info_frame)
        newEmailLabel = ctk.CTkLabel(newEmailFrame, text="Email: ")
        newEmailLabel.pack(anchor="w")
        newEmailEntry = ctk.CTkEntry(newEmailFrame, textvariable=self.newEmail)
        newEmailEntry.pack()
        newEmailFrame.pack()

        self.newPassword = ctk.StringVar()
        newPasswordFrame = ctk.CTkFrame(account_info_frame)
        newPasswordLabel = ctk.CTkLabel(newPasswordFrame, text="Password: ")
        newPasswordLabel.pack(anchor="w")
        newPasswordEntry = ctk.CTkEntry(newPasswordFrame, textvariable=self.newPassword)
        newPasswordEntry.pack()
        newPasswordFrame.pack()

        self.confirmPassword = ctk.StringVar()
        confirmPasswordFrame = ctk.CTkFrame(account_info_frame)
        confirmPasswordLabel = ctk.CTkLabel(confirmPasswordFrame, text="Confirm Password: ")
        confirmPasswordLabel.pack(anchor="w")
        confirmPasswordEntry = ctk.CTkEntry(confirmPasswordFrame, textvariable=self.confirmPassword)
        confirmPasswordEntry.pack()
        confirmPasswordFrame.pack()

        personal_info_frame.pack(side="left",padx=10)
        account_info_frame.pack(side="left",padx=10)
        top_frame.pack()

        # return to login/confirm register frame
        registerButtonFrame = ctk.CTkFrame(registrationPage)
        returnButton = ctk.CTkButton(registerButtonFrame, text="Return to Login", command=self.login)
        returnButton.pack(side="left", padx="5")
        self.confirmRegistrationButton = ctk.CTkButton(registerButtonFrame, text="Confirm", command=self.confirm_registration)
        self.confirmRegistrationButton.pack(side="left", padx="5")
        registerButtonFrame.pack(pady="10",side="bottom")

        registrationPage.place(relx=0.5, rely=0.45, anchor="center")

    def test_credentials(self):
        query = f"SELECT * FROM USERS WHERE USERNAME = \'{self.username.get()}\';"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        if len(result):
            user = result[0]
            if user[3] == self.password.get():
                self.firstName.set(user[4])
                self.lastName.set(user[5])
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
            self.confirmRegistrationButton.configure(state="disabled")
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

        homepage_ui = ctk.CTkImage(light_image=img.open("assets/home page ui.png"), size=(1536, 800))
        homepage_ui_label = ctk.CTkLabel(self.master,image=homepage_ui,text="")
        homepage_ui_label.place(relx=0,rely=0,anchor="nw")

        rent_button = ctk.CTkButton(
            master=self.master,
            text="Go",
            width=158,
            height=40,
            font=("Poppins Medium",14),
            bg_color="#FFFFFF",
            fg_color="#1572D3",
            text_color="white",
            command=self.rental_page
        )
        rent_button.place(x=1210  ,y=204,anchor="nw")

        account_button = ctk.CTkButton(
            master=self.master,
            text="Go",
            width=158,
            height=42,
            font=("Poppins Medium", 14),
            bg_color="#FFFFFF",
            fg_color="#1572D3",
            text_color="white"
        )
        account_button.place(x=1210, y=441, anchor="nw")

        book_button = ctk.CTkButton(
            master=self.master,
            text="Go",
            width=158,
            height=42,
            font=("Poppins Medium", 14),
            bg_color="#FFFFFF",
            fg_color="#1572D3",
            text_color="white"
        )
        book_button.place(x=1210, y=673, anchor="nw")

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
            width=159,
            height=42,
            font=("Poppins Medium", 18),
            command=lambda : self.set_search_option("5 Passengers")
        )
        five_passenger.place(x=53, y=170, anchor="nw")

        seven_passenger = ctk.CTkButton(
            self.master,
            text="7 Passengers",
            bg_color="white",
            fg_color="#f0f4fc",
            text_color="#1572D3",
            border_color="#f0f4fc",
            width=159,
            height=42,
            font=("Poppins Medium", 18),
            command=lambda : self.set_search_option("7 Passengers")
        )
        seven_passenger.place(x=263, y=170, anchor="nw")

        self.manu_year.trace("w", lambda name, index, mode, sv=self.manu_year: self.set_search_option("Manufacturer Year"))
        manufacturer_year_entry = ctk.CTkEntry(
            self.master,
            bg_color="white",
            fg_color="#f0f4fc",
            text_color="#1572D3",
            border_color="#f0f4fc",
            width=167,
            height=38,
            font=("Poppins Medium", 20),
            textvariable=self.manu_year
        )
        manufacturer_year_entry.place(x=53,y=287)

        auto_button = ctk.CTkButton(
            self.master,
            text="Auto",
            bg_color="white",
            fg_color="#f0f4fc",
            text_color="#1572D3",
            border_color="#f0f4fc",
            width=97,
            height=42,
            font=("Poppins Medium", 18),
            command=lambda : self.set_search_option("Auto")
        )
        auto_button.place(x=53, y=403, anchor="nw")

        manual_button = ctk.CTkButton(
            self.master,
            text="Manual",
            bg_color="white",
            fg_color="#f0f4fc",
            text_color="#1572D3",
            border_color="#f0f4fc",
            width=118,
            height=42,
            font=("Poppins Medium", 18),
            command=lambda : self.set_search_option("Manual")
        )
        manual_button.place(x=187, y=403, anchor="nw")

        price_1 = ctk.CTkButton(
            self.master,
            text="$",
            bg_color="white",
            fg_color="#f0f4fc",
            text_color="#1572D3",
            border_color="#f0f4fc",
            width=74,
            height=42,
            font=("Poppins Medium", 18),
            command=lambda : self.set_search_option("Price 1")
        )
        price_1.place(x=53, y=518, anchor="nw")

        price_2 = ctk.CTkButton(
            self.master,
            text="$$",
            bg_color="white",
            fg_color="#f0f4fc",
            text_color="#1572D3",
            border_color="#f0f4fc",
            width=83,
            height=42,
            font=("Poppins Medium", 18),
            command=lambda : self.set_search_option("Price 2")
        )
        price_2.place(x=178, y=518, anchor="nw")

        price_3 = ctk.CTkButton(
            self.master,
            text="$$$",
            bg_color="white",
            fg_color="#f0f4fc",
            text_color="#1572D3",
            border_color="#f0f4fc",
            width=92,
            height=42,
            font=("Poppins Medium", 18),
            command=lambda : self.set_search_option("Price 3")
        )
        price_3.place(x=309, y=518, anchor="nw")

        reset_button = ctk.CTkButton(
            self.master,
            text="Reset",
            bg_color="white",
            fg_color="#1572D3",
            text_color="white",
            border_color="#1572D3",
            width=137,
            height=38,
            font=("Poppins Medium", 18),
            command=lambda : self.set_search_option("Reset")
        )
        reset_button.place(x=74, y=610, anchor="nw")

        search_button = ctk.CTkButton(
            self.master,
            text="Search",
            bg_color="white",
            fg_color="#1572D3",
            text_color="white",
            border_color="#1572D3",
            width=137,
            height=38,
            font=("Poppins Medium", 18)
        )
        search_button.place(x=237, y=610, anchor="nw")

        back_button = ctk.CTkButton(
            self.master,
            text="Back",
            bg_color="white",
            fg_color="#1572D3",
            text_color="white",
            border_color="#1572D3",
            width=107,
            height=48,
            font=("Poppins Medium", 18),
            command=self.home_page
        )
        back_button.place(x=31, y=725, anchor="nw")

        car_frame = ctk.CTkScrollableFrame(
            master=self.master,
            width=1056-30,
            height=760,
            bg_color="white",
            fg_color="white"
        )
        car_frame.place(x=480,y=10,anchor="nw")
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
                font=("Poppins Medium", 14)
            )
            rentButton.place(x=708, y=166, anchor="nw")

    def set_search_option(self,option):
        disable = False
        match option:
            case "5 Passengers":
                self.search_options["capacity"] = 5
            case "7 Passengers":
                self.search_options["capacity"] = 7
            case "Manufacturer Year":
                self.search_options["manufacturer year"] = self.manu_year.get()
                if len(self.manu_year.get())==4:
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