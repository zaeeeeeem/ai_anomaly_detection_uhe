import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.services.rag_service import rag_service
import pypdf


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    """Split text into overlapping chunks"""
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk)
        start = end - overlap

    return chunks


def process_pdf(file_path: str, doc_id: str):
    """Process a PDF file and add to vector store"""
    print(f"Processing {file_path}...")

    with open(file_path, "rb") as f:
        pdf = pypdf.PdfReader(f)
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""

    chunks = chunk_text(text)

    documents = []
    for i, chunk in enumerate(chunks):
        documents.append(
            {
                "doc_id": doc_id,
                "chunk_id": f"chunk_{i}",
                "text": chunk,
                "metadata": {
                    "source": file_path,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                },
            }
        )

    rag_service.add_documents(documents)
    print(f"✓ Added {len(documents)} chunks from {doc_id}")


def process_text(file_path: str, doc_id: str):
    """Process a text file and add to vector store"""
    print(f"Processing {file_path}...")

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    chunks = chunk_text(text)

    documents = []
    for i, chunk in enumerate(chunks):
        documents.append(
            {
                "doc_id": doc_id,
                "chunk_id": f"chunk_{i}",
                "text": chunk,
                "metadata": {
                    "source": file_path,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                },
            }
        )

    rag_service.add_documents(documents)
    print(f"✓ Added {len(documents)} chunks from {doc_id}")


def main():
    """Ingest all documents from the documents directory"""
    docs_dir = Path("documents/medical_guidelines")

    if not docs_dir.exists():
        print(f"Creating {docs_dir}...")
        docs_dir.mkdir(parents=True, exist_ok=True)
        print("Please add medical guideline PDFs/text files to this directory.")
        return

    for file_path in docs_dir.glob("*"):
        if file_path.is_file():
            doc_id = file_path.stem

            if file_path.suffix.lower() == ".pdf":
                process_pdf(str(file_path), doc_id)
            elif file_path.suffix.lower() in [".txt", ".md"]:
                process_text(str(file_path), doc_id)
            else:
                print(f"Skipping unsupported file: {file_path}")

    print("\n✓ Document ingestion complete!")


if __name__ == "__main__":
    main()
