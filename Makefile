.PHONY: all install process clean

# Default target
all: install process

# Install dependencies
install:
    pip install -r scripts/requirements.txt

# Process all data
process:
    python scripts/explanatory_note.py
    python scripts/description.py
    python scripts/merge_cofog.py

# Clean generated files
clean:
    rm -f cofog_tartalom_eng.docx