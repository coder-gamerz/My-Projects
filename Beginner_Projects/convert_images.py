from PIL import Image

image_path = input('Enter your image path: ')
image_name = input('Enter name for newly formed image (with file extension): ')

img = Image.open(fr'{image_path}').convert('RGB')
img.save(image_name)
