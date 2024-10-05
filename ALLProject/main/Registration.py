from tkinter import messagebox
import customtkinter as ctk

class RegistrationPage:
    def __init__(self, _root, _cursor, _connection):
        self.registrationPage = ctk.CTkFrame(_root)
        self.cursor = _cursor
        self.connection = _connection

        self.registerLabel = ctk.CTkLabel(self.registrationPage,text="Register an account", font=("Arial", 24))
        self.registerLabel.pack(anchor="center", pady="10")

        self.newUsername = ctk.StringVar()
        self.newUsernameFrame = ctk.CTkFrame(self.registrationPage)
        self.newUsernameLabel = ctk.CTkLabel(self.newUsernameFrame,text="Username: ")
        self.newUsernameLabel.pack(anchor="w")
        self.newUsernameEntry = ctk.CTkEntry(self.newUsernameFrame, textvariable=self.newUsername)
        self.newUsernameEntry.pack()
        self.newUsernameFrame.pack(anchor="center")

        self.newEmail = ctk.StringVar()
        self.newEmailFrame = ctk.CTkFrame(self.registrationPage)
        self.newEmailLabel = ctk.CTkLabel(self.newEmailFrame,text="Email: ")
        self.newEmailLabel.pack(anchor="w")
        self.newEmailEntry = ctk.CTkEntry(self.newEmailFrame,textvariable=self.newEmail)
        self.newEmailEntry.pack()
        self.newEmailFrame.pack(anchor="center")

        self.newPassword = ctk.StringVar()
        self.newPasswordFrame = ctk.CTkFrame(self.registrationPage)
        self.newPasswordLabel = ctk.CTkLabel(self.newPasswordFrame,text="Password: ")
        self.newPasswordLabel.pack(anchor="w")
        self.newPasswordEntry = ctk.CTkEntry(self.newPasswordFrame, textvariable=self.newPassword)
        self.newPasswordEntry.pack()
        self.newPasswordFrame.pack(anchor="center")

        self.confirmPassword = ctk.StringVar()
        self.confirmPasswordFrame = ctk.CTkFrame(self.registrationPage)
        self.confirmPasswordLabel = ctk.CTkLabel(self.confirmPasswordFrame,text="Confirm Password: ")
        self.confirmPasswordLabel.pack(anchor="w")
        self.confirmPasswordEntry = ctk.CTkEntry(self.confirmPasswordFrame, textvariable=self.confirmPassword)
        self.confirmPasswordEntry.pack()
        self.confirmPasswordFrame.pack(anchor="center")

        #return to login/confirm register frame
        self.registerButtonFrame = ctk.CTkFrame(self.registrationPage)
        self.returnButton = ctk.CTkButton(self.registerButtonFrame, text="Return to Login", command=self.deactivate)
        self.returnButton.pack(side="left", padx="5")
        self.confirmRegistrationButton = ctk.CTkButton(self.registerButtonFrame, text="Confirm", command=self.confirm_registration)
        self.confirmRegistrationButton.pack(side="left", padx="5")
        self.registerButtonFrame.pack(pady="10")

    #return to log in
    def deactivate(self):
        self.registrationPage.place_forget()
        # loginPage.place(relx=0.5, rely=0.45, anchor="center")

    def db_find_user(self, _username):
        query = f"SELECT * FROM USER WHERE USERNAME = \'{_username}\';"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    #register button
    def confirm_registration(self):
        #check if all the details entered are valid or not
        error = ""
        result = self.db_find_user(self.newUsername.get())
        if len(self.newUsername.get())<8:
            error = "Username must be 8 characters minimum"
        elif len(result):
            error = "Username taken"
        elif not "@" in self.newEmail.get():
            error = "Email is invalid"
        elif len(self.newPassword.get())<8:
            error = "Password must be 8 characters minimum"
        elif not any(i.isdigit() for i in self.newPassword.get()):
            error = "Password must contain at least one digit"
        elif self.newPassword.get()!=self.confirmPassword.get():
            error = "Passwords do not match"

        if error :messagebox.showerror("Error", error)
        else:
            query = f"INSERT INTO USER (USERNAME, EMAIL, USER_PASSWORD) VALUES(\'{self.newUsername.get()}\',\'{self.newEmail.get()}\',\'{self.newPassword.get()}\')"
            self.cursor.execute(query)
            self.connection.commit()