import tkinter as tk
from tkinter import ttk, messagebox
import math

class CalculatorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Aivitas kalkulators")
        
        # Neļauj logam mainīties izmēram
        self.master.resizable(width=False, height=False)

        self.result_var = tk.StringVar()
        self.expression = ""

        self.create_widgets()

    def create_widgets(self):
        # Ievades lauks rezultāta parādīšanai
        entry_frame = ttk.Frame(self.master, padding="10")
        entry_frame.grid(row=0, column=0, columnspan=4)

        entry = ttk.Entry(entry_frame, textvariable=self.result_var, justify='right', font=('Arial', 14))
        entry.grid(row=0, column=0, columnspan=4, sticky='nsew')

        # Atļauj tikai ciparu ievadi un iestata ciparu formātu
        entry.configure(validate="key", validatecommand=(entry.register(self.validate_input), "%P"))

        # Pogas
        buttons = [
            ('%', 'purple'), ('CE', 'purple'), ('C', 'purple'), ('Del', 'purple'),
            ('¹/ₓ', 'purple'), ('x²', 'purple'), ('²√x', 'purple'), ('/', 'purple'),
            ('7', 'purple'), ('8', 'purple'), ('9', 'purple'), ('*', 'purple'),  # changed from 'x' to '*'
            ('4', 'purple'), ('5', 'purple'), ('6', 'purple'), ('-', 'purple'),
            ('1', 'purple'), ('2', 'purple'), ('3', 'purple'), ('+', 'purple'),
            ('+/_', 'purple'), ('0', 'purple'), ('.', 'purple'), ('=', 'purple'),
            ('(', 'purple'), (')', 'purple')  # added brackets
        ]

        button_frame = ttk.Frame(self.master)
        button_frame.grid(row=1, column=0, columnspan=4)

        row_val = 1
        col_val = 0
        for text, color in buttons:
            button = ttk.Button(button_frame, text=text, command=lambda b=text: self.on_button_click(b), style=f'{color}.TButton')
            button.grid(row=row_val, column=col_val, sticky='nsew', ipadx=15, ipady=15)
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

        # Konfigurē stila iestatījumus pogām
        style = ttk.Style()
        style.configure('purple.TButton', background='purple', font=('Arial', 12, 'bold'), anchor='center', width=3)

        # Izvēlnes josla
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        # Palīdzības izvēlne
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Palīdzība", menu=help_menu)
        help_menu.add_command(label="Lietotāja rokasgrāmata", command=self.show_user_guide)

    def on_button_click(self, button):
        if button == '=':
            try:
                result = eval(self.expression)
                self.result_var.set(self.format_number(result))
                self.expression = str(result)
            except Exception as e:
                self.result_var.set("Kļūda")
                self.expression = ""
        elif button == 'CE':
            self.expression = self.expression[:-1]
            self.result_var.set(self.format_number(self.expression))
        elif button == 'C':
            self.expression = ""
            self.result_var.set("")
        elif button == 'Del':
            self.expression = ""
            self.result_var.set("")
        elif button == '¹/ₓ':
            self.expression = '1/(' + self.expression + ')'
            self.result_var.set(self.format_number(self.expression))
        elif button == 'x²':
            self.expression += '**2'
            self.result_var.set(self.format_number(self.expression))
        elif button == '²√x':
            try:
                result = math.sqrt(eval(self.expression))
                self.result_var.set(self.format_number(result))
                self.expression = str(result)
            except Exception as e:
                self.result_var.set("Kļūda")
                self.expression = ""
        elif button == '+/_':
            # Maina pašreizējo vērtību zīmi
            if self.expression and self.expression[0] == '-':
                self.expression = self.expression[1:]
            else:
                self.expression = '-' + self.expression
            self.result_var.set(self.format_number(self.expression))
        else:
            self.expression += str(button)
            self.result_var.set(self.format_number(self.expression))

    def validate_input(self, value):
        # Pārbauda ievadi, lai atļautu ciparus, decimālpunktu, '-', '*', '(' un ')'
        return all(char.isdigit() or char == '.' or char == '-' or char == '*' or char == '(' or char == ')' for char in value) or value == ''

    def format_number(self, number):
        # Pievieno komatus, lai uzlabotu lielo skaitļu lasāmību
        try:
            number = f'{float(number):,.6f}'.rstrip('0').rstrip('.')
            if ',' in number:
                int_part, frac_part = number.split('.')
                int_part = int_part.replace(',', '')
                number = f'{int_part:,.0f}.{frac_part}'
            return number
        except ValueError:
            return number

    def show_user_guide(self):
        user_guide_text = (
            "Lietotāja rokasgrāmata pārkārtotam kalkulatoram\n"
            "\n"
            "1. Pamata matemātiskās operācijas:\n"
            "   - Saskaitīšana (+)\n"
            "   - Atnemšana (-)\n"
            "   - Reizināšana (*)\n"
            "   - Dalīšana (/)\n"
            "\n"
            "2. Papildu funkcijas:\n"
            "   - Procenti (%)\n"
            "   - Dzēst ievadīto vērtību (CE)\n"
            "   - Dzēst visu (C)\n"
            "   - Dzēst pēdējo ciparu (Del)\n"
            "   - Inversa vērtība (¹/ₓ)\n"
            "   - Kvadrāts (x²)\n"
            "   - Kvadrātsakne (²√x)\n"
            "   - Mainīt zīmi (+/_)\n"
            "\n"
            "3. Lietošana:\n"
            "   - Nospiediet pogas, lai veiktu aprēķinus.\n"
            "   - Atbalsta ciparu ievadi no tastatūras.\n"
            "   - Izmantojiet '=' pogu, lai iegūtu izteiksmes rezultātu.\n"
        )

        messagebox.showinfo("Lietotāja rokasgrāmata", user_guide_text)

def main():
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
