from tkinter import *

def login_enter(event):
    if event.keysym=="Return":
        test_credentials()

root = Tk()
root.title("Car Rental App")
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))
root.state("zoomed")
root.bind("<KeyRelease>",login_enter)

loginPage = Frame(root)
loginPage.place(relx=0.5,rely=0.45,anchor= CENTER)
#loginPage.bind("<KeyRelease>",LoginEnter)

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

#login button
def test_credentials():
    if username.get()=="Admin" and password.get()=="Admin@1234":
        print("Login successful")
        loginPage.place_forget()
loginButton = Button(loginPage, text="Login", command=test_credentials)
loginButton.pack()

root.mainloop()