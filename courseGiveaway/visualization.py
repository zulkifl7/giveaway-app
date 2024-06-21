import matplotlib.pyplot as plt

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
