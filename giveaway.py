import random
import pandas as pd
import matplotlib.pyplot as plt
import ttkbootstrap as ttk
from tkinter import messagebox, simpledialog
import threading
import time
import webbrowser
import urllib.parse
import pyautogui

#! Function to read attendee names and mobile numbers from a CSV file
def read_attendees_from_csv(file_path):
    """
    Reads attendee names and mobile numbers from a CSV file.

    Args:
    - file_path (str): Path to the CSV file containing attendee data.

    Returns:
    - list: A list of tuples containing attendee name and mobile number.
    """
    df = pd.read_csv(file_path)
    attendees = df[['Name', 'Mobile Number']].values.tolist()
    return attendees

#! Function to select a random winner
def select_winner(attendees):
    """
    Randomly selects a winner from a list of attendees.

    Args:
    - attendees (list): List of tuples containing attendee name and mobile number.

    Returns:
    - tuple: A tuple containing winner's name and mobile number.
    """
    winner = random.choice(attendees)
    return winner[0], winner[1]  # Return name and mobile number

#! Visual representation of the selection process using a pie chart
def visualize_selection(attendees, winner_name):
    """
    Creates a pie chart to visualize the selection probability of each attendee.

    Args:
    - attendees (list): List of tuples containing attendee name and mobile number.
    - winner_name (str): Name of the randomly selected winner.
    """
    # Count occurrences of each attendee
    counts = {attendee[0]: 0 for attendee in attendees}
    for attendee in attendees:
        counts[attendee[0]] += 1
    
    # Create labels and counts for the pie chart
    labels = list(counts.keys())
    counts = list(counts.values())
    
    # Highlight the winner's slice
    explode = [0.1 if attendee == winner_name else 0 for attendee in labels]
    
    # Create pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(counts, labels=labels, autopct='%1.1f%%', explode=explode, shadow=True, startangle=140)
    plt.title('Random Winner Selection Probability')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

#! Function to display the loading screen
def show_loading_screen(attendees, canvas, label, root):
    """
    Displays a loading animation while processing attendee data.

    Args:
    - attendees (list): List of tuples containing attendee name and mobile number.
    - canvas (tkinter.Canvas): Canvas widget for displaying loading animation.
    - label (tkinter.Text): Text object within the canvas to update with attendee names.
    - root (tkinter.Tk): Main Tkinter window object.
    """
    for _ in range(10):  # Loop to create a simple loading animation
        for name, _ in attendees:
            canvas.itemconfig(label, text=name)
            root.update_idletasks()
            time.sleep(0.1)

#! Function to start the winner selection process
def start_selection():
    """
    Initiates the process of selecting a random winner from attendees.
    Reads attendee data from a CSV file, shows a loading screen, and then displays the winner.
    """
    attendees = read_attendees_from_csv('attendees.csv')
    if attendees:
        threading.Thread(target=show_loading_and_selection, args=(attendees,)).start()  # Start loading screen animation in a separate thread
    else:
        messagebox.showwarning("No Attendees", "No attendees found in the CSV file.")

#! Function to handle loading animation and selection process
def show_loading_and_selection(attendees):
    """
    Manages the loading animation and winner selection process.
    
    Args:
    - attendees (list): List of tuples containing attendee name and mobile number.
    """
    show_loading_screen(attendees, canvas, loading_label, root)
    winner_name, winner_mobile = select_winner(attendees)
    canvas.itemconfig(loading_label, text=winner_name)  # Display the winner's name on the canvas
    visualize_selection(attendees, winner_name)
    
    # Ask user for confirmation to send WhatsApp message
    confirm_send = messagebox.askokcancel("Send WhatsApp Message", f"Send message to {winner_name} on WhatsApp?")
    
    if confirm_send:
        send_whatsapp_message(winner_mobile, winner_name)
        # Notify user that message has been sent
        messagebox.showinfo("Message Sent", f"Message sent to {winner_name} on WhatsApp.")
    else:
        messagebox.showinfo("Message Not Sent", "Message sending canceled.")

#! Function to send WhatsApp message to the winner
def send_whatsapp_message(mobile_number, winner_name):
    """
    Opens WhatsApp Web with a pre-filled message to the winner's mobile number.

    Args:
    - mobile_number (str): Mobile number of the winner.
    - winner_name (str): Name of the winner.
    """
    message = f"Hello {winner_name}, you are selected to join our 'Learn Python in 16 days' course!"

    # Encode message for URL
    encoded_message = urllib.parse.quote(message)

    # Open WhatsApp Web with pre-filled message
    webbrowser.open(f"https://web.whatsapp.com/send?phone={mobile_number}&text={encoded_message}")

    # Note: Manually sending the message is required by the user due to restrictions in automation.
    # to bypass this we are using pyauto gui for press enter

    # Wait for the browser to load (adjust sleep time as needed)
    time.sleep(10)

    pyautogui.press('enter')  # Press enter to send the message

#! Main GUI setup and event loop
# Create the main window with ttkbootstrap style
root = ttk.Window(themename="flatly")
root.title("Random Winner Selection")
root.geometry("600x400")

# Set transparency level (0-1, 0 being fully transparent)
root.attributes('-alpha', 0.9)

# Create and place the Start button with modern style
start_button = ttk.Button(root, text="Start", command=start_selection, style="success.TButton", width=20)
start_button.pack(pady=20)

# Customize button style for modern look
style = ttk.Style()
style.configure('success.TButton', foreground='white', background='#4CAF50', font=('Helvetica', 16), borderwidth=5, relief='raised', padding=10, border_radius=10)

# Create and place the Label with modern font
label = ttk.Label(root, text="Press 'Start' to select a random winner", font=("Helvetica", 14))
label.pack(pady=10)

# Create a canvas for the loading screen animation
canvas = ttk.Canvas(root, width=500, height=100)
canvas.pack(pady=20)

# Create a label for displaying names during loading animation
loading_label = canvas.create_text(250, 50, text="", font=("Helvetica", 20))

# Run the GUI event loop
root.mainloop()
