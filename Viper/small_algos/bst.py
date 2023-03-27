class Node:
    def __init__(self,key,parent=None):
        self.key = key
        self.left = None
        self.right = None
        self.parent = parent

    def __repr__(self):
        return f"""self={self.key}
left={self.left}
right={self.right}"""
    def __gt__(self,x):
        return self.key > x
    def __lt__(self,x):
        return self.key < x
    
        
class BST:
    root = None
    
    @classmethod
    def insert(cls,node):
        if not cls.root:
            cls.root = node
            return
        
        cur_node = cls.root
        while node.parent is None:
            if node < cur_node:
                if cur_node.left:
                    cur_node = cur_node.left
                else:
                    cur_node.left = node
                    node.parent = cur_node
            else:
                if cur_node.right:
                    cur_node = cur_node.right
                else:
                    cur_node.right = node
                    node.parent = cur_node
    @classmethod
    def find(cls,node):
        smallest_child = None
        if node.right:
            cur_node = node.right
            while cur_node.left:
                cur_node = cur_node.left
            return cur_node
        if node.parent:
            cur_node = node
            while cur_node.parent.right == cur_node: #as long parent is smaller
                cur_node = cur_node.parent
                if not cur_node.parent:
                    break
            else:
                smallest_child = cur_node.parent
        return smallest_child
                    

    
if __name__ == "__main__":
    root = Node(30)
    t = Node(40)
    BST.insert(root)
    for x in (23,51,12,32,16,43,713):
        BST.insert(Node(x))
    BST.insert(t)
    # print(root)
    print(BST.find(t).key)
    