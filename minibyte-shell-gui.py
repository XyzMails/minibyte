import tkinter as tk
import os
import datetime
from art import *
from termcolor import colored
import time
import sys
import io

variables = {}

def print_func(args):
    if args.startswith("@"):
        var_name = args[1:]
        if var_name in variables:
            return variables[var_name]
        else:
            return f"Error: Variable '{var_name}' not found."
    else:
        return args

def set_variable(args):
    if '=' in args:
        var_name, var_value = args.split('=')
        var_name = var_name.strip()
        var_value = var_value.strip()
        variables[var_name] = var_value
        return f"Variable {var_name} has been set to {var_value} successfully."
    else:
        return "Error: Missing '=' in variable assignment."

def do_math(expression):
    for var_name in variables:
        expression = expression.replace("@" + var_name, str(variables[var_name]))

    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

def datafile(args):
    if os.path.exists(args):
        path = os.path.abspath(args)
        filename = os.path.basename(args)
        file_stats = os.stat(args)
        created = datetime.datetime.fromtimestamp(file_stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
        size = file_stats.st_size
        return f"File Path: {path}\nFile Name: {filename}\nDate Created: {created}\nFile Size (bytes): {size}"
    else:
        return f"Error: File '{args}' not found."

def compare_numbers(args):
    try:
        # Split the input into two numbers
        num1, num2 = map(float, args.split())
        
        # Compare the numbers and create a message
        if num1 < num2:
            message = f"({num1} < {num2}) {num2} Beats {num1}!"
        elif num1 > num2:
            message = f"({num1} > {num2}) {num1} Beats {num2}!"
        else:
            message = f"({num1} == {num2}) It's a Tie!"
        
        return message
    except ValueError:
        return "Error: Invalid input. Please provide two numbers."


def help_func(args=None):
    return "minibyte Commands:\n" \
           "print [message or variable] - Print a message or variable\n" \
           "var [variable]=[value] - Set a variable\n" \
           "math [expression] - Perform mathematical operations\n" \
           "math>compare [num1] [num2] - Compare two numbers\n" \
           "datafile [filepath] - Display information about a file\n" \
           "help - Show this help message\n" \
           "new>folder [foldername] - Create a new folder\n" \
           "new>file [filename].[extension] - Create a new file\n" \
           "title [new_title] - Change the title\n" \
           "execfile [filepath] - Execute code from a .byte file\n" \
           "whoami - Display user information\n" \
           "cls - Clear the screen\n" \
           "wait [seconds] - Pause execution for the specified number of seconds\n" \
           "if [something] do [string here] - Execute conditional commands"

def create_new_folder(args):
    folder_name = args.strip()
    path = os.path.join(os.getcwd(), folder_name)
    os.makedirs(path)
    return f"Created new folder: {path}"

def create_new_file(args):
    if '.' in args:
        filename, extension = args.split('.')
        filename = filename.strip()
        extension = extension.strip()
        path = os.path.join(os.getcwd(), filename + '.' + extension)
        with open(path, 'w') as new_file:
            pass
        return f"Created new file: {path}"
    else:
        return "Error: Missing extension in filename."

def title(args):
    root.title(args)  # Set the Tkinter window title

def execfile(args):
    if args.endswith(".byte"):
        try:
            with open(args, 'r') as code_file:
                code = code_file.read()
                result = eval(code)
                return str(result)
        except Exception as e:
            return f"Error: {str(e)}"
    else:
        return "Error: Invalid file extension. Only .byte files are supported."

def whoami(args=None):
    username = os.getlogin()
    current_directory = os.getcwd()
    return f"User: {username}\nCurrent Directory: {current_directory}"

def clear_screen(args=None):
    output_textbox.config(state="normal")
    output_textbox.delete(1.0, tk.END)
    output_textbox.config(state="disabled")

def wait(args):
    try:
        seconds = float(args)
        time.sleep(seconds)
    except ValueError:
        return "Error: Invalid argument. Please provide a valid number of seconds."

def if_statement(args):
    parts = args.split(" do ")
    if len(parts) == 2:
        condition, action = parts
        if eval(condition):
            return action
        else:
            return ""
    else:
        return "Error: Invalid if statement. Use 'if [condition] do [action]'."

# all functions
functions = {
    "print": print_func,
    "var": set_variable,
    "math": do_math,
    "datafile": datafile,
    "help": help_func,
    "new>folder": create_new_folder,
    "new>file": create_new_file,
    "title": title,
    "execfile": execfile,
    "whoami": whoami,
    "cls": clear_screen,
    "wait": wait,
    "if": if_statement,
    "math>compare": compare_numbers,
}

# gui setup
root = tk.Tk()
root.title("minibyte>GUI")
root.minsize(920, 620)
root.geometry("920x620")  # Make the window larger

root.tk_setPalette(background='#36393f', foreground='white')
root.option_add('*TButton*highlightColor', 'white')
root.option_add('*TButton*selectColor', '#202225')
root.option_add('*TButton*font', ('Segoe UI', 10))
root.option_add('*TButton*padding', (6, 3))
root.option_add('*TButton*relief', 'flat')
root.option_add('*TButton*background', '#202225')
root.option_add('*TButton*foreground', 'white')
root.option_add('*TButton.border', 0)

output_frame = tk.Frame(root, background='#36393f')
output_frame.pack(fill="both", expand=True)

output_textbox = tk.Text(output_frame, font=("Consolas", 12), wrap="word", spacing1=1, bg='#202225', fg='white')
output_textbox.pack(fill="both", expand=True)

input_frame = tk.Frame(root, background='#36393f')
input_frame.pack(fill="x")

username = os.getlogin()

username_prompt = tk.Label(input_frame, text=f"{username}@minibyte>", font=("Consolas", 12), bg='#36393f', fg='white')
username_prompt.pack(side="left")

text_input = tk.Entry(input_frame, font=("Consolas", 12), bg='#36393f', fg='white', insertbackground='white')
text_input.pack(fill="x", expand=True)

def handle_input(event):
    user_input = text_input.get()
    text_input.delete(0, tk.END)

    parts = user_input.split()
    if not parts:
        return

    command = parts[0]

    if command in functions:
        if len(parts) > 1:
            args = ' '.join(parts[1:])
            result = functions[command](args)
            if result is not None:
                output_text(result)
        else:
            result = functions[command]()
            output_text(result)
    else:
        output_text("Error: Invalid command. Type 'help' for a list of commands.")

def output_text(text):
    output_textbox.config(state="normal")
    output_textbox.insert("end", text + "\n")
    output_textbox.config(state="disabled")

class StdoutRedirector:
    def write(self, text):
        output_text(text)

sys.stdout = StdoutRedirector()

text_input.bind("<Return>", handle_input)

from art import *

text = "minibyte made by niko"
ascii_art = text2art(text, font="small")

output_text(ascii_art)


root.mainloop()
