# Import the required modules
import sys
import os
import random
import subprocess
import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
import time


def generate_passphrase():
    # Import the random module
    import random
    # Open a file containing a list of words
    with open("words.txt", "r") as f:
        # Read all the words and store them in a list
        words = f.read().splitlines()
    # Choose 5 random words from the list
    passphrase = random.sample(words, 7)
    # Generate a random number between 0 and 9
    number = random.randint(0, 9)
    # Choose a random word from the passphrase to add the number to
    index = random.randint(0, 4)
    # Decide whether to add the number before or after the word
    position = random.choice(["before", "after"])
    # Get the word at the chosen index
    word = passphrase[index]
    # If the position is before, add the number before the word
    if position == "before":
        modified_word = str(number) + word
    # If the position is after, add the number after the word
    else:
        modified_word = word + str(number)
    # Replace the word at the chosen index with the modified word
    passphrase[index] = modified_word
    # Join the words with dashes and return the passphrase
    return "-".join(passphrase)


def display_fileinput():
    window = tk.Tk()
    window.resizable(0, 0)
    window.title("auto-encrypt")
    window.geometry("300x200")

    global file_name
    file_name = tk.StringVar()

    # Create a label to display the file name and path
    label = tk.Label(window, text="No file selected")
    label.pack(pady=10)

    def encrypt_file():
        button.config(state="disabled")
        buttonEncrypt.config(state="disabled")
        file = file_name.get()
        # Construct the command to run 7zip with the encryption options
        command = f'7z a -p"{passphrase}" -mx=9 -mhe=on "{file}.7z" "{file}"'
        # Run the command and wait for it to finish
        subprocess.run(command, shell=True, check=True)
        shred_file()
        window.destroy()

    def shred_file():
        file = file_name.get()
        file = file.replace('/', '\\')
        print('shredding ' + file)
        command = f'bleachbit --shred "{file}"'
        subprocess.run(command, shell=True, check=True)

    def open_file():
        # Use filedialog.askopenfilename to get the file name
        file = filedialog.askopenfilename()
        file_name.set(file)

        # Update the label text with the file name and path
        label.config(text=file)

        # Return the file name
        buttonEncrypt.config(state="normal")

    # Create a button to invoke the open_file function
    button = tk.Button(window, text="Select File", command=open_file)
    button.pack(pady=10)

    # Create a button to encrypt the file
    buttonEncrypt = tk.Button(
        window, text="Encrypt", state="disabled", command=encrypt_file)
    buttonEncrypt.pack(pady=10)

    window.mainloop()


def display_passphrase(passphrase):

    secondsUntilClose = 20

    # Create a tkinter window
    window = tk.Tk()
    window.resizable(0, 0)

    # Set the window title and size
    window.title("Passphrase")
    window.geometry("400x100")

    # Create a label to show the passphrase
    label = tk.Entry(window, width=50)
    label.pack(pady=10)
    label.insert(-1, passphrase)
    label.config(state="readonly")

    # Create a progress bar to show the time left
    progress = ttk.Progressbar(window, orient=tk.HORIZONTAL,
                               length=200, mode="determinate")  # Use ttk.Progressbar
    progress.pack(pady=10)
    progress["value"] = 100

    # Define a function to update the progress bar and close the window after 60 seconds
    def update_progress():

        nonlocal secondsUntilClose

        # Get the current value of the progress bar
        value = progress["value"]

        # If the value is less than 100, increase it by 1 and update the progress bar
        if value > 0:
            value -= (100/secondsUntilClose)
            secondsUntilClose -= 1
            progress["value"] = value
            # Schedule the function to run again after 1 second
            window.after(1000, update_progress)
        # Otherwise, destroy the window
        else:
            window.destroy()

    # Start the update function
    update_progress()
    # Start the main loop of the window
    window.mainloop()


''' START SCRIPT '''
try:
    # Generate a passphrase
    passphrase = generate_passphrase()

    # Get the file name from the user input
    display_fileinput()

    # Display the passphrase
    display_passphrase(passphrase)

    # Exit
    exit()
except Exception as e:
    print(e)
    exit()
