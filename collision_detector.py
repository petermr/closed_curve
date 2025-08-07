#!/usr/bin/env python3
"""
Collision Detection System for AtPoE curves.
"""

from typing import List, Tuple, Optional


class IncrementalCollisionDetector:
    def __init__(self):
        self.segments = []
    
    def add_segments(self, curve: List[Tuple[float, float]]):
        if len(curve) < 2:
            return
        
        for i in range(len(curve)):
            p1 = curve[i]
            p2 = curve[(i + 1) % len(curve)]
            self.segments.append((p1, p2))
    
    def check_collision(self, p1: Tuple[float, float], p2: Tuple[float, float]) -> bool:
        for seg_p1, seg_p2 in self.segments:
            if self._do_segments_intersect(p1, p2, seg_p1, seg_p2):
                return True
        return False
    
    def _do_segments_intersect(self, p1: Tuple[float, float], p2: Tuple[float, float], 
                              p3: Tuple[float, float], p4: Tuple[float, float]) -> bool:
        def ccw(A: Tuple[float, float], B: Tuple[float, float], C: Tuple[float, float]) -> bool:
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
        
        return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)
    
    def clear(self):
        self.segments.clear()


if __name__ == "__main__":
    detector = IncrementalCollisionDetector()
    print("Collision detector initialized successfully!")
