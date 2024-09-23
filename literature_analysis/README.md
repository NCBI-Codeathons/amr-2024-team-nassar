# Literature Analysis on Self-Resistance Genes
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
We need keyword to search relevant articles from PubMed. For example, when we want to retrieve literature search result with combinations of these keywords in abstract part:
- Self-resistance
- Regulators
- Genome

The query will be:
```SQL
(self-resistance[Abstract]AND regulators[Abstract]) OR (self-resistance[Abstract]AND Genome[Abstract])
```

**Please let me know the list of keywords to narrow down the search research enough and from where we should search for the keywords.**

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