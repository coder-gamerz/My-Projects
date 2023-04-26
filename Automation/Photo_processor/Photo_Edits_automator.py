from PIL import Image, ImageEnhance, ImageFilter
import os

path = r"C:\Users\shrey\OneDrive\Documents\Automation\Photo_processor\images" 
pathOut = r"C:\Users\shrey\OneDrive\Documents\Automation\Photo_processor\edited_images" 

for filename in os.listdir(path):
    img = Image.open(f"{path}/{filename}")
    edit = img.filter(ImageFilter.SHARPEN).convert('L')

    factor = 1.5
    enhancer = ImageEnhance.Contrast(edit)
    edit = enhancer.enhance(factor)

    clean_name = os.path.splitext(filename)[0]
    edit.save(f'{pathOut}/{clean_name}_edited.jpeg')
    
# A simple photo processor to process photos in bulk
    
