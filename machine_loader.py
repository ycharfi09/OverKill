"""
Machine Definition Loader for OverKill
Loads .okt files and creates machine configurations
"""

import re
from typing import Dict, Tuple, List, Any


class MachineConfig:
    """Represents a machine configuration loaded from .okt file"""
    
    def __init__(self):
        self.memory_size = (256, 256)  # Default 256x256
        self.regions = []  # List of (name, start, end, permissions)
        self.named_registers = {}  # name -> (x, y, type)
        self.register_types = {}  # (x, y) -> type
        self.permissions = {}  # (x, y) -> permissions (rw, r, readonly)
    
    def is_valid_coordinate(self, x: int, y: int) -> bool:
        """Check if coordinates are within memory bounds"""
        return 0 <= x < self.memory_size[0] and 0 <= y < self.memory_size[1]
    
    def get_permission(self, x: int, y: int) -> str:
        """Get permission for a coordinate (default: rw)"""
        return self.permissions.get((x, y), "rw")
    
    def get_type(self, x: int, y: int) -> str:
        """Get type for a coordinate (default: int)"""
        return self.register_types.get((x, y), "int")
    
    def resolve_name(self, name: str) -> Tuple[int, int]:
        """Resolve a named register to coordinates"""
        if name in self.named_registers:
            return self.named_registers[name][:2]
        return None


def parse_coordinate(coord_str: str) -> Tuple[int, int]:
    """Parse coordinate string like '12;4' or '12A;4F' (hex)"""
    parts = coord_str.split(';')
    if len(parts) != 2:
        raise ValueError(f"Invalid coordinate format: {coord_str}")
    
    # Try parsing as hex first, then decimal
    try:
        x = int(parts[0], 16) if any(c in parts[0].upper() for c in 'ABCDEF') else int(parts[0])
        y = int(parts[1], 16) if any(c in parts[1].upper() for c in 'ABCDEF') else int(parts[1])
        return (x, y)
    except ValueError:
        raise ValueError(f"Invalid coordinate format: {coord_str}")


def load_machine_config(filepath: str) -> MachineConfig:
    """Load machine configuration from .okt file"""
    config = MachineConfig()
    
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # Parse memory size
        if line.startswith('memory'):
            match = re.match(r'memory\s+(\d+)x(\d+)', line)
            if match:
                config.memory_size = (int(match.group(1)), int(match.group(2)))
        
        # Parse region
        elif line.startswith('region'):
            match = re.match(r'region\s+(\w+)\s+([\w;]+)\s+to\s+([\w;]+)\s+(\w+)', line)
            if match:
                name = match.group(1)
                start = parse_coordinate(match.group(2))
                end = parse_coordinate(match.group(3))
                perms = match.group(4)
                config.regions.append((name, start, end, perms))
                
                # Set permissions for all coordinates in region
                for x in range(start[0], end[0] + 1):
                    for y in range(start[1], end[1] + 1):
                        config.permissions[(x, y)] = perms
        
        # Parse register definition
        elif line.startswith('reg'):
            match = re.match(r'reg\s+([\w;]+)\s+(\w+)(?:\s+(\w+))?', line)
            if match:
                coord = parse_coordinate(match.group(1))
                reg_type = match.group(2)
                name = match.group(3) if match.group(3) else None
                
                config.register_types[coord] = reg_type
                if name:
                    config.named_registers[name] = (coord[0], coord[1], reg_type)
    
    return config


if __name__ == "__main__":
    # Test the loader
    print("Machine Loader Test")
    config = MachineConfig()
    print(f"Default memory size: {config.memory_size}")
    print(f"Valid (0,0): {config.is_valid_coordinate(0, 0)}")
    print(f"Valid (300,300): {config.is_valid_coordinate(300, 300)}")
