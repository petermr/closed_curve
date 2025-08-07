#!/usr/bin/env python3
"""
Graphics Bundle System for AtPoE (Admitting the Possibilities of Error).
"""

from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass


class StrokeStyle(Enum):
    SOLID = "solid"
    DASHED = "dashed"
    DOTTED = "dotted"
    DASH_DOT = "dash-dot"


@dataclass
class GraphicsBundle:
    name: str
    color: str
    width: int
    stroke_style: StrokeStyle
    description: str


class BundleLibrary:
    def __init__(self):
        self.bundles = self._create_default_bundles()
    
    def _create_default_bundles(self) -> Dict[str, GraphicsBundle]:
        bundles = {}
        
        bundles["Classic Black"] = GraphicsBundle(
            name="Classic Black",
            color="black",
            width=2,
            stroke_style=StrokeStyle.SOLID,
            description="Clean, professional black lines"
        )
        
        bundles["Classic Red"] = GraphicsBundle(
            name="Classic Red",
            color="red",
            width=2,
            stroke_style=StrokeStyle.SOLID,
            description="Bold red lines for emphasis"
        )
        
        bundles["Classic Blue"] = GraphicsBundle(
            name="Classic Blue",
            color="blue",
            width=2,
            stroke_style=StrokeStyle.SOLID,
            description="Calming blue lines"
        )
        
        return bundles
    
    def get_bundle(self, name: str) -> Optional[GraphicsBundle]:
        return self.bundles.get(name)
    
    def get_all_bundles(self) -> List[GraphicsBundle]:
        return list(self.bundles.values())
    
    def get_bundle_names(self) -> List[str]:
        return list(self.bundles.keys())


if __name__ == "__main__":
    library = BundleLibrary()
    print(f"Available bundles: {len(library.get_all_bundles())}")
    for name in library.get_bundle_names():
        bundle = library.get_bundle(name)
        print(f"  - {name}: {bundle.color}, {bundle.width}px, {bundle.stroke_style.value}")
