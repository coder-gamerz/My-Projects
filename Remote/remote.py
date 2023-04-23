import sys
import subprocess as sb
import PySimpleGUI as py

def execute(stuff):
    cmd = sb.Popen(stuff, stdout=sb.PIPE, stderr=None, shell=True)
    print(cmd.communicate()[0])

def up():
    execute('adb shell input keyevent 19')

def down():
    execute('adb shell input keyevent 20')

def home():
    execute('adb shell input keyevent 3')

def left():
    execute('adb shell input keyevent 21')

def right():
    execute('adb shell input keyevent 22')

def select():
    execute('adb shell input keyevent 23')

def back():
    execute('adb shell input keyevent 4')

def volume_up():
    execute('adb shell input keyevent 24')

def volume_down():
    execute('adb shell input keyevent 25')

def volume_mute():
    execute('adb shell input keyevent 164')

def power():
    execute('adb shell input keyevent 26')


def main():
    execute('adb disconnect')
    execute('adb connect 192.168.29.251')

    row2 = [
        [py.Button('^')]
    ]

    row3 = [
        [py.Button('<'), py.Button('0'), py.Button('>')]
    ]

    row4 = [
        [py.Button('⌄')]
    ]

    row5 = [
        [py.Button('⌂'), py.Button('←')]
    ]

    row6 = [
        [py.Button('+')]
    ]

    row8 = [
        [py.Button('🔇')]
    ]

    row9 = [
        [py.Button('-')]
    ]

    row7 = [
        [py.Button('O')]
    ]

    row10 = [
        []
    ]

    row11 = [
        []
    ]

    row12 = [
        []
    ]

    gui = [
        [py.Frame(layout=row7, title='')],
        [py.Frame(layout=row10, title='')],
        [py.Frame(layout=row2, title='')],
        [py.Frame(layout=row3, title='')],
        [py.Frame(layout=row4, title='')],
        [py.Frame(layout=row11, title='')],
        [py.Frame(layout=row5, title='')],
        [py.Frame(layout=row12, title='')],
        [py.Frame(layout=row6, title='')],
        [py.Frame(layout=row8, title='')],
        [py.Frame(layout=row9, title='')]
    ]

    py.LOOK_AND_FEEL_TABLE['MyCreatedTheme'] = {'BACKGROUND': '#000000',
                                        'TEXT': '# FFCC66',
                                        'INPUT': '# 339967',
                                        'TEXT_INPUT': '# 000000',
                                        'SCROLL': '# 99CC99',
                                        'BUTTON': ('#000000', '#6d1010'),
                                        'PROGRESS': ('# D1826B', '#6d1010'),
                                        'BORDER': 1, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0, }
    
    py.theme('MyCreatedTheme')
    win = py.Window('T.V Remote', gui, size=(204, 400), element_justification='c')
    

    while True:
        event,values = win.read()
        if event == '^':
            up()

        if event == '⌄':
            down()
        
        if event == '<':
            left()
        
        if event == '>':
            right()
        
        if event == '0':
            select()
        
        if event == '←':
            back()
        
        if event == '⌂':
            home()

        if event == '-':
            volume_down()

        if event == '+':
            volume_up()

        if event == '🔇':
            volume_mute()

        if event == 'O':
            power()

        if event == py.WIN_CLOSED:
            sys.exit(0)
        
                   

if __name__ == '__main__':
    main()

