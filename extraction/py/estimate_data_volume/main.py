import json
import os

def estimate_one_row_data_size() -> float:

    # Sample data in dictionary format for JSON conversion
    sample_data = {
        "pitch_type": "SI",
        "game_date": "2020-09-18T00:00:00.000+0000",
        "release_speed": 91.4,
        "release_pos_x": 1.83,
        "release_pos_z": 4.81,
        "player_name": "Sherriff, Ryan",
        "batter": 600524,
        "pitcher": 595411,
        "events": "NaN",
        "description": "called_strike"
    }

    # Convert dictionary to JSON and save to a file
    json_path = "sample_pitch_data.json"
    with open(json_path, 'w') as json_file:
        json.dump(sample_data, json_file)

    # Get the size of the file
    file_size = os.path.getsize(json_path)

    # Remove the file
    os.remove(json_path)
    return file_size


def estimate_records_per_second_active_play(row_size: int, total_size_tb: float, game_length_seconds: int, active_play_ratio: float = 0.5) -> float:
    """
    Estimate the number of records processed per second during active play.

    Args:
    row_size (int): Size of one row of data in bytes.
    total_size_tb (float): Total size of data for one game in terabytes.
    game_length_seconds (int): Average game duration in seconds.
    active_play_ratio (float): Fraction of the game duration that is active play.

    Returns:
    float: Estimated number of records per second during active play.
    """
    # Convert total size from terabytes to bytes
    total_size_bytes = total_size_tb * (10**12)
    
    # Adjust game length to only account for active play
    active_play_seconds = game_length_seconds * active_play_ratio
    
    # Calculate the number of records
    number_of_records = total_size_bytes / row_size
    
    # Calculate records per second during active play
    records_per_second = number_of_records / active_play_seconds
    
    return records_per_second


def main():
    # Estimate the size of one row of data
    one_row_size = estimate_one_row_data_size()

    TOTAL_DATA_SIZE_TB = 7.0
    # Total game duration in seconds (3 hours)
    GAME_LENGTH_SECONDS = 3 * 60 * 60
    # Assuming active play is about 50% of the total game time
    ACTIVE_PLAY_RATIO = 0.5
    
    # Calculate the average records per second during active play
    avg_records_per_sec = estimate_records_per_second_active_play(one_row_size, TOTAL_DATA_SIZE_TB, GAME_LENGTH_SECONDS, ACTIVE_PLAY_RATIO)
    
    # Print the result
    print(f"Average records per second during active play: {avg_records_per_sec:.2f}")

if __name__ == "__main__":
    main()
