#!/usr/bin/python3

from Bio import SeqIO
import os

def create_cds_dataframe(fasta_dir):
    """Creates a DataFrame from all CDS FASTA files in a directory."""

    data = []

    # Iterate over all files in the directory
    for filename in os.listdir(fasta_dir):
        # Check if the file ends with '.faa'
        if filename.endswith(".faa"):
            filepath = os.path.join(fasta_dir, filename)

            # Parse the FASTA file and extract headers and sequences
            for record in SeqIO.parse(filepath, "fasta"):
                data.append({"header": record.id, "sequence": str(record.seq)})

    return pd.DataFrame(data)


fasta_dir = "protein_fastas/"

# Create the DataFrame from the FASTA files
all_df = create_cds_dataframe(fasta_dir)
all_df.to_csv("all_dbs.tsv", sep='\t', index=False)

microbigge_df = pd.read_csv('AMR_metadata/All.tsv', sep='\t')

protein_ids = microbigge_df['Protein'].tolist()
# Remove NaN values from the list
protein_ids = [protein_id for protein_id in protein_ids if pd.notna(protein_id)]

####tring a faster way instead!
# Convert the list of protein IDs to a set for faster lookup
#protein_id_set = set(protein_ids)

# Filter rows where the header contains an exact match for any protein ID
# Here, we use a list comprehension to find headers that exactly match any protein ID from the set
#amr_df = all_df[all_df['header'].apply(lambda x: any(protein_id == x for protein_id in protein_id_set))]

# Get non-matching rows
non_matching_df = all_df[~all_df.index.isin(amr_df.index)]

# Save matching sequences to a TSV file
amr_df.to_csv("amr_sequences.tsv", sep='\t', index=False)

# Save non-matching sequences to another TSV file
non_matching_df.to_csv("non_amr_sequences.tsv", sep='\t', index=False)
