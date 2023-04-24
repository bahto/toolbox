from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import tempfile


def convert_images_to_pdf(image_directory, output_filename):
    # Open een nieuw PDF-bestand
    c = canvas.Canvas(output_filename, pagesize=A4)

    # Bepaal de grootte van de pagina en de marges
    page_width, page_height = A4
    left_margin = 30
    bottom_margin = 30
    image_margin = 10
    image_width = (page_width - 2*left_margin - image_margin) / 2
    image_height = image_width * 1.5

    # Lijst alle bestanden in de directory op
    files = os.listdir(image_directory)
    # Sorteer de lijst op bestandsnaam
    files.sort()

    # Maak een lege lijst voor de afbeeldingen
    images = []

    # Laad elke afbeelding en voeg deze toe aan de lijst
    for file in files:
        if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
            image_path = os.path.join(image_directory, file)
            try:
                image = Image.open(image_path)
                images.append(image)
            except IOError:
                pass

    # Plaats elke afbeelding op de pagina en sla op
    for i in range(0, len(images), 2):
        # Plaats de eerste afbeelding
        x = left_margin
        y = page_height - bottom_margin - image_height

        with tempfile.NamedTemporaryFile(delete=False, suffix='.{}'.format(images[i].format.lower())) as f:
            images[i].save(f.name)
            c.drawImage(f.name, x, y, width=image_width, height=image_height)

        # Plaats de tweede afbeelding (indien aanwezig)
        if i+1 < len(images):
            x = left_margin + image_width + image_margin

            with tempfile.NamedTemporaryFile(delete=False, suffix='.{}'.format(images[i+1].format.lower())) as f:
                images[i+1].save(f.name)
                c.drawImage(f.name, x, y, width=image_width, height=image_height)

        # Ga naar een nieuwe pagina indien er meer afbeeldingen zijn
        if i+2 < len(images):
            c.showPage()

    # Sla het PDF-bestand op
    c.save()
# Test het script
image_directory = "images"
output_filename = "images.pdf"
convert_images_to_pdf(image_directory, output_filename)
