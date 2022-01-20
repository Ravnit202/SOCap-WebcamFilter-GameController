from tkinter import *
import os

def move_app(e):
	window.geometry(f'+{e.x_root}+{e.y_root}')

def quitter(e):
	window.quit()

def startWebcamEffects():
    os.system("python ./Webcam/startWebcam.py")
    window.wm_attributes("-topmost", 1)

def startGameController():
    os.system("python ./Game/startGameController.py")
    window.wm_attributes("-topmost", 1)

window = Tk()

window.geometry("852x315+500+300")

window.overrideredirect(True)
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 315,
    width = 855,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = -1, y = 0)

background_img = PhotoImage(file = f"./images/ui_images/background.png")
background = canvas.create_image(
    233.5, 153.0,
    image=background_img)

webcam_img = PhotoImage(file = f"./images/ui_images/webcam_img.png")
webcam_btn = Button(
    image = webcam_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = startWebcamEffects,
    relief = "flat")

webcam_btn.place(
    x = 678, y = 103,
    width = 83,
    height = 36)

game_img = PhotoImage(file = f"./images/ui_images/game_img.png")
game_btn = Button(
    image = game_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = startGameController,
    relief = "flat")

game_btn.place(
    x = 676, y = 208,
    width = 83,
    height = 36)


title_bar = Frame(window, bg="#292929", relief="raised", bd=0)
title_bar.pack(side=TOP, fill=BOTH)
title_bar.bind("<B1-Motion>", move_app)

title_label = Label(title_bar, text="  SoCap  ", bg="#292929", fg="white")
title_label.pack(side=LEFT, pady=2)

close_label = Label(title_bar, text="  X  ", bg="#292929", fg="white", relief="sunken", bd=0)
close_label.pack(side=RIGHT, pady=2)
close_label.bind("<Button-1>", quitter)


window.resizable(False, False)
window.mainloop()
