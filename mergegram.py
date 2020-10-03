import numpy as np
import networkx as nx
from networkx.algorithms import tree
from scipy.sparse.csgraph import minimum_spanning_tree

class Mergegram():
    def __init__(self, D):
        self.n = D.shape[0]
        G = nx.from_numpy_array(D)
        mst = tree.minimum_spanning_edges(G, algorithm="kruskal", data=True)
        self.edgelist = sorted([(e[0], e[1], e[2]['weight']) for e in list(mst)], 
                               key=lambda x: (x[2], x[0], [1]))
        self.UF = {(d,):0.0 for d in range(self.n)} #Union-Find with prev function images
        self.full = {(d,):0.0 for d in range(self.n)} #Union-Find without removing elements (for plotting) 
        self.output = []
        self._fit()
        
    def _fit(self):
        for e in self.edgelist:
            c1, c2 = self._find(e[0]), self._find(e[1])
            self.output.append((self.UF[c1], e[2]))
            self.output.append((self.UF[c2], e[2]))
            self.UF.pop(c1)
            self.UF.pop(c2)
            t = c1 + c2
            self.UF[t] = e[2]
            self.full[t] = e[2]
            
    def _find(self, c):
        try:
            return self.UF[c]
        except:
            for u in self.UF.keys():
                if type(u)==tuple and c in u:
                    return u
     
    def get_mergegram(self):
        return self.output
