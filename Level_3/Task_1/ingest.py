# rag/ingest.py

import os
import chromadb


CHROMA_PATH = "chroma_db"
KNOWLEDGE_PATH = "knowledge_base"


client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


collection = client.get_or_create_collection(
    name="environmental_knowledge"
)


def ingest_documents():

    if not os.path.exists(KNOWLEDGE_PATH):

        print("knowledge_base folder not found.")

        return

    documents = []
    metadatas = []
    ids = []

    counter = 0

    for filename in os.listdir(KNOWLEDGE_PATH):

        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(
            KNOWLEDGE_PATH,
            filename
        )

        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as file:

            text = file.read()

        # Split large documents
        chunk_size = 1200

        for start in range(
            0,
            len(text),
            chunk_size
        ):

            chunk = text[start:start + chunk_size]

            if len(chunk.strip()) < 50:
                continue

            documents.append(chunk)

            metadatas.append({
                "source": filename,
                "title": filename.replace(
                    ".txt",
                    ""
                )
            })

            ids.append(
                f"doc_{counter}"
            )

            counter += 1

    if documents:

        collection.upsert(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

        print(
            f"Successfully indexed {len(documents)} chunks."
        )

    else:

        print(
            "No documents found."
        )


if __name__ == "__main__":
    ingest_documents()