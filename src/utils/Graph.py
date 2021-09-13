from copy import copy


class CFG():
    def __init__(self, block_stack):
        self.graph = self.generate_graph(block_stack)
        self.tree = self.spanning_tree()
        self.block_stack = block_stack
        # self.graph = {
        #     1: [[2, 10]],
        #     2: [[4, 5], [3, 5]],
        #     3: [[6, 5]],
        #     4: [[5, 5]],
        #     5: [[6, 5]],
        #     6: [[8, 6], [7, 4]],
        #     7: [[8, 4]],
        #     8: [[9, 17], [10, 10]],
        #     9: [[8, 17]],
        #     10: [[11, 10]],
        #     11: [[13, 8], [12, 2]],
        #     12: [[17, 2]],
        #     13: [[15, 6], [14, 2]],
        #     14: [[17, 2]],
        #     15: [[17, 2], [16, 4]],
        #     16: [[17, 4]],
        #     17: [['EXIT', 10]],
        #     'EXIT': [['START', 10]],
        #     'START': [[1, 10]]
        # }

    def getGraph(self):
        return self.graph
    def getTree(self):
        return self.tree

    def generate_graph(self, blocks):
        graph = {}
        #block = (block.type, block.id, break_marker, false)
        for t, block_id, f, m in blocks:
            graph[block_id] = []

        # graf is a list of [block.id, weight]
        graph['START'] = [[blocks[0][1], 1]]
        graph['EXIT'] = [['START', 1]]
        # last block is connected to EXIT
        graph[blocks[-1][1]].append(['EXIT', 1])

        for i in range(0, len(blocks)):
            # follow = 0 --> block is inside if_then, else, elif, for or first ordinary block
            # follow = 1 --> block is after if_then, else, elif
            # follow = 2 --> block follows for loop
            block_type, block_id, follows, marked = blocks[i]
            previous_id = block_id - 1

            if follows != 0:  # current block follows for loop or if condition --> previous blocks needs to be linked to current block
                blocks[i - 1][3] = True

                if follows == 1:  # current block is after if condition --> every if else elif  action block has to be linked to current block

                    # check blocks before current block if block is marked (block is marked if it's a block action in if, elif and else condition) than link that block to current block
                    for j in reversed(range(block_id)):
                        if blocks[j][3] and blocks[j][2] != 2:
                            if [block_id, 1] not in graph[blocks[j][1]]:
                                graph[blocks[j][1]].append([block_id, 1])

                        # if we get to if block there is no need to go deeper beacuse every condition block is linked to current block
                        if blocks[j][0] == 'IF_THEN' and j != block_id - 1:
                            break
                else:  # current block is after for loop
                    for_block_id = 0
                    # find block_id for for loop block
                    for j in reversed(range(block_id)):
                        if blocks[j][0] == 'FOR':
                            for_block_id = blocks[j][1]
                            break
                        # set mark for for-block to False
                        blocks[j][3] = False

                    # connect previous block (block inside of a for loop) to a for-loop block
                    if [for_block_id, 1] not in graph[previous_id]:
                        graph[previous_id].append([for_block_id, 1])

                    # connect for-loop block to a current block
                    if [block_id, 1] not in graph[for_block_id]:
                        graph[for_block_id].append([block_id, 1])

            if block_type == 'IF_THEN':
                # link previous block to if-then block
                if block_id != 1:
                    if [block_id, 1] not in graph[previous_id]:
                        graph[previous_id].append([block_id, 1])

                j = block_id

                # while loop is connecting if-block with it's else or elif block or block that follows - breaks when it finds first
                # change : while j < len(blocks)
                while (j < len(blocks)):
                    #     # if blocks[j][0] == 'if':
                    #         # if_counters += 1
                    if blocks[j][0] in ['ELSE', 'ELIF'] or blocks[j][2] == 1:
                        if [blocks[j][1], 1] not in graph[block_id]:
                            graph[block_id].append([blocks[j][1], 1])
                        break

                    j += 1

            elif block_type == 'ELIF':
                for j in reversed(range(block_id)):
                    # blocks[j][1] is block_id so it cannot be in list ['ELIF', 'IF_THEN'] - this if always happens

                    if blocks[j][2] != 0 or blocks[j][1] not in ['ELIF', 'IF_THEN']:
                        break

                    # if we change to blocks[j][0] first j is equal to ELIF block_id so we get to this code that connects ELIF block to block before that (block action for if-block or block action for elif block) and that doesnt make sense
                    if [blocks[j-1][1], 1] not in graph[blocks[j][1]]:
                        graph[blocks[j][1]].append([blocks[j-1][1], 1])

                # idi u napred i nadji decu sa kojom nisi povezan
                # if_counters = 0
                j = block_id
                # block_id is from 1 to number of nodes
                # blocks[i] is from 0 to number of nodes - 1
                # add while j < len(blocks)
                while (j<len(blocks)):  # connects current block to ELSE or ELIF block or block that follows IF-THEN condition - breaks when it finds first
                    #     # if blocks[j][0] == 'if':
                    #         # if_counters += 1

                    if blocks[j][0] in ['ELSE', 'ELIF'] or blocks[j][2] == 1:
                        if [blocks[j][1], 1] not in graph[block_id]:
                            graph[block_id].append([blocks[j][1], 1])
                        break

                    j += 1
                # markes block before current block to True (action block to if condition or else, elif action block)
                blocks[i - 1][3] = True
            elif block_type == 'ORDINARY':
                # this segment links all Ordinary blocks to its previous block except the block after for
                if block_id != 1:
                    # block after for loop block (for-loop block already connects for-loop to ordinary block inside)
                    if blocks[i][2] == 2:
                        continue

                    if [block_id, 1] not in graph[previous_id]:
                        graph[previous_id].append([block_id, 1])

            elif block_type == 'ELSE':
                # ELSE is already linked to inside ordinary block in condition above
                # goes through previous blocks same problem as for ELIF (dont understand the idea)
                for j in reversed(range(block_id)):
                    if blocks[j][2] != 0 or blocks[j][1] not in ['ELIF', 'IF']:
                        break

                    if [blocks[j-1][1], 1] not in graph[blocks[j][1]]:
                        graph[blocks[j][1]].append([blocks[j-1][1], 1])
                # marks block inside of a ELSE branch
                blocks[i - 1][3] = True
            elif block_type == 'FOR':
                # connects previous block to for-block
                # inside block is connected to for block in condition follows == 2 and for block is connected to inside block there
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

    def isCyclicUtil(self, v, visited, parent):
        visited[v] = True
        for dest, weight in self.tree[v]:
            if visited[dest] == False:
                if self.isCyclicUtil(dest, visited, v) == True:
                    return True
            elif dest != parent:
                return True

        return False
    def isTree(self):
        visited = {}
        visited["START"] = False
        visited["EXIT"] = False
        for block in self.block_stack:
            visited[block[1]] = False

        if self.isCyclicUtil("EXIT", visited, -1) == True:
            return False

        for node in self.tree:
            if visited[node] == False:
                return False
        return True