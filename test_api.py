import requests

response = requests.get(
    "http://localhost:8000/blast/search",
    json={"seq_id": "8332116"}
)

results = response.json()
print(results)

response = requests.get(
    "http://localhost:8000/protbert/inference",
    json={"prot_seq": "ATTTTCCCGAACGGTTTGCCAAATGCGCGC"}
)

results = response.json()
print(results)
