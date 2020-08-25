import pyfiglet
from os import listdir
from os.path import isfile, join

path = "/home/mainak/Downloads/pyfiglet/pyfiglet/fonts"
files = [f for f in listdir(path) if isfile(join(path, f))]
for f in files[50:60]:
    font = str(f.split('.')[0])
    try:
        print("FONT: ", font)
        pyfiglet.print_figlet("Tic-Tac-Toe", font=font, colors="LIGHT_RED")
    except Exception as e:
        pass