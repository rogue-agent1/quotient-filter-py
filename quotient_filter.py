#!/usr/bin/env python3
"""Quotient filter — cache-friendly probabilistic set."""
import hashlib, sys

class QuotientFilter:
    def __init__(self, q=10, r=6):
        self.q = q; self.r = r; self.size = 1 << q
        self.slots = [None] * self.size
        self.occupied = [False] * self.size
        self.continuation = [False] * self.size
        self.shifted = [False] * self.size
    def _fingerprint(self, item):
        h = int(hashlib.sha256(item.encode()).hexdigest(), 16)
        fq = (h >> self.r) & (self.size - 1)
        fr = h & ((1 << self.r) - 1)
        return fq, fr
    def insert(self, item):
        fq, fr = self._fingerprint(item)
        if self.slots[fq] is None:
            self.slots[fq] = fr; self.occupied[fq] = True; return True
        self.occupied[fq] = True
        pos = fq
        while self.slots[pos] is not None: pos = (pos + 1) % self.size
        self.slots[pos] = fr; self.shifted[pos] = (pos != fq); self.continuation[pos] = True
        return True
    def __contains__(self, item):
        fq, fr = self._fingerprint(item)
        if not self.occupied[fq]: return False
        pos = fq
        for _ in range(self.size):
            if self.slots[pos] is None: return False
            if self.slots[pos] == fr: return True
            pos = (pos + 1) % self.size
            if not self.shifted[pos] and not self.continuation[pos]: return False
        return False

if __name__ == "__main__":
    qf = QuotientFilter()
    for a in sys.argv[1:] or ["hello","world"]: qf.insert(a)
    for a in sys.argv[1:] or ["hello","world","foo"]: print(f"{a}: {'yes' if a in qf else 'no'}")
