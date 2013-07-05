#!/usr/bin/python

import ast
import argparse

desc = '''
reader.py -- A reader for 61A
'''

def grade(module, func_name):
    pass

def node_count(module, func_name):
    'Count the number of ast nodes in the source file.'
    tlds = list(ast.iter_child_nodes(module))
    for tld in tlds:
        if isinstance(tld, ast.FunctionDef) and tld.name == func_name:
            return len(list(ast.walk(tld)))
    return 0
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('source_file')
    parser.add_argument('function_name')
    args = parser.parse_args()

    with open(args.source_file, 'r') as f:
        module = ast.parse(f.read())

    grade(module, args.function_name)
