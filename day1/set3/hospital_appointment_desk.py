import csv
import random
import time
from datetime import datetime
from pathlib import Path
from bisect import bisect_right

HERE = Path(__file__).resolve().parent
PATIENT_FILE = HERE / "patients.csv"
APPOINTMENT_FILE = HERE / "appointments.csv"
DT_FORMAT = "%Y-%m-%d %H:%M"


def load_csv(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# TASK 1: Linear and binary search by patient ID.
def linear_search(records, patient_id):
    comparisons = 0
    for record in records:
        comparisons += 1
        if record["patient_id"] == patient_id:
            return record, comparisons
    return None, comparisons


def binary_search(records, patient_id):
    low, high = 0, len(records) - 1
    comparisons = 0
    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        value = records[mid]["patient_id"]
        if value == patient_id:
            return records[mid], comparisons
        if value < patient_id:
            low = mid + 1
        else:
            high = mid - 1
    return None, comparisons


def benchmark_searches(records, lookups=1000):
    # Both algorithms receive the same successful query IDs.
    rng = random.Random(42)
    ids = [records[rng.randrange(len(records))]["patient_id"] for _ in range(lookups)]
    t0 = time.perf_counter()
    for patient_id in ids:
        linear_search(records, patient_id)
    linear_seconds = time.perf_counter() - t0

    t0 = time.perf_counter()
    for patient_id in ids:
        binary_search(records, patient_id)
    binary_seconds = time.perf_counter() - t0
    return linear_seconds, binary_seconds, ids


# TASK 2: Sort by urgency (5 highest) descending, then arrival time ascending.
def sort_key(appointment):
    return (-int(appointment["urgency"]),
            datetime.strptime(appointment["arrival_time"], DT_FORMAT))


def selection_sort(items):
    a = items[:]
    swaps = 0
    for i in range(len(a) - 1):
        best = i
        for j in range(i + 1, len(a)):
            if sort_key(a[j]) < sort_key(a[best]):
                best = j
        if best != i:
            a[i], a[best] = a[best], a[i]
            swaps += 1
    return a, swaps


def quick_sort(items):
    a = items[:]
    swaps = 0

    def partition(low, high):
        nonlocal swaps
        pivot = sort_key(a[high])
        i = low - 1
        for j in range(low, high):
            if sort_key(a[j]) <= pivot:
                i += 1
                if i != j:
                    a[i], a[j] = a[j], a[i]
                    swaps += 1
        if i + 1 != high:
            a[i + 1], a[high] = a[high], a[i + 1]
            swaps += 1
        return i + 1

    def quick(low, high):
        if low < high:
            p = partition(low, high)
            quick(low, p - 1)
            quick(p + 1, high)

    quick(0, len(a) - 1)
    return a, swaps


# TASK 3: Hash set detects duplicate patient + exact slot-start combinations.
def find_double_bookings(appointments):
    seen = set()
    duplicates = []
    for appt in appointments:
        key = (appt["patient_id"], appt["slot_start"])
        if key in seen:
            duplicates.append((appt["appointment_id"], key[0], key[1]))
        else:
            seen.add(key)
    return duplicates


# TASK 4: Queue and stack built from linked nodes, not library collections.
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
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


class Stack:
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


# TASK 5: Weighted interval scheduling DP for maximum COUNT of non-overlapping visits.
# With a count-only objective, earliest-finish-time greedy is also optimal;
# DP is included as required and to show the recurrence.
def appointment_intervals(raw_appointments, doctor_id):
    result = []
    for appt in raw_appointments:
        if appt["doctor_id"] == doctor_id:
            start = datetime.strptime(appt["slot_start"], DT_FORMAT)
            end = datetime.strptime(appt["slot_end"], DT_FORMAT)
            result.append((start, end, appt["appointment_id"]))
    return result


def max_appointments_dp(intervals):
    # Sort by finish time; p[i] = count of earlier intervals finishing <= start_i.
    ordered = sorted(intervals, key=lambda x: (x[1], x[0]))
    finishes = [item[1] for item in ordered]
    n = len(ordered)
    dp = [0] * (n + 1)
    chosen = [[] for _ in range(n + 1)]
    for i in range(1, n + 1):
        start, end, appt_id = ordered[i - 1]
        p = bisect_right(finishes, start, 0, i - 1)
        include_count = 1 + dp[p]
        exclude_count = dp[i - 1]
        if include_count > exclude_count:
            dp[i] = include_count
            chosen[i] = chosen[p] + [appt_id]
        else:
            dp[i] = exclude_count
            chosen[i] = chosen[i - 1][:]
    return dp[n], chosen[n]


def max_appointments_greedy(intervals):
    ordered = sorted(intervals, key=lambda x: (x[1], x[0]))
    selected = []
    last_end = None
    for start, end, appt_id in ordered:
        if last_end is None or start >= last_end:
            selected.append(appt_id)
            last_end = end
    return len(selected), selected


def main():
    patients = load_csv(PATIENT_FILE)
    appointments = load_csv(APPOINTMENT_FILE)
    patients.sort(key=lambda r: r["patient_id"])  # Binary search requires sorted data.

    print(f"Patients loaded: {len(patients):,}")
    print(f"Appointments loaded: {len(appointments):,}")

    # 1
    linear_t, binary_t, lookup_ids = benchmark_searches(patients, 1000)
    print("\n TASK 1 - 1,000 patient-ID look-ups")
    print(f"Linear search elapsed: {linear_t:.6f} seconds")
    print(f"Binary search elapsed: {binary_t:.6f} seconds")
    print(f"Speed-up (linear/binary): {linear_t / binary_t:.2f}x" if binary_t else "Speed-up: n/a")
    demo_id = lookup_ids[0]
    _, lc = linear_search(patients, demo_id)
    _, bc = binary_search(patients, demo_id)
    print(f"Example ID {demo_id}: linear comparisons={lc}, binary comparisons={bc}")
    print("Comparison bounds for n=20,000: linear best=1, average=10,000.5, worst=20,000;")
    print("binary best=1, average about 14.36, worst=15 (successful look-up).")

    # 2 - sort a manageable sample for practical timing; full dataset would make selection sort
    # intentionally slow. Use the first 1,000 appointments for a fair same-input comparison.
    sample = appointments[:1000]
    t0 = time.perf_counter()
    selection_result, selection_swaps = selection_sort(sample)
    selection_seconds = time.perf_counter() - t0
    t0 = time.perf_counter()
    quick_result, quick_swaps = quick_sort(sample)
    quick_seconds = time.perf_counter() - t0
    assert [sort_key(x) for x in selection_result] == [sort_key(x) for x in quick_result]
    print("\nTASK 2 - urgency and arrival-time sorting (same 1,000-row sample)")
    print(f"Selection sort: swaps={selection_swaps}, time={selection_seconds:.6f}s")
    print(f"Quick sort:     swaps={quick_swaps}, time={quick_seconds:.6f}s")
    print("First 5 sorted appointment IDs:", [x["appointment_id"] for x in quick_result[:5]])

    # 3
    duplicates = find_double_bookings(appointments)
    print("\nTASK 3 - double-booked patient/slot pairs")
    print(f"Duplicate records flagged: {len(duplicates)}")
    for item in duplicates[:5]:
        print(" ", item)

    # 4
    walkins = Queue()
    for token in ["WALKIN-101", "WALKIN-102", "WALKIN-103"]:
        walkins.enqueue(token)
    print("\nTASK 4 - queue / stack")
    print("Walk-in FIFO service order:", [walkins.dequeue() for _ in range(3)])
    history = Stack()
    for patient in ["PT000123", "PT000456", "PT000789"]:
        history.push(patient)
    print("Most recently viewed patient (stack pop):", history.pop())

    # 5
    doctor = "DR001"
    intervals = appointment_intervals(appointments, doctor)
    dp_count, dp_ids = max_appointments_dp(intervals)
    greedy_count, greedy_ids = max_appointments_greedy(intervals)
    print("\nTASK 5 - non-overlapping appointments for", doctor)
    print(f"DP maximum count: {dp_count}")
    print(f"Greedy maximum count: {greedy_count}")
    print("DP and greedy counts agree:", dp_count == greedy_count)
    print("DP selected appointment IDs (first 10):", dp_ids[:10])
    print("\nAll five tasks completed.")


if __name__ == "__main__":
    main()
