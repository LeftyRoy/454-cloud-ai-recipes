import GCloudSql
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox

class mainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.titleFont = tkfont.Font(family="Helvetica", size="18", weight="bold")
        self.bodyFont = tkfont.Font(family="Helvetica", size="14", weight="bold")
        self.loggedIn = -1
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = dict() # dict of empty frames

        for F in {loginFrame}:
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("loginFrame")

    def show_frame(self, name):
        frame = self.frames[name]
        if name=="mainMenu":
            frame.updateBalances()
        if name=="loginFrame":
            self.loggedIn = -1
        frame.tkraise()

    def loginUser(self, user):
        self.loggedIn = GCloudSql.login(user)
        print("Logged In " + user)
        if(self.loggedIn[1] == None):
            pass
        else:
            pass


class loginFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.selCanv = tk.Canvas(self) # canvas for select user options
        canv = tk.Canvas(self) # middle canvas
        canv.pack(anchor=tk.W, side=tk.RIGHT, padx=(0, 15))
        self.selCanv.pack(anchor=tk.W, side=tk.LEFT, padx=(15, 0))
        self.selectUserLabel = tk.Label(self.selCanv, text="Select a user: ", font=controller.titleFont)
        self.selectUserLabel.pack(anchor=tk.N, side=tk.TOP, padx=2, pady=5)
        createUserLabel = tk.Label(canv, text="Create a new user: ", font=controller.titleFont)
        createUserLabel.pack(anchor=tk.N, side=tk.TOP, padx=2, pady=5)
        userNameLabel = tk.Label(canv, text="Enter a Name: ", font=controller.bodyFont)
        userNameLabel.pack(anchor=tk.N, side=tk.TOP, padx=2, pady=5)
        self.uNameField = tk.Entry(canv, bd=5, justify=tk.CENTER)
        self.uNameField.pack(anchor=tk.N, side=tk.TOP, padx=2, pady=5)
        createButton = tk.Button(canv, text="Create", font=controller.titleFont, command=lambda: self.CreatePressed(self.uNameField.get()))
        createButton.pack(anchor=tk.N, side=tk.TOP, padx=2, pady=5)
        self.userBttns = list()
        self.updateUsers()
        
    def CreatePressed(self, name):
        if(len(name)<1):
            messagebox.showerror("ERROR", "Name too small")
            self.updateUsers()
            return
        if(GCloudSql.insert_name(name)):
            self.updateUsers()
            self.controller.loginUser(name)
        else:
            self.updateUsers()
            messagebox.showerror("ERROR", "This user already exists")


    def updateUsers(self):
        userList = GCloudSql.getAllUsers()
        if(len(userList)==0):
            self.selectUserLabel.configure(text="No Users Found")
        for user in self.userBttns:
            user.destroy()
        self.userBttns = list()
        for user in userList:
            userBtn = tk.Button(self.selCanv, text=str(user[0]), font=self.controller.bodyFont, command=lambda u=user[0]: self.controller.loginUser(u))
            userBtn.pack(anchor=tk.N, side=tk.TOP, padx=2, pady=5)
            self.userBttns.append(userBtn)

class questionaireFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.selCanv = tk.Canvas(self)