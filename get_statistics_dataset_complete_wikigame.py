import json
import pandas as pd

f = open("./dataset/dataset_wiki_game_complete.json", "r")
data = json.load(f)

# Lists to collect global data
all_matches = []
all_stats = []

# Analyze each key
for key, matches in data.items():
    if key.startswith("FROM_") and "_TO_" in key:
        start_node = key.split("_TO_")[0].replace("FROM_", "")
        end_node = key.split("_TO_")[1]

        for match in matches:
            all_matches.append({
                "from_node": start_node,
                "to_node": end_node,
                "player_name": match["player_name"],
                "path_length": len(match["path_concept"]),
                "path": " -> ".join(match["path_concept"]),
                "won": match["won"],
                "time": match["time"],
                "points": match["points"]
            })

        # Statistics for this combination
        df_temp = pd.DataFrame(matches)
        df_temp["path_length"] = df_temp["path_concept"].apply(lambda x: len(x))

        total_games = len(df_temp)
        won_games = df_temp["won"].sum()
        win_percentage = (won_games / total_games) * 100 if total_games > 0 else 0
        avg_steps_to_win = df_temp[df_temp["won"] == True]["path_length"].mean()
        avg_time_to_win = df_temp[df_temp["won"] == True]["time"].mean()

        all_stats.append({
            "from_node": start_node,
            "to_node": end_node,
            "total_games": total_games,
            "won_games": won_games,
            "win_percentage": round(win_percentage, 2),
            "avg_steps_to_win": round(avg_steps_to_win, 2) if pd.notna(avg_steps_to_win) else "N/A",
            "avg_time_to_win": round(avg_time_to_win, 2) if pd.notna(avg_time_to_win) else "N/A"
        })

# Final DataFrames
df_matches = pd.DataFrame(all_matches)
df_stats = pd.DataFrame(all_stats)

# Write to Excel
with pd.ExcelWriter("./statistics/wikigame_statistics.xlsx", engine="openpyxl") as writer:
    df_matches.to_excel(writer, sheet_name="All Matches", index=False)
    df_stats.to_excel(writer, sheet_name="Statistics", index=False)

print("Excel generated: 'wikigame_statistics.xlsx'")