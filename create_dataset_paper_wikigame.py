import pandas as pd
import json

def classify_games_by_difficulty(excel_file_path):
    # Load the Excel sheets
    df_games = pd.read_excel(excel_file_path, sheet_name="All Game")
    df_stats = pd.read_excel(excel_file_path, sheet_name="Statistics")

    # Final dictionary organized by difficulty
    result = {
        "MEDIUM": [],
        "HARD": [],
        "VERY_HARD": [],
        "IMPOSSIBLE": []
    }

    # Iterate over each row of the "Statistics" sheet
    for _, row in df_stats.iterrows():
        from_node = row["from_node"]
        to_node = row["to_node"]
        win_percentage = row["win_percentage"]
        avg_human_step_to_win = row["avg_steps_to_win"]

        # Determine the difficulty category
        if 50 <= win_percentage <= 75:
            difficulty = "MEDIUM"
        elif 25 <= win_percentage <= 49:
            difficulty = "HARD"
        elif 1 <= win_percentage <= 24:
            difficulty = "VERY_HARD"
        elif win_percentage < 1:  # win_percentage == 0
            difficulty = "IMPOSSIBLE"
        else:
            difficulty = "SKIP"
        
        if difficulty != "SKIP":
            # Filter the corresponding games in "All Game"
            filtered_games = df_games[
                (df_games["from_node"] == from_node) & (df_games["to_node"] == to_node)
            ]

            # Extract path and won for each game
            list_path_user_with_result = [
                (row_game["path"], bool(row_game["won"])) 
                for _, row_game in filtered_games.iterrows()
            ]

            # Build the block for the pair to insert in the dictionary
            game_entry = {
                "start_node": from_node,
                "end_node": to_node,
                "avg_human_step_to_win": avg_human_step_to_win,
                "list_path_user_with_result": list_path_user_with_result
            }

            result[difficulty].append(game_entry)

    return result

# Create the dataset for the paper
json_result = classify_games_by_difficulty("./statistics/wikigame_statistics.xlsx")

# Save the dataset in a JSON file
with open("./dataset/dataset_paper.json", "w") as f:
    json.dump(json_result, f, indent=2)
