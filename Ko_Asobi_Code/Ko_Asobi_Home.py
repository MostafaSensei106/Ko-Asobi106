import tkinter.messagebox
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
import subprocess
def main():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("../Assets/Assets_Ko_Asobi_Home")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    class Logic_Button():
        def Run_Ko_Snake(self):
            subprocess.run(["python", "Ko_Asobi_Snake_Game.py"])
            print("Ko-Asobi Snake Game Complete")

        def Run_Ko_Pong_Game(self):
            subprocess.run(["python", "Ko_Asobi_Pong_Game.py"])
            print("Ko-Asobi Pong Game Complete")


        def Soon_Games_Massage(self):
            tkinter.messagebox.showinfo("Ko-Asobi", "Ko-Asobi Game Come Soon")

        def Cridts_Massage(self):
            tkinter.messagebox.showinfo("Ko-Asobi", "This Game Make By Mostafa Mahmoud")

        def Exit_Ko_game(self):
            window.destroy()
            print("Ko-Asobi Game Exited")

    window = Tk()
    window.geometry("1920x1080")
    window.configure(bg="#D6EEFB")
    window.title("Ko-Asobi")
    canvas = Canvas(window, bg="#D6EEFB", highlightthickness=0)

    ko_Logic = Logic_Button()

    canvas = Canvas(
        window,
        bg="#D6EEFB",
        height=1080,
        width=1920,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))

    image_1 = canvas.create_image(
        960.0,
        540.0,
        image=image_image_1
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))

    image_2 = canvas.create_image(
        302.0,
        540.0,
        image=image_image_2
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))

    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: ko_Logic.Run_Ko_Snake(),
        relief="flat"
    )

    button_1.place(
        x=109.0,
        y=278.0,
        width=385.0,
        height=75.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))

    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: ko_Logic.Run_Ko_Pong_Game(),
        relief="flat"
    )

    button_2.place(
        x=110.0,
        y=376.0,
        width=385.0,
        height=75.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))

    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: ko_Logic.Soon_Games_Massage(),
        relief="flat"
    )

    button_3.place(
        x=109.0,
        y=474.0,
        width=385.0,
        height=75.0
    )

    button_image_4 = PhotoImage(
        file=relative_to_assets("button_4.png"))

    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: ko_Logic.Exit_Ko_game(),
        relief="flat"
    )

    button_4.place(
        x=109.0,
        y=670.0,
        width=385.0,
        height=75.0
    )

    button_image_5 = PhotoImage(
        file=relative_to_assets("button_5.png"))

    button_5 = Button(
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: ko_Logic.Cridts_Massage(),
        relief="flat"
    )

    button_5.place(
        x=109.0,
        y=572.0,
        width=385.0,
        height=75.0
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        302.0,
        121.0,
        image=image_image_3
    )

    window.resizable(False, False)
    window.mainloop()

if __name__ == '__main__':
    main()