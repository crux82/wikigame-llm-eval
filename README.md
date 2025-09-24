## WikiGame LLM Evaluation Pipeline

This repository contains a full, reproducible pipeline to evaluate Large Language Models (LLMs) on the WikiGame (Wikipedia Speedrun) task. The pipeline automates data preparation, experiment execution, and result collection via `main.sh`.

### Why WikiGame?
Wikipedia can be modeled as a directed graph of articles and hyperlinks. The WikiGame challenges an agent to navigate from a start page to a target page by following valid internal links. This task probes:
- **Structural knowledge**: Does the model know which links truly exist between pages?
- **Reasoning and planning**: Can it compose multi-hop paths rather than rely on isolated fact recall?
- **Generalization vs memorization**: Do models reconstruct plausible yet invalid shortcuts, or adhere to the real graph?

The paper (`main.tex`) reports a controlled comparison between humans and multiple LLMs across increasing information settings, with success rate, error types, and path efficiency as core metrics.

## Research Context and Goals

- **Objective**: Assess whether LLMs internalize Wikipedia’s structure and can solve graph navigation without or with local structural cues.
- **Human baseline**: ~4,000 WikiGame sessions scraped from the public platform were analyzed to derive empirical difficulty. A 120-pair evaluation set was built by sampling 30 games from each bin: Medium, Hard, Very Hard, Impossible (Easy was excluded due to scarcity).
- **Key questions**:
  - How do models perform when “blind” to outgoing links?
  - Does stepwise reasoning help?
  - How much do explicit outgoing links reduce structural errors?

## Experimental Settings (summarized)

- **Blind (No Reasoning)**: Model sees only Start and End titles; outputs a path (titles separated by `->`).
- **Blind + Chain-of-Thought (CoT)**: As above, but the model first explains decisions step-by-step, then outputs the final path.
- **Link-Aware (Stepwise Choice)**: At each step the model is shown the real outgoing links from the current page and must pick exactly one. Output is only the chosen title, no reasoning.

Full prompt templates are included in `main.tex` (Appendix) and mirrored in the project’s `prompts.py`.

## Models Evaluated (paper)

- **OpenAI GPT-4 family**: `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano`, `gpt-4o-mini` (temperature 0 for reproducibility).
- **Open-weight**: Llama 3.1-8B-Instruct (greedy decoding on local GPU).

## Key Results (high level)

- **Success rate**:
  - In Blind settings, only the largest model (GPT-4.1) approaches or matches human performance on easier bins; performance declines with model size.
  - In Link-Aware mode, access to outgoing links dramatically boosts accuracy for GPT models; GPT-4.1 reaches near-perfect (up to 100%) even on the hardest tasks. Llama 3.1-8B benefits less.
- **Dominant error mode (Blind/CoT)**: **Invalid links** (transitions between two real pages without an actual hyperlink). Hallucinated pages are rarer (<10% for most models/settings).
- **Effect of CoT**: Mixed. It seldom reduces invalid links and can sometimes increase them (overgeneration) in smaller models; helps in specific cases for Llama.
- **Navigation efficiency**: Blind paths are often shorter than human paths but frequently rely on invalid shortcuts. Link-Aware paths are longer but structurally valid and closer to human-like navigation.

These findings suggest large LLMs internalize broad aspects of Wikipedia’s structure but still possess “patchy” global maps. Providing explicit link context closes most gaps, particularly for larger GPT variants.

## Pipeline Overview

`main.sh` orchestrates three steps:

1. **Generate Human Statistics**
   - Script: `get_statistics_dataset_complete_wikigame.py`
   - Input: `./dataset/dataset_wiki_game_complete.json`
   - Output: `./statistics/wikigame_statistics.xlsx`
   - Description: Computes human performance stats and difficulty bins.

2. **Create Paper Dataset**
   - Script: `create_dataset_paper_wikigame.py`
   - Input: `./statistics/wikigame_statistics.xlsx`
   - Output: `./dataset/dataset_paper.json`
   - Description: Builds the 120 start–goal pairs stratified by difficulty.

3. **Run LLM Experiments**
   - Script: `get_result_paper_wikigame.py`
   - Input: `./dataset/dataset_paper.json`
   - Output: `./results/results_wikigame.xlsx`
   - Description: Evaluates models under the three settings; collects success, path length, and error metrics.

All intermediate and final artifacts are saved under `statistics`, `dataset`, and `results`.

## Setup

### Prerequisites

- **Python 3.8+**
- **pip**
- **Internet connection** (Wikipedia API and LLM endpoints)

### Install

1. Clone the repository:
   ```bash
   git clone https://github.com/crux82/wikigame-llm-eval.git
   cd wikigame-llm-eval
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   If needed, ensure the following are available: `pandas`, `requests`, `beautifulsoup4`, `openpyxl`.

3. Configure API keys and endpoints in `api_key.py`:
   ```python
   GPT_API_KEY = "Bearer sk-..."
   LLAMA_ENDPOINT_URL = "http://ip:port/endpoint"
   ```
   - `GPT_API_KEY`: your OpenAI key with the `Bearer ` prefix.
   - `LLAMA_ENDPOINT_URL`: your local/remote Llama 3.1-8B endpoint.

   Important: the pipeline will not run without valid credentials.

## Usage

Run the full pipeline:

```bash
bash main.sh
```

Outputs:
- Results spreadsheet: `./results/results_wikigame.xlsx`
- Intermediate stats: `./statistics/wikigame_statistics.xlsx`
- Evaluation set: `./dataset/dataset_paper.json`

You can adjust the number of games, max steps, and other parameters in `settings.py`.

## Implementation Notes

- Wikipedia utilities are in `wikigametools.py`, including:
  - `is_disambiguation_page(title)`
  - `get_internal_links_from_article(title)`
  - `get_all_visible_existing_internal_links(title, steps)`
- Prompts for the three settings are specified in `main.tex` (Appendix) and programmatically constructed in `prompts.py`.
- The pipeline enforces strict output formats to automatically parse model responses and compute metrics.

## Project Structure
- `main.sh` — Main pipeline script
- `get_statistics_dataset_complete_wikigame.py` — Human statistics extraction
- `create_dataset_paper_wikigame.py` — Dataset creation for LLM evaluation
- `get_result_paper_wikigame.py` — LLM experiment runner
- `wikigametools.py` — Wikipedia parsing and link utilities
- `prompts.py` — Prompt templates and constructors
- `api_key.py` — API keys and endpoint configuration
- `settings.py` — Experiment settings
- `dataset/` — Input and intermediate datasets
- `statistics/` — Output folder for statistics
- `results/` — Output folder for experiment results

## Interpreting Results (guide)

- **Success Rate**: fraction of tasks where the model reaches the goal via valid links.
- **Invalid Link Rate**: path contains at least one step between existing pages without an actual hyperlink (dominant Blind error).
- **Invalid Page Rate**: path contains at least one non-existent page (rarer).
- **Avg Path Length (± st.dev.)**: computed over successful paths; Blind tends to be shorter (but riskier), Link-Aware longer (but valid).

When comparing to humans: human performance drops with difficulty; large GPT models match or exceed humans primarily when link options are visible.

## Citation

If you use this repository, please cite the accompanying paper:
```
coming soon
```

Links to dataset artifacts and the camera-ready paper will be added upon publication.
