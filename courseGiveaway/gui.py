import threading
import time
import ttkbootstrap as ttk
from tkinter import messagebox

from data_processing import read_attendees_from_csv, select_winner
from visualization import visualize_selection
from automation import send_whatsapp_message

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

def show_loading_and_selection(attendees, canvas, loading_label, root):
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

def start_selection(canvas, loading_label, root):
    """
    Initiates the process of selecting a random winner from attendees.
    Reads attendee data from a CSV file, shows a loading screen, and then displays the winner.
    """
    attendees = read_attendees_from_csv('attendees.csv')
    if attendees:
        threading.Thread(target=show_loading_and_selection, args=(attendees, canvas, loading_label, root)).start()  # Start loading screen animation in a separate thread
    else:
        messagebox.showwarning("No Attendees", "No attendees found in the CSV file.")

# Main GUI setup and event loop
if __name__ == "__main__":
    # Create the main window with ttkbootstrap style
    root = ttk.Window(themename="journal")
    root.title("Random Winner Selection")
    root.geometry("600x400")

    # Set transparency level (0-1, 0 being fully transparent)
    root.attributes('-alpha', 1)

    # Create and place the Start button with modern style
    start_button = ttk.Button(root, text="Start", command=lambda: start_selection(canvas, loading_label, root), style="success.TButton", width=20)
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
