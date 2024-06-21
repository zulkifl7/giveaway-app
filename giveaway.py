import random
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, Button, Label, Canvas, messagebox
import threading
import time

# Function to read attendee names from a CSV file
def read_attendees_from_csv(file_path):
    df = pd.read_csv(file_path)
    attendees = df['Name'].tolist()
    return attendees

# Function to select a random winner
def select_winner(attendees):
    winner = random.choice(attendees)
    return winner

# Visual representation of the selection process
def visualize_selection(attendees, winner):
    fig, ax = plt.subplots()
    ax.barh(attendees, [1]*len(attendees), color='skyblue')
    ax.barh(winner, 1, color='green')
    plt.xlabel('Attendees')
    plt.ylabel('Selection Process')
    plt.title('Random Winner Selection')
    plt.show()

# Function to display the loading screen
def show_loading_screen(attendees, canvas, label, root):
    for _ in range(10):  # Loop to create a simple loading animation
        for name in attendees:
            canvas.itemconfig(label, text=name)
            root.update_idletasks()
            time.sleep(0.1)

# Function to start the winner selection process
def start_selection():
    attendees = read_attendees_from_csv('attendees.csv')
    if attendees:
        threading.Thread(target=show_loading_and_selection, args=(attendees,)).start()  # Start loading screen animation in a separate thread
    else:
        messagebox.showwarning("No Attendees", "No attendees found in the CSV file.")

# Function to handle loading animation and selection process
def show_loading_and_selection(attendees):
    show_loading_screen(attendees, canvas, loading_label, root)
    winner = select_winner(attendees)
    canvas.itemconfig(loading_label, text=winner)  # Display the winner's name on the canvas
    visualize_selection(attendees, winner)
    messagebox.showinfo("Winner", f"The winner is: {winner}")

# Create the main window
root = Tk()
root.title("Random Winner Selection")

# Create and place the Start button
start_button = Button(root, text="Start", command=start_selection, font=("Arial", 16), bg="green", fg="white")
start_button.pack(pady=20)

# Create and place the Label
label = Label(root, text="Press 'Start' to select a random winner", font=("Arial", 14))
label.pack(pady=10)

# Create a canvas for the loading screen animation
canvas = Canvas(root, width=400, height=200)
canvas.pack()

# Create a label for displaying names during loading animation
loading_label = canvas.create_text(200, 100, text="", font=("Arial", 24))

# Run the GUI event loop
root.mainloop()

