"""
Language Parser for OverKill
Parses .ok program files
"""

import re
from typing import List, Dict, Any, Optional, Tuple


class Instruction:
    """Base class for instructions"""
    def __init__(self, line_no: int):
        self.line_no = line_no


class SetRegInstruction(Instruction):
    """set reg X;Y = int N [named name]"""
    def __init__(self, line_no: int, coord: str, value: Any, reg_type: str, name: Optional[str] = None):
        super().__init__(line_no)
        self.coord = coord
        self.value = value
        self.reg_type = reg_type
        self.name = name


class ReadInstruction(Instruction):
    """read X;Y into variable"""
    def __init__(self, line_no: int, coord: str, variable: str):
        super().__init__(line_no)
        self.coord = coord
        self.variable = variable


class WriteInstruction(Instruction):
    """write variable into X;Y"""
    def __init__(self, line_no: int, variable: str, coord: str):
        super().__init__(line_no)
        self.variable = variable
        self.coord = coord


class WhenInstruction(Instruction):
    """when condition ... otherwise ..."""
    def __init__(self, line_no: int, condition: str, then_block: List[Instruction], else_block: List[Instruction] = None):
        super().__init__(line_no)
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block or []


class WaitInstruction(Instruction):
    """wait N"""
    def __init__(self, line_no: int, milliseconds: int):
        super().__init__(line_no)
        self.milliseconds = milliseconds


class RepeatForeverInstruction(Instruction):
    """repeat forever"""
    def __init__(self, line_no: int):
        super().__init__(line_no)


class WatchInstruction(Instruction):
    """watch reg X;Y on read/write"""
    def __init__(self, line_no: int, coord: str, watch_type: str):
        super().__init__(line_no)
        self.coord = coord
        self.watch_type = watch_type


class ModeInstruction(Instruction):
    """mode warn/strict"""
    def __init__(self, line_no: int, mode: str):
        super().__init__(line_no)
        self.mode = mode


class Program:
    """Represents a parsed OverKill program"""
    def __init__(self):
        self.machine_file = None
        self.first_section = []
        self.second_section = []
        self.mode = "warn"


def parse_condition(condition_str: str) -> Dict:
    """Parse a condition string"""
    # Simple condition parser - supports ==, !=, <, >, and, or
    condition_str = condition_str.strip()
    
    # Handle logical operators
    if ' and ' in condition_str:
        parts = condition_str.split(' and ', 1)
        return {
            'type': 'and',
            'left': parse_condition(parts[0]),
            'right': parse_condition(parts[1])
        }
    
    if ' or ' in condition_str:
        parts = condition_str.split(' or ', 1)
        return {
            'type': 'or',
            'left': parse_condition(parts[0]),
            'right': parse_condition(parts[1])
        }
    
    # Handle comparison operators
    for op in ['==', '!=', '<=', '>=', '<', '>']:
        if op in condition_str:
            parts = condition_str.split(op, 1)
            return {
                'type': 'comparison',
                'operator': op,
                'left': parts[0].strip(),
                'right': parts[1].strip()
            }
    
    # Simple variable or value
    return {
        'type': 'value',
        'value': condition_str
    }


def parse_program(filepath: str) -> Program:
    """Parse an OverKill program from .ok file"""
    program = Program()
    
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    current_section = None
    line_no = 0
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        line_no = i + 1
        i += 1
        
        if not line or line.startswith('#'):
            continue
        
        # Parse machine file declaration
        if line.startswith('run on'):
            match = re.match(r'run on\s+"([^"]+)"', line)
            if match:
                program.machine_file = match.group(1)
        
        # Parse sections
        elif line == 'First':
            current_section = 'First'
        elif line == 'Second':
            current_section = 'Second'
        
        # Parse mode
        elif line.startswith('mode'):
            match = re.match(r'mode\s+(warn|strict)', line)
            if match:
                program.mode = match.group(1)
                inst = ModeInstruction(line_no, match.group(1))
                if current_section == 'First':
                    program.first_section.append(inst)
                elif current_section == 'Second':
                    program.second_section.append(inst)
        
        # Parse set reg instruction
        elif line.startswith('set reg'):
            match = re.match(r'set reg\s+([\w;]+)\s*=\s*(\w+)\s+(.+?)(?:\s+named\s+(\w+))?$', line)
            if match:
                coord = match.group(1)
                reg_type = match.group(2)
                value_str = match.group(3)
                name = match.group(4) if match.group(4) else None
                
                # Parse value
                try:
                    if reg_type == "int":
                        value = int(value_str)
                    elif reg_type == "bool":
                        value = value_str.lower() == "true"
                    else:
                        value = value_str
                except:
                    value = 0
                
                inst = SetRegInstruction(line_no, coord, value, reg_type, name)
                if current_section == 'First':
                    program.first_section.append(inst)
                elif current_section == 'Second':
                    program.second_section.append(inst)
        
        # Parse read instruction
        elif line.startswith('read'):
            match = re.match(r'read\s+([\w;]+)\s+into\s+(\w+)', line)
            if match:
                coord = match.group(1)
                variable = match.group(2)
                inst = ReadInstruction(line_no, coord, variable)
                if current_section == 'First':
                    program.first_section.append(inst)
                elif current_section == 'Second':
                    program.second_section.append(inst)
        
        # Parse write instruction
        elif line.startswith('write'):
            match = re.match(r'write\s+(\w+)\s+into\s+([\w;]+)', line)
            if match:
                variable = match.group(1)
                coord = match.group(2)
                inst = WriteInstruction(line_no, variable, coord)
                if current_section == 'First':
                    program.first_section.append(inst)
                elif current_section == 'Second':
                    program.second_section.append(inst)
        
        # Parse when instruction (simplified - single line for now)
        elif line.startswith('when'):
            match = re.match(r'when\s+(.+)', line)
            if match:
                condition = match.group(1)
                # For simplicity, we'll handle single-line conditionals
                inst = WhenInstruction(line_no, condition, [], [])
                if current_section == 'First':
                    program.first_section.append(inst)
                elif current_section == 'Second':
                    program.second_section.append(inst)
        
        # Parse wait instruction
        elif line.startswith('wait'):
            match = re.match(r'wait\s+(\d+)', line)
            if match:
                milliseconds = int(match.group(1))
                inst = WaitInstruction(line_no, milliseconds)
                if current_section == 'First':
                    program.first_section.append(inst)
                elif current_section == 'Second':
                    program.second_section.append(inst)
        
        # Parse repeat forever
        elif line == 'repeat forever':
            inst = RepeatForeverInstruction(line_no)
            if current_section == 'Second':
                program.second_section.append(inst)
        
        # Parse watch instruction
        elif line.startswith('watch'):
            match = re.match(r'watch reg\s+([\w;]+)\s+on\s+(read|write|both)', line)
            if match:
                coord = match.group(1)
                watch_type = match.group(2)
                inst = WatchInstruction(line_no, coord, watch_type)
                if current_section == 'First':
                    program.first_section.append(inst)
                elif current_section == 'Second':
                    program.second_section.append(inst)
    
    return program


if __name__ == "__main__":
    # Test parser
    print("Parser Test")
    prog = Program()
    print(f"Default mode: {prog.mode}")
