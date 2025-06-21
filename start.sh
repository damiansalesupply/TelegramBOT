#!/bin/bash

# Zapisz credentials.json z ENV do pliku (fallback dla starszych wersji)
if [ ! -z "$GOOGLE_CREDENTIALS_JSON" ]; then
    echo "$GOOGLE_CREDENTIALS_JSON" > credentials.json
fi

# Odpal selektor trybu (main.py decyduje polling vs webhook)
python3 main.py