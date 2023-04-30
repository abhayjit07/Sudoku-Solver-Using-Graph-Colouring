
class Node:

    def __init__(self, idx, data=0):  # Constructor
        '''
        __init__(self, idx, data=0): Constructor method that initializes the id and data attributes of a node.
        idx is the unique identifier of the node and data is the optional data value associated with the node.

        '''
        self.id = idx
        self.data = data
        self.connectedTo = dict()

    def addNeighbour(self, neighbour, weight=0):
        """
        neighbour : Node Object
        weight : Default Value = 0
        adds the neightbour_id : wt pair into the dictionary
        """
        if neighbour.id not in self.connectedTo.keys():
            self.connectedTo[neighbour.id] = weight

    # setter
    def setData(self, data):
        '''
        Sets the data attribute of the node to a new value.
        This method is a setter for the data attribute.
        '''
        self.data = data

    # getter
    def getConnections(self):
        '''
        getConnections(self): A method that returns the keys (i.e., ids) of the node's connectedTo dictionary.
        
        '''
        return self.connectedTo.keys()

    def getID(self):
        '''
        getID(self): A method that returns the id of the node.
       
        '''
        return self.id

    def getData(self):
        '''
         getData(self): A method that returns the data of the node.
       
        '''
        return self.data

    def getWeight(self, neighbour):
        '''
         getWeight(self, neighbour): A method that returns the weight of the edge between the node and a given neighbour.
        
        '''
        return self.connectedTo[neighbour.id]

    def __str__(self):
        '''
        str(self): A special method that returns a string representation of the node, showing its data and the data of its neighbours.
        '''
        return str(self.data) + " Connected to : " + \
            str([x.data for x in self.connectedTo])


class Graph:

    totalV = 0  # total vertices in the graph

    def __init__(self):
        """
        allNodes = Dictionary (key:value)
                   idx : Node Object
        """
        self.allNodes = dict()

    def addNode(self, idx):
        """ adds the node """
        if idx in self.allNodes:
            return None

        Graph.totalV += 1
        node = Node(idx=idx)
        self.allNodes[idx] = node
        return node

    def addNodeData(self, idx, data):
        """ set node data acc to idx """
        if idx in self.allNodes:
            node = self.allNodes[idx]
            node.setData(data)
        else:
            print("No ID to add the data.")

    def addEdge(self, src, dst, wt=0):
        """
        Adds edge between 2 nodes
        Undirected graph
        src = node_id = edge starts from
        dst = node_id = edge ends at
        To make it a directed graph comment the second line
        """
        self.allNodes[src].addNeighbour(self.allNodes[dst], wt)
        self.allNodes[dst].addNeighbour(self.allNodes[src], wt)

    def isNeighbour(self, u, v):
        """
        check neighbour exists or not
        """
        if u >= 1 and u <= 256 and v >= 1 and v <= 256 and u != v:
            if v in self.allNodes[u].getConnections():
                return True
        return False

    def printEdges(self):
        """ print all edges """
        for idx in self.allNodes:
            node = self.allNodes[idx]
            for con in node.getConnections():
                print(node.getID(), " --> ",
                      self.allNodes[con].getID())

    
    def getNode(self, idx):
        if idx in self.allNodes:
            return self.allNodes[idx]
        return None

    def getAllNodesIds(self):
        return self.allNodes.keys()



