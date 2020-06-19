
class Node():
    def __init__(self,data, parent, index, id = None, scope = "global"):
        self.data = data
        self.children = []
        self.parent = parent
        self.index = index
        self.id = id
        self.scope = scope

    def __repr__(self, level = 0):
        value = self.id if self.data in ['[0-9]*', '[a-zA-Z]*'] else self.data
        ret = str(level) + "|" + "\t\t" * level + repr(value)
        if len(self.children) == 0:
            ret += " *LEAF\n"
        else:
            ret += "\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret

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

    def set_symbol_table(self):
        node = self
        symbol_table =[]
        while len(node.children) != 0:
            node = node.children[0]
        while node.parent != None:
            if node.data in ["int","char"]:
                tp = node.data
                size = 4 if tp=="int" else 1
                while node.data != ';' :
                    node = node.get_next()
                    if node.data == "[a-zA-Z]*":
                        symbol_table.append([node.id,tp,"block local",size])
            node = node.get_next()
        return symbol_table


if __name__ == "__main__":
    node = Node("asdf", None, 0)
    node.set_child([1,2,3])
    node.children[0].set_child([4])
    node.children[1].set_child([5,6])
    node.children[2].set_child([7,8])
    node.children[2].children[0].set_child([9])
    #node2 = node.children[0].children[0]
    #node.node_print()
    print(node)

    _node = node
   # while _node != None :
    #    print(node.data)
     #   _node = _node.get_next()


