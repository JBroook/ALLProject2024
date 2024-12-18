import math
import os
from tkinter import messagebox, ttk, filedialog
import sqlite3 as sql
import matplotlib.pyplot as plt
import numpy as np
import customtkinter as ctk
from PIL import Image as img
import re
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import string, random
import pyglet
from tkcalendar import Calendar
from reportlab.pdfgen import canvas
from datetime import date, datetime
import time
import bcrypt

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

    conn = sql.connect("DriveEase.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT CAR_ID FROM BOOKINGS WHERE CAR_ID = {array[0]} AND CURRENT_BOOKING = 1")
    if cursor.fetchall():
        return False

    conn.close()

    return True

def check_response(message, user_id):
    match message:
        case "I want to confirm a booking.":
            conn = sql.connect("DriveEase.db")
            cursor = conn.cursor()
            cursor.execute(f"SELECT STATUS FROM BOOKINGS WHERE USER_ID = {user_id} AND CURRENT_BOOKING = 1")
            status = cursor.fetchone()
            if status:
                if status[0]=="Pending":
                    return "Your booking has been logged in our database and is pending approval from an Administrator! This process will complete within 1 business day."
                elif status[0]=="Approved":
                    return "Your booking has already been approved by an Administrator, please proceed to the Home Page>My Bookings>Current Bookings to pay for your rental!"
                elif status[0] == "Paid":
                    return "The payment for your current booking has already been confirmed! Enjoy your ride!"
            else:
                return "No active bookings have been found in our database. Ensure that you have confirmed your selection in the rental page first"
        case "How do I pay for my rental?":
            return "You can pay for your active booking by heading to Homepage>My Bookings>Current Booking and clicking the “Pay” button. The \"Pay\" button will appear once our status is \"Approved\" "
        case "When will my booking be approved?":
            return "The Administrator has been notified of your booking request and will approve/reject your booking soon. This process usually occurs within one business day after the booking request has been made."
        case "Why was my booking rejected?":
            return "Your booking can be rejected for a variety of reasons. These include, but are not limited to: Your booking duration was too long, your account reputation is too low, the requested vehicle is not available."
        case "I want to talk to a live operator":
            return "I understand. Please message the following number (+60102433090) on WhatsApp or email us at driveease3@gmail.com for more support"

def check_date(test_str, format):
    res = True
    # using try-except to check for truth value
    try:
        res = bool(datetime.strptime(test_str, format))
    except ValueError:
        res = False

    return res

class App:
    def __init__(self, master):
        #app settings
        self.selected_booking = None
        self.selected_car_id = None
        self.image_path = None
        self.master = master
        self.master.title("DriveEase")
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
            "id" : -1,
            "contact" : "0",
            "ic" : "0"
        }
        self.search_options = {
            "capacity": "any",
            "manufacturer year": "any",
            "transmission": "any",
            "price": "any"
        }
        self.current_calendar = "pickup"
        self.rating_button_list = []
        self.rating = 0

        #database stuff
        self.sqliteConnection = sql.connect("DriveEase.db")
        self.cursor = self.sqliteConnection.cursor()

        self.master.bind("<KeyRelease>", self.login_enter)
        self.master.bind("<<CalendarSelected>>",lambda x : self.set_calendar("change",x))
        # self.cursor.execute("SELECT * FROM CARS WHERE CAR_ID = 1")
        # self.rental_details(self.cursor.fetchall()[0])
        self.login()
        # self.rating_page((3, '10-11-2024', '30-11-2024', 'Bayan Lepas', -1, 1, 2, 1, 'Pending', 5100, 1, 2010, 'Honda Accord', 255, 'honda accord.png', 5, 4.5, 'Auto'))

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

        #forgot password
        forgotPasswordButton = ctk.CTkButton(
            self.master,text="Forgot password?",
            bg_color="white",fg_color="white",text_color="#1572D3",
            width=100/1536*self.width,height=20/864*self.height,hover_color="grey",
            font=("Poppins Medium",10/864*self.height),command=self.get_email
        )
        forgotPasswordButton.place(x=185/1536*self.width,y=540/864*self.height)

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
        loginButton.place(x=185/1536*self.width,y=600/864*self.height,anchor="nw")

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
        registerButton.place(x=401/1536*self.width,y=600/864*self.height,anchor="nw")

    def get_email(self):
        self.newWindow = ctk.CTkToplevel(self.master)
        # sets the title of the
        # Toplevel widget
        self.newWindow.title("Enter email")

        # sets the geometry of toplevel
        self.newWindow.geometry("400x200")

        # A Label widget to show in toplevel
        ctk.CTkLabel(self.newWindow, text="Enter your email\nA verification code will be sent").pack()
        self.recovery_email = ctk.StringVar()
        ctk.CTkEntry(self.newWindow, textvariable=self.recovery_email).pack()
        ctk.CTkButton(self.newWindow, text="Submit", command=self.reset_password).pack()

    def reset_password(self, valid=False):
        if not valid:
            self.newWindow.destroy()
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.recovery_email.get()):
                messagebox.showerror("Error","Invalid email")
                return None #break out and close window
            elif len(self.db_find_email(self.recovery_email.get().lower()))==0:
                messagebox.showerror("Error", "No user with this email found")
                return None  # break out and close window


            self.random_code = ''.join(random.choices(string.ascii_letters, k=6))

            msg = MIMEMultipart("alternative")
            with open("assets/HTML/PasswordResetEmail.html", "r") as file:
                html_content = file.read().replace("replaceable",self.random_code)

            # msg.set_content("If you did not reset your password, ignore this message.\nYour verification code is: " + self.random_code)
            msg['Subject'] = 'DriveEase Verification Code'
            msg['From'] = "driveease3@gmail.com"
            msg['To'] = self.recovery_email.get()

            html_part = MIMEText(html_content, "html")
            msg.attach(html_part)

            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("driveease3@gmail.com", "pskq ccbv rqvb jrwf")
            s.send_message(msg)
            s.quit()

            self.newWindow = ctk.CTkToplevel(self.master)

            # sets the title of the
            # Toplevel widget
            self.newWindow.title("Confirm your email")

            # sets the geometry of toplevel
            self.newWindow.geometry("400x200")

            # A Label widget to show in toplevel
            ctk.CTkLabel(self.newWindow, text="Enter your verification code").pack()
            self.verification_code = ctk.StringVar()
            ctk.CTkEntry(self.newWindow, textvariable=self.verification_code).pack()
            ctk.CTkButton(self.newWindow, text="Submit", command=self.check_password_token).pack()
        else :
            for i in self.master.winfo_children():
                i.destroy()
            # bg image
            forgot_password_ui = ctk.CTkImage(light_image=img.open("assets/reset password ui.png"), size=(self.width, self.height-64))
            forgot_password_ui_label = ctk.CTkLabel(master=self.master, image=forgot_password_ui, text="")
            forgot_password_ui_label.place(relx=0, rely=0, anchor="nw")

            self.newResetPassword = ctk.StringVar()
            newPasswordEntry = ctk.CTkEntry(master=self.master,
                                         textvariable=self.newResetPassword,
                                         width=402 / 1536 * self.width,
                                         height=54 / 864 * self.height,
                                         bg_color="white",
                                         fg_color="#D9D9D9",
                                         border_color="#D9D9D9",
                                         text_color="black",
                                         font=("Poppins Light", 24),
                                         show="*"
                                         )
            newPasswordEntry.place(x=186 / 1536 * self.width, y=375 / 864 * self.height, anchor="nw")

            self.newConfirmPassword = ctk.StringVar()
            confirmPasswordEntry = ctk.CTkEntry(
                self.master,
                textvariable=self.newConfirmPassword,
                width=402 / 1536 * self.width,
                height=54 / 864 * self.height,
                bg_color="white",
                fg_color="#D9D9D9",
                border_color="#D9D9D9",
                text_color="black",
                font=("Poppins Light", 24),
                show="*"
            )
            confirmPasswordEntry.place(x=186 / 1536 * self.width, y=484 / 864 * self.height, anchor="nw")

            # login/register frame
            confirmButton = ctk.CTkButton(
                self.master,
                text="Confirm",
                bg_color="white",
                fg_color="#1572D3",
                text_color="white",
                border_color="#1572D3",
                width=187 / 1536 * self.width,
                height=57 / 864 * self.height,
                font=("Poppins Medium", 18),
                command=lambda : self.change_password(self.recovery_email.get())
            )
            confirmButton.place(x=185 / 1536 * self.width, y=600 / 864 * self.height, anchor="nw")

            # Back Button
            back_button = ctk.CTkButton(
                self.master, text="Back", bg_color="white", fg_color="#1572D3",
                text_color="white",
                border_color="#1572D3", width=89 / 1280 * self.width,
                height=39 / 720 * self.height, font=("Poppins Medium", 18 / 1536 * self.width),
                command=self.login
            )
            back_button.place(x=45 / 1280 * self.width, y=588 / 720 * self.height)

    def change_password(self,email):
        if len(self.newResetPassword.get()) < 8:
            messagebox.showerror("Invalid Password","Password must be 8 characters minimum")
        elif not any(i.isdigit() for i in self.newResetPassword.get()):
            messagebox.showerror("Invalid Password","Password must contain at least one digit")
        elif self.newResetPassword.get() != self.newConfirmPassword.get():
            messagebox.showerror("Invalid Password","Passwords do not match")
        else:
            self.cursor.execute(
                '''
                UPDATE USERS SET USER_PASSWORD = ? WHERE EMAIL = ?
                ''', (bcrypt.hashpw(self.newResetPassword.get().encode(), bcrypt.gensalt()),email)
            )
            self.sqliteConnection.commit()
            messagebox.showinfo("Success","Your password has been successfully reset")
            self.login()


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
        user_entry.place(x=360 / 1280 * self.width, y=194 / 720 * self.height)

        # Password
        self.newPassword = ctk.StringVar()
        password_entry = ctk.CTkEntry(self.master, placeholder_text="******", width=215/1536*self.width, height=34/864*self.height, bg_color="white",
                                      fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black",textvariable=self.newPassword,show="*")
        password_entry.place(x=360 / 1280 * self.width, y=262 / 720 * self.height)

        # Confirm Password
        self.confirmPassword = ctk.StringVar()
        confirm_entry = ctk.CTkEntry(self.master, placeholder_text="******", width=215/1536*self.width, height=34/864*self.height, bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black",textvariable=self.confirmPassword,show="*")
        confirm_entry.place(x=360 / 1280 * self.width, y=343 / 720 * self.height)

        # contact no
        self.newContactNo = ctk.StringVar()
        contact_no_entry = ctk.CTkEntry(self.master, placeholder_text="+60123456789", width=215 / 1536 * self.width,
                                  height=34 / 864 * self.height,
                                  bg_color="white",
                                  fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black",
                                  textvariable=self.newContactNo)
        contact_no_entry.place(x=600 / 1280 * self.width, y=194 / 720 * self.height)

        # ic no
        self.newIcNo = ctk.StringVar()
        ic_entry = ctk.CTkEntry(self.master, placeholder_text="020304040456", width=215 / 1536 * self.width,
                                      height=34 / 864 * self.height, bg_color="white",
                                      fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black",
                                      textvariable=self.newIcNo)
        ic_entry.place(x=600 / 1280 * self.width, y=262 / 720 * self.height)

        # Login Button
        back_button = ctk.CTkButton(self.master, text="Back to Login", bg_color="white", fg_color="#1572D3",
                                    text_color="white",
                                    border_color="#1572D3", width=135/1536*self.width, height=41/864*self.height, font=("Poppins Medium", 18), command=self.login)
        back_button.place(x=500 / 1280 * self.width, y=500 / 720 * self.height)

        # Confirm Button
        self.confirm_button = ctk.CTkButton(self.master, text="Continue", bg_color="white", fg_color="#1572D3",
                                       text_color="white",
                                       border_color="#1572D3", width=135/1536*self.width, height=41/864*self.height, font=("Poppins Medium", 18),
                                       command=self.confirm_registration)
        self.confirm_button.place(x=656 / 1280 * self.width, y=500 / 720 * self.height)

    def test_credentials(self):
        query = f"SELECT * FROM USERS WHERE USERNAME = \'{self.username.get()}\';"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        if len(result):
            user = result[0]
            if bcrypt.checkpw(self.password.get().encode(), user[3]):
                if user[1]!="Admin":
                    self.user_info["first name"] = user[4]
                    self.user_info["last name"] = user[5]
                    self.user_info["username"] = user[1]
                    self.user_info["email"] = user[2]
                    self.user_info["id"] = user[0]
                    self.user_info["contact"] = user[7]
                    self.user_info["ic"] = user[8]
                    self.home_page()
                else:
                    self.admin_home()
            else:
                messagebox.showerror("Error", "Password is wrong")
        else:
            messagebox.showerror("Error", "Username doesn't exist")

    def db_find_user(self, _username):
        query = f"SELECT * FROM USERS WHERE USERNAME = \'{_username}\';"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def db_find_email(self, _email):
        query = f"SELECT * FROM USERS WHERE EMAIL = \'{_email}\';"
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
        elif len(self.db_find_email(self.newEmail.get().lower())):
            error = "Email already taken"
        elif not check_date(self.newDOB.get(),"%Y-%m-%d"):
            error = "Date of birth is invalid"
        elif len(self.newPassword.get())<8:
            error = "Password must be 8 characters minimum"
        elif not any(i.isdigit() for i in self.newPassword.get()):
            error = "Password must contain at least one digit"
        elif self.newPassword.get()!=self.confirmPassword.get():
            error = "Passwords do not match"
        elif not self.newContactNo.get().replace("+","").isdigit():
            error = "Invalid contact number"
        elif not self.newIcNo.get().replace("-","").isdigit() or len(self.newIcNo.get())<10:
            error = "Invalid IC number"

        if error :messagebox.showerror("Error", error)
        else:
            self.confirm_button.configure(state="disabled")
            #send verification code email
            msg = MIMEMultipart("alternative")
            self.random_code = ''.join(random.choices(string.ascii_letters, k=6))
            with open("assets/HTML/VerificationCodeEmail.html", "r") as file:
                html_content = file.read().replace("replaceable", self.random_code)

            # print(self.random_code)
            msg['Subject'] = 'DriveEase Verification Code'
            msg['From'] = "driveease3@gmail.com"
            msg['To'] = self.newEmail.get()

            html_part = MIMEText(html_content, "html")
            msg.attach(html_part)

            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("driveease3@gmail.com","pskq ccbv rqvb jrwf")
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
        if event.keysym == "Return" and self.user_info["id"]==-1:
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
            text_color="white",
            command=self.bookings_page
        )
        book_button.place(x=1210/1536*self.width, y=673/864*self.height, anchor="nw")

        help_button = ctk.CTkButton(
            master=self.master,
            text="?",
            width=49 / 1536 * self.width,
            height=49 / 864 * self.height,
            font=("Poppins Medium", 26),
            bg_color="#FFFFFF",
            fg_color="#1572D3",
            text_color="white",
            command=self.help_page
        )
        help_button.place(x=29 / 1536 * self.width, y=720 / 864 * self.height, anchor="nw")

    def help_page(self):
        for i in self.master.winfo_children():
            i.destroy()

        chat_history = ["Hi, there! How may I help you?"]

        help_page_ui = ctk.CTkImage(light_image=img.open("assets/help page ui.png"), size=(self.width, self.height - 64))
        help_page_ui_label = ctk.CTkLabel(self.master, image=help_page_ui, text="")
        help_page_ui_label.place(relx=0, rely=0, anchor="nw")

        self.chat_log_frame = ctk.CTkScrollableFrame(
            self.master,bg_color="white",fg_color="#D9D9D9",
            width=750/1536*self.width,height=500/864*self.height
        )
        self.chat_log_frame.place(x=300/1536*self.width,y=164/864*self.height)

        self.add_message("DriveEase Assistant",chat_history[0])
        

        option_frame = ctk.CTkScrollableFrame(
            self.master, bg_color="white", fg_color="#D9D9D9",
            width=300/1536*self.width, height=500/864*self.height
        )
        option_frame.place(x=1090/1536*self.width, y=164/864*self.height)

        option_list = [
            "I want to confirm a booking.",
            "How do I pay for my rental?",
            "When will my booking be \napproved?",
            "Why was my booking \nrejected?",
            "I want to talk to a live \noperator"
        ]
        for i in range(len(option_list)):
            frame = ctk.CTkFrame(option_frame,bg_color="#D9D9D9",fg_color="white")
            button = ctk.CTkButton(frame,text=option_list[i],
            bg_color="#D9D9D9",
            fg_color="#1572D3",
            text_color="white",
            border_color="#1572D3",
            width=300 / 1536 * self.width,
            height=116 / 864 * self.height,
            font=("Poppins Medium", 18/1536*self.width),
            command= lambda x=option_list[i] : self.add_message("User",x.replace("\n",""))
            )
            button.pack()
            frame.pack(pady=5)

            # Back Button
            back_button = ctk.CTkButton(
                self.master, text="Back", bg_color="white", fg_color="#1572D3",
                text_color="white",
                border_color="#1572D3", width=89 / 1280 * self.width,
                height=39 / 720 * self.height, font=("Poppins Medium", 18 / 1536 * self.width),
                command=self.home_page
            )
            back_button.place(x=45 / 1280 * self.width, y=588 / 720 * self.height)

    def add_message(self, user, message):
        frame = ctk.CTkFrame(self.chat_log_frame,width=500,height=40,fg_color="transparent")
        name_label = ctk.CTkLabel(frame,text=user,
                                  bg_color="#D9D9D9",text_color="#1572D3",
                                  font=("Poppins Semibold",24)
                                  )
        name_label.place(x=10,y=0)
        frame.pack(expand=True, fill="x")
        height = math.ceil(len(message) / 73)
        message_box = ctk.CTkTextbox(
            self.chat_log_frame,bg_color="#D9D9D9",text_color="black",fg_color="#D9D9D9",
            font=("Poppins Medium",18),
            width=700,height=40*height, wrap="word"
        )
        message_box.insert('end',message)
        message_box.configure(state="disabled")
        message_box.pack(expand=True,fill="x")

        if user=="User":
            # print(check_response(message, self.user_info["id"]))
            self.add_message("DriveEase Assistant",check_response(message,self.user_info["id"]))
            self.master.after(1, self.chat_log_frame._parent_canvas.yview_moveto, 1.0)

        self.master.after(1, self.chat_log_frame._parent_canvas.yview_moveto, 1.0)

    def check_verification(self):
        if self.verification_code.get()==self.random_code:
            # Encrypt the password
            hashed_password = bcrypt.hashpw(self.newPassword.get().encode(), bcrypt.gensalt())
            # Store user details with hashed password in the database
            self.cursor.execute('''
                                        INSERT INTO USERS (USERNAME, EMAIL, USER_PASSWORD, FIRST_NAME, LAST_NAME, DATE_OF_BIRTH,
                                        CONTACT_NUMBER, IC_NUMBER)
                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                                    ''', (self.newUsername.get(), self.newEmail.get().strip().lower(), hashed_password,
                                          self.newFirstName.get(), self.newLastName.get(), self.newDOB.get(), self.newContactNo.get().replace("+",""),
                                          self.newIcNo.get().replace("-","")
                                          )
                                )
            self.sqliteConnection.commit()
            self.newWindow.destroy()
            messagebox.showinfo("Success","Your account was successfully created. Welcome to DriveEase!")
            self.login()
        else:
            messagebox.showerror("Wrong code","Wrong code: Try again")

    def check_password_token(self):
        if self.verification_code.get() == self.random_code:
            self.newWindow.destroy()
            self.reset_password(True)
        else:
            messagebox.showerror("Wrong code", "Wrong code: Try again")

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

        # Back Button
        back_button = ctk.CTkButton(
            self.master, text="Back", bg_color="white", fg_color="#1572D3",
            text_color="white",
            border_color="#1572D3", width=89 / 1280 * self.width,
            height=39 / 720 * self.height, font=("Poppins Medium", 18 / 1536 * self.width),
            command=self.home_page
        )
        back_button.place(x=45 / 1280 * self.width, y=588 / 720 * self.height)

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
        # print("shit",results)
        for car in results:
            if not check_filter_options(option_filter,car):
                continue

            car_slot_frame = ctk.CTkFrame(master=car_frame,bg_color="white",fg_color="white")
            slot_image = ctk.CTkImage(light_image=img.open('assets/car slot frame.png'),size=(903/1536*self.width,248/864*self.height))
            slot_image_label = ctk.CTkLabel(master=car_slot_frame,image=slot_image, text="")
            slot_image_label.pack()

            #car image
            pil_image = img.open("assets/cars/" + car[4])
            car_image = ctk.CTkImage(light_image=img.open("assets/cars/" + car[4]), size=(272/1536*self.width,round(272*pil_image.size[1]/pil_image.size[0])/864*self.height))
            car_image_label = ctk.CTkLabel(master=car_slot_frame, image=car_image, text="")
            car_image_label.place(x=50/1536*self.width,y=56/864*self.height,anchor="nw")
            car_slot_frame.pack()

            #car name
            car_name = ctk.CTkLabel(master=car_slot_frame,text=car[2],font=("Poppins Medium",32/1536*self.width),text_color="black")
            car_name.place(x=380/1536*self.width,y=20/864*self.height)
            #rating
            car_rating = ctk.CTkLabel(master=car_slot_frame, text=car[6], font=("Poppins Regular", 20/1536*self.width), text_color="black")
            car_rating.place(x=410/1536*self.width, y=70/864*self.height)
            #capacity
            car_capacity = ctk.CTkLabel(master=car_slot_frame, text=str(car[5])+" Passengers", font=("Poppins Regular", 20/1536*self.width),
                                      text_color="#959595")
            car_capacity.place(x=416/1536*self.width, y=120/864*self.height)
            # year
            car_manufacturer_year = ctk.CTkLabel(master=car_slot_frame, text=car[1],
                                        font=("Poppins Regular", 20/1536*self.width),
                                        text_color="#959595")
            car_manufacturer_year.place(x=595/1536*self.width, y=120/864*self.height)
            # price
            car_price = ctk.CTkLabel(master=car_slot_frame, text="RM"+str(car[3]),
                                        font=("Poppins Semibold", 18/1536*self.width),
                                        text_color="black")
            car_price.place(x=502/1536*self.width, y=171/864*self.height)
            #rent button
            rentButton = ctk.CTkButton(
                master=car_slot_frame,
                text="Rent",
                bg_color="white",
                fg_color="#1572D3",
                text_color="white",
                border_color="#1572D3",
                width=137/1536*self.width,
                height=38/864*self.height,
                font=("Poppins Medium", 14/1536*self.width),
                command=lambda car_deets=car : self.rental_details(car_deets)
            )

            rentButton.place(x=708/1536*self.width, y=166/864*self.height, anchor="nw")
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
                self.search_options["transmission"]  = "Auto"
            case "Manual":
                self.search_options["transmission"] = "Manual"
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
        name_label.place(x=300/1536*self.width,y=600/864*self.height,anchor="center")

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

        self.account_contact = ctk.StringVar()
        self.account_contact.set(self.user_info["contact"])
        self.contact_entry = ctk.CTkEntry(self.master, width=357.85 / 1707 * self.width,
                                           height=56.69 / 1067 * self.height,
                                           bg_color="white",
                                           fg_color="#D9D9D9",
                                           border_color="#D9D9D9",
                                           text_color="black",
                                           font=("Poppins Light", 24),
                                           textvariable=self.account_contact
                                           )
        self.contact_entry.place(x=1122.44 / 1707 * self.width, y=500.77 / 1067 * self.height,
                                  anchor="nw")
        self.contact_entry.configure(state="readonly")

        self.account_ic = ctk.StringVar()
        self.account_ic.set(self.user_info["ic"])
        self.ic_entry = ctk.CTkEntry(self.master, width=357.85 / 1707 * self.width,
                                        height=56.69 / 1067 * self.height,
                                        bg_color="white",
                                        fg_color="#D9D9D9",
                                        border_color="#D9D9D9",
                                        text_color="black",
                                        font=("Poppins Light", 24),
                                        textvariable=self.account_ic
                                        )
        self.ic_entry.place(x=1122.44 / 1707 * self.width, y=638.95 / 1067 * self.height,
                               anchor="nw")

        self.ic_entry.configure(state="readonly")

        # Back Button
        back_button = ctk.CTkButton(
            self.master, text="Back", bg_color="white", fg_color="#1572D3",
            text_color="white",
            border_color="#1572D3", width=89 / 1280 * self.width,
            height=39 / 720 * self.height, font=("Poppins Medium", 18 / 1536 * self.width),
            command=self.home_page
        )
        back_button.place(x=45 / 1280 * self.width, y=588 / 720 * self.height)

        edit_btn = ctk.CTkButton(self.master, width=176.7 / 1707 * self.width,
                                           height=75 / 1067 * self.height, bg_color="white",
                                           fg_color="#1572D3", text="Edit", text_color="white",
                                           font=("Poppins Light", 24),command=self.enable_edit)
        edit_btn.place(x=1340 / 1707 * self.width, y=725 / 1067 * self.height, anchor="nw")

        # Logout Button
        out_button = ctk.CTkButton(self.master, text="Logout", bg_color="white", fg_color="#1572D3",
                                   text_color="white",
                                   border_color="#1572D3", width=89 / 1280 * self.width,
                                   height=39 / 720 * self.height, font=("Poppins Medium", 18),
                                   command=self.logout
                                   )
        out_button.place(x=1148 / 1280 * self.width, y=586 / 720 * self.height)

    def enable_edit(self):
        self.first_name_entry.configure(state="normal")
        self.last_name_entry.configure(state="normal")
        self.username_entry.configure(state="normal")
        self.contact_entry.configure(state="normal")
        self.ic_entry.configure(state="normal")

        self.finish_btn = ctk.CTkButton(self.master, width=176.7 / 1707 * self.width,
                                 height=75 / 1067 * self.height, bg_color="white",
                                 fg_color="#1572D3", text="Done", text_color="white",
                                 font=("Poppins Light", 24), command=self.disable_edit)
        self.finish_btn.place(x=1150 / 1707 * self.width, y=725 / 1067 * self.height, anchor="nw")

    def disable_edit(self):
        self.user_info["first name"] = self.first_name.get()
        self.user_info["last name"] = self.last_name.get()
        self.user_info["email"] = self.email.get()
        self.user_info["contact"] = self.account_contact.get()
        self.user_info["ic"] = self.account_ic.get()

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
            self.contact_entry.configure(state="readonly")
            self.ic_entry.configure(state="readonly")

            self.finish_btn.destroy()
            self.cursor.execute(
                '''
                UPDATE USERS
                SET FIRST_NAME = ?, LAST_NAME = ?, USERNAME = ?, EMAIL = ?, CONTACT_NUMBER = ?, IC_NUMBER = ?
                WHERE USER_ID =  ?
                ''',
                (self.user_info["first name"],
                 self.user_info["last name"],
                 self.user_info["username"],
                 self.user_info["email"],
                 self.user_info["contact"],
                 self.user_info["ic"],
                 self.user_info["id"]
                 ))
            self.sqliteConnection.commit()

    def rental_details(self, car_array, current=0):
        for i in self.master.winfo_children():
            i.destroy()

        rental_details_ui = ctk.CTkImage(light_image=img.open("assets/rental details ui.png"),
                                       size=(self.width, self.height - 68))
        rental_details_ui_label = ctk.CTkLabel(self.master, image=rental_details_ui, text="")
        rental_details_ui_label.place(x=0, y=0, anchor="nw")

        pil_image = img.open("assets/cars/"+car_array[4])
        car_image = ctk.CTkImage(light_image=pil_image,
                                         size=(600/1536*self.width, round(600*pil_image.size[1]/pil_image.size[0]) / 864 * self.height))
        car_image_label = ctk.CTkLabel(self.master, image=car_image, text="",fg_color="white")
        car_image_label.place(x=55/1536*self.width, y=300/864*self.height, anchor="nw")

        #car details
        #capacity
        capacity_label = ctk.CTkLabel(
            master=self.master,
            text=str(car_array[5])+" Passengers",
            font=("Poppins Regular",32/1536*self.width),
            text_color="#959595",
            fg_color="white"
        )
        capacity_label.place(x=897/1536*self.width,y=162 / 864 * self.height,anchor="nw")
        # transmission
        transmission_label = ctk.CTkLabel(
            master=self.master,
            text=car_array[7],
            font=("Poppins Regular", 32/1536*self.width),
            text_color="#959595",
            fg_color="white"
        )
        transmission_label.place(x=1212/1536*self.width, y=162 / 864 * self.height, anchor="nw")
        # manufacturer year
        manu_year_label = ctk.CTkLabel(
            master=self.master,
            text=car_array[1],
            font=("Poppins Regular", 32/1536*self.width),
            text_color="#959595",
            fg_color="white"
        )
        manu_year_label.place(x=897/1536*self.width, y=222 / 864 * self.height, anchor="nw")
        # price
        self.car_price = car_array[3]
        price_label = ctk.CTkLabel(
            master=self.master,
            text=f"RM{car_array[3]}",
            font=("Poppins Semibold", 32/1536*self.width),
            text_color="black",
            fg_color="white"
        )
        price_label.place(x=1360/1536*self.width, y=250 / 864 * self.height, anchor="e")
        #name
        name_label = ctk.CTkLabel(
            master=self.master,
            text=car_array[2],
            font=("Poppins Medium", 64/1536*self.width),
            text_color="black",
            fg_color="white"
        )
        name_label.place(x=858/1536*self.width, y=60 / 864 * self.height, anchor="nw")

        #pick up location
        self.pickup_location = ctk.StringVar()
        pickup_location_list = ctk.CTkComboBox(
            self.master,
            width=263/1536*self.width,height=41 / 864 * self.height,
            values=self.pickup_location_list,
            bg_color="white",
            fg_color="#D9D9D9",
            border_color="white",
            button_color="#D9D9D9",
            text_color="black",
            font=("Poppins Medium",16/1536*self.width),
            dropdown_font=("Poppins Medium",16/1536*self.width),
            variable=self.pickup_location
        )
        pickup_location_list.place(x=890/1536*self.width,y=370 / 864 * self.height,anchor="nw")

        #pick up date
        self.pickup_date = ctk.StringVar()
        self.pickup_date_button = ctk.CTkButton(
            self.master,text="",
            bg_color="white",fg_color="#D9D9D9",hover_color="#B6B6B6",text_color="black",
            font=("Poppins Medium",16/1536*self.width),
            anchor="w",
            width=263/1536*self.width,height=41 / 864 * self.height,
            command=lambda : self.set_calendar("create pickup")
        )
        self.pickup_date_button.place(x=890/1536*self.width,y=460 / 864 * self.height,anchor="nw")

        # return date
        self.return_date = ctk.StringVar()
        self.return_date_button = ctk.CTkButton(
            self.master, text="",
            bg_color="white", fg_color="#D9D9D9", hover_color="#B6B6B6", text_color="black",
            font=("Poppins Medium", 16/1536*self.width),
            anchor="w",
            width=263/1536*self.width, height=41 / 864 * self.height,
            command=lambda: self.set_calendar("create return")
        )
        self.return_date_button.place(x=890/1536*self.width, y=560 / 864 * self.height, anchor="nw")

        #duration and total charge calculation
        self.rent_duration = ctk.IntVar()
        self.duration_label = ctk.CTkLabel(
            self.master,text=str(self.rent_duration.get())+" Day"+ ("s" if self.rent_duration.get()!=1 else ""),
            font=("Poppins Medium",24/1536*self.width),
            bg_color="white",fg_color="white",text_color="black"
        )
        self.duration_label.place(x=1200/1536*self.width, y=358 / 864 * self.height)

        self.rent_charge = ctk.IntVar()
        self.charge_label = ctk.CTkLabel(
            self.master, text=f"RM{self.rent_duration.get():.2f}",
            font=("Poppins Medium", 24/1536*self.width),
            bg_color="white",fg_color="white",text_color="black"
        )
        self.charge_label.place(x=1200 / 1536 * self.width, y=451 / 864 * self.height)

        #confirm button
        #what confirm does is different based on whether we are making a new booking
        #or updating an active one
        if current==0:
            confirm_func = lambda x=car_array[0] : self.make_booking(x)
        else:
            confirm_func = lambda x=current : self.update_booking(x)

        confirm_btn = ctk.CTkButton(self.master, width=170 / 1536 * self.width,
                                 height=54 / 864 * self.height, bg_color="white",
                                 fg_color="#1572D3", text="Confirm", text_color="white",
                                 font=("Poppins Light", 24/1536*self.width),
                                 command=confirm_func)
        confirm_btn.place(x=1065 / 1536 * self.width, y=642 / 864 * self.height,
                       anchor="nw")
        # Back Button
        back_button = ctk.CTkButton(
            self.master, text="Back", bg_color="white", fg_color="#1572D3",
            text_color="white",
            border_color="#1572D3", width=89 / 1280 * self.width,
            height=39 / 720 * self.height, font=("Poppins Medium", 18 / 1536 * self.width),
            command=self.rental_page if current==0 else self.current_booking
        )
        back_button.place(x=45 / 1280 * self.width, y=588 / 720 * self.height)

    def make_booking(self, car_id):
        self.cursor.execute(f"SELECT * FROM BOOKINGS WHERE USER_ID = {self.user_info["id"]} AND CURRENT_BOOKING = 1")
        current_bookings = self.cursor.fetchall()

        if self.pickup_location.get()=="" or self.pickup_date.get()=="" or self.return_date.get()=="":
            messagebox.showerror("Empty field", "Please fill in all fields")
        elif time.strptime(self.pickup_date.get(),"%Y-%m-%d")<time.strptime(date.today().strftime('%Y-%m-%d'),'%Y-%m-%d'):
            messagebox.showerror("Invalid start date", "Your selected start date is invalid.\nTry again.")
        elif time.strptime(self.return_date.get(),"%Y-%m-%d")<time.strptime(self.pickup_date.get(),"%Y-%m-%d"):
            messagebox.showerror("Invalid return date", "Your selected return date is invalid.\nTry again.")
        elif len(current_bookings):
            messagebox.showerror("Another booking is active", "You already have an active booking")
        else:
            days_rented = datetime.strptime(self.return_date.get(),"%Y-%m-%d")-datetime.strptime(self.pickup_date.get(),"%Y-%m-%d")
            self.cursor.execute(f"SELECT PRICE FROM CARS WHERE CAR_ID = {car_id}")
            total_charge = self.cursor.fetchone()[0]*(days_rented.days+1)
            # print(total_charge)

            self.cursor.execute(
                '''
                INSERT INTO BOOKINGS (
                START_DATE, END_DATE, 
                LOCATION, 
                CAR_ID, USER_ID, CURRENT_BOOKING, STATUS, TOTAL_CHARGE
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    self.pickup_date.get(),
                    self.return_date.get(),
                    self.pickup_location.get(),
                    car_id,
                    self.user_info["id"],
                    1,
                    "Pending",
                    total_charge
                )
            )
            messagebox.showinfo("Booking made", "Your booking is made\nPlease await approval")
            self.sqliteConnection.commit()
            self.home_page()

    def update_booking(self, booking_id):
        if self.pickup_location.get() == "" or self.pickup_date.get() == "" or self.return_date.get() == "":
            messagebox.showerror("Empty field", "Please fill in all fields")
        elif time.strptime(self.pickup_date.get(), "%Y-%m-%d") < time.strptime(date.today().strftime('%Y-%m-%d'),
                                                                               '%Y-%m-%d'):
            messagebox.showerror("Invalid start date", "Your selected start date is invalid.\nTry again.")
        elif time.strptime(self.return_date.get(), "%Y-%m-%d") < time.strptime(self.pickup_date.get(), "%Y-%m-%d"):
            messagebox.showerror("Invalid return date", "Your selected return date is invalid.\nTry again.")
        else:
            self.cursor.execute(f"SELECT CAR_ID FROM BOOKINGS WHERE BOOKING_ID = {booking_id}")
            car_id = self.cursor.fetchone()[0]
            days_rented = datetime.strptime(self.return_date.get(), "%Y-%m-%d") - datetime.strptime(self.pickup_date.get(), "%Y-%m-%d")
            self.cursor.execute(f"SELECT PRICE FROM CARS WHERE CAR_ID = {car_id}")
            total_charge = self.cursor.fetchone()[0] * (days_rented.days+1)
            self.cursor.execute(
                '''
                UPDATE BOOKINGS SET 
                START_DATE = ?, END_DATE = ?, 
                LOCATION = ?, TOTAL_CHARGE = ?
                WHERE BOOKING_ID = ?
                ''', (self.pickup_date.get(), self.return_date.get(), self.pickup_location.get(),total_charge,booking_id)
            )
            messagebox.showinfo("Booking updated", "Your booking is updated\nPlease await approval")
            self.sqliteConnection.commit()
            self.current_booking()

    def set_calendar(self, code, event=None):
        match code:
            case "create pickup":
                self.return_date_button.configure(state="disabled")
                self.current_calendar = "pickup"
                self.pickup_date_calendar = Calendar(
                    self.master, selectmode='day',
                    showweeknumbers=False, cursor="hand2", date_pattern='y-mm-dd',
                    borderwidth=0, bordercolor='white',
                    font="Poppins 16"
                )
                self.pickup_date_calendar.place(x=1300, y=600, anchor="nw")
            case "create return":
                self.pickup_date_button.configure(state="disabled")
                self.current_calendar = "return"
                self.return_date_calendar = Calendar(
                    self.master, selectmode='day',
                    showweeknumbers=False, cursor="hand2", date_pattern='y-mm-dd',
                    borderwidth=0, bordercolor='white',
                    font="Poppins 16"
                )
                self.return_date_calendar.place(x=1300, y=650, anchor="nw")
            case "change":
                if self.current_calendar=="pickup":
                    self.pickup_date_button.configure(text=self.pickup_date_calendar.get_date())
                    self.pickup_date.set(self.pickup_date_calendar.get_date())
                    self.pickup_date_calendar.destroy()
                    self.return_date_button.configure(state="normal")
                else:
                    self.return_date_button.configure(text=self.return_date_calendar.get_date())
                    self.return_date.set(self.return_date_calendar.get_date())
                    self.return_date_calendar.destroy()
                    self.pickup_date_button.configure(state="normal")

                if self.pickup_date.get() and self.return_date.get():
                    if time.strptime(self.pickup_date.get(), "%Y-%m-%d") < time.strptime(
                            date.today().strftime('%Y-%m-%d'), '%Y-%m-%d'):
                        messagebox.showerror("Invalid start date", "Your selected start date is invalid.\nTry again.")
                    elif time.strptime(self.return_date.get(), "%Y-%m-%d") < time.strptime(self.pickup_date.get(),
                                                                                           "%Y-%m-%d"):
                        messagebox.showerror("Invalid return date", "Your selected return date is invalid.\nTry again.")
                    else:# all date details valid, calculate duration and charge
                        self.rent_duration.set((datetime.strptime(self.return_date.get(),"%Y-%m-%d")-datetime.strptime(self.pickup_date.get(),"%Y-%m-%d")).days+1)
                        self.rent_charge.set(self.rent_duration.get()*self.car_price)

                        self.duration_label.configure(text=str(self.rent_duration.get())+" Day"+ ("s" if self.rent_duration.get()!=1 else ""))
                        self.charge_label.configure(text=f"RM{self.rent_charge.get():.2f}")



    def past_rentals(self):
        for i in self.master.winfo_children():
            i.destroy()
        # bg image
        past_rentals_ui = ctk.CTkImage(light_image=img.open("assets/past booking ui.png"), size=(self.width, self.height-71))
        past_rentals_ui_label = ctk.CTkLabel(master=self.master, image=past_rentals_ui, text="")
        past_rentals_ui_label.place(relx=0, rely=0, anchor="nw")


        # Back Button
        back_button = ctk.CTkButton(
            self.master, text="Back", bg_color="white", fg_color="#1572D3",
            text_color="white",
            border_color="#1572D3", width=89 / 1280 * self.width,
            height=39 / 720 * self.height, font=("Poppins Medium", 18 / 1536 * self.width),
            command=self.bookings_page
        )
        back_button.place(x=45 / 1280 * self.width, y=588 / 720 * self.height)

        self.cursor.execute(f"SELECT * FROM BOOKINGS INNER JOIN CARS ON BOOKINGS.CAR_ID = CARS.CAR_ID WHERE CURRENT_BOOKING = 0 AND STATUS = 'Paid' AND USER_ID = {self.user_info["id"]}")
        booking_list = self.cursor.fetchall()
        # print("shit", booking_list)

        if len(booking_list)==0:
            ctk.CTkLabel(
                self.master,text="No completed bookings...",font=("Poppins Semibold",36),
                text_color="black",bg_color="white",fg_color="white"
            ).place(x=self.width/2,y=self.height/2,anchor="center")
        else:
            rentals_frame = ctk.CTkScrollableFrame(
                self.master,
                bg_color="white", fg_color="white",
                width=900 / 1536 * self.width, height=550 / 864 * self.height
            )
            rentals_frame.place(x=298 / 1536 * self.width, y=149 / 864 * self.height, anchor="nw")

        for all_details in booking_list:
            # print("deets",all_details)
            if all_details[5]==self.user_info["id"]:
                if time.strptime(all_details[2],"%Y-%m-%d")<time.strptime(date.today().strftime('%Y-%m-%d'),'%Y-%m-%d') or all_details[6]==0:
                    self.cursor.execute(f"UPDATE BOOKINGS SET CURRENT_BOOKING = 0 WHERE BOOKING_ID = {all_details[0]}")
                    self.sqliteConnection.commit()
                else:
                    continue
            else:
                continue

            self.cursor.execute(f"SELECT SCORE FROM RATINGS WHERE BOOKING_ID = {all_details[0]}")
            all_details = list(all_details)
            all_details.insert(9,self.cursor.fetchone())
            all_details = tuple(all_details)
            # print(all_details)
            booking = all_details[0:10]
            car = all_details[10:18]

            slot_frame = ctk.CTkFrame(
                rentals_frame,width=895/1536*self.width,height=240/864*self.height,
                bg_color="white",fg_color="white"
            )
            #image
            img_string = "assets/past booking slot frame rated.png" if (booking[9] is not None and booking[9]!=0) else "assets/past booking slot frame.png"
            slot_image = ctk.CTkImage(light_image=img.open(img_string),
                                           size=(895/1536*self.width,240/864*self.height))
            slot_image_label = ctk.CTkLabel(
                master=slot_frame, image=slot_image, text="",
                bg_color="white"
            )
            slot_image_label.place(x=0, y=0, anchor="nw")

            # print(car)
            # car image
            pil_image = img.open("assets/cars/" + car[4])
            car_image = ctk.CTkImage(light_image=pil_image,
                                     size=(272/1536*self.width, round(272 * pil_image.size[1] / pil_image.size[0])/864*self.height))
            car_image_label = ctk.CTkLabel(master=slot_frame, image=car_image, text="")
            car_image_label.place(x=30/1536*self.width, y=56/864*self.height, anchor="nw")
            #start and end date
            start_label = ctk.CTkLabel(
                master=slot_frame,text=booking[1],
                bg_color="white",fg_color="white",text_color="#747474",
                font=("Poppins Regular",20)
            )
            start_label.place(x=432/1536*self.width,y=70/864*self.height)
            end_label = ctk.CTkLabel(
                master=slot_frame, text=booking[2],
                bg_color="white", fg_color="white", text_color="#747474",
                font=("Poppins Regular", 20)
            )
            end_label.place(x=432/1536*self.width, y=97/864*self.height)
            #location
            location_label = ctk.CTkLabel(
                master=slot_frame, text=booking[3],
                bg_color="white", fg_color="white", text_color="#747474",
                font=("Poppins Regular", 20/1536*self.width)
            )
            location_label.place(x=370/1536*self.width, y=138/864*self.height)

            # car name
            car_name = ctk.CTkLabel(master=slot_frame, text=car[2], font=("Poppins Medium", 32/1536*self.width), text_color="black")
            car_name.place(x=325/1536*self.width, y=20/864*self.height)

            #rating/ratings button
            if booking[9] is None or booking[9]==0:
                rate_button = ctk.CTkButton(
                    slot_frame,text="Rate",width=105/1536*self.width,height=47/864*self.height,
                    font=("Poppins Medium",16/1536*self.width),
                    bg_color="white",fg_color="#1572D3",text_color="white",
                    command=lambda x = all_details: self.rating_page(x, False)
                )
                rate_button.place(x=705/1536*self.width,y=120/864*self.height)
            else:
                rating_label = ctk.CTkLabel(
                    slot_frame,text=booking[9],
                    font=("Poppins Medium",64/1536*self.width),
                    bg_color="white",fg_color="white",text_color="black"
                )
                rating_label.place(x=715/1536*self.width,y=60/864*self.height)
                view_button = ctk.CTkButton(
                    slot_frame,text="View",
                    bg_color="white",fg_color="#1572D3",text_color="white",
                    width=105,height=47,font=("Poppins Medium",16/1536*self.width),command=lambda x=all_details: self.rating_page(x, True)
                )
                view_button.place(x=715/1536*self.width,y=145/864*self.height)

            slot_frame.pack()

    def current_booking(self):
        for i in self.master.winfo_children():
            i.destroy()

        # get booking details
        self.cursor.execute(f"SELECT * FROM BOOKINGS WHERE USER_ID = {self.user_info["id"]}")
        booking = []
        for i in self.cursor.fetchall():
            if i[6] == 1:
                booking = i
                break

        if booking:
            current_booking_ui = ctk.CTkImage(light_image=img.open("assets/current booking ui.png"),
                                              size=(self.width, self.height - 68))
            current_booking_ui_label = ctk.CTkLabel(self.master, image=current_booking_ui, text="")
            current_booking_ui_label.place(x=0, y=0, anchor="nw")

            self.cursor.execute(f"SELECT * FROM CARS WHERE CAR_ID = {booking[4]}")
            car = self.cursor.fetchone()

            pil_image = img.open("assets/cars/"+car[4])
            car_image_ph = ctk.CTkImage(light_image=pil_image,
                                        size=(600 / 1707 * self.width, round(600 * pil_image.size[1] / pil_image.size[0]) / 1069 * self.height))
            car_image_ph_label = ctk.CTkLabel(self.master, image=car_image_ph, text="",bg_color="white",fg_color="white")
            car_image_ph_label.place(x=333 / 1707 * self.width, y=310 / 1067 * self.height, anchor="nw")

            car_name = ctk.CTkLabel(self.master, width=442 / 1707 * self.width, height=61 / 1067 * self.height,
                                    fg_color="#FFFFFF", bg_color="#FFFFFF", text=car[2], text_color="#000000",
                                    font=("Poppins", 32))
            car_name.place(x=1030 / 1707 * self.width, y=240 / 1067 * self.height, anchor="nw")

            capacity = ctk.CTkLabel(self.master, width=125 / 1707 * self.width, height=39 / 1067 * self.height,
                                    fg_color="#FFFFFF", bg_color="#FFFFFF", text=str(car[5])+" Passengers", anchor="w",
                                    text_color="#747474", font=("Poppins Light", 24))
            capacity.place(x=1100 / 1707 * self.width, y=333 / 1067 * self.height, anchor="nw")

            type = ctk.CTkLabel(self.master, width=115 / 1707 * self.width, height=39 / 1067 * self.height,
                                fg_color="#FFFFFF", bg_color="#FFFFFF", text=car[7], anchor="w",
                                text_color="#747474", font=("Poppins Light", 24))
            type.place(x=1350 / 1707 * self.width, y=333 / 1067 * self.height, anchor="nw")

            start_date = ctk.CTkLabel(self.master, width=242 / 1707 * self.width, height=35 / 1067 * self.height,
                                      fg_color="#FFFFFF", bg_color="#FFFFFF", text=booking[1], anchor="w",
                                      text_color="#747474", font=("Poppins Light", 22))
            start_date.place(x=1171 / 1707 * self.width, y=395 / 1067 * self.height, anchor="nw")

            end_date = ctk.CTkLabel(self.master, width=251 / 1707 * self.width, height=35 / 1067 * self.height,
                                    fg_color="#FFFFFF", bg_color="#FFFFFF", text=booking[2], anchor="w",
                                    text_color="#747474", font=("Poppins Light", 22))
            end_date.place(x=1171 / 1707 * self.width, y=431 / 1067 * self.height, anchor="nw")

            location = ctk.CTkLabel(self.master, width=305 / 1707 * self.width, height=39 / 1067 * self.height,
                                    fg_color="#FFFFFF", bg_color="#FFFFFF", text=booking[3], anchor="w",
                                    text_color="#747474", font=("Poppins Light", 24))
            location.place(x=1098 / 1707 * self.width, y=484 / 1067 * self.height, anchor="nw")

            price = ctk.CTkLabel(self.master, width=264 / 1707 * self.width, height=39 / 1067 * self.height,
                                 fg_color="#FFFFFF", bg_color="#FFFFFF", text=f"RM{booking[8]:.2f}", anchor="w",
                                 text_color="#9C9C9C", font=("Poppins", 24))
            price.place(x=1157 / 1707 * self.width, y=552 / 1067 * self.height, anchor="nw")

            status_label = ctk.CTkLabel(self.master, width=150 / 1707 * self.width, height=54.4 / 1067 * self.height,
                                        fg_color="#FFFFFF", bg_color="#FFFFFF", text="Status:", text_color="#000000",
                                        font=("Poppins", 36))
            status_label.place(x=400 / 1707 * self.width, y=809 / 1067 * self.height, anchor="nw")

            status = ctk.CTkLabel(self.master, width=307.46 / 1707 * self.width, height=54 / 1067 * self.height,
                                  fg_color="#FFFFFF", bg_color="#FFFFFF", text=booking[7], text_color="#000000",
                                  font=("Poppins", 30))
            status.place(x=566 / 1707 * self.width, y=809 / 1067 * self.height, anchor="nw")

            update_btn = ctk.CTkButton(self.master, width=171 / 1707 * self.width, height=60.4 / 1067 * self.height,
                                       bg_color="white", fg_color="#1572D3", text="Update", text_color="#FFFFFF",
                                       font=("Poppins", 24),command=lambda : self.rental_details(car,booking[0]))
            update_btn.place(x=1071 / 1707 * self.width, y=621.08 / 1067 * self.height, anchor="nw")
            if booking[7]!="Pending":
                update_btn.configure(state="disabled")

            cancel_btn = ctk.CTkButton(self.master, width=171 / 1707 * self.width, height=60.4 / 1067 * self.height,
                                       bg_color="white", fg_color="#1572D3", text="Cancel", text_color="#FFFFFF",
                                       font=("Poppins", 24),command=lambda : self.prompt_cancel(booking[0]))
            cancel_btn.place(x=1273 / 1707 * self.width, y=621.08 / 1067 * self.height, anchor="nw")
            if booking[7]=="Paid":
                update_btn.configure(state="disabled")

            if booking[7]=="Approved":
                pay_btn = ctk.CTkButton(self.master, width=153 / 1707 * self.width, height=54.4 / 1067 * self.height,
                                        bg_color="white", fg_color="#1572D3", text="Pay", text_color="#FFFFFF",
                                        font=("Poppins", 24),command=lambda : self.payment_page(booking[0]))
                pay_btn.place(x=1098 / 1707 * self.width, y=809 / 1067 * self.height, anchor="nw")
        else:
            current_booking_ui = ctk.CTkImage(light_image=img.open("assets/current booking ui empty.png"),
                                              size=(self.width, self.height - 68))
            current_booking_ui_label = ctk.CTkLabel(self.master, image=current_booking_ui, text="")
            current_booking_ui_label.place(x=0, y=0, anchor="nw")

            rent_button = ctk.CTkButton(self.master, width=171 / 1707 * self.width, height=60.4 / 1067 * self.height,
                                       bg_color="white", fg_color="#1572D3", text="Rent Now", text_color="#FFFFFF",
                                       font=("Poppins", 24), command=self.rental_page)
            rent_button.place(x=853 / 1707 * self.width, y=533 / 1067 * self.height, anchor="center")

        # Back Button
        back_button = ctk.CTkButton(
            self.master, text="Back", bg_color="white", fg_color="#1572D3",
            text_color="white",
            border_color="#1572D3", width=89 / 1280 * self.width,
            height=39 / 720 * self.height, font=("Poppins Medium", 18 / 1536 * self.width),
            command=self.bookings_page
        )
        back_button.place(x=45 / 1280 * self.width, y=588 / 720 * self.height)

    def prompt_cancel(self, booking_id):
        self.cancel_prompt = ctk.CTkToplevel(self.master)
        ctk.CTkLabel(self.cancel_prompt,text="Cancel your booking?",font=("Poppins Semibold",24)).pack()
        ctk.CTkLabel(self.cancel_prompt, text="This action is permanent", font=("Poppins Medium", 18)).pack()
        ctk.CTkButton(self.cancel_prompt, text="Confirm", font=("Poppins Medium", 18),command=lambda : self.cancel_booking(booking_id)).pack()

    def cancel_booking(self, booking_id):
        self.cancel_prompt.destroy()
        self.cursor.execute(
            "UPDATE BOOKINGS SET CURRENT_BOOKING = ?, STATUS = ? WHERE BOOKING_ID = ?",
            (0,"Cancelled",booking_id)
        )
        self.sqliteConnection.commit()
        messagebox.showinfo("Booking cancelled", "Your booking is cancelled")
        self.current_booking()

    def bookings_page(self):
        for i in self.master.winfo_children():
            i.destroy()
        # Background Image
        background_image = ctk.CTkImage(img.open("assets/Booking_Status.png"),
                                                  size=(self.width, self.height - 64))
        background_image_label = ctk.CTkLabel(master=self.master.master, image=background_image, text="")
        background_image_label.place(relx=0, rely=0)

        # Current Booking
        current_button = ctk.CTkButton(self.master, text="Current Booking", bg_color="white",
                                                 fg_color="#1572D3", text_color="white",
                                                 border_color="#1572D3", width=775 / 1280 * self.width,
                                                 height=88 / 720 * self.height, font=("Poppins Medium", 18),
                                                 command=self.current_booking
                                       )
        current_button.place(x=230 / 1280 * self.width, y=240 / 720 * self.height)

        # Past Booking
        past_button = ctk.CTkButton(self.master, text="Past Booking", bg_color="white", fg_color="#1572D3",
                                              text_color="white",
                                              border_color="#1572D3", width=775 / 1280 * self.width,
                                              height=88 / 720 * self.height, font=("Poppins Medium", 18),command=self.past_rentals)
        past_button.place(x=230 / 1280 * self.width, y=387 / 720 * self.height)

        # Back Button
        back_button = ctk.CTkButton(
            self.master, text="Back", bg_color="white", fg_color="#1572D3",
            text_color="white",
            border_color="#1572D3", width=89 / 1280 * self.width,
            height=39 / 720 * self.height, font=("Poppins Medium", 18 / 1536 * self.width),
            command=self.home_page
        )
        back_button.place(x=45 / 1280 * self.width, y=588 / 720 * self.height)

    def payment_page(self, booking_id):
        background_image = ctk.CTkImage(img.open("assets/payment page ui.png"), size=(self.width, self.height - 64))
        background_image_label = ctk.CTkLabel(master=self.master, image=background_image, text="")
        background_image_label.place(relx=0, rely=0)

        # Cardholder's Name
        self.cardholder_name_entry = ctk.CTkEntry(self.master, placeholder_text="Alice Tan Wong", width=320 / 1280 * self.width,
                                  height=34 / 720 * self.height, bg_color="white",
                                  fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
        self.cardholder_name_entry.place(x=451 / 1280 * self.width, y=240 / 720 * self.height)

        # Card Number
        self.number_entry = ctk.CTkEntry(self.master, placeholder_text="1234 5678 9012 3456", width=320 / 1280 * self.width,
                                    height=34 / 720 * self.height, bg_color="white",
                                    fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
        self.number_entry.place(x=451 / 1280 * self.width, y=320 / 720 * self.height)

        # Expiry Date
        self.expiry_entry = ctk.CTkEntry(self.master, placeholder_text="01/24", width=159 / 1280 * self.width,
                                    height=34 / 720 * self.height, bg_color="white",
                                    fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
        self.expiry_entry.place(x=451 / 1280 * self.width, y=400 / 720 * self.height)

        # CVC
        self.cvc_entry = ctk.CTkEntry(self.master, placeholder_text="* * *", width=122 / 1280 * self.width,
                                 height=34 / 720 * self.height, bg_color="white",
                                 fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black")
        self.cvc_entry.place(x=650 / 1280 * self.width, y=400 / 720 * self.height)

        self.cursor.execute(f'''SELECT START_DATE, END_DATE, PRICE FROM BOOKINGS INNER JOIN CARS ON BOOKINGS.CAR_ID = CARS.CAR_ID
                            WHERE BOOKING_ID = {booking_id}''')
        results = self.cursor.fetchone()
        duration = (datetime.strptime(results[1],"%Y-%m-%d")-datetime.strptime(results[0],"%Y-%m-%d")).days+1
        charge_label = ctk.CTkLabel(
            self.master,text=f"RM{duration*results[2]:.2f}",
            bg_color="white",fg_color="white",text_color="black",
            font=("Poppins Medium",16)
        )
        charge_label.place(x=542/1536*self.width,y=580/864*self.height)

        # Pay Button
        confirm_button = ctk.CTkButton(self.master, text="Pay", bg_color="white", fg_color="Green", text_color="white",
                                       border_color="#1572D3", width=89 / 1280 * self.width,
                                       height=39 / 720 * self.height, font=("Poppins Medium", 18),
                                       command=lambda : self.confirm_payment(booking_id)
                                       )
        confirm_button.place(x=450 / 1280 * self.width, y=550 / 720 * self.height)

        # Back Button
        back_button = ctk.CTkButton(
            self.master, text="Back", bg_color="white", fg_color="#1572D3",
            text_color="white",
            border_color="#1572D3", width=89 / 1280 * self.width,
            height=39 / 720 * self.height, font=("Poppins Medium", 18 / 1536 * self.width),
            command=self.current_booking
        )
        back_button.place(x=45 / 1280 * self.width, y=588 / 720 * self.height)

    def confirm_payment(self, booking_id):
        name = self.cardholder_name_entry.get()
        number = self.number_entry.get().strip().replace(" ","")
        expiry_date = self.expiry_entry.get().strip()
        code = self.cvc_entry.get().strip()
        self.cursor.execute(f"SELECT TOTAL_CHARGE FROM BOOKINGS WHERE BOOKING_ID = {booking_id}")
        charge = self.cursor.fetchone()

        # Validate input
        if not name or not number or not expiry_date or not code:
            messagebox.showerror("Error", "All fields are required!")
        elif not number.replace(" ","").isdigit():
            messagebox.showerror("Error", "Card number is invalid")
        elif not expiry_date.replace("/","").isdigit() or len(expiry_date)!=5:
            messagebox.showerror("Error", "Expiry date is invalid")
        elif not code.isdigit() or len(code)!=3:
            messagebox.showerror("Error", "CVC code is invalid")
        else:
            self.cursor.execute("INSERT INTO PAYMENTS (NAME, CARD_NUMBER, EXPIRY, CVC, BOOKING_ID, DATE_PAID) "
                      "VALUES (?, ?, ?, ?, ?, ?)", (name, number, expiry_date, code, booking_id, date.today().strftime("%Y-%m-%d")))
            self.cursor.execute(f"UPDATE BOOKINGS SET STATUS = \'Paid\' WHERE BOOKING_ID = {booking_id}")
            self.sqliteConnection.commit()
            messagebox.showinfo("Success", "Payment successful!")
            self.current_booking()

            msg = MIMEMultipart("alternative")
            with open("assets/HTML/PaymentConfirmationEmail.html", "r") as file:
                html_content = file.read().replace("replaceable1", f"RM{charge[0]:.2f}")
                html_content = html_content.replace("replaceable2", f"**** {number[len(number)-4:]}")

            html_part = MIMEText(html_content, "html")
            msg.attach(html_part)

            msg['Subject'] = 'DriveEase Verification Code'
            msg['From'] = "driveease3@gmail.com"
            msg['To'] = self.user_info["email"]

            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("driveease3@gmail.com", "pskq ccbv rqvb jrwf")
            s.send_message(msg)
            s.quit()

    def rating_page(self, all_details, rating_done):
        # print(all_details)
        booking = all_details[0:10]
        car = all_details[10:18]
        rate_booking_ui = ctk.CTkImage(light_image=img.open("assets/car rating ui.png"),
                                       size=(self.width, self.height - 68))
        rate_booking_ui_label = ctk.CTkLabel(self.master, image=rate_booking_ui, text="")
        rate_booking_ui_label.place(x=0, y=0, anchor="nw")

        car_name = ctk.CTkLabel(self.master, fg_color="#FFFFFF", bg_color="#FFFFFF", text=car[2],
                                text_color="#000000", font=("Poppins", 56/1536*self.width))
        car_name.place(x=317 / 1707 * self.width, y=203 / 1067 * self.height, anchor="nw")

        car_picture = ctk.CTkImage(light_image=img.open("assets/cars/"+car[4]),
                                   size=(580.22 / 1707 * self.width, 307.49 / 1067 * self.height))
        car_picture_label = ctk.CTkLabel(self.master, image=car_picture, text="", bg_color="white",fg_color="white")
        car_picture_label.place(x=261 / 1707 * self.width, y=331.09 / 1067 * self.height, anchor="nw")

        start_date = ctk.CTkLabel(self.master, fg_color="#FFFFFF", bg_color="#FFFFFF", anchor="w", text=booking[1],
                                  text_color="#747474", font=("Poppins", 26 / 1067 * self.height))
        start_date.place(x=352 / 1707 * self.width, y=692 / 1067 * self.height, anchor="nw")

        end_date = ctk.CTkLabel(self.master, fg_color="#FFFFFF", bg_color="#FFFFFF", anchor="w", text=booking[2],
                                text_color="#747474", font=("Poppins", 26 / 1067 * self.height))
        end_date.place(x=352 / 1707 * self.width, y=738 / 1067 * self.height, anchor="nw")

        location = ctk.CTkLabel(self.master, fg_color="#FFFFFF", bg_color="#FFFFFF", anchor="w", text=booking[3],
                                text_color="#747474", font=("Poppins", 26 / 1067 * self.height))
        location.place(x=668 / 1707 * self.width, y=693 / 1067 * self.height, anchor="nw")

        self.review_textbox = ctk.CTkTextbox(self.master, width=492 / 1707 * self.width,
                                       height=449 / 1067 * self.height,
                                       bg_color="white",
                                       fg_color="#D9D9D9",
                                       border_color="#D9D9D9",
                                       corner_radius=8,
                                       wrap="word",
                                       scrollbar_button_color="#000000",
                                       text_color="black",
                                       font=("Poppins Light", 32/1536*self.width))
        self.review_textbox.place(x=1068 / 1707 * self.width, y=306 / 1067 * self.height, anchor="nw")

        self.rating_button_list.clear()
        for i in range(5):
            btn = ctk.CTkButton(self.master, width=79 / 1707 * self.width, height=75 / 1067 * self.height,
                                 command=lambda x=i+1: self.rating_button(x),
                                 bg_color="white", fg_color="#EFBF14", text="☆", text_color="#FFFFFF",
                                 font=("Poppins", 32/1536*self.width))
            btn.place(x=(1084+95*i) / 1707 * self.width, y=182 / 1067 * self.height, anchor="nw")
            self.rating_button_list.append(btn)

        bck_btn = ctk.CTkButton(self.master, width=171 / 1707 * self.width, height=69 / 1067 * self.height,
                                bg_color="white", fg_color="#1572D3", text="Back", text_color="white",
                                font=("Poppins", 24/1536*self.width),command=self.past_rentals)
        bck_btn.place(x=72 / 1707 * self.width, y=878 / 1067 * self.height, anchor="nw")

        if rating_done:
            self.cursor.execute(f"SELECT SCORE, REVIEW FROM RATINGS WHERE BOOKING_ID = {all_details[0]}")
            info = self.cursor.fetchone()
            for i in range(len(self.rating_button_list)):
                if i<info[0]:
                    self.rating_button_list[i].configure(state="disabled",text="★",text_color_disabled="white")

            self.review_textbox.insert("insert", info[1])
            self.review_textbox.configure(state="disabled")

            # edit_btn = ctk.CTkButton(self.master, width=171 / 1707 * self.width, height=69 / 1067 * self.height,
            #                             bg_color="white", fg_color="#1572D3", text="Edit", text_color="white",
            #                             font=("Poppins", 24),
            #                             command=lambda: self.save_rating(booking[0])
            #                             )
            # edit_btn.place(x=1389 / 1707 * self.width, y=786 / 1067 * self.height, anchor="nw")
        else:
            confirm_btn = ctk.CTkButton(self.master, width=171 / 1707 * self.width, height=69 / 1067 * self.height,
                                        bg_color="white", fg_color="#1572D3", text="Confirm", text_color="white",
                                        font=("Poppins", 24),
                                        command=lambda: self.save_rating(booking[0])
                                        )
            confirm_btn.place(x=1389 / 1707 * self.width, y=786 / 1067 * self.height, anchor="nw")

    def rating_button(self, star_selected):
        for i in range(5):
            if i<star_selected:
                self.rating_button_list[i].configure(text="★")
            else:
                self.rating_button_list[i].configure(text="☆")
        self.rating = star_selected
        # print(self.rating)

    def save_rating(self,booking_id):
        self.cursor.execute(
            '''
            INSERT INTO RATINGS (SCORE, REVIEW, BOOKING_ID, RATING_DATE)
            VALUES (?, ?, ?, ?)
            ''',
            (
                self.rating,
                self.review_textbox.get(1.0,"end-1c"),
                booking_id,
                datetime.today().strftime("%Y-%m-%d")
            )
        )
        self.sqliteConnection.commit()
        messagebox.showinfo("Review saved","Thank you for leaving your review!")
        self.past_rentals()

    def admin_home(self):
        for i in self.master.winfo_children():
            i.destroy()

        # Background Image
        background_image = ctk.CTkImage(img.open("assets/admin menu ui.png"),
                                                  size=(self.width, self.height - 64))
        background_image_label = ctk.CTkLabel(master=self.master.master, image=background_image, text="")
        background_image_label.place(relx=0, rely=0)

        # Logout Button
        out_button = ctk.CTkButton(self.master, text="Logout", bg_color="white", fg_color="#1572D3",
                                             text_color="white",
                                             border_color="#1572D3", width=89 / 1280 * self.width,
                                             height=39 / 720 * self.height, font=("Poppins Medium", 18),
                                             command=self.logout
                                   )
        out_button.place(x=1148 / 1280 * self.width, y=586 / 720 * self.height)

        # Manage Bookings Button
        booking_button = ctk.CTkButton(self.master, text="Go", bg_color="white", fg_color="#1572D3",
                                                 text_color="white",
                                                 border_color="#1572D3", width=89 / 1280 * self.width,
                                                 height=39 / 720 * self.height, font=("Poppins Medium", 18),
                                                 command=self.manage_bookings
                                       )
        booking_button.place(x=999 / 1280 * self.width, y=280 / 720 * self.height)

        # Manage Cars Button
        cars_button = ctk.CTkButton(self.master, text="Go", bg_color="white", fg_color="#1572D3",
                                              text_color="white",
                                              border_color="#1572D3", width=89 / 1280 * self.width,
                                              height=39 / 720 * self.height, font=("Poppins Medium", 18),command=self.manage_cars)
        cars_button.place(x=380 / 1280 * self.width, y=280 / 720 * self.height)

        # Performance Report Button
        performance_button = ctk.CTkButton(self.master, text="Go", bg_color="white", fg_color="#1572D3",
                                                     text_color="white",
                                                     border_color="#1572D3", width=89 / 1280 * self.width,
                                                     height=39 / 720 * self.height,
                                                     font=("Poppins Medium", 18),command=self.performance_report)
        performance_button.place(x=729 / 1280 * self.width, y=506 / 720 * self.height)

    def logout(self):
        self.login()
        self.user_info = {
            "first name": "Default",
            "last name": "User",
            "username": "Unknown",
            "email": "Unknown",
            "id": -1,
            "contact" : "",
            "ic" : ""
        }
        self.search_options = {
            "capacity": "any",
            "manufacturer year": "any",
            "transmission": "any",
            "price": "any"
        }
        self.current_calendar = "pickup"
        self.rating_button_list = []
        self.rating = 0

    def performance_report(self):
        for i in self.master.winfo_children():
            i.destroy()
        # bg image
        past_rentals_ui = ctk.CTkImage(light_image=img.open("assets/performance report ui.png"), size=(self.width, self.height-71))
        past_rentals_ui_label = ctk.CTkLabel(master=self.master, image=past_rentals_ui, text="")
        past_rentals_ui_label.place(relx=0, rely=0, anchor="nw")

        self.cursor.execute(
            '''SELECT SUM(BOOKINGS.TOTAL_CHARGE) FROM BOOKINGS 
            INNER JOIN PAYMENTS ON PAYMENTS.BOOKING_ID = BOOKINGS.BOOKING_ID
            WHERE PAYMENTS.DATE_PAID = DATE('now')'''
        )

        today_income = self.cursor.fetchone()[0]
        today_income_label = ctk.CTkLabel(
            self.master,text=f"RM{today_income if today_income else 0:.2f}",
            bg_color="white",fg_color="white",text_color="black",
            font=("Poppins Medium",36/1536*self.width)
        )
        today_income_label.place(x=88/1536*self.width,y=240/864*self.height)

        self.cursor.execute(
            '''SELECT SUM(BOOKINGS.TOTAL_CHARGE) FROM BOOKINGS 
                INNER JOIN PAYMENTS ON PAYMENTS.BOOKING_ID = BOOKINGS.BOOKING_ID
                WHERE DATE(DATE_PAID) <= DATE('now') AND DATE(DATE_PAID) >= DATE('now','-7 day')'''
        )

        result = self.cursor.fetchone()[0]
        week_income = 0 if not result else result
        week_income_label = ctk.CTkLabel(
            self.master,text=f"RM{week_income:.2f}",
            bg_color="white",fg_color="white",text_color="#656565",
            font=("Poppins Medium",24/1536*self.width)
        )
        week_income_label.place(x=352/1536*self.width,y=306/864*self.height)

        self.cursor.execute("SELECT AVG(SCORE) FROM RATINGS")
        review_average = self.cursor.fetchone()[0]
        review_average_label = ctk.CTkLabel(
            self.master,text=f"{review_average if review_average else 0:.2f}",
            bg_color="white",fg_color="white",text_color="black",
            font=("Poppins Medium",36/1536*self.width)
        )
        review_average_label.place(x=92/1536*self.width,y=520/864*self.height)

        self.cursor.execute("SELECT COUNT(SCORE) FROM RATINGS")
        review_count = self.cursor.fetchone()[0]
        review_count_label = ctk.CTkLabel(
            self.master, text=f"{review_count}",
            bg_color="white", fg_color="white", text_color="#656565",
            font=("Poppins Medium", 24/1536*self.width)
        )
        review_count_label.place(x=457/1536*self.width,y=585/864*self.height)

        self.cursor.execute("SELECT COUNT(USER_ID) FROM USERS")
        user_count = self.cursor.fetchone()[0]
        user_count_label = ctk.CTkLabel(
            self.master, text=f"{user_count}",
            bg_color="white", fg_color="white", text_color="black",
            font=("Poppins Medium", 36/1536*self.width)
        )
        user_count_label.place(x=596/1536*self.width, y=240/864*self.height)
        #pie chart
        self.cursor.execute("SELECT COUNT(DISTINCT USER_ID) FROM BOOKINGS B INNER JOIN PAYMENTS P ON B.BOOKING_ID = P.BOOKING_ID")
        paid_users = self.cursor.fetchone()[0]
        new_users = user_count-paid_users
        total = user_count
        y = np.array([paid_users,new_users])
        my_colors = ["#1034FF","#10FF68"]
        percentage_labels = [f"{paid_users/total*100:.2f}%",f"{new_users/total*100:.2f}%"]
        plt.pie(y, colors=my_colors,startangle=90, labels=percentage_labels, textprops={'fontsize': 20})
        plt.savefig("assets/user_pie_chart", facecolor='w', bbox_inches="tight", pad_inches=0.3, transparent=True)

        pie_chart = ctk.CTkImage(light_image=img.open("assets/user_pie_chart.png"),
                                       size=(300/1536*self.width,300*(428/553)/864*self.height))
        pie_chart_label = ctk.CTkLabel(master=self.master, image=pie_chart, text="")
        pie_chart_label.place(x=734/1536*self.width, y=428/864*self.height, anchor="center")

        text_list = ["Past Day","Past Week","Past Month","Past Year"]
        for i in range(4):
            button = ctk.CTkButton(
                self.master,text=text_list[i],
                bg_color="white",fg_color="#1572D3",text_color="white",
                width=185/1536*self.width,height=169/864*self.height,
                font=("Poppins Medium",20/1536*self.width),command=lambda x=text_list[i]: self.print_pdf(x)
            )
            button.place(x=(1035+208*(i%2))/1536*self.width,y=(258+189*(i>1))/864*self.height)

            # Back Button
            back_button = ctk.CTkButton(
                self.master, text="Back", bg_color="white", fg_color="#1572D3",
                text_color="white",
                border_color="#1572D3", width=89 / 1280 * self.width,
                height=39 / 720 * self.height, font=("Poppins Medium", 18 / 1536 * self.width),
                command=self.admin_home
            )
            back_button.place(x=45 / 1280 * self.width, y=588 / 720 * self.height)
    def print_pdf(self,time_option):
        # Create a PDF canvas object
        c = canvas.Canvas("Sales Report.pdf", pagesize="A4")

        # Set up font and size
        c.setFont("Helvetica", 12)

        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(60, 740, f" Drive Ease Sales Report ({time_option})")

        # Line break
        c.setFont("Helvetica", 12)
        y_position = 720

        match time_option:
            case "Past Day":
                # List of sections to be printed in the report
                self.cursor.execute(
                    '''SELECT SUM(TOTAL_CHARGE) FROM BOOKINGS B 
                    INNER JOIN PAYMENTS P ON P.BOOKING_ID = B.BOOKING_ID
                    WHERE DATE(P.DATE_PAID) = DATE('now')
                    '''
                )
                revenue = self.cursor.fetchone()[0]
                self.cursor.execute(
                    '''SELECT COUNT(B.BOOKING_ID) FROM BOOKINGS B 
                    INNER JOIN PAYMENTS P ON P.BOOKING_ID = B.BOOKING_ID
                    WHERE DATE(P.DATE_PAID) = DATE('now')
                    '''
                )
                rental_count = self.cursor.fetchone()[0]
                self.cursor.execute(
                    '''SELECT SUM(TOTAL_CHARGE) FROM BOOKINGS B 
                    INNER JOIN PAYMENTS P ON P.BOOKING_ID = B.BOOKING_ID
                    WHERE DATE(P.DATE_PAID) = DATE('now','-1 day')
                    '''
                )
                percent_change = self.cursor.fetchone()[0]
                percent_change = (revenue-percent_change)/percent_change if percent_change else 0

                self.cursor.execute(
                    '''SELECT MODEL, IMAGE, MANUFACTURER_YEAR, TRANSMISSION, PRICE, CAPACITY FROM CARS C 
                    INNER JOIN BOOKINGS B ON C.CAR_ID = B.CAR_ID
                    GROUP BY MODEL
                    ORDER BY COUNT(B.CAR_ID)
                    '''
                )
                most_popular = self.cursor.fetchone()

                self.cursor.execute(
                    '''SELECT AVG(SCORE) FROM RATINGS
                    WHERE RATING_DATE = DATE('now')
                    '''
                )
                average_rating = self.cursor.fetchone()[0]
                report_data = {
                    "Total Revenue:": f"RM{revenue if revenue else 0:.2f}",
                    "Total Paid Rentals:": f"{rental_count}",
                    f"Percentage Change in Revenue from {time_option}:": f"{percent_change:.2f}%",
                    "Average Ratings:": f"{average_rating if average_rating else 0:.1f}/5",
                    "Most Popular Car:": most_popular[0]
                }
            case "Past Week":
                # List of sections to be printed in the report
                self.cursor.execute(
                    '''SELECT SUM(TOTAL_CHARGE) FROM BOOKINGS B 
                    INNER JOIN PAYMENTS P ON P.BOOKING_ID = B.BOOKING_ID
                    WHERE DATE(P.DATE_PAID) <= DATE('now') AND DATE(P.DATE_PAID) >= DATE('now','-7 day')
                    '''
                )
                revenue = self.cursor.fetchone()[0]
                self.cursor.execute(
                    '''SELECT COUNT(B.BOOKING_ID) FROM BOOKINGS B 
                    INNER JOIN PAYMENTS P ON P.BOOKING_ID = B.BOOKING_ID
                    WHERE DATE(P.DATE_PAID) <= DATE('now') AND DATE(P.DATE_PAID) >= DATE('now','-7 day')
                    '''
                )
                rental_count = self.cursor.fetchone()[0]
                self.cursor.execute(
                    '''SELECT SUM(TOTAL_CHARGE) FROM BOOKINGS B 
                    INNER JOIN PAYMENTS P ON P.BOOKING_ID = B.BOOKING_ID
                    WHERE DATE(P.DATE_PAID) <= DATE('now','-7 day') AND DATE(P.DATE_PAID) >= DATE('now','-14 day')
                    '''
                )
                percent_change = self.cursor.fetchone()[0]
                percent_change = (revenue - percent_change) / percent_change if percent_change else 0

                self.cursor.execute(
                    '''SELECT MODEL, IMAGE, MANUFACTURER_YEAR, TRANSMISSION, PRICE, CAPACITY FROM CARS C 
                    INNER JOIN BOOKINGS B ON C.CAR_ID = B.CAR_ID
                    GROUP BY MODEL
                    ORDER BY COUNT(B.CAR_ID)
                    '''
                )
                most_popular = self.cursor.fetchone()

                self.cursor.execute(
                    '''SELECT AVG(SCORE) FROM RATINGS
                    WHERE RATING_DATE <= DATE('now') AND DATE(RATING_DATE) >= DATE('now','-7 day')
                    '''
                )
                average_rating = self.cursor.fetchone()[0]
                report_data = {
                    "Total Revenue:": f"RM{revenue if revenue else 0:.2f}",
                    "Total Paid Rentals:": f"{rental_count}",
                    f"Percentage Change in Revenue from {time_option}:": f"{percent_change:.2f}%",
                    "Average Ratings:": f"{average_rating if average_rating else 0:.1f}/5",
                    "Most Popular Car:": most_popular[0]
                }
            case "Past Month":
                # List of sections to be printed in the report
                self.cursor.execute(
                    '''SELECT SUM(TOTAL_CHARGE) FROM BOOKINGS B 
                    INNER JOIN PAYMENTS P ON P.BOOKING_ID = B.BOOKING_ID
                    WHERE DATE(P.DATE_PAID) <= DATE('now') AND DATE(P.DATE_PAID) >= DATE('now','-1 month')
                    '''
                )
                revenue = self.cursor.fetchone()[0]
                self.cursor.execute(
                    '''SELECT COUNT(B.BOOKING_ID) FROM BOOKINGS B 
                    INNER JOIN PAYMENTS P ON P.BOOKING_ID = B.BOOKING_ID
                    WHERE DATE(P.DATE_PAID) <= DATE('now') AND DATE(P.DATE_PAID) >= DATE('now','-1 month')
                    '''
                )
                rental_count = self.cursor.fetchone()[0]
                self.cursor.execute(
                    '''SELECT SUM(TOTAL_CHARGE) FROM BOOKINGS B 
                    INNER JOIN PAYMENTS P ON P.BOOKING_ID = B.BOOKING_ID
                    WHERE DATE(P.DATE_PAID) <= DATE('now','-1 month') AND DATE(P.DATE_PAID) >= DATE('now','-2 month')
                    '''
                )
                percent_change = self.cursor.fetchone()[0]
                percent_change = (revenue - percent_change) / percent_change if percent_change else 0

                self.cursor.execute(
                    '''SELECT MODEL, IMAGE, MANUFACTURER_YEAR, TRANSMISSION, PRICE, CAPACITY FROM CARS C 
                    INNER JOIN BOOKINGS B ON C.CAR_ID = B.CAR_ID
                    GROUP BY MODEL
                    ORDER BY COUNT(B.CAR_ID)
                    '''
                )
                most_popular = self.cursor.fetchone()

                self.cursor.execute(
                    '''SELECT AVG(SCORE) FROM RATINGS
                    WHERE RATING_DATE <= DATE('now') AND DATE(RATING_DATE) >= DATE('now','-1 month')
                    '''
                )
                average_rating = self.cursor.fetchone()[0]
                report_data = {
                    "Total Revenue:": f"RM{revenue if revenue else 0:.2f}",
                    "Total Paid Rentals:": f"{rental_count}",
                    f"Percentage Change in Revenue from {time_option}:": f"{percent_change:.2f}%",
                    "Average Ratings:": f"{average_rating if average_rating else 0:.1f}/5",
                    "Most Popular Car:": most_popular[0]
                }

            case "Past Year":
                # List of sections to be printed in the report
                self.cursor.execute(
                    '''SELECT SUM(TOTAL_CHARGE) FROM BOOKINGS B 
                    INNER JOIN PAYMENTS P ON P.BOOKING_ID = B.BOOKING_ID
                    WHERE DATE(P.DATE_PAID) <= DATE('now') AND DATE(P.DATE_PAID) >= DATE('now','-1 year')
                    '''
                )
                revenue = self.cursor.fetchone()[0]
                self.cursor.execute(
                    '''SELECT COUNT(B.BOOKING_ID) FROM BOOKINGS B 
                    INNER JOIN PAYMENTS P ON P.BOOKING_ID = B.BOOKING_ID
                    WHERE DATE(P.DATE_PAID) <= DATE('now') AND DATE(P.DATE_PAID) >= DATE('now','-1 year')
                    '''
                )
                rental_count = self.cursor.fetchone()[0]
                self.cursor.execute(
                    '''SELECT SUM(TOTAL_CHARGE) FROM BOOKINGS B 
                    INNER JOIN PAYMENTS P ON P.BOOKING_ID = B.BOOKING_ID
                    WHERE DATE(P.DATE_PAID) <= DATE('now','-1 year') AND DATE(P.DATE_PAID) >= DATE('now','-2 year')
                    '''
                )
                percent_change = self.cursor.fetchone()[0]
                percent_change = (revenue - percent_change) / percent_change if percent_change else 0

                self.cursor.execute(
                    '''SELECT MODEL, IMAGE, MANUFACTURER_YEAR, TRANSMISSION, PRICE, CAPACITY FROM CARS C 
                    INNER JOIN BOOKINGS B ON C.CAR_ID = B.CAR_ID
                    GROUP BY MODEL
                    ORDER BY COUNT(B.CAR_ID)
                    '''
                )
                most_popular = self.cursor.fetchone()

                self.cursor.execute(
                    '''SELECT AVG(SCORE) FROM RATINGS
                    WHERE RATING_DATE <= DATE('now') AND DATE(RATING_DATE) >= DATE('now','-1 year')
                    '''
                )
                average_rating = self.cursor.fetchone()[0]
                report_data = {
                    "Total Revenue:": f"RM{revenue if revenue else 0:.2f}",
                    "Total Paid Rentals:": f"{rental_count}",
                    f"Percentage Change in Revenue from {time_option}:": f"{percent_change:.2f}%",
                    "Average Ratings:": f"{average_rating if average_rating else 0:.1f}/5",
                    "Most Popular Car:": most_popular[0]
                }

        # Loop through the report data and add it to the PDF
        for section, value in report_data.items():
            c.drawString(60, y_position, section)
            c.drawString(380, y_position, value)
            y_position -= 20  # Adjust for next line

            # Draw the image of the car (replace 'car_image_path' with the actual path of the car image)
            y2_position = 500
            pil_image = img.open(f"assets/cars/{most_popular[1]}")
            c.drawImage(f"assets/cars/{most_popular[1]}", 100, y2_position, width=200,
                        height=200 * pil_image.size[1] / pil_image.size[0])  # Adjust width and height as needed

            # Car information (for the single car)
            car_model = most_popular[0]
            car_year = most_popular[2]
            transmission = most_popular[3]
            car_price = most_popular[4]
            capacity = most_popular[5]

            # Set the x and y positions for the car info (to the right of the image)
            car_info_x = 320
            car_info_y = y2_position + 80  # Start below the image

            # Add car details next to the image
            c.drawString(car_info_x, car_info_y, f"Car Model: {car_model}")
            c.drawString(car_info_x, car_info_y - 15, f"Manufacture Year: {car_year}")
            c.drawString(car_info_x, car_info_y - 30, f"Transmission Type: {transmission}")
            c.drawString(car_info_x, car_info_y - 45, f"Price: RM{car_price:.2f}")
            c.drawString(car_info_x, car_info_y - 60, f"Capacity: {capacity} Passengers")

            # Save the PDF file
        c.save()
        messagebox.showinfo("PDF Generated", "Your Sales Report PDF was successfully generated")

    def manage_cars(self):
        for i in self.master.winfo_children():
            i.destroy()

        manage_car_ui = ctk.CTkImage(light_image=img.open("assets/manage car details ui.png"),
                                     size=(self.width, self.height - 68))
        manage_car_ui_label = ctk.CTkLabel(self.master, image=manage_car_ui, text="")
        manage_car_ui_label.place(x=0, y=0, anchor="nw")

        self.registration_number_entry = ctk.CTkEntry(self.master, width=363 / 1707 * self.width,
                                                 height=34 / 1067 * self.height,
                                                 bg_color="#F0F4FC",
                                                 fg_color="#D9D9D9",
                                                 border_color="#D9D9D9",
                                                 text_color="black",
                                                 font=("Poppins Light", 24))
        self.registration_number_entry.place(x=1041 / 1707 * self.width, y=143 / 1067 * self.height, anchor="nw")

        self.model_entry = ctk.CTkEntry(self.master, width=363 / 1707 * self.width,
                                   height=34 / 1067 * self.height,
                                   bg_color="#F0F4FC",
                                   fg_color="#D9D9D9",
                                   border_color="#D9D9D9",
                                   text_color="black",
                                   font=("Poppins Light", 24))
        self.model_entry.place(x=1041 / 1707 * self.width, y=189 / 1067 * self.height, anchor="nw")

        self.capacity_entry = ctk.CTkEntry(self.master, width=363 / 1707 * self.width,
                                      height=34 / 1067 * self.height,
                                      bg_color="#F0F4FC",
                                      fg_color="#D9D9D9",
                                      border_color="#D9D9D9",
                                      text_color="black",
                                      font=("Poppins Light", 24))
        self.capacity_entry.place(x=1041 / 1707 * self.width, y=234 / 1067 * self.height, anchor="nw")

        self.transmission_entry = ctk.CTkEntry(self.master, width=363 / 1707 * self.width,
                                          height=34 / 1067 * self.height,
                                          bg_color="#F0F4FC",
                                          fg_color="#D9D9D9",
                                          border_color="#D9D9D9",
                                          text_color="black",
                                          font=("Poppins Light", 24))
        self.transmission_entry.place(x=1041 / 1707 * self.width, y=279 / 1067 * self.height, anchor="nw")

        self.manufacture_year_entry = ctk.CTkEntry(self.master, width=363 / 1707 * self.width,
                                              height=34 / 1067 * self.height,
                                              bg_color="#F0F4FC",
                                              fg_color="#D9D9D9",
                                              border_color="#D9D9D9",
                                              text_color="black",
                                              font=("Poppins Light", 24))
        self.manufacture_year_entry.place(x=1041 / 1707 * self.width, y=325 / 1067 * self.height, anchor="nw")

        self.price_entry = ctk.CTkEntry(self.master, width=363 / 1707 * self.width,
                                   height=34 / 1067 * self.height,
                                   bg_color="#F0F4FC",
                                   fg_color="#D9D9D9",
                                   border_color="#D9D9D9",
                                   text_color="black",
                                   font=("Poppins Light", 24))
        self.price_entry.place(x=1041 / 1707 * self.width, y=371 / 1067 * self.height, anchor="nw")

        self.image_display = ctk.CTkLabel(self.master, width=494 / 1707 * self.width,
                                     height=358 / 1067 * self.height,
                                     text="",
                                     bg_color="#F0F4FC",
                                     fg_color="#FFFFFF",
                                     corner_radius=9)
        self.image_display.place(x=208 / 1707 * self.width, y=144 / 1067 * self.height, anchor="nw")

        insert_image_btn = ctk.CTkButton(self.master, width=208 / 1707 * self.width,
                                         height=45.39 / 1067 * self.height,
                                         bg_color="#F0F4FC",
                                         fg_color="#1572D3",
                                         text="Insert Image",
                                         text_color="#FFFFFF",
                                         font=("Poppins", 24),
                                         command=lambda:self.manage_car_button("insert")
                                         )
        insert_image_btn.place(x=783 / 1707 * self.width, y=417 / 1067 * self.height, anchor="nw")

        save_btn = ctk.CTkButton(self.master, width=150 / 1707 * self.width,
                                 height=58 / 1067 * self.height,
                                 bg_color="#F0F4FC",
                                 fg_color="#1572D3",
                                 text="Save",
                                 text_color="#FFFFFF",
                                 font=("Poppins", 24),
                                 command=lambda:self.manage_car_button("save")
                                 )
        save_btn.place(x=783 / 1707 * self.width, y=488 / 1067 * self.height, anchor="nw")

        update_btn = ctk.CTkButton(self.master, width=150 / 1707 * self.width,
                                   height=58 / 1067 * self.height,
                                   bg_color="#F0F4FC",
                                   fg_color="#1572D3",
                                   text="Update",
                                   text_color="#FFFFFF",
                                   font=("Poppins", 24),
                                   command=lambda:self.manage_car_button("update")
                                 )
        update_btn.place(x=955 / 1707 * self.width, y=488 / 1067 * self.height, anchor="nw")

        delete_btn = ctk.CTkButton(self.master, width=150 / 1707 * self.width,
                                   height=58 / 1067 * self.height,
                                   bg_color="#F0F4FC",
                                   fg_color="#1572D3",
                                   text="Delete",
                                   text_color="#FFFFFF",
                                   font=("Poppins", 24),
                                   command=lambda:self.manage_car_button("delete")
                                 )
        delete_btn.place(x=1127 / 1707 * self.width, y=488 / 1067 * self.height, anchor="nw")

        clear_btn = ctk.CTkButton(self.master, width=150 / 1707 * self.width,
                                  height=58 / 1067 * self.height,
                                  bg_color="#F0F4FC",
                                  fg_color="#1572D3",
                                  text="Clear",
                                  text_color="#FFFFFF",
                                  font=("Poppins", 24),
                                  command=lambda:self.manage_car_button("clear")
                                 )
        clear_btn.place(x=1299 / 1707 * self.width, y=488 / 1067 * self.height, anchor="nw")

        # Back Button
        back_button = ctk.CTkButton(
            self.master, text="Back", bg_color="white", fg_color="#1572D3",
            text_color="white",
            border_color="#1572D3", width=89 / 1280 * self.width,
            height=39 / 720 * self.height, font=("Poppins Medium", 18 / 1536 * self.width),
            command=self.admin_home
        )
        back_button.place(x=45 / 1280 * self.width, y=588 / 720 * self.height)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Poppins Medium", 18), rowheight=30, background="#FFFFFF")
        style.configure("Treeview", font=("Poppins", 16), rowheight=32)
        frame = ctk.CTkFrame(self.master)
        frame.place(x=260/1536*self.width,y=480/864*self.height)
        self.car_treeview = ttk.Treeview(frame, columns=(
        "ID", "Registration Number", "Manufacturer Year", "Model", "Price", "Capacity", "Transmission"), show="headings")
        self.car_treeview.pack()
        self.car_treeview.bind("<<TreeviewSelect>>", self.select_car)

        self.car_treeview.heading("ID", text="ID")
        self.car_treeview.column("ID", width=100, anchor="center")
        self.car_treeview.heading("Manufacturer Year", text="Manufacturer Year")
        self.car_treeview.column("Manufacturer Year", width=200, anchor="center")
        self.car_treeview.heading("Registration Number", text="Registration Number")
        self.car_treeview.column("Registration Number", width=300, anchor="center")
        self.car_treeview.heading("Model", text="Model")
        self.car_treeview.column("Model", width=200, anchor="center")
        self.car_treeview.heading("Price", text="Price (RM)")
        self.car_treeview.column("Price", width=150, anchor="center")
        self.car_treeview.heading("Capacity", text="Capacity")
        self.car_treeview.column("Capacity", width=150, anchor="center")
        self.car_treeview.heading("Transmission", text="Transmission")
        self.car_treeview.column("Transmission", width=200, anchor="center")

        #insert all current car values
        self.cursor.execute("SELECT CAR_ID, PLATE_NUMBER, MANUFACTURER_YEAR, MODEL, PRICE, CAPACITY, TRANSMISSION FROM CARS")
        for i in self.cursor.fetchall():
            # print(i)
            self.car_treeview.insert("","end",values=i)

    def select_car(self, event):
        selected_item = self.car_treeview.selection()
        if selected_item:
            item = self.car_treeview.item(selected_item)
            values = item['values']
            self.selected_car_id = values[0]

            self.cursor.execute(f'SELECT * FROM CARS WHERE CAR_ID = {self.selected_car_id}')
            car_data = self.cursor.fetchone()

            if car_data:
                self.registration_number_entry.delete(0, 'end')
                self.registration_number_entry.insert(0, car_data[8])
                self.model_entry.delete(0, 'end')
                self.model_entry.insert(0, car_data[2])
                self.capacity_entry.delete(0, 'end')
                self.capacity_entry.insert(0, car_data[5])
                self.transmission_entry.delete(0, 'end')
                self.transmission_entry.insert(0, car_data[7])
                self.manufacture_year_entry.delete(0, 'end')
                self.manufacture_year_entry.insert(0, car_data[1])
                self.price_entry.delete(0, 'end')
                self.price_entry.insert(0, car_data[3])

                image_path = car_data[4]
                if image_path:
                    try:
                        pil_image = img.open("assets/cars/"+image_path)
                        car_image = ctk.CTkImage(light_image=pil_image,
                                           size=((200*pil_image.size[0]/pil_image.size[1]) / 1707 * self.width, 200 / 1067 * self.height))
                        self.image_display.configure(image=car_image)
                        self.image_display.image = car_image

                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to load image: {e}")

    def manage_car_button(self,button):
        match button:
            case "insert":
                self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
                if self.image_path:
                    try:
                        new_image = ctk.CTkImage(light_image=img.open(self.image_path),
                                           size=(450 / 1707 * self.width, 300 / 1067 * self.height))
                        self.image_display.configure(image=new_image)
                        self.image_display.image = new_image

                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to load image: {e}")
            case "save":
                registration_number = self.registration_number_entry.get()
                model = self.model_entry.get()
                capacity = self.capacity_entry.get()
                transmission = self.transmission_entry.get()
                manufacture_year = self.manufacture_year_entry.get()
                price = self.price_entry.get()
                if not self.image_path:
                    messagebox.showwarning("Warning", "Please upload an image.")
                    return

                self.cursor.execute(f'SELECT * FROM CARS WHERE PLATE_NUMBER = \'{registration_number}\'')
                if self.cursor.fetchone():
                    messagebox.showwarning("Warning", "This registration number already exists.")
                    return

                self.cursor.execute(''' 
                            INSERT INTO cars (PLATE_NUMBER, MODEL, CAPACITY, TRANSMISSION, MANUFACTURER_YEAR, PRICE, IMAGE, RATING)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (registration_number, model, capacity, transmission, manufacture_year, price, os.path.basename(self.image_path), 0))
                self.sqliteConnection.commit()

                pil_image = img.open(self.image_path)
                pil_image.save("assets/cars/"+os.path.basename(self.image_path))

                messagebox.showinfo("Success", "Data saved successfully!")
                self.manage_car_button("refresh")
            case "update":
                if self.selected_car_id is not None:
                    registration_number = self.registration_number_entry.get()
                    model = self.model_entry.get()
                    capacity = self.capacity_entry.get()
                    transmission = self.transmission_entry.get()
                    manufacture_year = self.manufacture_year_entry.get()
                    price = self.price_entry.get()

                    self.cursor.execute(''' 
                               UPDATE CARS 
                               SET PLATE_NUMBER = ?, MODEL = ?, CAPACITY = ?, TRANSMISSION = ?, MANUFACTURER_YEAR = ?, PRICE = ?
                               WHERE CAR_ID = ?
                           ''', (registration_number, model, capacity, transmission, manufacture_year, price, self.selected_car_id))
                    self.sqliteConnection.commit()
                    messagebox.showinfo("Success", "Car updated successfully!")
                    self.manage_car_button("refresh")
                    self.manage_car_button("clear")
                else:
                    messagebox.showwarning("Warning", "Please select a car to update.")
            case "delete":
                if self.selected_car_id is not None:
                    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this car?")
                    if confirm:
                        self.cursor.execute('DELETE FROM CARS WHERE CAR_ID = ?', (self.selected_car_id,))
                        self.sqliteConnection.commit()
                        messagebox.showinfo("Success", "Car deleted successfully!")
                        self.manage_car_button("refresh")
                        self.manage_car_button("clear")
                else:
                    messagebox.showwarning("Warning", "Please select a car to delete.")
            case "clear":
                self.selected_car_id = None
                self.registration_number_entry.delete(0, 'end')
                self.model_entry.delete(0, 'end')
                self.capacity_entry.delete(0, 'end')
                self.transmission_entry.delete(0, 'end')
                self.manufacture_year_entry.delete(0, 'end')
                self.price_entry.delete(0, 'end')
                self.image_display.configure(image="")
            case "refresh":
                for row in self.car_treeview.get_children():
                    self.car_treeview.delete(row)

                self.cursor.execute(
                    'SELECT CAR_ID, PLATE_NUMBER, MODEL, CAPACITY, TRANSMISSION, MANUFACTURER_YEAR, PRICE FROM CARS')
                rows = self.cursor.fetchall()

                for row in rows:
                    self.car_treeview.insert("", "end", values=row)


    def manage_bookings(self):
        # Background Image
        background_image = ctk.CTkImage(img.open("assets/manage bookings ui.png"),
                                        size=(self.width, self.height - 64))
        background_image_label = ctk.CTkLabel(master=self.master.master, image=background_image, text="")
        background_image_label.place(relx=0, rely=0)

        # Left Box

        # Booking ID
        self.book_entry = ctk.CTkEntry(self.master, width=217 / 1280 * self.width,
                                  height=34 / 720 * self.height, bg_color="white",
                                  fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black",state="disabled")
        self.book_entry.place(x=351 / 1280 * self.width, y=75 / 720 * self.height)

        # Customer Name
        self.name_entry = ctk.CTkEntry(self.master, width=217 / 1280 * self.width,
                                  height=34 / 720 * self.height, bg_color="white",
                                  fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black",state="disabled")
        self.name_entry.place(x=351 / 1280 * self.width, y=115 / 720 * self.height)

        # location
        self.location_entry = ctk.CTkEntry(self.master, width=217 / 1280 * self.width,
                                     height=34 / 720 * self.height, bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black",state="disabled")
        self.location_entry.place(x=351 / 1280 * self.width, y=154 / 720 * self.height)

        # Start Date
        self.start_entry = ctk.CTkEntry(self.master, width=217 / 1280 * self.width,
                                   height=34 / 720 * self.height, bg_color="white",
                                   fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black",state="disabled")
        self.start_entry.place(x=351 / 1280 * self.width, y=193 / 720 * self.height)

        # End Date
        self.end_entry = ctk.CTkEntry(self.master, width=217 / 1280 * self.width,
                                 height=34 / 720 * self.height, bg_color="white",
                                 fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black",state="disabled")
        self.end_entry.place(x=351 / 1280 * self.width, y=233 / 720 * self.height)

        # Approved Button
        self.app_button = ctk.CTkButton(self.master, text="Approve", bg_color="white", fg_color="#1572D3",
                                   text_color="white",
                                   border_color="#1572D3", width=87 / 1280 * self.width, height=32 / 588 * self.height,
                                   font=("Poppins Medium", 18), command=lambda : self.confirm_booking("approve"))
        self.app_button.place(x=541 / 1280 * self.width, y=328 / 720 * self.height)

        # Right Box

        # Model
        self.model_entry = ctk.CTkEntry(self.master, width=217 / 1280 * self.width,
                                   height=34 / 720 * self.height, bg_color="white",
                                   fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black",state="disabled")
        self.model_entry.place(x=972 / 1280 * self.width, y=75 / 720 * self.height)

        # Capacity
        self.capacity_entry = ctk.CTkEntry(self.master, width=217 / 1280 * self.width,
                                      height=34 / 720 * self.height, bg_color="white",
                                      fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black",state="disabled")
        self.capacity_entry.place(x=972 / 1280 * self.width, y=115 / 720 * self.height)

        # Transmission
        self.mission_entry = ctk.CTkEntry(self.master, width=217 / 1280 * self.width,
                                     height=34 / 720 * self.height, bg_color="white",
                                     fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black",state="disabled")
        self.mission_entry.place(x=972 / 1280 * self.width, y=154 / 720 * self.height)

        # Price
        self.price_entry = ctk.CTkEntry(self.master, width=217 / 1280 * self.width,
                                   height=34 / 720 * self.height, bg_color="white",
                                   fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black",state="disabled")
        self.price_entry.place(x=972 / 1280 * self.width, y=193 / 720 * self.height)

        # Status
        self.status_entry = ctk.CTkEntry(self.master, width=217 / 1280 * self.width,
                                    height=34 / 720 * self.height, bg_color="white",
                                    fg_color="#D9D9D9", border_color="#D9D9D9", text_color="black",state="disabled")
        self.status_entry.place(x=972 / 1280 * self.width, y=233 / 720 * self.height)

        # Reject Button
        self.reject_button = ctk.CTkButton(self.master, text="Reject", bg_color="white", fg_color="#1572D3",
                                      text_color="white",
                                      border_color="#1572D3", width=87 / 1280 * self.width,
                                      height=32 / 588 * self.height,
                                      font=("Poppins Medium", 18), command=lambda : self.confirm_booking("reject"))
        self.reject_button.place(x=669 / 1280 * self.width, y=328 / 720 * self.height)

        # Back Button
        back_button = ctk.CTkButton(
            self.master, text="Back", bg_color="white", fg_color="#1572D3",
            text_color="white",
            border_color="#1572D3", width=89 / 1280 * self.width,
            height=39 / 720 * self.height, font=("Poppins Medium", 18 / 1536 * self.width),
            command=self.admin_home
        )
        back_button.place(x=45 / 1280 * self.width, y=588 / 720 * self.height)

        # Treeview

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Poppins Medium", 18), rowheight=100)
        style.configure("Treeview", font=("Poppins", 16), rowheight=32 )
        frame = ctk.CTkFrame(self.master)
        frame.place(x=260 / 1536 * self.width, y=480 / 864 * self.height)
        self.booking_treeview = ttk.Treeview(frame, columns=("ID", "Customer Name","Start Date", "End Date", "Model", "Location", "Charge", "Status"),
                                show="headings")

        self.booking_treeview.heading("ID", text="ID")
        self.booking_treeview.column("ID", width=80, anchor="center")

        self.booking_treeview.heading("Customer Name", text="Customer Name")
        self.booking_treeview.column("Customer Name", width=300, anchor="center")

        self.booking_treeview.heading("Model", text="Model")
        self.booking_treeview.column("Model", width=150, anchor="center")

        self.booking_treeview.heading("Location", text="Location")
        self.booking_treeview.column("Location", width=200, anchor="center")

        self.booking_treeview.heading("Charge", text="Charge")
        self.booking_treeview.column("Charge", width=150, anchor="center")

        self.booking_treeview.heading("Start Date", text="Start Date")
        self.booking_treeview.column("Start Date", width=200, anchor="center")

        self.booking_treeview.heading("End Date", text="End Date")
        self.booking_treeview.column("End Date", width=200, anchor="center")

        self.booking_treeview.heading("Status", text="Status")
        self.booking_treeview.column("Status", width=150, anchor="center")

        self.booking_treeview.pack()#place(x=310, y=578, width=1453, height=365)

        self.booking_treeview.bind("<<TreeviewSelect>>", self.select_booking)

        # insert all current booking values
        self.cursor.execute(
            '''
            SELECT BOOKING_ID, CONCAT(FIRST_NAME,' ',LAST_NAME), START_DATE, END_DATE, MODEL, LOCATION, TOTAL_CHARGE, STATUS FROM BOOKINGS
            INNER JOIN USERS ON BOOKINGS.USER_ID = USERS.USER_ID
            INNER JOIN CARS ON BOOKINGS.CAR_ID = CARS.CAR_ID
            '''
        )
        for i in self.cursor.fetchall():
            displayed_data = list(i)
            # print(displayed_data)
            self.booking_treeview.insert("", "end", values=displayed_data)

    def select_booking(self,event):
        self.selected_booking = self.booking_treeview.selection()
        if self.selected_booking:
            item_values = self.booking_treeview.item(self.selected_booking, "values")

            self.cursor.execute(f'''SELECT * FROM CARS 
                                INNER JOIN BOOKINGS
                                ON BOOKINGS.CAR_ID = CARS.CAR_ID
                                WHERE BOOKINGS.BOOKING_ID = {item_values[0]}''')
            car_data = self.cursor.fetchone()

            self.name_entry.configure(state="normal")
            self.name_entry.delete(0, 'end')
            self.name_entry.insert(0, item_values[1])
            self.name_entry.configure(state="disabled")

            self.start_entry.configure(state="normal")
            self.start_entry.delete(0, 'end')
            self.start_entry.insert(0, item_values[2])
            self.start_entry.configure(state="disabled")

            self.end_entry.configure(state="normal")
            self.end_entry.delete(0, 'end')
            self.end_entry.insert(0, item_values[3])
            self.end_entry.configure(state="disabled")

            self.book_entry.configure(state="normal")
            self.book_entry.delete(0, 'end')
            self.book_entry.insert(0, item_values[0])
            self.book_entry.configure(state="disabled")

            self.mission_entry.configure(state="normal")
            self.mission_entry.delete(0, 'end')
            self.mission_entry.insert(0, car_data[7])
            self.mission_entry.configure(state="disabled")

            self.capacity_entry.configure(state="normal")
            self.capacity_entry.delete(0, 'end')
            self.capacity_entry.insert(0, car_data[5])
            self.capacity_entry.configure(state="disabled")

            self.status_entry.configure(state="normal")
            self.status_entry.delete(0, 'end')
            self.status_entry.insert(0, item_values[7])
            self.status_entry.configure(state="disabled")

            self.model_entry.configure(state="normal")
            self.model_entry.delete(0, 'end')
            self.model_entry.insert(0, item_values[4])
            self.model_entry.configure(state="disabled")

            self.location_entry.configure(state="normal")
            self.location_entry.delete(0, 'end')
            self.location_entry.insert(0, item_values[5])
            self.location_entry.configure(state="disabled")

            self.price_entry.configure(state="normal")
            self.price_entry.delete(0, 'end')
            self.price_entry.insert(0, item_values[6])
            self.price_entry.configure(state="disabled")

            if item_values[7]=="Pending":
                self.app_button.configure(state="normal")
                self.reject_button.configure(state="normal")
            elif item_values[7]=="Approved":
                self.app_button.configure(state="disabled")
                self.reject_button.configure(state="normal")
            elif item_values[7]=="Paid":
                self.app_button.configure(state="disabled")
                self.reject_button.configure(state="disabled")
            else:
                self.app_button.configure(state="disabled")
                self.reject_button.configure(state="disabled")

    def confirm_booking(self, mode):
        item_values = self.booking_treeview.item(self.selected_booking, "values")
        self.status_entry.configure(state="normal")
        self.status_entry.delete(0, 'end')
        self.status_entry.configure(state="disabled")
        msg = MIMEMultipart("alternative")

        if mode=="approve":
            self.cursor.execute("UPDATE BOOKINGS SET STATUS = 'Approved' WHERE BOOKING_ID = ?", item_values[0])
            messagebox.showinfo("Approved","Booking approved. Confirmation email sent")
            self.status_entry.insert(0, "Approved")

            msg['Subject'] = 'Your DriveEase Booking Has Been Approved!'

            with open("assets/HTML/BookingApprovalEmail.html", "r") as file:
                html_content = file.read()
        else:
            self.cursor.execute("UPDATE BOOKINGS SET STATUS = 'Rejected', CURRENT_BOOKING = 0 WHERE BOOKING_ID = ?", item_values[0])
            messagebox.showinfo("Rejected", "Booking rejected. Rejection email sent")
            self.status_entry.insert(0, "Rejected")

            msg['Subject'] = 'Your DriveEase Booking Has Been Rejected'
            with open("assets/HTML/BookingRejectionEmail.html", "r") as file:
                html_content = file.read()

        html_content = html_content.replace("car model", item_values[4])
        html_content = html_content.replace("start date", item_values[2])
        html_content = html_content.replace("end date", item_values[3])

        html_part = MIMEText(html_content, "html")
        msg.attach(html_part)

        self.cursor.execute(
            f"SELECT EMAIL FROM USERS U INNER JOIN BOOKINGS B ON B.USER_ID = U.USER_ID WHERE B.BOOKING_ID = {item_values[0]}")
        user_email = self.cursor.fetchone()[0]

        msg['From'] = "driveease3@gmail.com"
        msg['To'] = user_email

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("driveease3@gmail.com", "pskq ccbv rqvb jrwf")
        s.send_message(msg)
        s.quit()

        self.sqliteConnection.commit()

        for row in self.booking_treeview.get_children():
            self.booking_treeview.delete(row)

        self.cursor.execute(
            '''
            SELECT BOOKING_ID, CONCAT(FIRST_NAME,' ',LAST_NAME), START_DATE, END_DATE, MODEL, LOCATION, TOTAL_CHARGE, STATUS FROM BOOKINGS
            INNER JOIN USERS ON BOOKINGS.USER_ID = USERS.USER_ID
            INNER JOIN CARS ON BOOKINGS.CAR_ID = CARS.CAR_ID
            '''
        )
        for i in self.cursor.fetchall():
            self.booking_treeview.insert("", "end", values=i)

        if mode=="approve":
            self.app_button.configure(state="disabled")
            self.reject_button.configure(state="normal")
        elif mode=="reject":
            self.app_button.configure(state="disabled")
            self.reject_button.configure(state="disabled")