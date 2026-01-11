# Simple Mock RAG for POC
# In a real app, this would use ChromaDB or Qdrant

MOCK_CORPUS = [
    {
        "id": 1,
        "content": "La chimiothérapie est un traitement qui utilise des médicaments pour détruire les cellules cancéreuses. Elle peut causer la chute des cheveux (alopécie), la fatigue, et des nausées. Ce n'est pas automatique pour tout le monde."
    },
    {
        "id": 2,
        "content": "La radiothérapie utilise des rayons à haute énergie pour tuer les cellules cancéreuses. Elle est souvent localisée et fatigue moins que la chimio, mais peut irriter la peau."
    },
    {
        "id": 3,
        "content": "Le casque réfrigérant peut aider à réduire la chute des cheveux pendant la chimiothérapie en réduisant le flux sanguin vers le cuir chevelu."
    },
    {
        "id": 4,
        "content": "La fatigue est le symptôme le plus courant. Il est important de se reposer et de demander de l'aide pour les tâches quotidiennes."
    }
]

def retrieve_context(query: str):
    # Very naive keyword search for POC
    query = query.lower()
    relevant_chunks = []
    
    keywords = query.split()
    for doc in MOCK_CORPUS:
        score = 0
        for word in keywords:
            if word in doc['content'].lower():
                score += 1
        
        if score > 0:
            relevant_chunks.append(doc['content'])
    
    if relevant_chunks:
        return "\n".join(relevant_chunks)
    return ""
