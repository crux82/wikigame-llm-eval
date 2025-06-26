# WikiGame LLM Evaluation Pipeline

This project provides a pipeline to evaluate Large Language Models (LLMs) on the WikiGame (Wikipedia Speedrun) task. The process is fully automated via the `main.sh` script, which orchestrates data preparation, experiment execution, and result collection.

## Prerequisites

- **Python 3.8+**
- **pip** (for installing dependencies)
- **Internet connection** (for Wikipedia API and LLM endpoints)

## Setup

1. **Clone the repository** (if not already done):
   ```bash
   git clone https://github.com/crux82/wikigame-llm-eval.git
   cd wikigame-llm-eval
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *(If `requirements.txt` is missing, install: pandas, requests, beautifulsoup4, openpyxl)*

3. **Configure API keys and endpoints:**
   - Open the file `api_key.py`.
   - Insert your OpenAI API key in the `GPT_API_KEY` variable (format: `Bearer sk-...`).
   - Insert your LLAMA endpoint URL in the `LLAMA_ENDPOINT_URL` variable.

   **Example:**
   ```python
   GPT_API_KEY = "Bearer sk-..."
   LLAMA_ENDPOINT_URL = "http://ip:port/endpoint"
   ```

   **⚠️ The pipeline will not work without valid API keys and endpoints!**

## How the Pipeline Works

The main script (`main.sh`) executes the following steps:

1. **Generate Human Statistics**
   - Script: `get_statistics_dataset_complete_wikigame.py`
   - Input: `./dataset/dataset_wiki_game_complete.json`
   - Output: `./statistics/wikigame_statistics.xlsx`
   - Description: Processes human game data to compute statistics and prepares them for the next step.

2. **Create Paper Dataset**
   - Script: `create_dataset_paper_wikigame.py`
   - Input: `./statistics/wikigame_statistics.xlsx`
   - Output: `./dataset/dataset_paper.json`
   - Description: Builds a dataset of game pairs categorized by difficulty, ready for LLM evaluation.

3. **Run LLM Experiments**
   - Script: `get_result_paper_wikigame.py`
   - Input: `./dataset/dataset_paper.json`
   - Output: `./results/results_wikigame.xlsx`
   - Description: Runs the WikiGame task using various LLMs and contexts, saving all results and errors.

All intermediate and final outputs are saved in the `statistics`, `dataset`, and `results` folders.

## Usage

To run the full pipeline, simply execute:

```bash
bash main.sh
```

The final results will be available in `./results/results_wikigame.xlsx`.

## Notes
- Make sure your API keys and endpoints are valid and active.
- The process may take a while depending on the number of games and the speed of the LLM endpoints.
- You can adjust the number of games and steps in `settings.py`.

## Project Structure
- `main.sh` — Main pipeline script
- `get_statistics_dataset_complete_wikigame.py` — Human statistics extraction
- `create_dataset_paper_wikigame.py` — Dataset creation for LLM evaluation
- `get_result_paper_wikigame.py` — LLM experiment runner
- `api_key.py` — API keys and endpoint configuration
- `settings.py` — Experiment settings
- `results/` — Output folder for experiment results
- `statistics/` — Output folder for statistics
- `dataset/` — Input and intermediate datasets

## Citation
To cite the paper, please use the following:
```
coming soon
```



