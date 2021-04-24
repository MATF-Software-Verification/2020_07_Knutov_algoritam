from copy import copy


class CFG():
    def __init__(self, block_stack):
        self.graph = self.generate_graph(block_stack)
        self.graph = {
            1: [[2, 10]],
            2: [[4, 5], [3, 5]],
            3: [[6, 5]],
            4: [[5, 5]],
            5: [[6, 5]],
            6: [[8, 6], [7, 4]],
            7: [[8, 4]],
            8: [[9, 17], [10, 10]],
            9: [[8, 17]],
            10: [[11, 10]],
            11: [[13, 8], [12, 2]],
            12: [[17, 2]],
            13: [[15, 6], [14, 2]],
            14: [[17, 2]],
            15: [[17, 2], [16, 4]],
            16: [[17, 4]],
            17: [['EXIT', 10]],
            'EXIT': [['START', 10]],
            'START': [[1, 10]]
        }

    def getGraph(self):
        return self.graph

    def generate_graph(self, blocks):
        graph = {}
        for t, block_id, f, m in blocks:
            graph[block_id] = []

        graph['START'] = [[blocks[0][1], 1]]
        graph['EXIT'] = [['START', 1]]
        graph[blocks[-1][1]].append(['EXIT', 1])

        for i in range(0, len(blocks)):
            block_type, block_id, follows, marked = blocks[i]
            previous_id = block_id - 1

            if follows != 0:
                blocks[i - 1][3] = True

                if follows == 1:
                    for j in reversed(range(block_id)):
                        if blocks[j][3] and blocks[j][2] != 2:
                            if [block_id, 1] not in graph[blocks[j][1]]:
                                graph[blocks[j][1]].append([block_id, 1])

                        if blocks[j][0] == 'IF_THEN' and j != block_id - 1:
                            break
                else:
                    for_block_id = 0
                    for j in reversed(range(block_id)):
                        if blocks[j][0] == 'FOR':
                            for_block_id = blocks[j][1]
                            break
                        blocks[j][3] = False

                    if [for_block_id, 1] not in graph[previous_id]:
                        graph[previous_id].append([for_block_id, 1])

                    if [block_id, 1] not in graph[for_block_id]:
                        graph[for_block_id].append([block_id, 1])

            if block_type == 'IF_THEN':
                if block_id != 1:
                    if [block_id, 1] not in graph[previous_id]:
                        graph[previous_id].append([block_id, 1])

                j = block_id
                while (True):
                #     # if blocks[j][0] == 'if':
                #         # if_counters += 1
                    if blocks[j][0] in ['ELSE', 'ELIF'] or blocks[j][2] == 1:
                        if [blocks[j][1], 1] not in graph[block_id]:
                            graph[block_id].append([blocks[j][1], 1])
                        break

                    j += 1

            elif block_type == 'ELIF':
                # idi u nazad i povezi sve sto nisu nakon if / for
                for j in reversed(range(block_id)):
                    if blocks[j][2] != 0 or blocks[j][1] not in ['ELIF', 'IF_THEN']:
                        break

                    if [blocks[j-1][1], 1] not in graph[blocks[j][1]]:
                        graph[blocks[j][1]].append([blocks[j-1][1], 1])

                # idi u napred i nadji decu sa kojom nisi povezan
                # if_counters = 0
                j = block_id
                while (True):
                #     # if blocks[j][0] == 'if':
                #         # if_counters += 1
                    if blocks[j][0] in ['ELSE', 'ELIF'] or blocks[j][2] == 1:
                        if [blocks[j][1], 1] not in graph[block_id]:
                            graph[block_id].append([blocks[j][1], 1])
                        break

                    j += 1

                blocks[i - 1][3] = True        
            elif block_type == 'ORDINARY':
                if block_id != 1:
                    if blocks[i][2] == 2:
                        continue

                    if [block_id, 1] not in graph[previous_id]:
                        graph[previous_id].append([block_id, 1])

            elif block_type == 'ELSE':
                for j in reversed(range(block_id)):
                    if blocks[j][2] != 0 or blocks[j][1] not in ['ELIF', 'IF']:
                        break

                    if [blocks[j-1][1], 1] not in graph[blocks[j][1]]:
                        graph[blocks[j][1]].append([blocks[j-1][1], 1])

                blocks[i - 1][3] = True
            elif block_type == 'FOR':
                if block_id != 1:
                    if [block_id, 1] not in graph[previous_id]:
                        graph[previous_id].append([block_id, 1])


        return graph

    def spanning_tree(self):
        start_node = 'EXIT'

        marked_nodes = {}
        tree = {}

        # mark start node as visited
        marked_nodes[start_node] = True

        # initialize stack
        stack = [start_node]

        while len(stack) > 0:
            # take element (node) from the top of the stack
            current_node = stack[-1]

            if current_node not in tree:
                tree[current_node] = []

            # every node is visited
            if len(marked_nodes) == len(self.graph):
                spanning_tree = copy(tree)
                for node in spanning_tree:
                    for (dest_node, weight) in spanning_tree[node]:
                        if dest_node not in spanning_tree:
                            tree[dest_node] = []
                spanning_tree = copy(tree)
                return copy(tree)

            # visit unmarked neighbour
            has_unvisited = False
            for (dest_node, weight) in self.graph[current_node]:
                if dest_node not in marked_nodes:
                    stack.append(dest_node)
                    marked_nodes[dest_node] = True

                    tree[current_node].append([dest_node, weight])
                    has_unvisited = True

            # if every neighbor of the node
            # is visited remove it from stack
            if not has_unvisited:
                stack.pop()

        return -1

    def spanning_tree_inverse(self, tree=None):
        if not tree:
            tree = self.spanning_tree()

        inverse = {}
        for src_node in self.graph:
            inverse[src_node] = []

        for src_node in self.graph:
            for [dest_node, weight] in self.graph[src_node]:
                if [dest_node, weight] not in tree[src_node]:
                    inverse[src_node].append([dest_node, weight])

        return inverse

