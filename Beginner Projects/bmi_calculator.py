import customtkinter as tk
import decimal

foot_to_centimeter = 30.48
inch_to_centimeter = 2.54

def calculate_bmi():
    a = float(height_foot_entry.get())
    b = float(height_inch_entry.get())
    c = float(weight_entry.get())

    fcm = a * foot_to_centimeter
    icm = b * inch_to_centimeter
    hm = (fcm + icm) / 100

    def bmi(height_in_m, weight):
        hmt = height_in_m ** 2
        calculated_bmi = weight / hmt
        return decimal.Decimal(str(calculated_bmi)).quantize(decimal.Decimal('1.0'))
    
    def health_check():
        e = float(bmi(hm, c))

        if e < 18.5:
            return 'You are Underweight'
        elif e < 24.9 and e > 18.5:
            return 'You are Healthy'
        elif e < 29.9 and e > 25:
            return 'You are Overweight'
        elif e > 29.9:
            return 'You are FAT AF'

    d = bmi(hm, c)
    f = health_check()
    result_label.configure(text='Your BMI is: '+ str(d))
    healthy_or_not.configure(text=f)


window = tk.CTk()
window.title("BMI Calculator")


height_label = tk.CTkLabel(window, text="Height (in foot):")
height_label.pack()
height_foot_entry = tk.CTkEntry(window)
height_foot_entry.pack()

height_inch_label = tk.CTkLabel(window, text="Height (in inch):")
height_inch_label.pack()
height_inch_entry = tk.CTkEntry(window)
height_inch_entry.pack()

weight_label = tk.CTkLabel(window, text="Weight (in kg):")
weight_label.pack()
weight_entry = tk.CTkEntry(window)
weight_entry.pack()


calculate_button = tk.CTkButton(window, text="Calculate", command=calculate_bmi)
calculate_button.pack()


result_label = tk.CTkLabel(window, text="")
result_label.pack()

healthy_or_not = tk.CTkLabel(window, text="")
healthy_or_not.pack()

window.mainloop()
