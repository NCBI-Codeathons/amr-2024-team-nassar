# Deciphering self-resistance genes in microbial biosynthetic gene clusters to combat AMR

Team Nassar Members:
- Maaly Nassar (Team Leader), Elsevier
- Parul Sharma (Flex Lead), Emory University, Atlanta-GA, USA
- Dae-young Kim (Technical Lead), Children's National Hospital, Washington D.C., USA
- Madeline Galac (Writer Lead), NIAID BCBB, Washington DC, USA
- Brendan Jeffrey, NIAID BCBB, Corvallis, OR, USA

## Project Goals
Antimicrobial resistant treatments were mostly focused on discovering new antimicrobial drugs (e.g. BGCs by-products) or mutating antimicrobial resistance genes (AMR genes) and mechanisms towards losing their function (i.e. loss of function). Thus, the goal of this project is to:
1. Identify self-resistant (SR) genes in antimicrobial-producing microorganisms along with their mechanisms and regulators in literature and corresponding whole genome sequences using Large Language models (LLMs).
2. Fine-tune machine learning models (e.g. transformers or LLMs) to identify AMR and SR genes in whole genome sequences using NCBI [pathogen](https://www.ncbi.nlm.nih.gov/pathogens/), [isolates](https://www.ncbi.nlm.nih.gov/pathogens/isolates/), [MicroBIGG-E](https://www.ncbi.nlm.nih.gov/pathogens/microbigge/) and LLM-derived SR dataset.
3. Use AMR detection ML model to identify self-resistance genes and SR detection model to identify AMR genes to check for horizontal gene transfer and the possibility of AMR up-/downregulation by SR regulators

## Deliverables
- ML classifier for AMR genes using NCBI pathogen dataset
- Self-resistance microbial genes with their related accessions, self-resistance mechanisms, self-resistance compounds and microbes using few-shot LLM prompting and [GraphRAG](https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/)

## Results
#### [LLM-derived self-resistance entities](https://github.com/NCBI-Codeathons/amr-2024-team-nassar/tree/main/ai)
- PMC full text were retrieved for the 150 self-resistance pubmed abstracts retrieved by Leroy. Then, splitted into introduction, method, results and discussion sections with their corresponding sentences
- All sections were annotated with [EMERALD BGCs pipeline](https://gitlab.com/maaly7/emerald_bgcs_annotations) to identify BGCs genes, accessions, actions, compounds and classes
- llama 70B instruct model was then used to identify self-resistance genes, proteins, mechanism, regulators, accession and organisms in BGCs annotated sentences using few-shot prompting
#### Identifying genes to use in machine language models
We selected a list of bacterial genomes to build our model on by focusing on the ESKAPE pathogens (*Enterococcus faecium, Staphylococcus aureus, Klebsiella 
pneumoniae, Acinetobacter baumannii, Pseudomonas aeruginosa and Enterobacter spp.*) and those with complete genomes from the [NCBI Pathogen Detection Isolate Browser](https://www.ncbi.nlm.nih.gov/pathogens/isolates/) . The protein sequences in these genomes were then categorized as AMR or non-AMR using the [NCBI Pathogen Detection Microbial Browser for Identification of Genetic and Genomic Elements (MicroBIGG-E)](https://www.ncbi.nlm.nih.gov/pathogens/microbigge/).

## Future Work

## NCBI Codeathon Disclaimer
This software was created as part of an NCBI codeathon, a hackathon-style event focused on rapid innovation. While we encourage you to explore and adapt this code, please be aware that NCBI does not provide ongoing support for it.

For general questions about NCBI software and tools, please visit: [NCBI Contact Page](https://www.ncbi.nlm.nih.gov/home/about/contact/)
