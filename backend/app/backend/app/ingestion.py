
import os
import json
import uuid
from datetime import datetime
from pathlib import Path
# Configuration
RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")
OUTPUT_FILE = PROCESSED_DATA_DIR / "docs.jsonl"
def clean_text(text: str) -> str:
    """Basic normalization: remove extra whitespace and newlines."""
    return " ".join(text.split())

def ingest_documents():
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    documents = []
    supported_extensions = {'.txt', '.md'}

    print(f"--- Starting Ingestion from {RAW_DATA_DIR} ---")

    if not RAW_DATA_DIR.exists():
        print(f"Error: {RAW_DATA_DIR} not found.")
        return

    count = 0
    skipped = 0

    for file_path in RAW_DATA_DIR.rglob('*'):
        if file_path.suffix not in supported_extensions:
            continue

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # skip empty or very short files
            if len(content.strip()) < 500:
                skipped += 1
                continue

            doc = {
                "doc_id": str(uuid.uuid4())[:8],
                "title": file_path.stem.replace('_', ' ').title(),
                "text": clean_text(content),
                "source": str(file_path.relative_to(RAW_DATA_DIR)),
                "created_at": datetime.now().isoformat()
            }

            documents.append(doc)
            count += 1
            print(f"[{count}] Processed: {file_path.name}")

        except Exception as e:
            print(f"Failed to process {file_path}: {e}")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for doc in documents:
            f.write(json.dumps(doc) + '\n')

    print(f"--- Done: {count} saved, {skipped} skipped → {OUTPUT_FILE} ---")

if __name__ == "__main__":
    ingest_documents()
