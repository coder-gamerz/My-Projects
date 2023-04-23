from PIL import Image
from PIL import ExifTags
from gmplot import gmplot

name = ""
img = Image.open(r"C:\Users\shrey\OneDrive\Documents\{name}.jpg") 
exif = {
        ExifTags.TAGS[k]: v
        for k, v in img._getexif().items()
        if k in ExifTags.TAGS
        } 

north = exif['GPSInfo'][2]
east = exif['GPSInfo'][4]

lat = ((((north[0] * 60) * north[1]) * 60) * north[2]) / 60 / 60
long = ((((east[0] * 60) * east[1]) * 60) * east[2]) / 60 / 60
lat, long = float(lat), float(long)

gmap = gmplot.GoogleMapPlotter(lat, long, 12)
gmap.marker(lat, long, "yellow")
gmap.draw("loc.html")