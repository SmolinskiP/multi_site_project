# mm.py
import json

def parse_text_to_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    lines = text.strip().split("\n\n")

    title = lines[0].strip() if len(lines) > 0 else ""
    quote = lines[1].strip() if len(lines) > 1 else ""
    description = "\n\n".join(lines[2:]).strip() if len(lines) > 2 else ""

    data = {
        "title": title,
        "quote": quote,
        "description": description
    }

    return data

input_file_path = '/var/www/multi_site_project/media/dailystoic_back/text.txt'
output_file_path = '/var/www/multi_site_project/media/dailystoic/quote/text_pl.json'
result = parse_text_to_json(input_file_path)

import os
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=4)

input_file_path = '/var/www/multi_site_project/media/dailystoic_back/text_en.txt'
output_file_path = '/var/www/multi_site_project/media/dailystoic/quote/text_en.json'
result = parse_text_to_json(input_file_path)

os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=4)