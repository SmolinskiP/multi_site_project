# imager.py
# coding: utf8
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os

base_dir = '/var/www/multi_site_project/media'
font_path = os.path.join(base_dir, 'dailystoic_back/ModernAntiqua-Regular.ttf')
font_header = ImageFont.truetype(font_path, size=35)
font_quote = ImageFont.truetype(font_path, size=22)
font_main_text = ImageFont.truetype(font_path, size=22)

text_file = os.path.join(base_dir, 'dailystoic_back/text.txt')
text_en_file = os.path.join(base_dir, 'dailystoic_back/text_en.txt')

file = open(text_file, "r", encoding="utf8")
file_en = open(text_en_file, "r", encoding="utf8")
lines = file.readlines()
lines_en = file_en.readlines()
lines = lines[1:]
lines_en = lines_en[1:]
file.close()
file_en.close()

header = lines[0]
quote = lines[2]
main_text = lines[4]

header_en = lines_en[0]
quote_en = lines_en[2]
main_text_en = lines_en[4]

def Splitator(text, amount_of_characters):
    i=0
    lines = text.split(" ")
    temp_string = ""
    finalstring = ""
    while len(finalstring) < len(text):
        if len(temp_string) < amount_of_characters:
            try:
                temp_string = temp_string + lines[i] + " "
                i+=1
            except:
                finalstring = finalstring + temp_string + "\n"
                temp_string = ""
                return finalstring
                break
        else:
            finalstring = finalstring + temp_string + "\n"
            temp_string = ""
    return finalstring

final_header = Splitator(header, 25)
final_quote = Splitator(quote, 50)
final_main_text = Splitator(main_text, 50)

final_header_en = Splitator(header_en, 25)
final_quote_en = Splitator(quote_en, 50)
final_main_text_en = Splitator(main_text_en, 50)

i = 10
i += final_header.count('\n') * 36
i += final_quote.count('\n') * 25
i += final_main_text.count('\n') * 23

i_en = 10
i_en += final_header_en.count('\n') * 36
i_en += final_quote_en.count('\n') * 25
i_en += final_main_text_en.count('\n') * 23
print(i)

output_dir = os.path.join(base_dir, 'dailystoic')
os.makedirs(output_dir, exist_ok=True)

img = Image.new('RGBA', (650, i), color = (255, 255, 255, 0))
img_en = Image.new('RGBA', (650, i_en), color = (255, 255, 255, 0))
img.save(os.path.join(output_dir, 'empty.png'))
img_en.save(os.path.join(output_dir, 'empty_en.png'))
d = ImageDraw.Draw(img)
d_en = ImageDraw.Draw(img_en)

final_header = final_header.split("\n")
final_quote = final_quote.split("\n")
final_main_text = final_main_text.split("\n")

final_header_en = final_header_en.split("\n")
final_quote_en = final_quote_en.split("\n")
final_main_text_en = final_main_text_en.split("\n")


y = 10
for line in final_header:
    d.text((0,y), line, fill=(220, 220, 220), font=font_header)
    y+=35
y-=35 
for line in final_quote:
    d.text((0,y), line, fill=(220, 220, 220), font=font_quote)
    y+=24
y-=24
for line in final_main_text:
    d.text((0,y), line, fill=(220, 220, 220), font=font_main_text)
    y+=22

y = 10
for line in final_header_en:
    d_en.text((0,y), line, fill=(220, 220, 220), font=font_header)
    y+=35
y-=35 
for line in final_quote_en:
    d_en.text((0,y), line, fill=(220, 220, 220), font=font_quote)
    y+=24
y-=24
for line in final_main_text_en:
    d_en.text((0,y), line, fill=(220, 220, 220), font=font_main_text)
    y+=22

img.save(os.path.join(output_dir, 'daily.png'))
img_en.save(os.path.join(output_dir, 'daily_en.png'))