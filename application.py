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

        for F in {loginFrame, questionaireFrame, menuFrame, loadingFrame, recipeFrame}:
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("loginFrame")

    def show_frame(self, name, recipe=None):
        frame = self.frames[name]
        if name=="loginFrame":
            self.loggedIn = -1
        if name=="questionaireFrame":
            frame.updateGreeting()
        if name=="menuFrame":
            frame.updateRecipes()
        if name=="recipeFrame":
            frame.updateRecipe(recipe)
        frame.tkraise()

    def loginUser(self, user):
        self.frames["loadingFrame"].tkraise()
        self.loggedIn = GCloudSql.login(user)
        print("Logged In " + user)
        if(self.loggedIn[1] == None):
            self.show_frame("questionaireFrame")
        else:
            self.show_frame("menuFrame")
    
    def loadRecipe(self, recipe):
        r = str(recipe).split(",")
        print(r[1])
        r = list(GCloudSql.getRecipeByName(r[1]))
        user = self.loggedIn[0]
        tags = r[4].split(",")
        for tag in tags:
            GCloudSql.addScore(user, tag, 10)
        self.show_frame("recipeFrame", recipe=r)




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
        self.controller.show_frame("loadingFrame")
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
        self.i = 1 # iterations of updateRecipes
        self.recipes = []
        self.recipeBttons = list()
        self.iteratebtn= tk.Button(self, text="More Suggestions", font=controller.titleFont)
        self.Title = tk.Label(self,text="Our Suggested Recipes:", font=self.controller.titleFont)
    

    def updateRecipes(self, i=1):
        self.i = i
        print(i)
        self.recipes = GCloudSql.get_recipes()
        luser = str(self.controller.loggedIn[0])
        self.recipes = GCloudSql.filterResults(luser ,self.recipes)
        canv = tk.Canvas(self)
        canv.pack(anchor=tk.CENTER, side=tk.TOP)
        self.Title = tk.Label(canv,text="Our Suggested Recipes:", font=self.controller.titleFont)
        self.Title.pack(anchor=tk.N, side=tk.TOP, pady=10)
        for b in self.recipeBttons:
            b.destroy()
        
        self.recipeBttons = list()
        counter = 1*i
        for recipe in self.recipes:
            if(counter>=11)*i:
                break
            bttn = tk.Button(canv, text=recipe[1], font=self.controller.bodyFont, command= lambda r=recipe:self.controller.loadRecipe(r))
            bttn.pack(anchor=tk.N, side=tk.TOP, padx=(2,5), pady=5)
            self.recipeBttons.append(bttn)
            counter+=1
        self.iteratebtn.pack(anchor=tk.N, side=tk.TOP, pady=10)
    
    def nextIter(self):
        self.updateRecipes(self.i+1)

class loadingFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        canv = tk.Canvas(self)
        canv.pack(anchor=tk.CENTER)
        tk.Label(canv, text="Loading...", font=controller.titleFont).pack(anchor=tk.CENTER)

class recipeFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        canv = tk.Canvas(self)
        canv.pack(anchor=tk.N, side=tk.TOP)
        self.recipeName = tk.Label(canv, text="title", font=controller.titleFont)
        self.recipeName.pack(side=tk.TOP, pady=4)
        tk.Label(canv, text="Ingredients", font=controller.bodyFont, wraplength=700).pack(side=tk.TOP)
        self.recipeIng = tk.Label(canv, text=" ingredients", font=controller.smallFont)
        self.recipeIng.pack(side=tk.TOP, pady=5)
        tk.Label(canv, text="Instructions", font=controller.bodyFont, wraplength=700).pack(side=tk.TOP, pady=5)
        self.Instructions = tk.Label(canv, text=" inst ", font=controller.smallFont)
        self.Instructions.pack(side=tk.TOP, pady=5)
    
    def updateRecipe(self, recipe):
        self.recipeName.configure(text=recipe[1], wraplength=700)
        self.recipeIng.configure(text=recipe[3], wraplength=700)
        self.Instructions.configure(text=recipe[2], wraplength=700)