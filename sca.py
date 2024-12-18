import emoji

def print_winners_podium(data):
    """
    Prints a winners' podium using a step-like visualization.
    Data format: [{'name': 'Alice', 'score': 95}, {'name': 'Bob', 'score': 85}, ...]
    """
    # Sort data by score (descending)
    sorted_data = sorted(data, key=lambda x: x['score'], reverse=True)

    # Extract top 3 winners (or fewer if there are not enough participants)
    top_winners = sorted_data[:3]

    # Create podium heights for top 3
    heights = [3, 2, 1]  # First place has the tallest step
    podium_steps = ["🥇", "🥈", "🥉"]
    podium = []

    # Build the podium visual representation
    for i, winner in enumerate(top_winners):
        # Create step height with name and score
        step = f"{' ' * (3 - heights[i])}{podium_steps[i]} {winner['name']} ({winner['score']})"
        podium.append((heights[i], step))

    # Adjust formatting to align steps
    max_height = max(height for height, _ in podium)
    podium_representation = []
    for height, step in podium:
        spaces = " " * (max_height - height)
        podium_representation.append(f"{spaces}{step}")

    # Print podium
    print("\n🏆 Winners' Podium 🏆")
    print("\n".join(podium_representation))

    # Print the rest of the participants
    if len(sorted_data) > 3:
        print("\n🎖️ Honorable Mentions 🎖️")
        for i, participant in enumerate(sorted_data[3:], start=4):
            print(f"{i}. {participant['name']} ({participant['score']})")

    print("\n✨ Celebrate the Champions! ✨")


# Example data
participants = [
    {'name': 'Alice', 'score': 95},
    {'name': 'Bob', 'score': 85},
    {'name': 'Charlie', 'score': 90},
    {'name': 'Diana', 'score': 80},
    {'name': 'Eve', 'score': 75},
]

# Print the winners' podium
print_winners_podium(participants)
