from tkinter import *
import os

class MainWindow(Frame):

    def __init__(self, window=None, keys=['q','w','e','r','f','d']):
        Frame.__init__(self, window)
        self.window = window
        self.keys = keys

        window.geometry("852x315+500+300")
        self.window.overrideredirect(True) #Override the title bar
        self.window.configure(bg = "#ffffff")

        self.canvas = Canvas(
            window,
            bg = "#ffffff",
            height = 315,
            width = 855,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        self.canvas.place(x = -1, y = 0)

        self.game_img = PhotoImage(file = f"./images/ui_images/game_img.png")
        self.game_btn = Button(
            image = self.game_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.startGameController,
            relief = "flat") 
        self.game_btn.place(
            x = 675, y = 209,
            width = 83,
            height = 36)

        self.webcam_img = PhotoImage(file = f"./images/ui_images/webcam_img.png")
        self.webcam_btn = Button(
            image = self.webcam_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.startWebcamEffects,
            relief = "flat")
        self.webcam_btn.place(
            x = 678, y = 104,
            width = 83,
            height = 36)

        self.rebind_img = PhotoImage(file = f"./images/ui_images/rebind_img.png")
        self.rebind_btn = Button(
            image = self.rebind_img,
            borderwidth = 0,
            command = self.openPopup,
            highlightthickness = 0,
            
            relief = "flat")
        self.rebind_btn.place(
            x = 170, y = 256,
            width = 63,
            height = 21)

        self.background_img = PhotoImage(file = f"./images/ui_images/background.png")
        self.background = self.canvas.create_image(
            266.5, 211.5,
            image=self.background_img)

        self.title_bar = Frame(window, bg="#292929", relief="raised", bd=0)
        self.title_bar.pack(side=TOP, fill=BOTH)
        self.title_bar.bind("<B1-Motion>", self.move_app)

        self.title_label = Label(self.title_bar, text="  SOCap  ", bg="#292929", fg="white")
        self.title_label.pack(side=LEFT, pady=2)

        self.close_label = Label(self.title_bar, text="  X  ", bg="#292929", fg="white", relief="sunken", bd=0)
        self.close_label.pack(side=RIGHT, pady=2)
        self.close_label.bind("<Button-1>", self.quitter)

    def startWebcamEffects(self):
        self.window.wm_attributes("-topmost", 0) #Ensure window is behind opencv window
        os.system("python ./Webcam/startWebcam.py")
        self.window.wm_attributes("-topmost", 1) #Bring window back to the front

    def startGameController(self):
        self.window.wm_attributes("-topmost", 0) #Ensure window is behind opencv window
        param_string = ''
        for i in self.keys:
            param_string += i + " "

        os.system(f"python ./Game/startGameController.py {param_string}") #Bring window back to the front
        self.window.wm_attributes("-topmost", 1)

    def move_app(self,e):
        self.window.geometry(f'+{e.x_root}+{e.y_root}')

    def quitter(self,e):
        self.window.quit()

    def openPopup(self):
        root2 = Toplevel()
        app2 = PopupWindow(root2, self)

class PopupWindow(Frame):
    
    def __init__(self,window=None,mainWindow=None, keys = ['q','w','e','r','f','d']):
        Frame.__init__(self,window)
        self.window = window
        
        self.mainWindow = mainWindow
        self.keys = keys
        self.window.geometry("300x250+900+350")     
        self.window.overrideredirect(True) #Override the title bar
        self.window.configure(bg = "#ffffff")
        self.canvas = Canvas(
            window,
            bg = "#ffffff",
            height = 250,
            width = 300,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        self.canvas.place(x = 0, y = 0)
        self.window.wm_attributes("-topmost", 1)
        self.popup_tbox = Entry(
            self.canvas,
            bd = 0,
            bg = "#cfcfcf",
            highlightthickness = 0)
        self.popup_tbox.place(
            x = 54.0, y = 182,
            width = 191.0,
            height = 37)
        self.popup_tbox.bind('<Return>', self.saveKeys)
            
        self.background_img = PhotoImage(file = f"./images/ui_images/popup_bg.png")
        self.background = self.canvas.create_image(
            159.5, 148.0,
            image=self.background_img)

        self.popup_box_img = PhotoImage(file = f"./images/ui_images/popup_box.png")
        self.popup_box_img = self.canvas.create_image(
            149.5, 201.5,
            image = self.popup_box_img)

        self.title_bar = Frame(window, bg="#292929", relief="raised", bd=0)
        self.title_bar.pack(side=TOP, fill=BOTH)
        self.title_bar.bind("<B1-Motion>", self.move_app)

        self.title_label = Label(self.title_bar, text="  SoCap  ", bg="#292929", fg="white")
        self.title_label.pack(side=LEFT, pady=2)

        self.close_label = Label(self.title_bar, text="  X  ", bg="#292929", fg="white", relief="sunken", bd=0)
        self.close_label.pack(side=RIGHT, pady=2)
        self.close_label.bind("<Button-1>", self.quitter)

    def saveKeys(self, event=None):
        new_key_list = []
        for i in self.popup_tbox.get():
            if i.isalnum():
                new_key_list.append(i)
        if len(new_key_list) == 6:
            self.mainWindow.keys = new_key_list        
        elif len(new_key_list) < 6:
            self.mainWindow.keys[:len(new_key_list)] = new_key_list
        elif len(new_key_list) > 6:
            self.mainWindow.keys = new_key_list[0:6]
        self.quitter(None)

    def move_app(self,e):
        self.window.geometry(f'+{e.x_root}+{e.y_root}')

    def quitter(self,e):
        self.window.destroy()

if __name__ == "__main__":
    window = Tk()

    main_window = MainWindow(window)
    window.resizable(False, False)
    window.mainloop()
