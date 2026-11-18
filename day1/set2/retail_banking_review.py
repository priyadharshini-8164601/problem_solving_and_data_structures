
import csv
from datetime import datetime
from pathlib import Path

CSV_FILE = Path(__file__).with_name("transactions.csv")
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def load_transactions(path):
    with open(path, newline="", encoding="utf-8") as file:
        result = []
        for row in csv.DictReader(file):
            row["amount"] = float(row["amount"])
            row["posting_timestamp"] = datetime.strptime(row["posting_timestamp"], TIME_FORMAT)
            result.append(row)
        return result


# 1. Binary search and linear search
def binary_search(values, target):
    low, high, comparisons = 0, len(values) - 1, 0
    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        if values[mid] == target:
            return mid, comparisons
        if values[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1, comparisons


def linear_search(values, target):
    comparisons = 0
    for index, value in enumerate(values):
        comparisons += 1
        if value == target:
            return index, comparisons
    return -1, comparisons


def successful_binary_comparison_average(n):
    # Count the depth (number of midpoint comparisons) for every successful index.
    total = 0
    for target_index in range(n):
        low, high, depth = 0, n - 1, 0
        while low <= high:
            mid = (low + high) // 2
            depth += 1
            if mid == target_index:
                break
            if mid < target_index:
                low = mid + 1
            else:
                high = mid - 1
        total += depth
    return total / n if n else 0


# 2. Stable statement sorting
def insertion_sort_by_date(items):
    a = items[:]  # do not mutate caller's list
    for i in range(1, len(a)):
        current = a[i]
        j = i - 1
        # Strict > is important: equal timestamps retain their original order.
        while j >= 0 and a[j]["posting_timestamp"] > current["posting_timestamp"]:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = current
    return a


def merge_sort_by_date(items):
    if len(items) <= 1:
        return items[:]
    middle = len(items) // 2
    left = merge_sort_by_date(items[:middle])
    right = merge_sort_by_date(items[middle:])
    merged, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        # <= chooses from the left on ties, preserving original order (stability).
        if left[i]["posting_timestamp"] <= right[j]["posting_timestamp"]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


# 3. Duplicate-posting detection: hash map keyed by account, amount, merchant.
def detect_duplicate_postings(items, window_seconds=60):
    buckets = {}
    duplicates = []
    # Sort chronologically first so the sliding 60-second window is correct
    # even though the source CSV is ordered by transaction ID, not timestamp.
    chronological = sorted(items, key=lambda tx: tx["posting_timestamp"])
    for tx in chronological:
        key = (tx["account_id"], tx["amount"], tx["merchant"])
        timestamp = tx["posting_timestamp"]
        prior = buckets.setdefault(key, [])
        # Keep only earlier records still inside the time window.
        prior[:] = [old for old in prior
                    if 0 <= (timestamp - old["posting_timestamp"]).total_seconds() <= window_seconds]
        for old in prior:
            delta = (timestamp - old["posting_timestamp"]).total_seconds()
            if 0 <= delta <= window_seconds:
                duplicates.append((old, tx, int(delta)))
        prior.append(tx)
    return duplicates


# 4. FIFO queue and LIFO stack implemented with linked nodes (no library collections).
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedQueue:
    def __init__(self):
        self.front = self.rear = None
        self.size = 0

    def enqueue(self, value):
        node = Node(value)
        if self.rear is None:
            self.front = self.rear = node
        else:
            self.rear.next = node
            self.rear = node
        self.size += 1

    def dequeue(self):
        if self.front is None:
            raise IndexError("dequeue from empty queue")
        value = self.front.value
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self.size -= 1
        return value

    def is_empty(self):
        return self.front is None


class LinkedStack:
    def __init__(self):
        self.top = None
        self.size = 0

    def push(self, value):
        node = Node(value)
        node.next = self.top
        self.top = node
        self.size += 1

    def pop(self):
        if self.top is None:
            raise IndexError("pop from empty stack")
        value = self.top.value
        self.top = self.top.next
        self.size -= 1
        return value

    def is_empty(self):
        return self.top is None


# 5. Divide-and-conquer min/max and brute-force baseline
def min_max_divide_conquer(values):
    if not values:
        raise ValueError("min/max requires at least one amount")

    def solve(left, right):
        # Inclusive indices avoid making list slices at every recursive call.
        if left == right:
            return values[left], values[left]
        if right == left + 1:
            a, b = values[left], values[right]
            return (a, b) if a <= b else (b, a)
        middle = (left + right) // 2
        left_min, left_max = solve(left, middle)
        right_min, right_max = solve(middle + 1, right)
        return min(left_min, right_min), max(left_max, right_max)

    return solve(0, len(values) - 1)


def min_max_brute_force(values):
    if not values:
        raise ValueError("min/max requires at least one amount")
    smallest = largest = values[0]
    for value in values[1:]:
        if value < smallest:
            smallest = value
        if value > largest:
            largest = value
    return smallest, largest


def main():
    transactions = load_transactions(CSV_FILE)
    print(f"Loaded transactions: {len(transactions):,}")

    # IDs are ordered in the supplied CSV; verify before binary search.
    transaction_ids = [tx["transaction_id"] for tx in transactions]
    assert all(transaction_ids[i] <= transaction_ids[i+1]
               for i in range(len(transaction_ids)-1))
    n = len(transaction_ids)
    target = transaction_ids[n // 2]
    idx_b, comparisons_b = binary_search(transaction_ids, target)
    idx_l, comparisons_l = linear_search(transaction_ids, target)
    print("\n1) Search")
    print(f"Target: {target}; binary result index={idx_b}, comparisons={comparisons_b}")
    print(f"Linear result index={idx_l}, comparisons={comparisons_l}")
    print(f"Binary successful average comparisons over all {n:,} IDs: "
          f"{successful_binary_comparison_average(n):.4f}")
    print(f"Binary best=1, worst={n.bit_length()} comparisons (successful search)")
    print(f"Linear best=1, average={(n+1)/2:.1f}, worst={n:,} comparisons (successful search)")

    # Use a customer/account with enough rows; choose the most frequent account.
    counts = {}
    for tx in transactions:
        counts[tx["account_id"]] = counts.get(tx["account_id"], 0) + 1
    chosen_account = max(counts, key=counts.get)
    statement = [tx for tx in transactions if tx["account_id"] == chosen_account]
    ins = insertion_sort_by_date(statement)
    mer = merge_sort_by_date(statement)
    assert [(x["transaction_id"], x["posting_timestamp"]) for x in ins] == [
        (x["transaction_id"], x["posting_timestamp"]) for x in mer]
    print("\n2) Statement sorting")
    print(f"Account: {chosen_account}; statement rows: {len(statement)}")
    print("First 5 sorted rows (transaction_id, timestamp):")
    for tx in ins[:5]:
        print(f"  {tx['transaction_id']}  {tx['posting_timestamp']}")
    print("Insertion sort and merge sort agree; both are stable.")
    tied_time = datetime(2026, 11, 10, 12, 0, 0)
    tie_example = [
        {"transaction_id": "TX-A", "posting_timestamp": tied_time},
        {"transaction_id": "TX-B", "posting_timestamp": tied_time},
        {"transaction_id": "TX-C", "posting_timestamp": datetime(2026, 11, 10, 11, 59, 0)},
    ]
    tie_ins = insertion_sort_by_date(tie_example)
    tie_mer = merge_sort_by_date(tie_example)
    print("Equal-timestamp stability demo (input A, B; output):",
          [tx["transaction_id"] for tx in tie_ins if tx["posting_timestamp"] == tied_time])
    assert [tx["transaction_id"] for tx in tie_ins] == [tx["transaction_id"] for tx in tie_mer]

    dups = detect_duplicate_postings(transactions)
    print("\n3) Duplicate postings")
    print(f"Potential duplicate pairs found: {len(dups)}")
    for old, new, seconds in dups[:5]:
        print(f"  {old['transaction_id']} + {new['transaction_id']} "
              f"| {old['account_id']} | {old['amount']:.2f} | {old['merchant']} | {seconds}s")

    print("\n4) Queue and stack")
    review = LinkedQueue()
    for txid in ["TX000101", "TX000102", "TX000103"]:
        review.enqueue(txid)
    print("Manual-review FIFO order:", ", ".join(review.dequeue() for _ in range(3)))
    adjustments = LinkedStack()
    adjustments.push("ADJ-001: +100")
    adjustments.push("ADJ-002: -25")
    print("Reverse last adjustment (LIFO):", adjustments.pop())

    amounts = [tx["amount"] for tx in transactions]
    dc_result = min_max_divide_conquer(amounts)
    brute_result = min_max_brute_force(amounts)
    assert dc_result == brute_result
    print("\n5) Daily amount min/max")
    print(f"Divide-and-conquer: min={dc_result[0]:.2f}, max={dc_result[1]:.2f}")
    print(f"Brute-force scan:   min={brute_result[0]:.2f}, max={brute_result[1]:.2f}")
    print("\nAll checks completed successfully.")


if __name__ == "__main__":
    main()
