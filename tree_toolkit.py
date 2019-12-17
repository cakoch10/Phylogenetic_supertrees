from newick import read
from treelib import Node, Tree
import math

'''
creates a full binary tree of depth max_depth with node names pulled from name_stack
'''
def create_binary_tree(tr, parent, name_stack, max_depth, curr_depth):
    if max_depth == curr_depth:
        return
    else:
        id1 = name_stack.pop()
        id2 = name_stack.pop()
        label1 = "n" + str(id1)
        label2 = "n" + str(id2)
        tr.create_node(label1, id1, parent=parent)
        tr.create_node(label2, id2, parent=parent)
        create_binary_tree(tr, id1, name_stack, max_depth, curr_depth+1)
        create_binary_tree(tr, id2, name_stack, max_depth, curr_depth+1)

'''
computes the number of different pairs of leaves that are not in the subtree of node and all pairs that are in the 
subtree of node
'''
def computer_diff_pairs_subtree(tr, parent, node, num_pairs_diff_subtree, num_pairs_same_tree, q):
    parent_contrib = num_pairs_diff_subtree[parent]
    sib = tr.siblings(node)[0].identifier
    num_leaves_sib = len(tr.leaves(sib))
    num_leaves_parent = len(tr.leaves(parent))
    num_leaves_self = len(tr.leaves(node))
    num_pairs_diff_subtree[node] = parent_contrib + num_leaves_sib *(q - num_leaves_parent)
    num_pairs_same_tree[node] = num_pairs_same_tree[parent] + num_leaves_self*(num_leaves_self - 1)//2
    for child in tr.children(node):
        computer_diff_pairs_subtree(tr, node, child.identifier, num_pairs_diff_subtree, num_pairs_same_tree, q)


