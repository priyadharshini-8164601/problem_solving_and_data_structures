from collections import deque

print("=" * 65)
print("SET 2 - INSURANCE CLAIMS PROCESSING")
print("=" * 65)


# ============================================================
# TASK 1: BST - CLAIM IDS
# ============================================================

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class ClaimBST:
    def __init__(self):
        self.root = None

    def insert(self, root, value):
        if root is None:
            return Node(value)

        if value < root.value:
            root.left = self.insert(root.left, value)
        elif value > root.value:
            root.right = self.insert(root.right, value)

        return root

    def search(self, root, value):
        if root is None:
            return False

        if root.value == value:
            return True

        if value < root.value:
            return self.search(root.left, value)

        return self.search(root.right, value)

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

claims = [105, 102, 108, 101, 104, 107, 110]

bst = ClaimBST()
root = None

for claim in claims:
    root = bst.insert(root, claim)

print("Inorder:")
bst.inorder(root)

print("\nPreorder:")
bst.preorder(root)

print("\nPostorder:")
bst.postorder(root)

print("\n\nSearch claim 104:", bst.search(root, 104))
print("Search claim 999:", bst.search(root, 999))

print("Inorder traversal gives claims in sorted order.")


# ============================================================
# TASK 2: HASHING - DUPLICATE CLAIM DETECTION
# ============================================================

print("\n\nTASK 2: HASHING AND DUPLICATE DETECTION")


def normalize(policy, date):
    policy = "".join(policy.lower().split())
    date = date.strip().lower()
    return (policy, date)


claims_data = [
    ("POLICY101", "2026-11-10"),
    (" policy101 ", "2026-11-10"),
    ("POLICY202", "2026-11-11"),
    ("policy303", "2026-11-12"),
    ("POLICY202", "2026-11-11")
]

seen = set()

for policy, date in claims_data:
    key = normalize(policy, date)

    if key in seen:
        print("Duplicate claim detected:", policy, date)
    else:
        seen.add(key)
        print("New claim accepted:", policy, date)

print("Collisions are handled internally by Python dictionaries and sets.")


# ============================================================
# TASK 3: GRAPH - CLAIM APPROVAL STAGES
# ============================================================

print("\n\nTASK 3: GRAPH - CLAIM APPROVAL")


graph = {
    "Registration": ["Assessment"],
    "Assessment": ["Surveyor", "Settlement"],
    "Surveyor": ["Settlement"],
    "Settlement": []
}


def shortest_path(graph, start, target):
    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        node, path = queue.popleft()

        if node == target:
            return path

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None


path = shortest_path(graph, "Registration", "Settlement")

print("Shortest approval path:")
print(" -> ".join(path))


def detect_cycle(graph):
    visited = set()
    active = set()

    def dfs(node):
        visited.add(node)
        active.add(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in active:
                return True

        active.remove(node)
        return False

    for node in graph:
        if node not in visited:
            if dfs(node):
                return True

    return False


print("Circular approval process:", detect_cycle(graph))

# Introduce a cycle for demonstration
graph["Settlement"].append("Registration")

print("After introducing a cycle:", detect_cycle(graph))


# ============================================================
# TASK 4: SLIDING WINDOW - CONSECUTIVE DAYS ABOVE 100 CLAIMS
# ============================================================

print("\n\nTASK 4: SLIDING WINDOW")

daily_claims = [
    80, 120, 130, 150, 170, 90,
    110, 140, 160, 180, 200, 210,
    70, 80, 120, 130, 140
]

threshold = 100

longest = 0
current = 0
best_start = -1

for i, count in enumerate(daily_claims):
    if count > threshold:
        current += 1

        if current > longest:
            longest = current
            best_start = i - current + 1
    else:
        current = 0

print("Longest consecutive days above 100:", longest)

if longest > 0:
    print("Starting day index:", best_start)
    print("Ending day index:", best_start + longest - 1)
else:
    print("No days exceeded 100 claims.")


# ============================================================
# TASK 5: TWO POINTERS - MERGE SORTED CLAIM LISTS
# ============================================================

print("\n\nTASK 5: TWO POINTERS")

office1 = [101, 105, 109, 115, 120]
office2 = [102, 104, 110, 112, 125]

i = 0
j = 0

merged = []

while i < len(office1) and j < len(office2):

    if office1[i] <= office2[j]:
        merged.append(office1[i])
        i += 1

    else:
        merged.append(office2[j])
        j += 1

merged.extend(office1[i:])
merged.extend(office2[j:])

print("Office 1:", office1)
print("Office 2:", office2)
print("Merged sorted claims:", merged)


# ============================================================
# COMPLEXITY TABLE
# ============================================================

print("\n\nCOMPLEXITY TABLE")

print("""
Problem                         Time Complexity
------------------------------------------------
BST insertion                   O(h)
BST search                      O(h)
BST traversals                  O(n)
Duplicate detection             O(n) average
BFS shortest path               O(V + E)
DFS cycle detection             O(V + E)
Consecutive days analysis       O(n)
Merging two sorted lists        O(n + m)
""")

# Test cases

print("\nTEST CASES")

print("Empty BST search:", bst.search(None, 100))

empty_list = []
print("Empty input merge:", empty_list)

duplicate_test = ["A101", "A101", "A102"]
print("Duplicate test:", len(duplicate_test) != len(set(duplicate_test)))

print("=" * 65)
print("SET 2 EXECUTION COMPLETED")
print("=" * 65)