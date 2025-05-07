#!/bin/bash
# /var/www/multi_site_project/dailystoic_scripts.sh

# Aktywacja środowiska wirtualnego
source /var/www/multi_site_project/venv/bin/activate

# Ustawienie ścieżek
export PYTHONPATH=/var/www/multi_site_project

# Uruchamianie skryptów
cd /var/www/multi_site_project

# Newsletter 
python manage.py send_daily_newsletter

# Skrypty generowania cytatów
python multi_site_project/dailystoic_legacyscripts/extract_quote.py
python multi_site_project/dailystoic_legacyscripts/mm.py
python multi_site_project/dailystoic_legacyscripts/imager.py

echo "Skrypty wykonane: $(date)" >> /home/patryk/dailystoic_scripts.log