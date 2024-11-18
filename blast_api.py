from Bio import Blast
from io import BytesIO
import json
import zipfile
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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

                # FIXME: hard-coded here just for demo 
                d = d["BlastOutput2"]["report"]["results"]["search"]
                d["hits"] = d["hits"][:5]

                # FIXME: save in local json file for debugging
                with open(fname, "w") as f:
                    json.dump(d, f, indent=4)

                return d
            

        
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
    print('start query: ')
    blast = BlastAPI('DIT18@pitt.edu')
    results = blast.search_sequence(sequence_id)
    return results

# Initialize FastAPI app
app = FastAPI(
    title="BLAST Search API",
    description="API for performing BLAST search",
    version="1.0.0"
)

# Define request model
class BlastSearchRequest(BaseModel):
    seq_id: str

@app.get("/blast/search")
async def api_blast_search(request: BlastSearchRequest):
    """
    API endpoint to perform BLAST search
    
    Args:
        request: BlastSearchRequest containing sequence_id
        
    Returns:
        JSON: BLAST search results
    """
    try:
        print(request.seq_id)
        results = run_blast_search(request.seq_id)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # For local development, you can use uvicorn to run the API
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)