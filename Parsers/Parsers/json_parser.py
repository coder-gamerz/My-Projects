from json import *

json_data = r"C:\Users\shrey\OneDrive\Desktop\Code\JSON\json_intro.json"
with open(json_data, "r") as j:
    a = load(j)
    print(a)
