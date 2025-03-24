import requests
import zipfile
import io
import os
import re
import csv

en_version = 'https://unstats.un.org/unsd/classifications/Econ/Download/In%20Text/COFOG_english_structure.txt'
sp_version = 'https://unstats.un.org/unsd/classifications/Econ/Download/In%20Text/cofog_spanish_structure.zip'
fr_version = 'https://unstats.un.org/unsd/classifications/Econ/Download/In%20Text/cofog_French_structure.zip'

def download_file(url):
    response = requests.get(url)
    response.raise_for_status()
    return response

def get_txt_from_zip(zip_url):
    response = download_file(zip_url)
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        for filename in z.namelist():
            if 'COFOG' in filename and filename.endswith('.txt'):
                with z.open(filename) as f:
                    raw_text = f.read()
                    try:
                        decoded_text = raw_text.decode('utf-8')
                    except UnicodeDecodeError:
                        decoded_text = raw_text.decode('ISO-8859-1')

                    print(f"First 5 lines from {filename}:\n", "\n".join(decoded_text.splitlines()[:5]))  
                    return decoded_text  
    return None

def parse_cofog_data(text, language):
    lines = text.strip().split('\n')
    parsed_data = []

    for line in lines:
        line = line.strip()

        if "Code" in line and "Description" in line:
            continue  

        if language == "Spanish":
            parts = line.replace('"', '').split(',', 1)
        elif language == "French":
            # Handle fixed-width French format (split on multiple spaces)
            parts = re.split(r'\s{2,}', line, maxsplit=1)
        else:
            parts = line.split('\t') if '\t' in line else line.split(None, 1)

        if len(parts) == 2:
            code, description = parts
            parsed_data.append((code.strip(), description.strip()))

    return parsed_data

def parse_foreign_languages():
    sp_text = get_txt_from_zip(sp_version)
    fr_text = get_txt_from_zip(fr_version)
    return {
        'Spanish': parse_cofog_data(sp_text, "Spanish"),
        'French': parse_cofog_data(fr_text, "French")
    }

def parse_english_version():
    en_text = download_file(en_version).text
    return {'English': parse_cofog_data(en_text, "English")}

def merge_everything():
    english_data = parse_english_version()
    foreign_data = parse_foreign_languages()
    merged_data = {'English': english_data['English'], **foreign_data}
    return merged_data

def save_to_archive(data, archive_folder="archive"):
    os.makedirs(archive_folder, exist_ok=True)
    for lang, entries in data.items():
        filename = os.path.join(archive_folder, f"cofog_{lang.lower()}.csv")
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Code", "Description"])
            writer.writerows(entries)
    print(f"Saved all files in folder: {archive_folder}")

if __name__ == '__main__':
    cofog_data = merge_everything()
    save_to_archive(cofog_data)
    for lang, data in cofog_data.items():
        print(f'--- {lang} ---')
        for code, desc in data[:5]:
            print(f'{code}: {desc}')