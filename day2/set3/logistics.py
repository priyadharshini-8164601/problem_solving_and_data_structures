from collections import deque

print("=" * 65)
print("SET 3 - LOGISTICS NETWORK AND DELIVERY WINDOWS")
print("=" * 65)


# ============================================================
# TASK 1: BST - HUB CODES
# ============================================================

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class HubBST:
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

    def height(self, root):
        if root is None:
            return 0

        return 1 + max(
            self.height(root.left),
            self.height(root.right)
        )


print("\nTASK 1: BINARY SEARCH TREE")

hub_codes = [
    "H50", "H30", "H70", "H20", "H40",
    "H60", "H80", "H10", "H90"
]

bst = HubBST()
root = None

for hub in hub_codes:
    root = bst.insert(root, hub)

print("Hub codes inserted:", hub_codes)
print("Search H40:", bst.search(root, "H40"))
print("Search H100:", bst.search(root, "H100"))
print("BST height:", bst.height(root))

# Sorted insertion example
sorted_root = None

for hub in sorted(hub_codes):
    sorted_root = bst.insert(sorted_root, hub)

print("Height after sorted insertion:", bst.height(sorted_root))
print("Sorted insertion can make a BST skewed and increase its height.")


# ============================================================
# TASK 2: HASH MAP - PARCEL TRACKING
# ============================================================

print("\n\nTASK 2: HASH MAP - PARCEL TRACKING")

parcels = {
    "TRK101": "Chennai",
    "TRK102": "Coimbatore",
    "TRK103": "Madurai"
}

print("Tracking lookup:")
print("TRK101:", parcels.get("TRK101", "Not Found"))

scans = [
    ("TRK101", "Chennai"),
    ("TRK102", "Coimbatore"),
    ("TRK101", "Chennai"),
    ("TRK103", "Madurai"),
    ("TRK102", "Coimbatore"),
    ("TRK101", "Madurai")
]

seen_scans = set()

print("\nDuplicate scan detection:")

for tracking, hub in scans:
    key = (tracking, hub)

    if key in seen_scans:
        print("Duplicate scan:", tracking, "at", hub)
    else:
        seen_scans.add(key)
        print("New scan:", tracking, "at", hub)


# ============================================================
# TASK 3: GRAPH - LOGISTICS ROUTES
# ============================================================

print("\n\nTASK 3: GRAPH - LOGISTICS NETWORK")

graph = {
    "H1": ["H2", "H3"],
    "H2": ["H1", "H4", "H5"],
    "H3": ["H1", "H6"],
    "H4": ["H2", "H7"],
    "H5": ["H2", "H8"],
    "H6": ["H3", "H9"],
    "H7": ["H4", "H10"],
    "H8": ["H5"],
    "H9": ["H6"],
    "H10": ["H7"]
}

print("Adjacency List:")

for hub, neighbors in graph.items():
    print(hub, ":", neighbors)


# BFS - Fewest hops

def shortest_route(graph, start, destination):
    queue = deque([[start]])
    visited = {start}

    while queue:
        path = queue.popleft()
        current = path[-1]

        if current == destination:
            return path

        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    return None


route = shortest_route(graph, "H1", "H10")

print("\nShortest route from H1 to H10:")
print(" -> ".join(route))
print("Number of hops:", len(route) - 1)


# DFS - Reachable hubs

def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()

    visited.add(start)

    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)

    return visited


reachable = dfs(graph, "H1")

print("\nHubs reachable from central depot H1:")
print(sorted(reachable))


# ============================================================
# TASK 4: SLIDING WINDOW - HIGHEST 4-HOUR AVERAGE
# ============================================================

print("\n\nTASK 4: SLIDING WINDOW")

parcel_counts = [
    20, 25, 30, 35, 40, 45,
    50, 60, 70, 80, 75, 65,
    55, 45, 35, 25, 20, 15,
    10, 15, 20, 25, 30, 35
]

window = 4

current_sum = sum(parcel_counts[:window])
max_sum = current_sum
best_start = 0

for i in range(window, len(parcel_counts)):
    current_sum += parcel_counts[i] - parcel_counts[i - window]

    if current_sum > max_sum:
        max_sum = current_sum
        best_start = i - window + 1

average = max_sum / window

print("Highest 4-hour average:", average)
print("Starting hour:", best_start)
print("Ending hour:", best_start + window - 1)
print("Total parcels:", max_sum)


# ============================================================
# TASK 5: TWO POINTERS - PALINDROME ROUTE
# ============================================================

print("\n\nTASK 5: TWO POINTERS - PALINDROME ROUTE")


def is_palindrome(route):
    # Remove separators and convert to uppercase
    cleaned = "".join(
        char.upper()
        for char in route
        if char.isalnum()
    )

    left = 0
    right = len(cleaned) - 1

    while left < right:
        if cleaned[left] != cleaned[right]:
            return False

        left += 1
        right -= 1

    return True


route1 = "H1-H2-H3-H2-H1"
route2 = "H1-H2-H3-H4"

print("Route:", route1)
print("Is palindrome:", is_palindrome(route1))

print("\nRoute:", route2)
print("Is palindrome:", is_palindrome(route2))


# ============================================================
# ALGORITHM CHOICE SUMMARY
# ============================================================

print("\n\nALGORITHM CHOICE SUMMARY")

print("""
Problem                         Algorithm / Data Structure
------------------------------------------------------------
Hub code storage                Binary Search Tree
Hub code searching              BST Search
Parcel tracking                 Hash Map
Duplicate scan detection        Hash Set
Shortest route                  BFS
Reachable hubs                  DFS
Highest 4-hour average          Sliding Window
Palindrome route                Two Pointers
""")

print("=" * 65)
print("SET 3 EXECUTION COMPLETED")
print("=" * 65)