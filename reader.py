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

def loop_count(func_def):
  count =0
  for node in ast.walk(func_def):
    count += is_loop(node) 
  return count 

def max_loop_depth(func_def):
  loops = [] 
  for node in ast.iter_child_nodes(func_def):
    if is_loop(node):
      loops.append(node) 
  max_loop_depth = loops != [] 

  for loop in loops:
    this_loop_count = 0
    for node in ast.walk(loop):
      if is_loop(node):
        this_loop_count += 1
    max_loop_depth = max(this_loop_count,this_loop_count) 

  return max_loop_depth  
    

def is_loop(node):
  return type(node) in {ast.GeneratorExp,ast.For,ast.While,ast.ListComp} 



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('source_file')
    parser.add_argument('function_name')
    args = parser.parse_args()

    with open(args.source_file, 'r') as f:
        module = ast.parse(f.read())

    grade(module, args.function_name)
