from copy import copy, deepcopy
from pprint import pprint


class Knuth():
    def __init__(self, graph):
        self.adjacency_list = graph.graph
        self.spanning_tree = graph.spanning_tree()
        self.calculate_weights_steps = []

    
    def set_edge_weights(self):
        # create new adjacency list that will have weight for every edge
        # this will be the output
        self.adjacency_list_with_weights = {}

        for node in self.adjacency_list:
            self.adjacency_list_with_weights[node] = []

        # add edges not in the spanning tree to it
        for node in self.adjacency_list:
            for edge in self.adjacency_list[node]:
                if edge not in self.spanning_tree[node]:
                    self.adjacency_list_with_weights[node].append(copy(edge))

        spanning_tree_inverse_graph = deepcopy(self.adjacency_list_with_weights)

        # to emulate Knuth's algortihm
        # set weight to zero for every edge in adjacency list
        # that belongs to the spanning tree (edges with no counters!)
        for node in self.spanning_tree:
            for edge in self.spanning_tree[node]:
                edge_index = self.adjacency_list[node].index(edge)
                self.adjacency_list[node][edge_index][1] = 0

        # get edge representation of the spanning tree (needed for the algorithm)
        spanning_tree_edges = self.get_edges(self.spanning_tree)

        # set weights in spanning tree to zero (these weights will be calculated)
        for edge in spanning_tree_edges:
            edge[2] = 0

        # print('***')
        # pprint(self.adjacency_list_with_weights)
        # print('***')
        self.calculate_weights(spanning_tree_edges, 'START', None)

        return (
            spanning_tree_inverse_graph,
            self.calculate_weights_steps
        )


    def calculate_weights(self, spanning_tree_edges, node, edge):
        edges_in = self.get_incoming_edges(node)
        edges_out = self.get_outgoing_edges(node)

        in_sum = 0
        for in_edge in edges_in:
            if in_edge != edge and in_edge in spanning_tree_edges:
                self.calculate_weights(spanning_tree_edges, in_edge[0], in_edge)
            in_sum += in_edge[2]

        out_sum = 0
        for out_edge in edges_out:
            if out_edge != edge and out_edge in spanning_tree_edges:
                self.calculate_weights(spanning_tree_edges, out_edge[1], out_edge)
            out_sum += out_edge[2]

        if edge != None:
            edge[2] = max(in_sum, out_sum) - min(in_sum, out_sum)
            self.adjacency_list_with_weights[edge[0]].append([edge[1], edge[2]])
            self.calculate_weights_steps.append(deepcopy(self.adjacency_list_with_weights))


    def get_edges(self, graph=None):
        '''
        Get edges in [source_node, destination_node, weight] format
        '''

        if graph == None:
            graph = self.adjacency_list

        edges = []
        for src_node in graph:
            for [dest_node, weight] in graph[src_node]:
                edges.append([src_node, dest_node, weight])

        return edges


    def get_incoming_edges(self, node):
        ''' 
        Incoming edges of a node in a graph.
        Edge format: [source_node, destination_node, weight]
        '''

        edges = []
        for src_node in self.adjacency_list:
            for [dest_node, weight] in self.adjacency_list[src_node]:
                if dest_node == node:
                    edges.append([src_node, dest_node, weight])

        return edges


    def get_outgoing_edges(self, node):
        ''' 
        Outgoing edges of a node in a graph.
        Edge format: [source_node, destination_node, weight]
        '''

        return [
            [node, dest_node, weight]
            for [dest_node, weight] in self.adjacency_list[node]
        ]

