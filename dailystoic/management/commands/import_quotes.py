import os
import re
import datetime
from django.core.management.base import BaseCommand
from dailystoic.models import Quote

class Command(BaseCommand):
    help = 'Importuje cytaty DailyStoic z pliku tekstowego'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Ścieżka do pliku z cytatami')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'Plik {file_path} nie istnieje!'))
            return

        self.stdout.write(self.style.SUCCESS('Rozpoczęcie importu cytatów...'))
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Dzielimy plik na poszczególne cytaty
        quotes_raw = content.split('ENDEND')
        
        # Usuwamy puste elementy
        quotes_raw = [q.strip() for q in quotes_raw if q.strip()]
        
        quotes_count = 0
        current_year = datetime.datetime.now().year
        
        for i, quote_text in enumerate(quotes_raw):
            try:
                # Dzielimy na linie
                lines = quote_text.strip().split('\n')
                
                # Wyodrębniamy datę (pierwszy wiersz)
                date_line = lines[0].strip()
                
                # Wyodrębniamy tytuł (drugi wiersz)
                title = lines[1].strip()
                
                # Wyodrębniamy zawartość (od trzeciego wiersza do końca)
                remaining_content = '\n'.join(lines[2:]).strip()
                
                # Próbujemy oddzielić cytat od refleksji
                # Szukamy pierwszego wystąpienia myślnika i zakładamy,
                # że wszystko przed myślnikiem to cytat, a po nim refleksja
                parts = re.split(r'—|–|-', remaining_content, maxsplit=1)
                
                if len(parts) > 1:
                    # Znajdujemy pierwszą pustą linię po myślniku
                    author_and_source = parts[1].strip().split('\n', 1)
                    
                    if len(author_and_source) > 1:
                        # Cytat zawiera autora i źródło, plus myślnik wcześniej
                        quote_content = parts[0].strip() + "\n— " + author_and_source[0].strip()
                        reflection = author_and_source[1].strip()
                    else:
                        # Nie ma pustej linii - cała reszta to cytat
                        quote_content = parts[0].strip() + "\n— " + parts[1].strip()
                        reflection = ""
                else:
                    # Nie znaleziono myślnika - zakładamy, że wszystko to cytat
                    quote_content = remaining_content
                    reflection = ""
                
                # Przetwarzamy datę
                try:
                    # Zakładamy, że data jest w formacie "dzień miesiąc"
                    day, month_name = date_line.split()
                    
                    # Konwertujemy miesiąc z nazwy na numer
                    month_mapping = {
                        'stycznia': 1, 'lutego': 2, 'marca': 3, 'kwietnia': 4,
                        'maja': 5, 'czerwca': 6, 'lipca': 7, 'sierpnia': 8,
                        'września': 9, 'października': 10, 'listopada': 11, 'grudnia': 12
                    }
                    
                    month = month_mapping.get(month_name.lower(), 1)
                    day = int(day)
                    
                    date = datetime.date(current_year, month, day)
                except (ValueError, KeyError) as e:
                    # Jeśli nie udało się sparsować daty, używamy indeksu jako dnia roku
                    date = datetime.date(current_year, 1, 1) + datetime.timedelta(days=i)
                    self.stdout.write(self.style.WARNING(f'Nie udało się sparsować daty "{date_line}", używam daty {date}'))
                
                # Tworzymy lub aktualizujemy cytat
                quote, created = Quote.objects.update_or_create(
                    date=date,
                    defaults={
                        'title': title,
                        'content': quote_content,
                        'reflection': reflection,
                        'is_published': True
                    }
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Dodano cytat na dzień {date}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Zaktualizowano cytat na dzień {date}'))
                
                quotes_count += 1
            
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Błąd podczas przetwarzania cytatu {i+1}: {str(e)}'))
                self.stdout.write(self.style.ERROR(f'Treść: {quote_text[:100]}...'))
        
        self.stdout.write(self.style.SUCCESS(f'Import zakończony. Dodano lub zaktualizowano {quotes_count} cytatów.'))