import os
import fitz  # PyMuPDF
import pandas as pd


def parse_files(file_paths: list[str]) -> pd.DataFrame:
    """
    Parse a list of file paths and return a DataFrame with:
    - filename
    - text
    """

    parsed_data = []

    for file_path in file_paths:
        # Verification checks for file path validity
        if not isinstance(file_path, str):
            print(f"Skipping invalid path (not a string): {file_path}")
            continue

        if not os.path.exists(file_path):
            print(f"Skipping missing file: {file_path}")
            continue
        
        # Extract filename and extension
        filename = os.path.basename(file_path)
        file_extension = os.path.splitext(filename)[1].lower()

        # Only process supported file types
        if file_extension not in [".pdf", ".txt"]:
            print(f"Skipping unsupported file type: {filename}")
            continue
        
        # Parse PDF files using PyMuPDF and text files using standard file reading
        if file_extension == ".pdf":    
            try:
                document = fitz.open(file_path)
                full_text = ""

                for page in document:
                    full_text += page.get_text()

                document.close()

                parsed_data.append({
                    "filename": filename,
                    "text": full_text.strip()
                })

            except Exception as e:
                print(f"Error parsing {filename}: {e}")
        else:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    parsed_data.append({
                        "filename": filename,
                        "text": text.strip()
                    })
            except Exception as e:
                print(f"Error parsing {filename}: {e}")

    return pd.DataFrame(parsed_data, columns=["filename", "text"])