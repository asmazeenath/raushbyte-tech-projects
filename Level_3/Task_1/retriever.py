# rag/retriever.py

import os
import chromadb


CHROMA_PATH = "chroma_db"

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


def get_collection():

    try:
        return client.get_collection(
            name="environmental_knowledge"
        )

    except Exception:

        return client.create_collection(
            name="environmental_knowledge"
        )


def retrieve_scientific_evidence(query, top_k=5):

    collection = get_collection()

    try:

        results = collection.query(
            query_texts=[query],
            n_results=top_k
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        evidence = []

        for doc, metadata in zip(documents, metadatas):

            evidence.append({
                "text": doc,
                "source": metadata.get(
                    "source",
                    "Scientific knowledge base"
                ),
                "title": metadata.get(
                    "title",
                    "Environmental research"
                )
            })

        return evidence

    except Exception as e:

        return [{
            "text": f"Knowledge retrieval error: {e}",
            "source": "System",
            "title": "Retrieval error"
        }]