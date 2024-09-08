from tkinter import *
from tkinter import messagebox
import ttkbootstrap as ttk
import sqlite3 as sql

sqliteConnection = sql.connect(r"C:\Users\User\Documents\School\Databases\DriveEase.db")
cursor = sqliteConnection.cursor()

#possible states: login, register, home
state = "login"

def login_enter(event):
    if event.keysym=="Return":
        test_credentials()

def db_find_user(_username):
    query = f"SELECT * FROM USER WHERE USERNAME = \'{_username}\';"
    cursor.execute(query)
    return cursor.fetchall()

root = ttk.Window(themename="darkly")
root.title("Car Rental App")
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))
root.state("zoomed")
root.bind("<KeyRelease>",login_enter)

loginPage = Frame(root)
loginPage.place(relx=0.5,rely=0.45,anchor= CENTER)

loginLabel = Label(loginPage, text="Login to your account",font="Arial 24", pady="20")
loginLabel.pack()

#username stuff
username = StringVar()
usernameFrame = Frame(loginPage)
usernameLabel = Label(usernameFrame, text="Username: ")
usernameLabel.pack(side="left")
usernameEntry = Entry(usernameFrame, textvariable=username)
usernameEntry.pack(side="left")
usernameFrame.pack(anchor=CENTER)

#password stuff
password = StringVar()
passwordFrame = Frame(loginPage,pady="10")
passwordLabel = Label(passwordFrame, text="Password: ")
passwordLabel.pack(side="left")
passwordEntry = Entry(passwordFrame, show="*",textvariable=password)
passwordEntry.pack(side="left")
passwordFrame.pack(anchor=CENTER)

#login/register frame
loginButtonFrame = Frame(loginPage)

#login button
def test_credentials():
    query = f"SELECT * FROM USER WHERE USERNAME = \'{username.get()}\';"
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result):
        user = result[0]
        if user[3]==password.get():
            loginPage.place_forget()
        else: messagebox.showerror("Error", "Password is wrong")
    else:
        messagebox.showerror("Error", "Username doesn't exist")

loginButton = Button(loginButtonFrame, text="Login", command=test_credentials)
loginButton.pack(side="left",padx="5")

#register button
def enter_registration():
    loginPage.place_forget()
    registrationPage.place(relx=0.5,rely=0.45,anchor= CENTER)
registerButton = Button(loginButtonFrame, text="Register", command=enter_registration)
registerButton.pack(side="left",padx="5")
loginButtonFrame.pack()

#registration page
registrationPage = Frame(root)

registerLabel = Label(registrationPage,text="Register an account", font="Arial 24")
registerLabel.pack(anchor=CENTER)

newUsername = StringVar()
newUsernameFrame = Frame(registrationPage)
newUsernameLabel = Label(newUsernameFrame,text="Username: ")
newUsernameLabel.pack(anchor="w")
newUsernameEntry = Entry(newUsernameFrame, textvariable=newUsername)
newUsernameEntry.pack()
newUsernameFrame.pack(anchor="center")

newEmail = StringVar()
newEmailFrame = Frame(registrationPage)
newEmailLabel = Label(newEmailFrame,text="Email: ")
newEmailLabel.pack(anchor="w")
newEmailEntry = Entry(newEmailFrame,textvariable=newEmail)
newEmailEntry.pack()
newEmailFrame.pack(anchor="center")

newPassword = StringVar()
newPasswordFrame = Frame(registrationPage)
newPasswordLabel = Label(newPasswordFrame,text="Password: ")
newPasswordLabel.pack(anchor="w")
newPasswordEntry = Entry(newPasswordFrame, textvariable=newPassword)
newPasswordEntry.pack()
newPasswordFrame.pack(anchor="center")

confirmPassword = StringVar()
confirmPasswordFrame = Frame(registrationPage)
confirmPasswordLabel = Label(confirmPasswordFrame,text="Confirm Password: ")
confirmPasswordLabel.pack(anchor="w")
confirmPasswordEntry = Entry(confirmPasswordFrame, textvariable=confirmPassword)
confirmPasswordEntry.pack()
confirmPasswordFrame.pack(anchor="center")

#return to login/confirm register frame
registerButtonFrame = Frame(registrationPage)

#return to log in
def back_to_login():
    registrationPage.place_forget()
    loginPage.place(relx=0.5, rely=0.45, anchor=CENTER)
returnButton = Button(registerButtonFrame, text="Return to Login", command=back_to_login)
returnButton.pack(side="left",padx="5")

#register button
def confirm_registration():
    #check if all the details entered are valid or not
    error = ""
    result = db_find_user(newUsername.get())
    if len(newUsername.get())<8:
        error = "Username must be 8 characters minimum"
    elif len(result):
        error = "Username taken"
    elif not "@" in newEmail.get():
        error = "Email is invalid"
    elif len(newPassword.get())<8:
        error = "Password must be 8 characters minimum"
    elif not any(i.isdigit() for i in newPassword.get()):
        error = "Password must contain at least one digit"
    elif newPassword.get()!=confirmPassword.get():
        error = "Passwords do not match"

    if error :messagebox.showerror("Error", error)
    else:
        query = f"INSERT INTO USER (USERNAME, EMAIL, USER_PASSWORD) VALUES(\'{newUsername.get()}\',\'{newEmail.get()}\',\'{newPassword.get()}\')"
        cursor.execute(query)
        sqliteConnection.commit()


confirmRegistrationButton = Button(registerButtonFrame, text="Confirm", command=confirm_registration)
confirmRegistrationButton.pack(side="left",padx="5")
registerButtonFrame.pack(pady="10")

root.mainloop()