import random
import string
import tkinter as tk
from tkinter import ttk, messagebox


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("520x420")
        self.root.resizable(False, False)

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure("TLabel", font=("Arial", 11))
        self.style.configure("Title.TLabel", font=("Arial", 20, "bold"))
        self.style.configure("TButton", font=("Arial", 11, "bold"), padding=8)
        self.style.configure("TCheckbutton", font=("Arial", 10))

        main = ttk.Frame(root, padding=20)
        main.pack(fill="both", expand=True)

        ttk.Label(
            main,
            text="Password Generator",
            style="Title.TLabel"
        ).pack(pady=(0, 20))

        ttk.Label(main, text="Enter Password Length:").pack(anchor="w")

        self.length_var = tk.StringVar(value="12")

        ttk.Entry(
            main,
            textvariable=self.length_var,
            width=20
        ).pack(fill="x", pady=(5, 15))

        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digit_var = tk.BooleanVar(value=True)
        self.symbol_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(
            main,
            text="Include Uppercase Letters",
            variable=self.upper_var
        ).pack(anchor="w", pady=2)

        ttk.Checkbutton(
            main,
            text="Include Lowercase Letters",
            variable=self.lower_var
        ).pack(anchor="w", pady=2)

        ttk.Checkbutton(
            main,
            text="Include Numbers",
            variable=self.digit_var
        ).pack(anchor="w", pady=2)

        ttk.Checkbutton(
            main,
            text="Include Symbols",
            variable=self.symbol_var
        ).pack(anchor="w", pady=2)

        ttk.Button(
            main,
            text="Generate Password",
            command=self.generate_password
        ).pack(pady=20)

        ttk.Label(main, text="Generated Password:").pack(anchor="w")

        self.password_var = tk.StringVar()

        self.password_entry = ttk.Entry(
            main,
            textvariable=self.password_var,
            font=("Arial", 12),
            width=40
        )
        self.password_entry.pack(fill="x", pady=(5, 15))

        ttk.Button(
            main,
            text="Copy Password",
            command=self.copy_password
        ).pack()

    def generate_password(self):
        try:
            length = int(self.length_var.get())

            if length <= 0:
                messagebox.showerror(
                    "Error",
                    "Password length must be greater than 0."
                )
                return

        except ValueError:
            messagebox.showerror(
                "Error",
                "Please enter a valid number."
            )
            return

        char_sets = []

        if self.upper_var.get():
            char_sets.append(string.ascii_uppercase)

        if self.lower_var.get():
            char_sets.append(string.ascii_lowercase)

        if self.digit_var.get():
            char_sets.append(string.digits)

        if self.symbol_var.get():
            char_sets.append("!@#$%^&*()_+{}[]<>?/|")

        if not char_sets:
            messagebox.showerror(
                "Error",
                "Please select at least one character type."
            )
            return

        if length < len(char_sets):
            messagebox.showerror(
                "Error",
                f"Password length must be at least {len(char_sets)} for selected options."
            )
            return

        password_chars = []

        for chars in char_sets:
            password_chars.append(random.choice(chars))

        all_chars = "".join(char_sets)

        while len(password_chars) < length:
            password_chars.append(random.choice(all_chars))

        random.shuffle(password_chars)

        password = "".join(password_chars)

        self.password_var.set(password)

    def copy_password(self):
        password = self.password_var.get()

        if not password:
            messagebox.showwarning(
                "Warning",
                "Generate a password first."
            )
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        self.root.update()

        messagebox.showinfo(
            "Copied",
            "Password copied to clipboard!"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()