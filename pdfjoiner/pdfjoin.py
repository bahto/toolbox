import os
from PyPDF2 import PdfReader, PdfMerger
from PIL import Image

# Kies de naam van het uitvoerbestand en de locatie van de map met PDF's en afbeeldingen
output_directory = 'output'
output_filename = 'merged.pdf'
input_directory = 'input'

# Maak de input en output directory aan als deze nog niet bestaat
if not os.path.exists(input_directory):
    os.makedirs(input_directory)
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Verzamel de namen van alle PDF-bestanden en afbeeldingsbestanden in de map, gesorteerd op alfabetische volgorde
pdf_files = sorted([f for f in os.listdir(input_directory) if f.endswith('.pdf')])
image_files = sorted([f for f in os.listdir(input_directory) if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png')])
# Voeg de twee lijsten samen en sorteer ze opnieuw op alfabetische volgorde
all_files = sorted(pdf_files + image_files)

# Maak een object voor het samenvoegen van PDF-bestanden
merger = PdfMerger()

# Voeg elk bestand toe aan het samenvoegingsobject
for filename in all_files:
    filepath = os.path.join(input_directory, filename)
    if filename.endswith('.pdf'):
        merger.append(PdfReader(filepath))
    else:
        image = Image.open(filepath)
        pdf_bytes = image.convert('RGB').save('temp.pdf', format='PDF')
        merger.append(PdfReader('temp.pdf'))

# Schrijf de samengevoegde PDF naar een bestand in de output directory
output_filepath = os.path.join(output_directory, output_filename)
with open(output_filepath, 'wb') as output:
    merger.write(output)

# Verwijder tijdelijk PDF-bestand
try:
    os.remove('temp.pdf')
except OSError:
    pass