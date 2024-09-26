from Bio import SeqIO
from Bio import Entrez
from Bio import GenBank
import pandas as pd
import os
from pathlib import Path


class genes:
    
    def __init__(self):
        pass
    
        
    def prodigal(self,accs,output_dir):
        
        accs_proteins = {'accession':[],'id':[],'translation':[],'text':[]}
        
        for acc in accs:
            try:
                fgenes = Path(output_dir,acc+'.genes')
                faa = Path(output_dir,acc+'.faa')
                fna = Path(output_dir,acc+'.fna')
                if not Path(faa).is_file():
                    os.system(f'wget https://www.ebi.ac.uk/ena/browser/api/fasta/{acc}?download=true -O {fna}')
                    os.system(f'prodigal -i {fna} -o {fgenes} -a {faa}')
                for index, record in enumerate(SeqIO.parse(faa, "fasta")):
                    pid = record.id.split('|')[2]
                    accs_proteins['accession'].append(acc)
                    accs_proteins['id'].append(pid.split('_')[1].zfill(5))
                    accs_proteins['translation'].append(str(record.seq))
                    accs_proteins['text'].append(' '.join(str(record.seq))+'.')
            except:
                print(f'Prodigal failed to identify genes in {acc}')
                pass
            
        return pd.DataFrame(accs_proteins)    
        
        
        
    def genbank(self,accs):
        
        accs_proteins = {'accession':[],'id':[],'locus_tag':[],'gene':[],'product':[],'protein_id':[],'translation':[],'text':[]}
        
        for acc in accs:
            try:
                Entrez.email = "maaly13@yahoo.com"
                handle = Entrez.efetch(db="nuccore", id=acc, rettype="gb", retmode="text")
                for index, record in enumerate(SeqIO.parse(handle, "genbank")):
                    print(record.id)
                    g = 0
                    for ft in record.features:
                        qls = dict(ft.qualifiers)

                        if 'translation' in qls.keys():
                            accs_proteins['accession'].append(record.id)
                            accs_proteins['id'].append(str(g).zfill(5))
                            accs_proteins['locus_tag'].append(qls['locus_tag'][0]) if 'locus_tag' in qls.keys() else accs_proteins['locus_tag'].append(None)
                            accs_proteins['gene'].append(qls['gene'][0]) if 'gene' in qls.keys() else accs_proteins['gene'].append(None)
                            accs_proteins['product'].append(qls['product'][0])
                            accs_proteins['protein_id'].append(qls['protein_id'][0])
                            accs_proteins['translation'].append(qls['translation'][0])
                            accs_proteins['text'].append(' '.join(qls['translation'][0]))
                            g +=1
            except:
                print(f'No genes were annotated in genbank for this accession {acc}')
                        
        return pd.DataFrame(accs_proteins)
    
    


