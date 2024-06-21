import webbrowser
import urllib.parse
import time
import pyautogui

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

    # Wait for the browser to load 
    time.sleep(10)

    pyautogui.press('enter')  # Press enter to send the message
