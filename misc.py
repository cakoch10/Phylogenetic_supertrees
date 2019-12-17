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