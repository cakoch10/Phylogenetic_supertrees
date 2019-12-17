# from node import *


'''
from tree_algorithms import *
new_tr = Tree()
new_tr.create_node("n8", 8)
new_tr.create_node("n7", 7, parent=8)
new_tr.create_node("n9", 9, parent=8)
new_tr.create_node("n3", 3, parent=9)
new_tr.create_node("n1", 1, parent=9)
new_tr.create_node("n5", 5, parent=7)
new_tr.create_node("n6", 6, parent=7)

new_tr.create_node("n4", 4, parent=6)
new_tr.create_node("n2", 2, parent=6)

leafs = [1,2,3,4,5]
trips = root_triplets(new_tr)
t = two_maxrtc(leafs, trips)
'''
from newick import read
from treelib import Node, Tree
import math
from tree_toolkit import *

# Finds path from curr_node to the node with node_key
def find_path(tr, curr_node, path, node_key):
    # print("find_path")
    path.append(curr_node)
    if curr_node == node_key:
        return True
    for child in tr.children(curr_node):
        if (find_path(tr, child.identifier, path, node_key)):
            return True
    path.pop()
    return False

# computes the least common ancestor
def lca(tr, key1, key2):
    # print("lca called")
    path1 = []
    path2 = []
    find_path1 = find_path(tr, tr.root, path1, key1)
    find_path2 = find_path(tr, tr.root, path2, key2)
    if not find_path1 or not find_path2:
        raise Exception("no path found from root to node")
    index = 0
    min_len = min(len(path1), len(path2))
    while (path1[index] == path2[index] and index <min_len):
        index += 1
    return path1[index-1]


# computes all rooted triplets in a tree
def root_triplets(tr):
    print("root_triplets and num leaves:")
    # create dictionary triplet where triplet(z) is a set of forzen sets such that {x,y}
    # is in triplet(z) if xy|z is a resolved triplet in tr
    triplets = {}
    leafs = tr.leaves()
    print(len(leafs))
    for leaf in leafs:
        z = leaf.identifier
        for x_node in leafs:
            for y_node in leafs:
                x = x_node.identifier
                y = y_node.identifier
                # print("x: %i; y: %i, z: %i" % (x, y, z))
                if x != y and y != z and z != x:
                    # check if xy|z
                    lca_xy = lca(tr,x,y)
                    lca_xz = lca(tr,x,z)
                    lca_yz = lca(tr,y,z)
                    # print("xy: %i; xz %i; yz %i" % (lca_xy,lca_xz,lca_yz))
                    if lca_xz == lca_yz and lca_xy != lca_xz:
                        # print("in branch")
                        # need to add xy|z
                        xy = frozenset([x,y])
                        if z in triplets:
                            triplets[z].add(xy)
                        else:
                            triplets[z] = set()
                            triplets[z].add(xy)
    return triplets



# assume that if x=[] if x doesn't have an assignment. Likewise for the others. An assignment is id of node
def prq(x,y,z,tree,num_leafs,q,num_pairs_diff_subtree,num_pairs_same_tree):
    if x == [] and y == [] and z == []:
        return 1/3 - 4/3*1/((q+1)*(q+1))
    elif x != [] and y == [] and z == []:
        # if y is assigned to the leaf of x, z can be any other leaf, hence the num_leafs - 1
        # otherwise its the number of pairs, (z,y) that appear in different subtrees, hence num_pairs_diff_subtree
        return 1/num_leafs * 1/num_leafs * (num_leafs - 1 + num_pairs_diff_subtree[x[0]])
    elif x == [] and y != [] and z == []:
        return 1/num_leafs * 1/num_leafs * (num_leafs - 1 + num_pairs_diff_subtree[y[0]])
    elif x == [] and y == [] and z != []:
        return 1/num_leafs * 1/num_leafs * (num_leafs - 1 + 2*num_pairs_diff_subtree[z[0]])
    elif x != [] and y != [] and z == []:
        lca_node = lca(tree,x[0],y[0])
        return 1/num_leafs * (num_leafs - len(tree.leaves(lca_node)))
    elif x != [] and y == [] and z != []:
        lca_node = lca(tree,x[0],z[0])
        if lca_node == x[0]:
            return 0.0
        i = 0
        # want to check which subtree contains child
        child1 = tree.children(lca_node)[0].identifier
        child2 = tree.children(lca_node)[1].identifier
        if tree.subtree(child1).contains(x[0]):
            i = child1
        else:
            i = child2
        return 1/num_leafs * len(tree.leaves(i))
    elif x == [] and y != [] and z != []:
        lca_node = lca(tree,y[0],z[0])
        if lca_node == y[0]:
            return 0.0
        i = 0
        child1 = tree.children(lca_node)[0].identifier
        child2 = tree.children(lca_node)[1].identifier
        if tree.subtree(child1).contains(y[0]):
            i = child1
        else:
            i = child2
        return 1/num_leafs * len(tree.leaves(i))
    else:
        # last case is x!=[],y!=[],z!=[]
        return float((lca(tree,x[0],z[0]) == lca(tree,y[0],z[0])) and (lca(tree,x[0],z[0]) != lca(tree,x[0],y[0])))
        
        

# assume leaf_set is a set of positive integers and triplets, a set of rooted triplets
def qmaxrtc(q, leaf_set, triplets):
    # first we need to construct a full binary tree
    # assume q=2^k-1 for k>1. So we want to construct a complete binary tree of depth
    # k-1 and this will yield a tree of size q
    depth_tree = int(math.log(q+1,2)) - 1
    node_ids = [-(i+1) for i in range(0, q)] # ensure our labeling set is negative to be disjoint with leaf_set
    new_tr = Tree()
    new_tr.create_node("n0", 0)
    create_binary_tree(new_tr, 0, node_ids, depth_tree, 0)
    tree_leaf_set = [n.identifier for n in new_tr.leaves()]

    num_pairs_diff_subtree = {}
    num_pairs_same_tree = {}

    computer_diff_pairs_subtree(new_tr, 0, 0, num_pairs_diff_subtree, num_pairs_same_tree, q)


    # our goal is to asssign each leaf in leaf_set to an element of tree_leaf_set
    assignments = {}
    for leaf in leaf_set:
        assignments[leaf] = []

    prev = 1/3 - 4/3*(q+1)*(q+1)*len(triplets)

    # assign each leaf
    for leaf in leaf_set:
        leaf_triplets = []
        # to compute all triplets xy|z that l is a part of
        for t in triplets:
            if t == leaf:
                for f_set in triplets[t]:
                    leaf_triplets.append((f_set,leaf))
            else:
                for f_set in triplets[t]:
                    for elm in f_set:
                        if elm == leaf:
                            leaf_triplets.append((f_set,t))
        
        vals = {}
        # initialization
        # vals[potential_parent] will be E[W|assignments, leaf assigned to potential_parent] at the end
        for potential_parent in tree_leaf_set:
            vals[potential_parent] = prev
        
        for (f_set,z) in leaf_triplets:
            x,y = f_set
            # consider every possible assignment of leaf to a node in tree_leaf_set
            # base case is leaf is unassaigned
            assignments[leaf] = []
            for potential_parent in tree_leaf_set:
                prob = prq(assignments[x],
                            assignments[y],
                            assignments[z],
                            new_tr,
                            len(tree_leaf_set),
                            q,
                            num_pairs_diff_subtree,
                            num_pairs_same_tree)
                vals[potential_parent] -= prob

            for potential_parent in tree_leaf_set:
                assignments[leaf] = [potential_parent]
                prob = prq(assignments[x],
                            assignments[y],
                            assignments[z],
                            new_tr,
                            len(tree_leaf_set),
                            q,
                            num_pairs_diff_subtree,
                            num_pairs_same_tree)
                vals[potential_parent] += prob
        # now we want to compute max
        



def pr2(x, y, z):
    # a is 0 and b is 1
    if x == [-1] or y == [-1] or z == [0]:
        return 0
    p = 4/27
    if x == [0]:
        p = 3/2*p
    if y == [0]:
        p = 3/2*p
    if z == [-1]:
        p = 3*p
    return p

# def prq(x, y, z):
#     if 

# def qmaxrtc(q, leaf_set, triplets):
#     if q % 2 == 0:
#         q = q-1
#     ew_a = 1/3 - 4/3*1/((q+1)*(q+1))
#     ew = ew_a * len(triplets)


#     for leaf in leaf_set:

def two_maxrtc(leaf_set, triplets):
    print("two_maxrtc invoked")
    # n = len(leaf_set)
    # define a tree with two internal nodes
    # a is 0 and b is 1
    new_tr = Tree()
    new_tr.create_node("n0", -1)
    new_tr.create_node("n1", 0, parent=-1)

    prev = 4/27*(len(triplets))

    assignments = {}

    for leaf in leaf_set:
        assignments[leaf] = []

    for leaf in leaf_set:
        # want to compute the set of triplets a part of
        leaf_triplets = []
        for t in triplets:
            if t == leaf:
                for f_set in triplets[t]:
                    leaf_triplets.append((f_set,leaf))
            else:
                for f_set in triplets[t]:
                    for elm in f_set:
                        if elm == leaf:
                            leaf_triplets.append((f_set,t))
        
        aval = prev
        bval = prev
        for j in range(0, len(leaf_triplets)):
            (f_set, z2) = leaf_triplets[j]
            x2,y2 = f_set
            # x2 = f_set.pop()
            # y2 = f_set.pop()
            # if z2 == leaf:
            #     y2 = f_set.pop()
            #     x2 = f_set.pop()
            #     y2 = assignments[y2]
            #     x2 = assignments[x2]
            assignments[leaf] = []
            pr_two = pr2(assignments[x2],assignments[y2],assignments[z2])
            aval = aval - pr_two
            bval = bval - pr_two

            assignments[leaf] = [-1]
            pr_two = pr2(assignments[x2],assignments[y2],assignments[z2])
            aval = aval + pr_two

            assignments[leaf] = [0]
            pr_two = pr2(assignments[x2],assignments[y2],assignments[z2])
            bval = bval + pr_two

        assignments[leaf] = [0]
        prev = bval
        if aval > bval:
            assignments[leaf] = [-1]
            prev = aval
        name = "n" + str(leaf)
        new_tr.create_node(name, leaf, parent=assignments[leaf][0])
    
    return new_tr
    

def tree_size(stack_k, new_tr, parent_id):
    if not stack_k.empty():
        id = stack_k.pop()
        label = "n" + str(id)
        new_tr.create_node(label, id, parent=parent_id)
        tree_size(stack_k, new_tr, id)
        id2 = stack_k.pop()
        label = "n" + str(id2)
        new_tr.create_node(label, id2, parent=parent_id)
        tree_size(stack_k, new_tr, id2)




# dataset 1, 55 leaves
# 0.007703081232492998


# compute intersection of resolved triplets
def intersection(triplets1, triplets2):
    print("computing intersection")
    intersection_set = []
    for t1 in triplets1:
        for t2 in triplets2:
            if t1 == t2:
                for fset1 in triplets1[t1]:
                    for fset2 in triplets2[t2]:
                        if fset1 == fset2:
                            intersection_set.append((fset1,t1,t2))
            # fset1 = triplets1[t1]
            # (fset1,leaf1) = t1
            # (fset2,leaf2) = t2
            # x,y = fset1
            # x2,y2 = fset2
            # if x == x2 and y == y2 and leaf1 == leaf2:
            #     intersection_set.append(t1)
            # elif x == y2 and y == x2 and leaf1 == leaf2:
            #     intersection_set.append(t1)
    return len(intersection_set)


def parse_newick(trees, new_tr, parent_id, st_ids):
    # print("parsing newick")
    if trees == []:
        return

    # indices = [2*(i+1) for i in range(0, len(trees))]

    for i in range(0, len(trees)):
        tree = trees[i]
        id = st_ids.pop()
        label = "n" + str(id)
        new_tr.create_node(label, id, parent=parent_id)
        parse_newick(tree.descendants, new_tr, id, st_ids)
        # new_tr.create_node("n3", 3, parent=9)

    


def parse_tree(fname):
    trees = read(fname)
    new_tr = Tree()
    new_tr.create_node("root", 1)
    size = 2*len(trees[0].get_leaves())+1
    st_ids = []
    for i in range(2, size+2):
        st_ids.append(i)

    parse_newick(trees[0].descendants, new_tr, 1, st_ids)

    return new_tr

'''
1
size of tree:
221
size of triplet set
111
computing intersection
0.0011419753086419754

2
0.0018581802648440838
size of tree:
173
num triplets: 87

3
0.001621716904635995
size of tree:
183
num triplets:
92

4
size of tree:
185
size of triplet set
93

computing intersection
0.0018500099462900339
i is
5
size of tree:
163
size of triplet set
82
root_triplets and num leaves:
82
computing intersection
0.0029918272037361355
'''

def main():
    for i in [3]:
        name = "data" + str(i) + ".txt"
        t = parse_tree(name)
        # t = t.remove_subtree(101)
        print("i is ")
        print(i)
        print("size of tree:")
        print(len(t.all_nodes()))
        rt = root_triplets(t)
        print("size of triplet set")
        print(len(rt))
        leafs = []
        for i in t.leaves():
            leafs.append(i.identifier)
        rt2 = two_maxrtc(leafs, rt)
        print(len(rt2))
        denom = intersection(rt, root_triplets(rt2))
        print(len(rt)/denom)



if __name__ == "__main__":
    main()


