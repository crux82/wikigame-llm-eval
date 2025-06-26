#!/bin/bash
set -e

# Create output folders if they do not exist
test -d statistics || mkdir statistics
test -d results || mkdir results

# Step 1: Generate human statistics
echo "[1/3] Generating human statistics..."
python3 get_statistics_dataset_complete_wikigame.py

# Step 2: Create the paper dataset
echo "[2/3] Creating paper dataset..."
python3 create_dataset_paper_wikigame.py

# Step 3: Run LLM experiments
echo "[3/3] Running LLM experiments..."
python3 get_result_paper_wikigame.py

echo "Pipeline completed. Output in ./results/results_wikigame.xlsx"
