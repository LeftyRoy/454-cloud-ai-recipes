import GCloudSql
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox

class mainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.titleFont = tkfont.Font(family="Helvetica", size="18", weight="bold")
        self.bodyFont = tkfont.Font(family="Helvetica", size="14", weight="bold")
        self.smallFont = tkfont.Font(family="Helvetica", size="12")
        self.loggedIn = " "
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = dict() # dict of empty frames

        for F in {loginFrame, questionaireFrame, menuFrame}:
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("loginFrame")

    def show_frame(self, name):
        frame = self.frames[name]
        if name=="loginFrame":
            self.loggedIn = -1
        if name=="questionaireFrame":
            frame.updateGreeting()
        if name=="menuFrame":
            frame.updateRecipes()
        frame.tkraise()

    def loginUser(self, user):
        self.loggedIn = GCloudSql.login(user)
        print("Logged In " + user)
        if(self.loggedIn[1] == None):
            self.show_frame("questionaireFrame")
        else:
            self.show_frame("menuFrame")


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
        canvas = tk.Canvas(self)
        canvas.pack(anchor=tk.N, side=tk.TOP, pady=10)
        canvasBody = tk.Canvas(self)
        canvasBody.pack(anchor=tk.N, side=tk.TOP, pady=(5,0))
        self.greetingLbl = tk.Label(canvas,text="Hello", font=controller.titleFont)
        self.greetingLbl.pack(anchor=tk.N)
        tk.Label(canvas,text="We see that you are new here!", font=controller.smallFont).pack(anchor=tk.N, side=tk.TOP)
        tk.Label(canvasBody,text="Are you: ", font=controller.smallFont).pack(anchor=tk.N, side=tk.TOP)
        self.isVegan = tk.IntVar()
        tk.Checkbutton(canvasBody, text="Vegan", variable=self.isVegan, font=controller.smallFont).pack(anchor=tk.N, side=tk.TOP)
        self.isVegetarian = tk.IntVar()
        tk.Checkbutton(canvasBody, text="Vegetarian", variable=self.isVegetarian, font=controller.smallFont).pack(anchor=tk.N, side=tk.TOP)
        tk.Label(canvasBody,text="Any Allergies? Check all the apply. ", font=controller.smallFont).pack(anchor=tk.N, side=tk.TOP, pady=(100,10))
        self.cheese = tk.IntVar()
        tk.Checkbutton(canvasBody, text="Cheese", variable=self.cheese, font=controller.smallFont).pack(anchor=tk.N, side=tk.TOP)
        self.seafood = tk.IntVar()
        tk.Checkbutton(canvasBody, text="Seafood", variable=self.seafood, font=controller.smallFont).pack(anchor=tk.N, side=tk.TOP)
        self.alcohol = tk.IntVar()
        tk.Checkbutton(canvasBody, text="Alcohol", variable=self.alcohol, font=controller.smallFont).pack(anchor=tk.N, side=tk.TOP)
        tk.Button(canvasBody, text="Continue", font=self.controller.bodyFont, command = lambda: self.continuePressed()).pack(anchor=tk.N, side=tk.TOP, pady=(75,10))
    
    def updateGreeting(self):
        self.greetingLbl.configure(text="Hello " + self.controller.loggedIn[0] + "!")
    
    def continuePressed(self):
        luser = str(self.controller.loggedIn[0])
        GCloudSql.addScore(luser, "vegan", 100*self.isVegan.get())
        GCloudSql.addScore(luser, "vegetarian", 100*self.isVegetarian.get())

        GCloudSql.addScore(luser, "cheese", -100*self.cheese.get())
        GCloudSql.addScore(luser, "seafood", -100*self.seafood.get())
        GCloudSql.addScore(luser, "fish", -100*self.seafood.get())
        GCloudSql.addScore(luser, "shrimp", -100*self.seafood.get())
        GCloudSql.addScore(luser, "alcohol", -100*self.alcohol.get())

        self.controller.show_frame("menuFrame")

class menuFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.recipes = []
    

    def updateRecipes(self):
        self.recipes = GCloudSql.get_recipes()
        luser = str(self.controller.loggedIn[0])
        self.recipes = GCloudSql.filterResults(luser ,self.recipes)

        for k in self.recipes:
            print(k[0])