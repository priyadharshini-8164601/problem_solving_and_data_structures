from collections import deque
import time

print("=" * 65)
print("SET 1 - E-COMMERCE CATALOGUE AND TRAFFIC ANALYSIS")
print("=" * 65)


# ============================================================
# TASK 1: BINARY SEARCH TREE - PRODUCT CATEGORIES
# ============================================================

class BSTNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, value):
        self.root = self._insert(self.root, value)

    def _insert(self, root, value):
        if root is None:
            return BSTNode(value)

        if value < root.value:
            root.left = self._insert(root.left, value)
        elif value > root.value:
            root.right = self._insert(root.right, value)

        return root

    def search(self, value):
        current = self.root

        while current:
            if current.value == value:
                return True
            elif value < current.value:
                current = current.left
            else:
                current = current.right

        return False

    def inorder(self, root):
        if root:
            self.inorder(root.left)
            print(root.value, end=" ")
            self.inorder(root.right)

    def preorder(self, root):
        if root:
            print(root.value, end=" ")
            self.preorder(root.left)
            self.preorder(root.right)

    def postorder(self, root):
        if root:
            self.postorder(root.left)
            self.postorder(root.right)
            print(root.value, end=" ")


print("\nTASK 1: BINARY SEARCH TREE")

categories = [
    "Electronics", "Clothing", "Books", "Furniture",
    "Footwear", "Mobiles", "Laptops", "Accessories",
    "Beauty", "Sports", "Toys", "Groceries",
    "Watches", "Kitchen", "Jewellery"
]

tree = BST()

for category in categories:
    tree.insert(category)

print("Inorder Traversal:")
tree.inorder(tree.root)

print("\nPreorder Traversal:")
tree.preorder(tree.root)

print("\nPostorder Traversal:")
tree.postorder(tree.root)

print("\n\nSearch Electronics:", tree.search("Electronics"))
print("Search Pharmacy:", tree.search("Pharmacy"))


# ============================================================
# TASK 2: HASH TABLE WITH CHAINING AND BUILT-IN HASH MAP
# ============================================================

print("\n\nTASK 2: HASHING AND HASH MAP")

class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]

    def hash_function(self, key):
        return sum(ord(char) for char in key) % self.size

    def insert(self, key, value):
        index = self.hash_function(key)
        self.table[index].append((key, value))

    def search(self, key):
        index = self.hash_function(key)

        for k, v in self.table[index]:
            if k == key:
                return v

        return None


custom_hash = HashTable(10)

custom_hash.insert("SKU101", "Laptop")
custom_hash.insert("SKU110", "Mobile")

print("SKU101:", custom_hash.search("SKU101"))
print("SKU110:", custom_hash.search("SKU110"))

print("Collision demonstration:")
print("SKU101 and SKU110 bucket:",
      custom_hash.hash_function("SKU101"))

# Compare lookup using 100,000 SKUs

sku_data = {
    f"SKU{i}": f"Product{i}"
    for i in range(100000)
}

# Built-in dictionary
start = time.perf_counter()

for i in range(100000):
    result = sku_data.get(f"SKU{i}")

builtin_time = time.perf_counter() - start

# Custom hash table
large_hash = HashTable(200003)

for key, value in sku_data.items():
    large_hash.insert(key, value)

start = time.perf_counter()

for i in range(100000):
    result = large_hash.search(f"SKU{i}")

custom_time = time.perf_counter() - start

print("\nLookup comparison for 100,000 SKUs")
print("Built-in dictionary time:", round(builtin_time, 6), "seconds")
print("Custom hash table time:", round(custom_time, 6), "seconds")


# ============================================================
# TASK 3: GRAPH - MICROSERVICE DEPLOYMENT DEPENDENCIES
# ============================================================

print("\n\nTASK 3: GRAPH AND DEPLOYMENT ORDER")

graph = {
    "Cart": ["Pricing"],
    "Pricing": ["Inventory"],
    "Inventory": ["Payment"],
    "Payment": ["Notification"],
    "Notification": []
}


def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)

    while queue:
        node = queue.popleft()
        print(node, end=" ")

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)


def dfs(graph, node, visited=None):
    if visited is None:
        visited = set()

    visited.add(node)
    print(node, end=" ")

    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)


print("BFS Deployment Traversal:")
bfs(graph, "Cart")

print("\nDFS Deployment Traversal:")
dfs(graph, "Cart")


# Detect circular dependency using DFS

def detect_cycle(graph):
    visited = set()
    recursion_stack = set()

    def dfs_cycle(node):
        visited.add(node)
        recursion_stack.add(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs_cycle(neighbor):
                    return True
            elif neighbor in recursion_stack:
                return True

        recursion_stack.remove(node)
        return False

    for node in graph:
        if node not in visited:
            if dfs_cycle(node):
                return True

    return False


print("\nCircular dependency:", detect_cycle(graph))

# Introduce a circular dependency
graph["Notification"].append("Cart")

print("After adding Notification -> Cart:")
print("Circular dependency:", detect_cycle(graph))


# ============================================================
# TASK 4: SLIDING WINDOW - BUSIEST 3-HOUR WINDOW
# ============================================================

print("\n\nTASK 4: SLIDING WINDOW")

requests = [
    120, 150, 180, 200, 220, 250,
    300, 350, 400, 450, 500, 480,
    420, 390, 350, 300, 280, 260,
    240, 200, 180, 160, 140, 100
]

window_size = 3

current_sum = sum(requests[:window_size])
max_sum = current_sum
best_start = 0

for i in range(window_size, len(requests)):
    current_sum += requests[i] - requests[i - window_size]

    if current_sum > max_sum:
        max_sum = current_sum
        best_start = i - window_size + 1

print("Busiest 3-hour window:")
print("Starting hour:", best_start)
print("Ending hour:", best_start + 2)
print("Total requests:", max_sum)
print("Average requests:", max_sum / window_size)


# ============================================================
# TASK 5: TWO POINTERS - GIFT CARD PAIRS
# ============================================================

print("\n\nTASK 5: TWO POINTERS")

order_values = [100, 150, 200, 250, 300, 350, 400, 450]
gift_card_value = 500

left = 0
right = len(order_values) - 1

print("Pairs adding up to", gift_card_value)

while left < right:
    total = order_values[left] + order_values[right]

    if total == gift_card_value:
        print(order_values[left], "+", order_values[right],
              "=", gift_card_value)
        left += 1
        right -= 1

    elif total < gift_card_value:
        left += 1

    else:
        right -= 1


# ============================================================
# DECISION TABLE
# ============================================================

print("\n\nDECISION TABLE")

print("""
Problem                         Data Structure / Pattern
--------------------------------------------------------------
Product category management     Binary Search Tree
SKU lookup                      Hash Table / Dictionary
Microservice dependencies       Graph (BFS and DFS)
Circular dependency detection   DFS Cycle Detection
Peak traffic analysis           Sliding Window
Gift card pair identification   Two Pointers
""")

print("=" * 65)
print("SET 1 EXECUTION COMPLETED")
print("=" * 65)