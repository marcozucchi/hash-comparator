import argparse
import hashlib
import pathlib
import shutil

from termcolor import colored

VERSION = "0.0.1"

# Banner
print(colored(f"""
 _   _           _     _____                                       _             
| | | |         | |   /  __ \                                     | |            
| |_| | __ _ ___| |__ | /  \/ ___  _ __ ___  _ __   __ _ _ __ __ _| |_ ___  _ __ 
|  _  |/ _` / __| '_ \| |    / _ \| '_ ` _ \| '_ \ / _` | '__/ _` | __/ _ \| '__|
| | | | (_| \__ \ | | | \__/\ (_) | | | | | | |_) | (_| | | | (_| | || (_) | |   
\_| |_/\__,_|___/_| |_|\____/\___/|_| |_| |_| .__/ \__,_|_|  \__,_|\__\___/|_|   
                                            | |                                  
                                            |_|                                  
                                            By: Marco Zucchi Mesia                          
                                            v {VERSION}
""", color='white'))

parser = argparse.ArgumentParser(prog='digest', description='Compare Hash digests of files')
parser.add_argument('file', metavar='file', nargs=1, type=pathlib.Path,
                    help='Archivo del  que se quiere calcular los hashes')
parser.add_argument('--hash-type', dest='ht', nargs='*', default='md5', choices=hashlib.algorithms_available,
                    help='Digest types that want to be compared')
parser.add_argument('--hash-digest', dest='hd', nargs='*', help='Digests that want to be compared')
parser.add_argument('--version', action='version', version=VERSION)
results = parser.parse_args()

for item in zip(results.ht, results.hd):
    hashCalculator = hashlib.new(item[0])
    with open(results.file[0], 'rb') as f:
        chunk = 0
        while chunk != b'':
            chunk = f.read(1024)
            hashCalculator.update(chunk)

    digestForComparison = hashCalculator.hexdigest()
    if digestForComparison != item[1]:
        print(colored(item[0].center(shutil.get_terminal_size().columns, '='), color='red'))
        print(colored(f'El hash {item[0]} no coincide', color='red'))
        print(colored(f'Calculated hash: >> {digestForComparison}', color='red'))
        print(colored(f'Expected hash:   << {item[1]}', color='yellow'))
    else:
        print(colored('Both digest match', color='green'))
        print(colored(item[0].center(shutil.get_terminal_size().columns, '='), color='green'))
        print(colored(f'Calculated hash: >> {digestForComparison}', color='green'))
        print(colored(f'Expected hash:   << {item[1]}', color='green'))

    print()
