import math

def circle_area(radius):
    return math.pi * radius ** 2

def circle_perimeter(radius):
    return 2 * math.pi * radius

def rectangle_area(length, width):
    return length * width

def rectangle_perimeter(length, width):
    return 2 * (length + width)

def square_area(side):
    return side ** 2

def square_perimeter(side):
    return 4 * side

def triangle_area(base, height):
    return 0.5 * base * height

def triangle_perimeter(side1, side2, side3):
    return side1 + side2 + side3

def parallelogram_area(base, height):
    return base * height

def parallelogram_perimeter(base, height):
    return 2 * (base + height)

calculation_type = input("Do you want to calculate the area or perimeter? ")

shape_type = input("Which shape do you want to calculate? ")

if calculation_type == "area":
    if shape_type == "circle":
        radius = float(input("Enter the radius of the circle: "))
        area = circle_area(radius)
        print(f"The area of the circle is {area} units")
    elif shape_type == "rectangle":
        length = float(input("Enter the length of the rectangle: "))
        width = float(input("Enter the width of the rectangle: "))
        area = rectangle_area(length, width)
        print(f"The area of the rectangle is {area} units")
    elif shape_type == "square":
        side = float(input("Enter the side length of the square: "))
        area = square_area(side)
        print(f"The area of the square is {area} units")
    elif shape_type == 'triangle':
        b = float(input("Enter the base of the triangle: "))
        h = float(input("Enter the height of the triangle: "))
        area = triangle_area(b, h)
        print(f"The area of the triangle is {area} units")
    elif shape_type == 'parallelogram':
        b = float(input("Enter the base of the parallelogram: "))
        h = float(input("Enter the height of the parallelogram: "))
        area = parallelogram_area(b, h)
        print(f"The area of the parallelogram is {area} units")
    else:
        print("Invalid shape type")
elif calculation_type == "perimeter":
    if shape_type == "circle":
        radius = float(input("Enter the radius of the circle: "))
        perimeter = circle_perimeter(radius)
        print(f"The circumference of the circle is {perimeter} units")
    elif shape_type == "rectangle":
        length = float(input("Enter the length of the rectangle: "))
        width = float(input("Enter the width of the rectangle: "))
        perimeter = rectangle_perimeter(length, width)
        print(f"The perimeter of the rectangle is {perimeter} units")
    elif shape_type == "square":
        side = float(input("Enter the side length of the square: "))
        perimeter = square_perimeter(side)
        print(f"The perimeter of the square is {perimeter} units")
    elif shape_type == 'triangle':
        s1 = float(input("Enter the length of the first side: "))
        s2 = float(input("Enter the length of the second side: "))
        s3 = float(input("Enter the length of the third side: "))
        perimeter = triangle_perimeter(s1, s2, s3)
        print(f"The perimeter of the triangle is {perimeter} units")
    elif shape_type == "parallelogram":
        b = float(input("Enter the base of the parallelogram: "))
        h = float(input("Enter the height of the parallelogram: "))
        perimeter = rectangle_perimeter(b, h)
        print(f"The perimeter of the parallelogram is {perimeter} units")
    else:
        print("Invalid shape type")
else:
    print("Invalid calculation type")

# A simple area and perimeter calculator
    
