#!/usr/bin/python

import ast
import argparse
from collections import defaultdict

import sklearn.svm as svm

desc = '''
reader.py -- A reader for 61A
'''

def score_func(func_def):
    feat_vector = []
    all_globals = globals() 
    for global_name,global_var in all_globals.items():
      if global_name[:4] == 'feat':
        feat_vector.append(global_var(func_def)) 
    return feat_vector
          
def feat_node_count(func_def):
    'Count the number of ast nodes in the source file.'
    return len(list(ast.walk(func_def)))

def feat_dry_violations(func_def):
    'Hash patterns in the AST to check for repetitious code.'

    def compute_hashes(node, phash, dhash):
        'Track hashes of AST nodes while traversing the tree.'
        for child in ast.iter_child_nodes(node):
            dhash[phash] += 1
            compute_hashes(child, hash((phash, type(child))), dhash)

    hashes = defaultdict(int)
    compute_hashes(func_def, hash(type(func_def)), hashes)
    return sum(hashes.values()) - len(hashes)

def feat_loop_count(func_def):
  count =0
  for node in ast.walk(func_def):
    count += is_loop(node) 
  return count 

def feat_max_loop_depth(func_def):
  loops = [] 
  max_loop_depth = 0
  for node in ast.iter_child_nodes(func_def):
    if is_loop(node):
      loops.append(node) 

  for loop in loops:
    this_loop_count = 1
    for node in ast.walk(loop):
      if is_loop(node):
        this_loop_count += 1
    max_loop_depth = max(this_loop_count,this_loop_count) 

  return  max_loop_depth

def is_loop(node):
  return type(node) in {ast.GeneratorExp,ast.For,ast.While,ast.ListComp} 

def score(file_name):
    with open(args.source_file, 'r') as f:
        module = ast.parse(f.read())
    tlds = list(ast.iter_child_nodes(module))
    all_features = [] 
    for tld in tlds:
      if isinstance(tld, ast.FunctionDef):
            all_features += score_func(tld)
    return all_features 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('source_file')
    args = parser.parse_args()
    print(score(args.source_file)) 
