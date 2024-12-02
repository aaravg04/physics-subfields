from docx import Document
from docx.enum.shape import WD_INLINE_SHAPE_TYPE  # Import the enumeration
from docx.shared import RGBColor  # Import RGBColor for color checking

import os

def extract_images_from_docx(docx_path, output_dir):
    # Load the document
    doc = Document(docx_path)
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Initialize a counter for images and red text
    image_count = 0
    red_text_count = 0  # Counter for red text

    # Iterate through each shape in the document
    for i, shape in enumerate(doc.inline_shapes):
        if shape.type == WD_INLINE_SHAPE_TYPE.PICTURE:  # Check if the shape is a picture
            blip = shape._inline.graphic.graphicData.pic.blipFill.blip
            rId = blip.embed
            document_part = doc.part
            image_part = document_part.related_parts[rId]
            image_bytes = image_part._blob

            
            # Save the image
            image_filename = os.path.join(output_dir, f'image_{i + 1}.png')
            with open(image_filename, 'wb') as img_file:
                img_file.write(image_bytes)
            image_count += 1
            print(f'Saved image: {image_filename}')  # Debugging output

    # New section to find text colored with hex #ff4c4c
    target_color = RGBColor(255, 76, 76)  # RGB equivalent of #ff4c4c
    for paragraph in doc.paragraphs:
        red_texts = []  # List to hold red text pieces
        for run in paragraph.runs:
            if run.font.color and run.font.color.rgb == RGBColor(255, 0, 0):  # Check if the text is red
                red_texts.append(run.text)  # Collect red text
                red_text_count += 1
        if red_texts:  # If there are any red texts in the paragraph
            print(f'Red text found: {"".join(red_texts)}')  # Output the merged red text

    if image_count == 0:
        print("No images found in the document.")
    if red_text_count == 0:
        print("No red text found in the document.")

# Example usage
extract_images_from_docx('APSAbstracts.docx', 'data')
