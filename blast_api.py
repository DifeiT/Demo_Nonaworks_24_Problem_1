from Bio import Blast
from io import BytesIO
import json
import zipfile

class BlastAPI:
    def __init__(self, email: str):
        """Initialize the BLAST API with user email"""
        Blast.email = email
        #Blast.help = help(Blast.qblast)

    def parse_blast_zip(self, zip_data: bytes):
        """Parse multiple JSON files from the BLAST result as it may contain large sequences."""
        with BytesIO(zip_data) as bio:
            with zipfile.ZipFile(bio) as zf:
                # Optional: identify main data file by BLAST naming convention 
                metadata_file = next(f for f in zf.namelist() if f.endswith('_1.json'))
                
                # save to json files
                # for fname in zf.namelist():
                fname = metadata_file
                stream = zf.open(fname)
                data = stream.read().decode()
                d = json.loads(data)

                with open(fname, "w") as f:
                    json.dump(d, f, indent=4)
        
    def search_sequence(
        self,
        sequence_id: str,
        program: str = "blastn",
        database: str = "nt",
        format_type: str = "JSON2"
    ) -> dict:
        """
        Perform a BLAST search and return results.
        
        Args:
            sequence_id: The sequence ID to search
            program: BLAST program to use (default: blastn)
            database: Database to search against (default: nt)
            format_type: Output format (default: JSON2)
            
        Returns:
            dict: BLAST results in JSON format
        """

        #TODO: support more arguments for qblast function  

        result_stream = Blast.qblast(program, database, sequence_id, format_type=format_type)
        zip_data = result_stream.read()
        return self.parse_blast_zip(zip_data)

def run_blast_search(sequence_id: str):
    """
    Wrapper function to perform BLAST search.
    
    Args:
        sequence_id: The sequence ID to search
    """
    blast = BlastAPI('DIT18@pitt.edu')
    results = blast.search_sequence(sequence_id)
    return results

if __name__ == "__main__":
    # test 
    print("start testing:")
    run_blast_search("8332116")