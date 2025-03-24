import requests
from docx import Document
import re
import csv
import os

# URL of the COFOG DOCX file
DOCX_URL = "https://www.ksh.hu/docs/osztalyozasok/cofog/cofog_tartalom_eng.docx"
LOCAL_DOCX = "cofog_tartalom_eng.docx"

def download_docx(url, save_path):
    if not os.path.exists(save_path):
        print("Downloading COFOG document...")
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            print("Download complete.")
        else:
            print("Failed to download the document.")
            exit(1)

def extract_cofog_extended_notes(doc_path):
    doc = Document(doc_path)
    text = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
    
    cofog_data = {}
    current_code = None
    extended_note = []
    
    for line in text:
        match = re.match(r"(\d{1,2}(\.\d{1,2})*)\s+(.*)", line)  # Match COFOG codes
        if match:
            if current_code:  # Save previous entry
                cofog_data[current_code] = " ".join(extended_note)
            current_code = match.group(1)  # COFOG Code
            extended_note = [match.group(3)]
        elif current_code:
            extended_note.append(line)
    
    if current_code:
        cofog_data[current_code] = " ".join(extended_note)

    return cofog_data

def save_to_csv(data, filename="archive/cofog_extended_notes.csv"):
    """Save COFOG data to CSV, filtering out entries with notes < 50 characters."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Code", "ExplanatoryNote"])
        
        for code, note in data.items():
            if len(note) >= 50:
                writer.writerow([code, note])

    print(f"Filtered COFOG Explanatory Note saved to '{filename}'")

if __name__ == "__main__":
    download_docx(DOCX_URL, LOCAL_DOCX)
    cofog_notes = extract_cofog_extended_notes(LOCAL_DOCX)
    save_to_csv(cofog_notes)
    
    # Clean up - remove the downloaded DOCX file
    if os.path.exists(LOCAL_DOCX):
        os.remove(LOCAL_DOCX)
        print(f"Removed temporary file: {LOCAL_DOCX}")
    
