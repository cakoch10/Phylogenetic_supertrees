from newick import read
from Bio import Phylo


# methods to help with data wrangling

def f(s, i, term):
    names = []
    for k in range(s,i):
        name = term[k].name
        names.append(name)
    return names

def get_subtree(tree, i):
    terminals = tree.get_terminals()
    for j in range(0,len(terminals)-1):
        comm = tree.common_ancestor(f(j,j+3,terminals))
        n = len(comm.get_nonterminals())
        if 80 <= n and n<150:
            print("Writing subtree to file!")
            Phylo.write(comm,"data"+str(i)+".txt","newick")
            break

# main loop
for j in range(1,6):
    name = "Datafile_S" + str(j) + ".txt"
    tree = Phylo.read(name, "newick")
    get_subtree(tree,j)

# tree = Phylo.read(name, "newick")
# lst = ['Meiothermus_silvanus_DSM_9946_uid49485','Meiothermus_ruber_DSM_1279_uid46661','Thermus_thermophilus_HB8_uid58223']
# comm = tree.common_ancestor(lst)
# len(comm.get_nonterminals())
#  Phylo.write(comm,"data1.txt","newick")
