import os
import datetime

def extract_daily_quote():
    # Otwieramy źródłowe pliki z cytatami
    txt_file = open("/var/www/multi_site_project/media/dailystoic_back/dailystoic.txt", encoding="utf8")
    text = txt_file.read()
    txt_file.close()
    
    txt_file_en = open("/var/www/multi_site_project/media/dailystoic_back/dailystoic_en.txt", encoding="utf8")
    text_en = txt_file_en.read()
    txt_file_en.close()
    
    # Pobieramy aktualną datę
    x = datetime.datetime.now()
    y = x.strftime("%d")
    x = x.strftime("%m")
    
    # Usuwamy leading zero z dnia
    if y.startswith("0"):
        y = y[1:]
    
    # Mapowanie miesiąca na nazwę
    month_mapping = {
        "01": ("stycznia", "January", "sty.jpg", "Styczen: Jasnosc"),
        "02": ("lutego", "February", "lut.jpg", "Luty: Namietnosci i emocje"),
        "03": ("marca", "March", "mar.jpg", "Marzec: Swiadomosc"),
        "04": ("kwietnia", "April", "kwi.jpg", "Kwiecien: Obiektywna mysl"),
        "05": ("maja", "May", "maj.jpg", "Maj: Wlasciwe dzialania"),
        "06": ("czerwca", "June", "cze.jpg", "Czerwiec: Rozwiazywanie problemow"),
        "07": ("lipca", "July", "lip.jpg", "Lipiec: Powinnosci"),
        "08": ("sierpnia", "August", "sie.jpg", "Sierpiec: Pragmatyzm"),
        "09": ("września", "September", "wrz.jpg", "Wrzesien: Hart ducha i odpornosc"),
        "10": ("października", "October", "paz.jpg", "Pazdziernik: Cnota i dobroc"),
        "11": ("listopada", "November", "lis.jpg", "Listopad: Akceptacja - amor fati"),
        "12": ("grudnia", "December", "gru.jpg", "Grudzien: Rozmyslania nad smiertelnoscia")
    }
    
    miesiąc_pl, miesiąc_en, img, mailtitle = month_mapping.get(x, ("stycznia", "January", "sty.jpg", "Styczen: Jasnosc"))
    
    # Tworzymy wzorce do wyszukania w tekstach
    dzisiaj = f"{y} {miesiąc_pl}"
    today = f"{miesiąc_en} {y}"
    
    # Wycinamy odpowiednie fragmenty tekstów
    start = text.find(dzisiaj) + len(dzisiaj)
    text = text[start:]
    end = text.find("ENDEND")
    text = text[:end]
    
    start_en = text_en.find(today) + len(today)
    text_en = text_en[start_en:]
    end_en = text_en.find("ENDEND")
    text_en = text_en[:end_en]
    
    # Zapisujemy wyniki do plików
    out_dir = "/var/www/multi_site_project/media/dailystoic_back"
    os.makedirs(out_dir, exist_ok=True)
    
    with open(f"{out_dir}/text.txt", "w", encoding="utf8") as txt_file:
        txt_file.write(text)
    
    with open(f"{out_dir}/text_en.txt", "w", encoding="utf8") as txt_file_en:
        txt_file_en.write(text_en)
    
    print(f"Wyodrębniono cytaty na {dzisiaj} / {today}")

if __name__ == "__main__":
    extract_daily_quote()