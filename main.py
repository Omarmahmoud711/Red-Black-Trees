class Node():
    def __init__(self, val):
        self.val = val
        self.parent = None
        self.left = None
        self.right =None
        self.color = 1


class RBTree():
    def __init__(self):
        self.NULL = Node(0)
        self.NULL.color = 0
        self.NULL.left = None
        self.NULL.right = None
        self.root = self.NULL

    def insertNode(self, key):
        node = Node(key)
        node.parent = None
        node.val = key
        node.left = self.NULL
        node.right = self.NULL
        node.color = 1

        y = None
        x = self.root

        while x != self.NULL:
            y = x
            if node.val < x.val:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y == None:
            self.root = node
        elif node.val < y.val:
            y.left = node
        else:
            y.right = node

        if node.parent == None:
            node.color = 0
            return

        if node.parent.parent == None:
            return

        self.fixInsert(node)

    # def search(self, value):
    #     node = self.root
    #     while node.val != value:
    #         if node.val > value:
    #             node = node.left
    #         else:
    #             node = node.right
    #         if node.val == value:
    #             return node.val
    #     return 0
    def search(self, value):
        node = self.root
        while node != self.NULL and node.val != value:
            if node.val > value:
                node = node.left
            else:
                node = node.right
        return node.val if node != self.NULL else None

    def LR(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def RR(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.NULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def fixInsert(self, k):
        while k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.RR(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.LR(k.parent.parent)
            else:
                u = k.parent.parent.right
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.LR(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.RR(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 0

    def __printCall(self, node, indent, last):
        if node != self.NULL:
            print(indent, end=' ')
            if last == 'root':
                print("ROOT----", end=' ')
                indent += "     "
            elif last == 'right':
                print("R----", end=' ')
                indent += "     "
            elif last == 'left':
                print("L----", end=' ')
                indent += "|    "

            s_color = "RED" if node.color == 1 else "BLACK"
            print(str(node.val) + "(" + s_color + ")")
            self.__printCall(node.left, indent, 'left')
            self.__printCall(node.right, indent, 'right')

    def print_tree(self):
        self.__printCall(self.root, "", 'root')

        # Function to fix issues after deletion

    def fixDelete(self, x):
        while x != self.root and x.color == 0:  # Repeat until x reaches nodes and color of x is black
            if x == x.parent.left:  # If x is left child of its parent
                s = x.parent.right  # Sibling of x
                if s.color == 1:  # if sibling is red
                    s.color = 0  # Set its color to black
                    x.parent.color = 1  # Make its parent red
                    self.LR(x.parent)  # Call for left rotate on parent of x
                    s = x.parent.right
                # If both the child are black
                if s.left.color == 0 and s.right.color == 0:
                    s.color = 1  # Set color of s as red
                    x = x.parent
                else:
                    if s.right.color == 0:  # If right child of s is black
                        s.left.color = 0  # set left child of s as black
                        s.color = 1  # set color of s as red
                        self.RR(s)  # call right rotation on x
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = 0  # Set parent of x as black
                    s.right.color = 0
                    self.LR(x.parent)  # call left rotation on parent of x
                    x = self.root
            else:  # If x is right child of its parent
                s = x.parent.left  # Sibling of x
                if s.color == 1:  # if sibling is red
                    s.color = 0  # Set its color to black
                    x.parent.color = 1  # Make its parent red
                    self.RR(x.parent)  # Call for right rotate on parent of x
                    s = x.parent.left

                if s.right.color == 0 and s.right.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.left.color == 0:  # If left child of s is black
                        s.right.color = 0  # set right child of s as black
                        s.color = 1
                        self.LR(s)  # call left rotation on x
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = 0
                    s.left.color = 0
                    self.RR(x.parent)
                    x = self.root
        x.color = 0

    # Function to transplant nodes
    def __rb_transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    # Function to handle deletion
    def delete_node_helper(self, node, key):
        z = self.NULL
        while node != self.NULL:  # Search for the node having that value/ key and store it in 'z'
            if node.val == key:
                z = node

            if node.val <= key:
                node = node.right
            else:
                node = node.left

        if z == self.NULL:  # If Kwy is not present then deletion not possible so return
            print("Value not present in Tree !!")
            return

        y = z
        y_original_color = y.color  # Store the color of z- node
        if z.left == self.NULL:  # If left child of z is NULL
            x = z.right  # Assign right child of z to x
            self.__rb_transplant(z, z.right)  # Transplant Node to be deleted with x
        elif (z.right == self.NULL):  # If right child of z is NULL
            x = z.left  # Assign left child of z to x
            self.__rb_transplant(z, z.left)  # Transplant Node to be deleted with x
        else:  # If z has both the child nodes
            y = self.minimum(z.right)  # Find minimum of the right sub tree
            y_original_color = y.color  # Store color of y
            x = y.right
            if y.parent == z:  # If y is child of z
                x.parent = y  # Set parent of x as y
            else:
                self.__rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.__rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 0:  # If color is black then fixing is needed
            self.fixDelete(x)

    def height(self, node):
        if node == self.NULL:
            return 0
        else:
            left_height = self.height(node.left)
            right_height = self.height(node.right)
            return max(left_height, right_height) + 1

    def get_height(self):
        return self.height(self.root)


    # Deletion of node
    def delete_node(self, val):
        self.delete_node_helper(self.root, val)  # Call for deletion


bst = RBTree()
file = open('EN-US-Dictionary.txt', 'r')
n = 0
read = file.readlines()
for line in read:
    n = n + 1
    bst.insertNode(line.strip())
bst.print_tree()
t = True
S = True
D = True

while t:
    print("do U want to insert ? y/n ")
    if input() == "y":
        t = True
        insertNode = input("insert a node : ")
        found = bst.search(insertNode)
        if found:
            print("Error:Word already in the dictionary")
        else:
            bst.insertNode(insertNode)
            print("Inserted Successfully")
            n = n + 1
    else:
        t = False
while S:
    print("do U want to search? y/n ")
    if input() == "y":
        S = True
        deleteddWord = input("Enter the value you want search : ")
        found = bst.search(deleteddWord)
        if found:
            print("YES," + input() + " is in the BST tree")
        else:
            print("NO," + input() + " isn't in the BST tree")
    else:
        S = False
    print("do U want to Delete? y/n ")
    if input() == "y":
        D = True
        deleteddWord = input("Enter the value you want search : ")
        bst.delete_node(deleteddWord)
        bst.print_tree()

print("do U want to get height ?")
if input() == "y":
    print(bst.get_height())
