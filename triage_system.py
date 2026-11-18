"""Heap-backed priority queue for the hospital triage simulation."""

import heapq


class TriageSystem:
    """Serve the highest severity first, with FIFO ordering within ties."""

    def __init__(self):
        self._heap = []
        self._arrival_order = 0

    def add_patient(self, name, severity):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Patient name must be a nonblank string.")
        if isinstance(severity, bool) or not isinstance(severity, int) or not 1 <= severity <= 5:
            raise ValueError("Severity must be an integer from 1 to 5.")

        heapq.heappush(self._heap, (-severity, self._arrival_order, name))
        self._arrival_order += 1

    def process_next(self):
        if not self._heap:
            return None
        priority, _, name = heapq.heappop(self._heap)
        return name, -priority

    def peek_next(self):
        if not self._heap:
            return None
        priority, _, name = self._heap[0]
        return name, -priority

    def is_empty(self):
        return not self._heap

    def size(self):
        return len(self._heap)

    def clear(self):
        self._heap.clear()
