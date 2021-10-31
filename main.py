from sys import argv
from ERD import ERD

def usage():
    print(f'Usage: {argv[0]} <entity_file.xlsx>')

if __name__=='__main__':
    if len(argv) < 2:
        print('[*] No attribute file provided')
        usage()
        exit(-1)
    entity_file = argv[1]
    er_diagram = ERD(entity_file)
    er_diagram.generate()

    exit(0)