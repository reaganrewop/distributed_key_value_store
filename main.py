import hashlib
import os
import pickle
import time

class TreeNode(object):
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1

class AVL_Tree(object):
    root = None
    min_root = None
    def insert(self, root, key):
        if not root:
            return TreeNode(key)
        elif key < root.val:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(self.getHeight(root.left),
                           self.getHeight(root.right))

        balance = self.getBalance(root)

        if balance > 1 and key < root.left.val:
            return self.rightRotate(root)

        if balance < -1 and key > root.right.val:
            return self.leftRotate(root)

        if balance > 1 and key > root.left.val:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        if balance < -1 and key < root.right.val:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        if not self.min_root:
            self.min_root = key
        elif self.min_root > key:
            self.min_root = key

        return root

    def leftRotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.getHeight(z.left),
                         self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                         self.getHeight(y.right))

        return y

    def rightRotate(self, z):

        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self.getHeight(z.left),
                        self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                        self.getHeight(y.right))

        return y

    def getHeight(self, root):
        if not root:
            return 0

        return root.height

    def getBalance(self, root):
        if not root:
            return 0

        return self.getHeight(root.left) - self.getHeight(root.right)

    def preOrder(self, root):
        if not root:
            return
        print("{0} ".format(root.val), end="")

        self.preOrder(root.left)
        self.preOrder(root.right)

    def getHighest(self, root, key):

        if not root:
            return

        if root.val > key:
            if root.left:
                if root.left.val <= key:
                    return root.val
                else:
                    return self.getHighest(root.left, key)

        elif root.val < key:
            if root.right:
                if root.right.val > key:
                    return root.right.val
                else:
                    return self.getHighest(root.right , key)
            else:
                return

def initStore():
    store_list_id = list(range(10))
    store_hash_id = [hashlib.sha256(str(id).encode()).hexdigest() for id in store_list_id]
    #store_hash_id = list(range(10,0,-1))
    store_id_hash_map = dict([(list_id, hash_id) for list_id, hash_id in zip(store_list_id, store_hash_id)])
    AVL = AVL_Tree()
    AVL.root = None
    for node in store_hash_id:
        AVL.root = AVL.insert(AVL.root, node)

    return AVL, store_id_hash_map

def get_store_dict(store_id, c):
    if  store_id+".lk" not in set(os.listdir()):
        if store_id+".pkl" not in set(os.listdir()):
            pickle.dump({}, open(store_id+".pkl", "wb"))
        store_dict = pickle.load(open(store_id+".pkl", 'rb'))
        with open(store_id+".lk", 'w') as fp:
            pass
    elif store_id+".lk" not in set(os.listdir()):
        time.sleep((2**c)-1)
        get_store_dict(store_id, c+1)
    return store_dict

def get_store_dict_for_read(store_id):
    store_dict = pickle.loads(open(store_id+".pkl", "rb"))
    return store_dict

def dump(store_id):
    pickle.dump({}, open(store_id+".pkl", "wb"))
    os.remove(store_id+".lk")
    return

def findStore(key_sha_id, AVL):
    assigned_store = AVL.getHighest(AVL.root, key_sha_id)
    if assigned_store is None:
        assigned_store = AVL.min_root
    return assigned_store

def write(key, value, AVL):
    key_sha_id = hashlib.sha256(key.encode()).hexdigest()
    assigned_store = findStore(key_sha_id, AVL)
    store_dict = get_store_dict(assigned_store, 0)
    store_dict[key] = value
    dump(key_sha_id)
    return

def read(key):
    key_sha_id = hashlib.sha256(key.encode()).hexdigest()
    assigned_store = findStore(key_sha_id, AVL)
    store_dict = get_store_dict_for_read(assigned_store, 0)
    return store_dict[key]

if __name__ == "__main__":
    AVL, store_id_hash_map = initStore()
    test_set = [(str(key), value) for key, value in zip(range(20, 30), range(80, 90))]
    for single_set in test_set:
        write(single_set[0], single_set[1], AVL)

    for single_set in test_set:
        val = read(single_set[0])
        print ("key: ", single_set[0], "     val: ", val)

