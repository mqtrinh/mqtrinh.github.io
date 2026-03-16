import re, sys


if __name__ == '__main__':
    label = sys.argv[1]
    mode = sys.argv[2]
    coxeter = sys.argv[3]

    test_file = f'test/{mode}/{label}_{mode}_tested.txt'
    elt_file = f'sortable/{label}_sortable_{coxeter}.txt'

    with open(elt_file, 'r') as f:
        elts = re.split('\n', f.read().strip())

    with open(test_file, 'r') as f:
        content = f.read()
    
    list = []
    for elt in elts:
        if elt in content:
            list.append(elt)
    
    if list: 
        print('Elements found:')
        for elt in list:
            print(elt)
    else:
        print('No elements found.')


    
