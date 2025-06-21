#!/bin/bash

# Zapisz credentials.json z ENV do pliku
echo "$GOOGLE_CREDENTIALS_JSON" > credentials.json

# Odpal selektor trybu (main.py decyduje polling vs webhook)
python3 main.py