import random
import pandas as pd

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
