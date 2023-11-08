import os
import datetime
from art import *
from termcolor import colored
import time

# MiniByte Interpreter

text = "minibyte   by   niko"
ascii_art = text2art(text)
colored_ascii_art = colored(ascii_art, 'magenta', attrs=['bold'])
print(colored_ascii_art.center(80))  # Center the ASCII art in an 80-character-wide display

# Create a dictionary to store variables
variables = {}

# Define the print function
def print_func(args):
    if args.startswith("@"):
        var_name = args[1:]
        if var_name in variables:
            print(variables[var_name])
        else:
            print(f"Error: Variable '{var_name}' not found.")
    else:
        print(args)

# Define the set variable function
def set_variable(args):
    if '=' in args:
        var_name, var_value = args.split('=')
        variables[var_name.strip()] = var_value.strip()
    else:
        print("Error: Missing '=' in variable assignment.")

# Define the mathematical operations
def do_math(expression):
    for var_name in variables:
        expression = expression.replace("@" + var_name, str(variables[var_name]))
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

# Define the datafile function
def datafile(args):
    if os.path.exists(args):
        path = os.path.abspath(args)
        filename = os.path.basename(args)
        file_stats = os.stat(args)
        created = datetime.datetime.fromtimestamp(file_stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
        size = file_stats.st_size

        # Display file information
        print(f"File Path: {path}")
        print(f"File Name: {filename}")
        print(f"Date Created: {created}")
        print(f"File Size (bytes): {size}")
    else:
        print(f"Error: File '{args}' not found.")

# Define the help function
def help_func(args=None):
    print("minibyte Commands:")
    print("print [message or variable] - Print a message or variable")
    print("var [variable]=[value] - Set a variable")
    print("math [expression] - Perform mathematical operations")
    print("new>folder [foldername] - Create a new folder")
    print("new>file [filename].[extension] - Create a new file")
    print("datafile [filepath] - Display information about a file")
    print("execfile [filepath] - Execute code from a .byte file")
    print("title [new_title] - Change the title")
    print("whoami - Display user information")
    print("help - Show this help message")
    print("exit - Exit minibyte")
    print("cls - Clear the screen")
    print("wait [seconds] - Pause execution for the specified number of seconds")

# Define the create new folder function
def create_new_folder(args):
    folder_name = args.strip()
    path = os.path.join(os.getcwd(), folder_name)
    os.makedirs(path)
    return f"Created new folder: {path}"

# Define the create new file function
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
        print("Error: Missing extension in filename.")

# Define the title function
def title(args):
    os.system(f"title {args}")

# Define the execute code from file function
def execfile(args):
    if args.endswith(".byte"):
        try:
            with open(args, 'r') as code_file:
                code = code_file.read()
                exec(code)
                print("Code execution complete.")
        except Exception as e:
            print(f"Error: {str(e)}")
    else:
        print("Error: Invalid file extension. Only .byte files are supported.")

# Define the whoami function
def whoami(args=None):
    username = os.getlogin()
    current_directory = os.getcwd()
    print(f"User: {username}")
    print(f"Current Directory: {current_directory}")

# Define the clear screen function
def clear_screen(args=None):
    os.system('cls' if os.name == 'nt' else 'clear')

# Define the wait function
def wait(args):
    try:
        seconds = float(args)
        time.sleep(seconds)
    except ValueError:
        print("Error: Invalid argument. Please provide a valid number of seconds.")

# Dictionary of available functions
functions = {
    "print": print_func,
    "var": set_variable,
    "math": do_math,
    "help": help_func,
    "new>folder": create_new_folder,
    "new>file": create_new_file,
    "datafile": datafile,
    "title": title,
    "execfile": execfile,
    "whoami": whoami,
    "cls": clear_screen,
    "wait": wait,
}

# Main interpreter loop
title("minibyte by niko")

while True:
    user_input = input("minibyte> ")

    if user_input == "exit":
        break

    parts = user_input.split()
    command = parts[0]

    if command in functions:
        if len(parts) > 1:
            args = ' '.join(parts[1:])
            result = functions[command](args)
            if result is not None:
                print(result)
        else:
            functions[command]()
    else:
        print("Error: Invalid command. Type 'help' for a list of commands.")
