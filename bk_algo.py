"""Boruvka-Kruskal Algorithm for finding Minimum Spanning Tree in a Graph"""


class Graph:
    """A class to represent the graph"""

    def __init__(self, graph):
        self.vertices = graph[0]
        self.mst = []                                   # minimum spanning tree
        self.node_list = graph[1]
        self.size = []
        self.name = []
        self.next = []

    def merge_trees(self, node_v, node_w, p, q):
        """A function to merge trees"""
        self.name[node_w] = p
        u = self.next[node_w]
        while self.name[u] != p:
            self.name[u] = p
            u = self.next[u]
        self.size[p] = self.size[p] + self.size[q]
        self.next[node_v], self.next[node_w] = self.next[node_w], self.next[node_v]

    def get_mst(self):
        """A function to find and form minimum spanning tree using Boruvka's algorithm"""
        self.name = [x for x in range(self.vertices)]
        self.size = [1 for _ in range(self.vertices)]
        self.next = [x for x in range(self.vertices)]

        while len(self.mst) != self.vertices - 1:
            node_v, node_w, weight = self.node_list.pop()
            p = self.name[node_v]
            q = self.name[node_w]
            if p != q:
                if self.size[p] > self.size[q]:
                    self.merge_trees(node_w, node_v, q, p)
                else:
                    self.merge_trees(node_v, node_w, p, q)
                self.mst.append((node_v, node_w, weight))

    def get_mst_weight_and_path(self):
        """A function to find MST weight and path (route)"""
        path = []
        mst_weight = 0
        for node in self.mst:
            path.append(node)
            mst_weight += node[2]

        res = dict()
        for node in self.mst:
            v, w = node[0], node[1]
            if v not in res.keys():
                res[v] = []
            if w not in res.keys():
                res[w] = []
            res[v].append(w)
            res[w].append(v)
        sorted_res = dict(sorted(res.items()))
        for item in sorted_res.values():
            item.sort()
        return sorted_res, mst_weight


def make_graph(filename):
    """Input handler"""
    with open(filename) as file:
        vertices_num = int(file.readline().strip())
        data = [x.strip().split() for x in file.readlines()]
        node_list = list()

        for idx, lst in enumerate(data):
            lst = lst[:-1]
            node_v, node_w, weight = [int(x) - 1 for x in lst[::2]], \
                                     [i for i in [idx] * len(data)], \
                                     [int(z) for z in lst[1::2]]            # x-1 is to keep indices right
            node_list.append(list(zip(node_v, node_w, weight)))

        flat_list = [item for sublist in node_list for item in sublist]
        flat_list.sort(key=lambda x: -x[2])                         # sorts a list of nodes by weight (Descending)

    return Graph((vertices_num, flat_list))


def write_out(data):
    """Output handler"""
    sorted_dict, weight = data[0], data[1]
    with open('out.txt', 'w') as file:
        for value in sorted_dict.values():
            for item in value:
                file.write(str(item + 1))
                file.write(' ')
            file.write('0' + '\n')
        file.write(str(weight))


if __name__ == '__main__':
    graph1 = make_graph('in.txt')
    # print(graph1)
    graph1.get_mst()
    # print(graph1.get_mst_weight_and_path())
    write_out(graph1.get_mst_weight_and_path())
