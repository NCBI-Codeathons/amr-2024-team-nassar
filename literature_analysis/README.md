# Literature Analysis on Self-Resistance Genes
## Check List
- [x] PubMed keyword selection
- [ ] Data Collection
- [ ] Model Training
## Main Deliverables
Identification of
- Self-resistance genes,
- Their regulators and
- Whole genome/ Biosynthetic Gene Clusters (BCGs) accession numbers.
## Training Dataset
- [BGC DISCOVERY FOR T CELL IMMUNOLOGY](https://gitlab.com/maaly7/bgc_discovery_for_t_cell_immunology)
- [bgc_discovery_for_t_cell_immunology / data / training_dataset /emerald/ner_annotations.csv](https://gitlab.com/maaly7/bgc_discovery_for_t_cell_immunology/-/blob/master/data/training_dataset/emerald/ner_annotations.csv?ref_type=heads)
## Implementation Strategy
### Keyword Selection
We need keyword to search relevant articles from PubMed.

PubMed Query:
```SQL
"self-resistance" AND "gene" [TIAB]
```

### Data Collection
1. Download relative papers from [PubMed PMC](https://www.ncbi.nlm.nih.gov/pmc/tools/developers/).
2. Create list of files with method parts of the downloaded papers.
3. Do data cleaning if needed.

### Model Training
1. Select an LLM.
   - Maybe from this [LLM Leader board best models](https://huggingface.co/collections/open-llm-leaderboard/llm-leaderboard-best-models-652d6c7965a4619fb5c27a03)?
   - Since @maaly7 mentioned she has an experience with LLaMA model, I will choose on LLaMA type LLM.
2. Fine-tune the selected LLM: [Supervised Fine-tuning Trainer](https://huggingface.co/docs/trl/en/sft_trainer) with [the BGC emerald NER dataset](https://gitlab.com/maaly7/bgc_discovery_for_t_cell_immunology/-/blob/master/data/training_dataset/emerald/ner_annotations.csv?ref_type=heads).
3. Use GraphRAG or Neo4j graph builder based on the fine-tuned LLM.
4. Retrieve target entities according to [the main delieverables](#main-deliverables).

## GCP Environment Setup

### Git Installation
```bash
sudo apt-get update
sudo apt-get install git
which git /usr/bin/git

git config --global user.name "leroykim"
git config --global user.email "leroy.kim@umbc.edu"
git clone https://github.com/NCBI-Codeathons/amr-2024-team-nassar.git
```

### Virtual Environment Setup
```bash
which python3 #/usr/bin/python3
python3 --version #Python 3.11.2
sudo apt-get install python3.11-venv
cd /home/k163/codeathon/amr-2024-team-nassar/literature_analysis
python3 -m venv .venv
source .venv/bin/activate
```

### Poetry Setup
```bash
pip install --upgrade pip
pip install poetry
poetry install
```