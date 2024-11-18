from transformers import AutoTokenizer, AutoModel, pipeline
from Bio.Seq import Seq
import torch
import re
from scipy.spatial.distance import cosine
def generate_embeddings(dna_sequence=None, protein_seq=None):
    if dna_sequence != None:
        dna_sequence = Seq(dna_sequence)
        protein_sequence = " ".join(dna_sequence.translate())
    elif protein_seq != None:
        protein_sequence = " ".join(protein_seq)
    else:
        return None
    tokenizer = AutoTokenizer.from_pretrained("Rostlab/prot_bert", do_lower_case=False )
    model = AutoModel.from_pretrained("Rostlab/prot_bert")
    inputs = tokenizer(protein_sequence, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state  # Shape: (batch_size, seq_len, hidden_dim)

    # Aggregate embeddings (e.g., mean pooling for sequence-level representation)
    protein_embedding = embeddings.mean(dim=1).squeeze()  # Shape: (hidden_dim,)
    return protein_embedding

def predict_flurescent(seq):
    GFP = "MSKGEELFTGVVPILVELDGDVNGHKFSVSGEGEGDATYGKLTLKFICTTGKLPVPWPTLVTTFSYGVQCFSRYPDHMKQHDFFKSAMPEGYVQERTIFFKDDGNYKTRAEVKFEGDTLVNRIELKGIDFKEDGNILGHKLEYNYNSHNVYIMADKQKNGIKVNFKIRHNIEDGSVQLADHYQQNTPIGDGPVLLPDNHYLSTQSALSKDPNEKRDHMVLLEFVTAAGITHGMDELYK"
    e1 = generate_embeddings(dna_sequence=seq)
    e2 = generate_embeddings(protein_seq=GFP)
    return cosine(e1, e2)

def main(dna_sequence):
    score = predict_flurescent(dna_sequence)
    print(score)
    return score

if __name__ == "__main__":
    main('ATTCGAATTTTTTTAAAAAGCGCTCTACTCTGCTGAAAAACCCCTTGACGACGACGTGTGTGTGTGTCACCACAGGGTTTTT')

