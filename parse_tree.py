
class Node():
    def __init__(self,data, parent, index, id = None, scope = "global"):
        self.data = data
        self.children = []
        self.parent = parent
        self.index = index
        self.id = id
        self.scope = scope

    def set_child(self, data):
        for idx, item in enumerate(data):
            node = Node(item,self, idx)
            self.children.append(node)
        return self.children[0]

    def get_next(self):
        index = self.index
        node = self
        cur = self.parent
        while True:
            if cur != None :
                if len(cur.children)-1 == index:
                    index = cur.index
                    node = cur
                    cur = cur.parent
                else:
                    break
            else:
                return node
        cur = cur.children[index+1]
        while len(cur.children) != 0:
            cur = cur.children[0]
        return cur

    def node_print(self):
        node = self
        while len(node.children) != 0:
            node = node.children[0]
        while node.parent != None:
            if node.data in ['[0-9]*','[a-zA-Z]*']:
                print(node.id, end= ' ')
            else:
                print(node.data,end=' ')
            node = node.get_next()

    def get_root(self):
        node = self
        while node.parent != None:
            node = node.parent
        return node

if __name__ == "__main__":
    node = Node("asdf", None, 0)
    node.set_child([1,2,3])
    node.children[0].set_child([4])
    node.children[1].set_child([5,6])
    node.children[2].set_child([7,8])
    node.children[2].children[0].set_child([9])
    node2 = node.children[0].children[0]
    node.node_print()

    while node2 != None:
        print(node2.data)
        node2 = node2.get_next()


