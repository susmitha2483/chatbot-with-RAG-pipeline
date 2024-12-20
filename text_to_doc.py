import re
from langchain.text_splitter import MarkdownTextSplitter
from langchain.docstore.document import Document

# 1. Merge Hyphenated Words - Fix words split across lines with a hyphen
def merge_hyphenated_words(text):
    return re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)

# 2. Fix Newlines - Replace unnecessary newlines with spaces
def fix_newlines(text):
    return re.sub(r'\n(?!\n)', ' ', text)

# 3. Remove Multiple Newlines - Remove extra blank lines
def remove_multiple_newlines(text):
    return re.sub(r'\n\s*\n', '\n', text)

# 4. Clean Text - Combine all cleaning functions
def clean_text(text):
    text = merge_hyphenated_words(text)
    text = fix_newlines(text)
    text = remove_multiple_newlines(text)
    return text

# 5. Convert Text into Chunks and Documents
def text_to_docs(text, metadata):
    text_splitter = MarkdownTextSplitter(chunk_size=2048, chunk_overlap=128)
    chunks = text_splitter.split_text(text)
    
    # Create Document objects for each chunk
    documents = []
    for chunk in chunks:
        document = Document(page_content=chunk, metadata=metadata)
        documents.append(document)
    
    return documents

# 6. Get Document Chunks - Combine text cleaning and chunking
def get_doc_chunks(text, metadata):
    cleaned_text = clean_text(text)
    return text_to_docs(cleaned_text, metadata)
