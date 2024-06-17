#! /usr/bin/env python3

"""App with Tkinter to convert temperature (Celsius <--> Farhenheit)"""

import os
from pathlib import Path
import tkinter as tk
from PIL import ImageTk
import customtkinter as ctk
from entry_temp import Entry_temp

# conversion functions
def farhenheit_to_celsius(number: float) -> float:
    return ((number -32) * (5/9))

def celsius_to_farhenheit(number: float) -> float:
    return ((number * (9/5)) + 32)

class App(ctk.CTk):

    def __init__(self, name: str, size: tuple[int]):

        # window setup
        super().__init__()

        self.title(name)
        # center_window centers the window into the main monitor
        self.geometry(self.center_window(size[0], size[1], self._get_window_scaling()))
        self.minsize(size[0], size[1])
        self.maxsize(800, 400)

        # set the icon
        appearance_mode = ctk.get_appearance_mode()
        self.set_icon(appearance_mode)

        # track if the system changes theme and link the changing of icon to it
        ctk.AppearanceModeTracker.callback_list.append(self.set_icon)

        self.create_widgets()

        # coordonate the toggle of the switch with the change of theme
        ctk.AppearanceModeTracker.callback_list.append(self.set_toggle)

        # change entries with Tab
        self.entry_celsius.bind("<Tab>", lambda event: self.entry_far.focus())
        self.entry_far.bind("<Tab>", lambda event: self.entry_celsius.focus())

        self.entry_celsius.bind("<Delete>", lambda event: self.entry_celsius.delete_char(self.entry_far))
        self.entry_far.bind("<Delete>", lambda event: self.entry_far.delete_char(self.entry_celsius))

        self.entry_celsius.bind("<KeyPress-Right>", lambda event: self.entry_celsius.move_cursor(event.keysym))
        self.entry_celsius.bind("<KeyPress-Left>", lambda event: self.entry_celsius.move_cursor(event.keysym))
        self.entry_far.bind("<KeyPress-Right>", lambda event: self.entry_far.move_cursor(event.keysym))
        self.entry_far.bind("<KeyPress-Left>", lambda event: self.entry_far.move_cursor(event.keysym))

        # bind the check of the input and the conversion to the entry;
        # each entry is an instance of the Entry_temp class
        self.entry_celsius.bind("<KeyPress>", lambda event: self.entry_celsius.key_callback(event.char, self.entry_far))
        self.entry_far.bind("<KeyPress>", lambda event: self.entry_far.key_callback(event.char, self.entry_celsius))

        # auto-select text in the entry when the focus is on the widget
        self.entry_celsius.bind("<FocusIn>", lambda event: self.entry_celsius.select_range(0, tk.END))
        self.entry_far.bind("<FocusIn>", lambda event: self.entry_far.select_range(0, tk.END))

        # bind the focus of the left entry to the creation of the window
        self.bind("<Map>", lambda event: self.entry_celsius.focus())

        self.mainloop()

    def set_icon(self, appearance_mode: str) -> None:
        """convert any photo format into an icon and set it as the window's icon.
        Adapt the choice of the icon whether the mode is dark or light"""
        if appearance_mode == "Dark":
            path = os.path.join(Path(__file__).parent, "temp_icon_light.png")
        else:
            path = os.path.join(Path(__file__).parent, "temp_icon_dark.png")
        icon = ImageTk.PhotoImage(file = path)

        self.wm_iconbitmap()
        self.iconphoto(False, icon)

    def center_window(self, width: int, height: int, scale_factor: float = 1.0) -> str:
        """Centers the window to the main display/monitor"""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int(((screen_width/2) - (width/2)) * scale_factor)
        y = int(((screen_height/2) - (height/1.5)) * scale_factor)
        return f"{width}x{height}+{x}+{y}"

    def set_toggle(self, theme: str) -> None:
        if theme == "Dark":
            self.switch.select()
        else:
            self.switch.deselect()

    def change_theme(self) -> None:
        """switch the window's theme"""
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")

    def create_widgets(self) -> None:
        # main converter
        self.frame = ctk.CTkFrame(self, fg_color = "transparent")

        self.entry_celsius = Entry_temp(self.frame, celsius_to_farhenheit)

        self.label_celsius = ctk.CTkLabel(self.frame, text = "°C")

        self.label_equal = ctk.CTkLabel(self.frame, text = "=")

        self.entry_far = Entry_temp(self.frame, farhenheit_to_celsius)

        self.label_far = ctk.CTkLabel(self.frame, text = "F")

        # theme switch
        self.switch = ctk.CTkSwitch(
            self,
            text = "Changer de thème",
            fg_color = ("#60c7f0", "#0b4a63"),
            progress_color = ("#60c7f0", "#0b4a63"),
            command = self.change_theme
            )
        self.set_toggle(ctk.get_appearance_mode())
        self.switch.configure(font = (self.switch.cget("font"), 11, "bold"))

        self.create_layout()

    def create_layout(self) -> None:
        """pack and place layout"""
        self.frame.place(relx = 0.05, rely = 0.05, relheight = 0.9, relwidth = 0.9, anchor = "nw")

        self.entry_celsius.pack(side = "left", expand = True, fill = "x")
        self.label_celsius.pack(side = "left", padx = 3)
        self.label_equal.pack(side = "left", padx = 20)
        self.entry_far.pack(side = "left", expand = True, fill = "x")
        self.label_far.pack(side = "left", padx = 3)

        # place the switch in the bottom-right corner of the window
        self.switch.place(relx = 0.98, rely = 0.98, anchor = "se")


app = App("Convertisseur de température", (600, 250))