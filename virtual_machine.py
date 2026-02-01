"""
Virtual Machine for OverKill
Manages memory, registers, storage, and execution state
"""

from typing import Dict, Tuple, Any, List, Optional
from machine_loader import MachineConfig


class VMError(Exception):
    """Base exception for VM errors"""
    pass


class VMWarning:
    """Represents a VM warning"""
    def __init__(self, message: str):
        self.message = message


class VirtualMachine:
    """Virtual Machine that executes OverKill instructions"""
    
    def __init__(self, config: MachineConfig, mode: str = "warn"):
        self.config = config
        self.mode = mode  # "warn" or "strict"
        
        # Initialize memory grid
        self.memory = {}  # (x, y) -> value
        self.initialized = set()  # Set of (x, y) coordinates that have been written
        
        # Variables in the program
        self.variables = {}  # name -> value
        
        # Watchpoints
        self.watchpoints = {}  # (x, y) -> ("read" | "write" | "both")
        
        # Execution state
        self.running = False
        self.paused = False
        self.current_section = None  # "First" or "Second"
        self.repeat_forever = False
        
        # Logging
        self.warnings = []
        self.errors = []
        self.log = []
        
        # Track recent changes for visualization
        self.recent_changes = set()  # Set of (x, y) that changed recently
    
    def reset(self):
        """Reset the VM state"""
        self.memory.clear()
        self.initialized.clear()
        self.variables.clear()
        self.warnings.clear()
        self.errors.clear()
        self.log.clear()
        self.recent_changes.clear()
        self.running = False
        self.paused = False
        self.current_section = None
        self.repeat_forever = False
    
    def add_log(self, message: str):
        """Add a log message"""
        self.log.append(message)
    
    def add_warning(self, message: str):
        """Add a warning message"""
        warning = f"WARNING: {message}"
        self.warnings.append(warning)
        self.add_log(warning)
    
    def add_error(self, message: str):
        """Add an error message"""
        error = f"ERROR: {message}"
        self.errors.append(error)
        self.add_log(error)
        if self.mode == "strict":
            raise VMError(message)
    
    def check_bounds(self, x: int, y: int) -> bool:
        """Check if coordinates are within bounds"""
        if not self.config.is_valid_coordinate(x, y):
            self.add_error(f"Out of bounds access: ({x}, {y})")
            return False
        return True
    
    def check_permission(self, x: int, y: int, operation: str) -> bool:
        """Check if operation is allowed on coordinate"""
        perm = self.config.get_permission(x, y)
        
        if operation == "write":
            if perm in ["r", "readonly"]:
                self.add_error(f"Write to read-only location: ({x}, {y})")
                return False
        
        return True
    
    def check_initialized(self, x: int, y: int) -> bool:
        """Check if coordinate has been initialized before reading"""
        if (x, y) not in self.initialized:
            self.add_warning(f"Reading uninitialized location: ({x}, {y})")
            return False
        return True
    
    def check_watchpoint(self, x: int, y: int, operation: str):
        """Check if a watchpoint is triggered"""
        if (x, y) in self.watchpoints:
            watch_type = self.watchpoints[(x, y)]
            if watch_type == operation or watch_type == "both":
                self.add_warning(f"Watchpoint hit: {operation} at ({x}, {y})")
    
    def read_memory(self, x: int, y: int) -> Any:
        """Read value from memory/register"""
        if not self.check_bounds(x, y):
            return 0
        
        self.check_watchpoint(x, y, "read")
        self.check_initialized(x, y)
        
        return self.memory.get((x, y), 0)
    
    def write_memory(self, x: int, y: int, value: Any):
        """Write value to memory/register"""
        if not self.check_bounds(x, y):
            return
        
        if not self.check_permission(x, y, "write"):
            return
        
        self.check_watchpoint(x, y, "write")
        
        self.memory[(x, y)] = value
        self.initialized.add((x, y))
        self.recent_changes.add((x, y))
        self.add_log(f"Write: ({x}, {y}) = {value}")
    
    def resolve_coordinate(self, coord_str: str) -> Tuple[int, int]:
        """Resolve coordinate or named register"""
        # Check if it's a named register
        resolved = self.config.resolve_name(coord_str)
        if resolved:
            return resolved
        
        # Parse as coordinate
        from machine_loader import parse_coordinate
        return parse_coordinate(coord_str)
    
    def set_watchpoint(self, x: int, y: int, watch_type: str):
        """Set a watchpoint on a coordinate"""
        # If there's already a watchpoint and types differ, set to "both"
        if (x, y) in self.watchpoints:
            existing = self.watchpoints[(x, y)]
            if existing != watch_type and existing != "both":
                watch_type = "both"
        
        self.watchpoints[(x, y)] = watch_type
        self.add_log(f"Watchpoint set: ({x}, {y}) on {watch_type}")
    
    def get_memory_state(self) -> Dict:
        """Get current memory state for visualization"""
        return {
            "memory": dict(self.memory),
            "initialized": list(self.initialized),
            "recent_changes": list(self.recent_changes),
            "variables": dict(self.variables)
        }


if __name__ == "__main__":
    # Test the VM
    from machine_loader import MachineConfig
    
    config = MachineConfig()
    vm = VirtualMachine(config)
    
    print("VM Test")
    vm.write_memory(0, 0, 42)
    value = vm.read_memory(0, 0)
    print(f"Value at (0,0): {value}")
    print(f"Warnings: {vm.warnings}")
