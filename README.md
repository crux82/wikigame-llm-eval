# WikiGame LLM Evaluation Pipeline

Official companion repository for the CLiC-it 2025 paper:
“Evaluating Large Language Models on Wikipedia Graph Navigation: Insights from the WikiGame”.
This repository provides a reproducible benchmark to evaluate LLMs on Wikipedia graph navigation and compare them to humans.

Many thanks to [**Daniele Margiotta**](https://scholar.google.it/citations?user=3lyUOPgAAAAJ&hl=it), the major contributor of this pipeline.

## Table of Contents
- [Introduction](#introduction)
  - [What is the WikiGame?](#what-is-the-wikigame)
  - [Why a Pipeline (and Prompt Templates)?](#why-a-pipeline-and-prompt-templates)
  - [What’s Inside](#whats-inside)
- [Experiment Details](#experiment-details)
- [Setup](#setup)
- [Usage](#usage)
- [Citation](#citation)
- [License](#license)
- [Contact](#contact)

## Introduction
This repository accompanies the CLiC-it 2025 paper and provides the full experimental pipeline used in the study.  
Its purpose is to provide a **reproducible benchmark** for evaluating Large Language Models (LLMs) on the WikiGame - a task that requires not only factual recall, but also **structural reasoning**, **multi-hop navigation**, and adherence to the real hyperlink graph of Wikipedia.


### What is the WikiGame?
The [WikiGame](https://www.thewikigame.com/) (also known as Wikipedia Speedrun or Wikirace) is a challenge where the objective is to navigate from a start Wikipedia page to a target page by clicking only valid internal hyperlinks.  
This probes:
- **Structural knowledge**: do models know which links actually exist?
- **Multi-hop reasoning & planning**: can they compose paths rather than rely on isolated fact recall?
- **Generalization vs. memorization**: do they invent plausible but invalid shortcuts or adhere to the real graph?

### Why a Pipeline (and Prompt Templates)?
Evaluating LLMs on the WikiGame is not a standard benchmark. The pipeline is needed to:
- Derive a human baseline and difficulty bins from ~4,000 real games.
- Build a stratified, cost-manageable evaluation set (120 start--goal pairs).
- Run models under three controlled settings (Blind, Blind+CoT, Link-Aware) with strict, parseable outputs.
- Validate model paths against Wikipedia to detect invalid links vs nonexistent pages.
- Provide consistent prompts to guarantee comparability across models and runs.

### What’s Inside
- **Datasets**: human gameplay logs (~4,000 sessions) and a curated set of 120 start--goal pairs.
- **Pipeline scripts**: for preprocessing, dataset construction, and controlled LLM experiments.
- **Prompt templates**: for Blind, Blind+Chain-of-Thought, and Link-Aware settings (in `prompts.py`).
- **Evaluation framework**: strict output formats + automatic parsing; metrics include success rate, invalid link/page rates, and path length.
- **Results**: reproducible spreadsheets and analysis artifacts aligned with the paper.

---

## Experiment Details

**Experimental Settings**
- **Blind (No Reasoning)**: Start/End only; output path as `Title1 -> Title2 -> ...`.
- **Blind + Chain-of-Thought (CoT)**: explain reasoning, then output final path.
- **Link-Aware (Stepwise Choice)**: at each step, see the real outgoing links and pick exactly one; output only the chosen title.

**Models Evaluated**
- **OpenAI GPT-4 family**: `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano`, `gpt-4o-mini`.
- **Open-weight**: Llama 3.1-8B-Instruct (greedy decoding on local GPU).

**Pipeline Overview**
The evaluation workflow is organized in three sequential stages. Each stage consumes the output of the previous one and produces standardized artifacts for the next step.

| Step                      | Script                                   | Input → Output                              |
|---------------------------|------------------------------------------|---------------------------------------------|
| Generate Human Statistics | `get_statistics_dataset_complete_wikigame.py` | `dataset_wiki_game_complete.json` → `wikigame_statistics.xlsx` |
| Create Paper Dataset      | `create_dataset_paper_wikigame.py`       | `wikigame_statistics.xlsx` → `dataset_paper.json` |
| Run LLM Experiments       | `get_result_paper_wikigame.py`           | `dataset_paper.json` → `results_wikigame.xlsx` |

This design makes the pipeline modular: users can either run the full process end-to-end or execute individual steps depending on their needs.

---

## Setup

### Prerequisites
- Python 3.8 or later
- pip
- Internet connection (Wikipedia API + LLM endpoints)

### Install
```bash
git clone https://github.com/crux82/wikigame-llm-eval.git
cd wikigame-llm-eval
pip install -r requirements.txt
```

### Configure Credentials
Credentials can be set in `api_key.py` or via environment variables:

```bash
# .env (example)
OPENAI_API_KEY=sk-...
LLAMA_ENDPOINT_URL=http://ip:port/endpoint
```
---

## Usage

### Quick Start
To execute the entire pipeline end-to-end:
```bash
bash main.sh
```
This will compute human statistics, create the paper dataset of 120 start--goal pairs, and run the LLM experiments under all settings.

### Run Individual Steps
Each step can also be run separately:
```bash
# Compute human statistics
python get_statistics_dataset_complete_wikigame.py

# Build evaluation dataset
python create_dataset_paper_wikigame.py

# Run LLM experiments
python get_result_paper_wikigame.py
```

### Configurable Parameters
- Number of games, maximum steps per path, and model decoding options are defined in `settings.py`.
- API credentials must be set before running experiments.

### Outputs
Running the pipeline will produce:
- `./statistics/wikigame_statistics.xlsx` — human baseline statistics and difficulty bins.
- `./dataset/dataset_paper.json` — stratified evaluation set of 120 start--goal pairs.
- `./results/results_wikigame.xlsx` — aggregated model performance results.

### Tips for Reproducibility
- Use `temperature = 0` (OpenAI) or greedy decoding (open-weight models) for deterministic outputs.
- Do not alter the prompt templates: the parser requires strict output formats.
- Consider caching Wikipedia API calls to ensure consistency across runs.

---

## Citation
If you find this repository usefull, please cite the accompanying paper:
```
@inproceedings{margiotta2025wikigame,
  author    = {Daniele Margiotta and Danilo Croce and Roberto Basili},
  title     = {Evaluating Large Language Models on Wikipedia Graph Navigation: Insights from the WikiGame},
  booktitle = {Proceedings of the 11th Italian Conference on Computational Linguistics (CLiC-it 2025)},
  series    = {CEUR Workshop Proceedings},
  publisher = {CEUR},
  year      = {2025},
  address   = {Cagliari, Italy},
}
```

## License
This project is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).  
See the `LICENSE` file for full details.

## Contact
For questions, feedback, or issues, please open a GitHub issue or contact me directly at **croce@info.uniroma2.it**
