from xml.etree.ElementTree import *

path = r"C:\Users\shrey\OneDrive\Desktop\Code\Python\sample.xml"
tree = parse(path)
root = tree.getroot()
print(root)
