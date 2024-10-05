from tkinter import messagebox
import customtkinter as ctk

class LoginPage :
    def __init__(self, _root, _cursor):
        self.cursor = _cursor
        self.loginPage = ctk.CTkFrame(_root)
        self.loginPage.place(relx=0.5,rely=0.45,anchor= "center")

        self.loginLabel = ctk.CTkLabel(self.loginPage, text="Login to your account",font=("Arial", 24), pady="20")
        self.loginLabel.pack()

        #username stuff
        self.username = ctk.StringVar()
        self.usernameFrame = ctk.CTkFrame(self.loginPage)
        self.usernameLabel = ctk.CTkLabel(self.usernameFrame, text="Username: ")
        self.usernameLabel.pack(side="left")
        self.usernameEntry = ctk.CTkEntry(self.usernameFrame, textvariable=self.username)
        self.usernameEntry.pack(side="left")
        self.usernameFrame.pack(anchor="center")

        #password stuff
        self.password = ctk.StringVar()
        self.passwordFrame = ctk.CTkFrame(self.loginPage)
        self.passwordLabel = ctk.CTkLabel(self.passwordFrame, text="Password: ")
        self.passwordLabel.pack(side="left")
        self.passwordEntry = ctk.CTkEntry(self.passwordFrame, show="*",textvariable=self.password)
        self.passwordEntry.pack(side="left")
        self.passwordFrame.pack(anchor="center",pady="10")

        #login/register frame
        self.loginButtonFrame = ctk.CTkFrame(self.loginPage)
        self.loginButton = ctk.CTkButton(self.loginButtonFrame, text="Login", command=self.test_credentials)
        self.loginButton.pack(side="left",padx="5")
        self.registerButton = ctk.CTkButton(self.loginButtonFrame, text="Register", command=self.enter_registration)
        self.registerButton.pack(side="left", padx="5")
        self.loginButtonFrame.pack()

    def test_credentials(self):
        query = f"SELECT * FROM USER WHERE USERNAME = \'{self.username.get()}\';"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        if len(result):
            user = result[0]
            if user[3] == self.password.get():
                self.loginPage.place_forget()
            else:
                messagebox.showerror("Error", "Password is wrong")
        else:
            messagebox.showerror("Error", "Username doesn't exist")

    def enter_registration(self):
        self.loginPage.place_forget()
        #self.registrationPage.place(relx=0.5, rely=0.45, anchor="center")

    def deactivate(self):
        self.loginPage.place_forget()

    def activate(self):
        self.loginButton.pack(side="left",padx="5")