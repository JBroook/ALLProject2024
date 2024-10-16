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

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Car Rental App")
        self.master.geometry("800x500")
        self.master._state_before_windows_set_titlebar_color = 'zoomed'
        self.width = self.master.winfo_screenwidth()
        self.height = self.master.winfo_screenheight()
        self.firstName = ctk.StringVar()
        self.firstName.set("Default")
        self.lastName = ctk.StringVar()
        self.lastName.set("User")
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

    def rental_page(self):
        for i in self.master.winfo_children():
            i.destroy()

        car_frame = ctk.CTkScrollableFrame(master=self.master,width=1210,height=760)
        car_frame.place(x=300,y=10,anchor="nw")
        self.cursor.execute('SELECT * FROM CARS')
        results = self.cursor.fetchall()
        for car in results:
            single_frame = ctk.CTkFrame(master=car_frame)
            pil_image = img.open('assets/cars/'+car[4])
            size_ratio = pil_image.size[1]/pil_image.size[0]
            car_image = ctk.CTkImage(light_image=img.open("assets/cars/"+car[4]), size=(300,round(300*size_ratio)))
            car_image_label = ctk.CTkLabel(master=single_frame, image=car_image, text="")
            car_image_label.pack(side="left")
            model_label = ctk.CTkLabel(master=single_frame,text=car[2])
            model_label.pack(side="left")
            single_frame.pack(fill="x")
