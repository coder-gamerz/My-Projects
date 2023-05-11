import pyqrcode as p
from pyqrcode import QRCode

link = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley'
qr = p.create(link)

qr.png(r'C:\Users\shrey\OneDrive\Documents\My-Projects\Beginner Projects\QR_code\qr_codes\stack.png', scale=6)
