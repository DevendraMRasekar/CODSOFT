import tkinter as tk
from tkinter import messagebox


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title(" Calculator App")
        self.root.geometry("450x650")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(False, False)

        self.header_bg = "#313244"
        self.accent_color = "#cba6f7"
        self.text_color = "#cdd6f4"
        self.btn_bg = "#45475a"
        self.btn_active_bg = "#585b70"

        self.create_widgets()

    def create_widgets(self):
        header_frame = tk.Frame(self.root, bg=self.header_bg, pady=15)
        header_frame.pack(fill=tk.X)

        title_label = tk.Label(
            header_frame,
            text="📊 CALCULATOR 📊",
            font=("Arial", 16, "bold"),
            bg=self.header_bg,
            fg=self.accent_color
        )
        title_label.pack()

        subtitle_label = tk.Label(
            header_frame,
            font=("Arial", 9, "italic"),
            bg=self.header_bg,
            fg="#a6adc8"
        )
        subtitle_label.pack()

        input_frame = tk.Frame(self.root, bg="#1e1e2e", padx=30, pady=15)
        input_frame.pack(fill=tk.BOTH, expand=True)

        lbl_num1 = tk.Label(
            input_frame,
            text="Enter First Number (X):",
            font=("Arial", 11, "bold"),
            bg="#1e1e2e",
            fg=self.text_color
        )
        lbl_num1.pack(anchor=tk.W, pady=(5, 2))

        self.entry_num1 = tk.Entry(
            input_frame,
            font=("Arial", 12),
            bg="#313244",
            fg="#ffffff",
            insertbackground="white",
            bd=0,
            relief=tk.FLAT
        )
        self.entry_num1.pack(fill=tk.X, ipady=8)

        lbl_num2 = tk.Label(
            input_frame,
            text="Enter Second Number (Y):",
            font=("Arial", 11, "bold"),
            bg="#1e1e2e",
            fg=self.text_color
        )
        lbl_num2.pack(anchor=tk.W, pady=(12, 2))

        self.entry_num2 = tk.Entry(
            input_frame,
            font=("Arial", 12),
            bg="#313244",
            fg="#ffffff",
            insertbackground="white",
            bd=0,
            relief=tk.FLAT
        )
        self.entry_num2.pack(fill=tk.X, ipady=8)

        lbl_ops = tk.Label(
            input_frame,
            text="Select Operation:",
            font=("Arial", 11, "bold"),
            bg="#1e1e2e",
            fg=self.text_color
        )
        lbl_ops.pack(anchor=tk.W, pady=(15, 5))

        btn_frame = tk.Frame(input_frame, bg="#1e1e2e")
        btn_frame.pack(fill=tk.X)

        operators = [
            ('➕ Add', '+'),
            ('➖ Subtract', '-'),
            ('✖️ Multiply', '*'),
            ('➗ Divide', '/'),
            ('🚀 Exponent (X^Y)', '^'),
            ('🔢 Modulus (%)', '%'),
            ('📉 Floor Div (//)', '//')
        ]

        for i, (label, op) in enumerate(operators):
            row = i // 2
            col = i % 2
            column_span = 2 if i == len(operators) - 1 else 1

            btn = tk.Button(
                btn_frame,
                text=label,
                font=("Arial", 10, "bold"),
                bg=self.btn_bg,
                fg=self.text_color,
                activebackground=self.btn_active_bg,
                activeforeground="#ffffff",
                bd=0,
                cursor="hand2",
                command=lambda o=op: self.calculate(o)
            )
            btn.grid(
                row=row,
                column=col,
                columnspan=column_span,
                sticky="nsew",
                padx=4,
                pady=4,
                ipady=8
            )

            if column_span == 1:
                btn_frame.columnconfigure(col, weight=1)

        self.lbl_result_box = tk.Label(
            input_frame,
            text="Result will appear here",
            font=("Arial", 12, "bold"),
            bg="#252538",
            fg="#a6adc8",
            pady=12,
            bd=1,
            relief=tk.SOLID
        )
        self.lbl_result_box.pack(fill=tk.X, pady=(20, 5))

    def calculate(self, operation):
        self.lbl_result_box.config(bg="#252538", fg="#a6adc8")

        try:
            val1 = float(self.entry_num1.get())
            val2 = float(self.entry_num2.get())
        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Please enter valid numeric values in both fields."
            )
            return

        result = None
        display_op = operation

        try:
            if operation == '+':
                result = val1 + val2
            elif operation == '-':
                result = val1 - val2
            elif operation == '*':
                result = val1 * val2
            elif operation == '/':
                if val2 == 0:
                    raise ZeroDivisionError("Division by zero")
                result = val1 / val2
            elif operation == '^':
                display_op = "^"
                result = val1 ** val2
            elif operation == '%':
                if val2 == 0:
                    raise ZeroDivisionError("Modulus by zero")
                result = val1 % val2
            elif operation == '//':
                if val2 == 0:
                    raise ZeroDivisionError("Floor division by zero")
                result = val1 // val2
        except ZeroDivisionError:
            self.lbl_result_box.config(
                text="🚫 Error: Division by Zero!",
                bg="#f38ba8",
                fg="#11111b"
            )
            return
        except OverflowError:
            self.lbl_result_box.config(
                text="🚫 Error: Result is too large!",
                bg="#f38ba8",
                fg="#11111b"
            )
            return

        fmt_v1 = int(val1) if val1.is_integer() else val1
        fmt_v2 = int(val2) if val2.is_integer() else val2

        if isinstance(result, float) and result.is_integer():
            fmt_res = int(result)
        else:
            fmt_res = round(result, 4) if isinstance(result, float) else result

        final_text = f"{fmt_v1} {display_op} {fmt_v2} = {fmt_res}"

        self.lbl_result_box.config(
            text=f"🎉 {final_text}",
            bg="#a6e3a1",
            fg="#11111b"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()