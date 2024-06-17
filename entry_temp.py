import tkinter as tk
import customtkinter as ctk

class Entry_temp(ctk.CTkEntry):

    def __init__(self, parent, func) -> None:
        super().__init__(parent)

        self.char = None
        self.input = None
        self.convert = func

    def set(self, output: str) -> None:
        """delete the previous text in the entry and replace it with the output string"""
        # delete the whole text in entry
        self.delete(0, tk.END)
        # insert the output at index 0
        self.insert(0, output)

    def delete_char(self, output_entry: ctk.CTkEntry) -> None|str:
        index_cursor = self.index(tk.INSERT)
        self.input = self.get()

        if self.input == None:
            output_entry.set("")
            return "break"

        input = self.input[0:index_cursor] + self.input[index_cursor + 1:]
        self.set(input)
        output_entry.set(f"{self.convert(float(input)):.2f}")

    def move_cursor(self, keysym: str) -> None|str:
        index_cursor = self.index(tk.INSERT)

        if keysym == "Right":
            self.icursor(index_cursor)
        else:
            self.icursor(index_cursor)

    def key_callback(self, char: str, output_entry: ctk.CTkEntry) -> None|str:
        self.char = char
        # get the actual text in the entry (without the new char)
        self.input = self.get()

        if self.check_input_and_set_attributes():
            output_entry.set(f"{self.convert(float(self.input)):.2f}")
        else:
            if self.input == "":
                output_entry.set("")
            else:
                # don't take the event into account
                # the char will not be added to the entry line
                return "break"

    def check_input_and_set_attributes(self) -> bool:
        """check the char;
        set the correct value of the input"""
        index_cursor = self.index(tk.INSERT)

        # \x08 = the delete key
        if self.char == "\x08":
            self.input = self.input[:index_cursor - 1] + self.input[index_cursor:]
            if self.input == "":
                return False
            return True

        elif self.char.isdigit() or self.char == ".":
            self.input = self.input[:index_cursor] + self.char + self.input[index_cursor:]
            return True

        else:
            self.input = None
            return False