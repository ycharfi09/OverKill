"""
Execution Engine for OverKill
Executes parsed instructions on the virtual machine
"""

from typing import Optional
import time
from language_parser import *
from virtual_machine import VirtualMachine, VMError


class ExecutionEngine:
    """Executes OverKill programs"""
    
    def __init__(self, vm: VirtualMachine, program: Program):
        self.vm = vm
        self.program = program
        self.step_mode = False
        self.current_instruction = 0
        self.current_section = None
    
    def execute_instruction(self, instruction: Instruction) -> bool:
        """Execute a single instruction. Returns True to continue, False to stop."""
        try:
            if isinstance(instruction, ModeInstruction):
                self.vm.mode = instruction.mode
                self.vm.add_log(f"Mode set to: {instruction.mode}")
            
            elif isinstance(instruction, SetRegInstruction):
                x, y = self.vm.resolve_coordinate(instruction.coord)
                self.vm.write_memory(x, y, instruction.value)
                if instruction.name:
                    self.vm.config.named_registers[instruction.name] = (x, y, instruction.reg_type)
            
            elif isinstance(instruction, ReadInstruction):
                x, y = self.vm.resolve_coordinate(instruction.coord)
                value = self.vm.read_memory(x, y)
                self.vm.variables[instruction.variable] = value
                self.vm.add_log(f"Read: {instruction.variable} = {value} from ({x}, {y})")
            
            elif isinstance(instruction, WriteInstruction):
                if instruction.variable not in self.vm.variables:
                    self.vm.add_warning(f"Variable '{instruction.variable}' not initialized")
                    value = 0
                else:
                    value = self.vm.variables[instruction.variable]
                x, y = self.vm.resolve_coordinate(instruction.coord)
                self.vm.write_memory(x, y, value)
            
            elif isinstance(instruction, WhenInstruction):
                # Evaluate condition
                result = self.evaluate_condition(instruction.condition)
                if result:
                    for inst in instruction.then_block:
                        if not self.execute_instruction(inst):
                            return False
                else:
                    for inst in instruction.else_block:
                        if not self.execute_instruction(inst):
                            return False
            
            elif isinstance(instruction, WaitInstruction):
                self.vm.add_log(f"Wait: {instruction.milliseconds}ms")
                # For teaching purposes, we don't actually wait
                # Just log it
            
            elif isinstance(instruction, RepeatForeverInstruction):
                self.vm.repeat_forever = True
                self.vm.add_log("Repeat forever enabled")
            
            elif isinstance(instruction, WatchInstruction):
                x, y = self.vm.resolve_coordinate(instruction.coord)
                self.vm.set_watchpoint(x, y, instruction.watch_type)
            
            return True
            
        except VMError as e:
            self.vm.add_error(str(e))
            return False
        except Exception as e:
            self.vm.add_error(f"Execution error: {str(e)}")
            return False
    
    def evaluate_condition(self, condition: str) -> bool:
        """Evaluate a condition string"""
        condition = condition.strip()
        
        # Handle logical operators
        if ' and ' in condition:
            parts = condition.split(' and ', 1)
            return self.evaluate_condition(parts[0]) and self.evaluate_condition(parts[1])
        
        if ' or ' in condition:
            parts = condition.split(' or ', 1)
            return self.evaluate_condition(parts[0]) or self.evaluate_condition(parts[1])
        
        # Handle comparison operators
        for op in ['==', '!=', '<=', '>=', '<', '>']:
            if op in condition:
                parts = condition.split(op, 1)
                left = self.get_value(parts[0].strip())
                right = self.get_value(parts[1].strip())
                
                if op == '==':
                    return left == right
                elif op == '!=':
                    return left != right
                elif op == '<':
                    return left < right
                elif op == '>':
                    return left > right
                elif op == '<=':
                    return left <= right
                elif op == '>=':
                    return left >= right
        
        # Simple boolean value
        return self.get_value(condition) != 0
    
    def get_value(self, expr: str) -> Any:
        """Get value from expression (variable or literal)"""
        expr = expr.strip()
        
        # Check if it's a variable
        if expr in self.vm.variables:
            return self.vm.variables[expr]
        
        # Try to parse as integer
        try:
            return int(expr)
        except:
            pass
        
        # Try to parse as boolean
        if expr.lower() == 'true':
            return True
        elif expr.lower() == 'false':
            return False
        
        return 0
    
    def execute_section(self, section: List[Instruction]) -> bool:
        """Execute a section of instructions"""
        for instruction in section:
            if not self.vm.running or self.vm.paused:
                return False
            
            if not self.execute_instruction(instruction):
                return False
            
            if self.step_mode:
                return True  # Pause after each instruction in step mode
        
        return True
    
    def run(self):
        """Run the complete program"""
        self.vm.running = True
        self.vm.add_log("=== Starting execution ===")
        
        # Execute First section
        self.vm.add_log("=== Executing First section ===")
        self.current_section = "First"
        if not self.execute_section(self.program.first_section):
            self.vm.running = False
            return
        
        # Execute Second section
        self.vm.add_log("=== Executing Second section ===")
        self.current_section = "Second"
        
        # Check if repeat forever is in the Second section
        has_repeat = any(isinstance(inst, RepeatForeverInstruction) 
                        for inst in self.program.second_section)
        
        if has_repeat:
            # Execute Second section in a loop
            iteration = 0
            max_iterations = 10000  # Safety limit
            while self.vm.running and not self.vm.paused and iteration < max_iterations:
                if not self.execute_section(self.program.second_section):
                    break
                iteration += 1
                if self.step_mode:
                    break
            
            if iteration >= max_iterations:
                self.vm.add_warning("Maximum iterations reached (10000)")
        else:
            # Execute Second section once
            self.execute_section(self.program.second_section)
        
        self.vm.add_log("=== Execution completed ===")
        self.vm.running = False
    
    def step(self):
        """Execute one instruction (step mode)"""
        self.step_mode = True
        if not self.vm.running:
            self.run()
        else:
            # Continue from where we left off
            if self.current_section == "First":
                if self.current_instruction < len(self.program.first_section):
                    inst = self.program.first_section[self.current_instruction]
                    self.execute_instruction(inst)
                    self.current_instruction += 1
            elif self.current_section == "Second":
                if self.current_instruction < len(self.program.second_section):
                    inst = self.program.second_section[self.current_instruction]
                    self.execute_instruction(inst)
                    self.current_instruction += 1
    
    def pause(self):
        """Pause execution"""
        self.vm.paused = True
    
    def reset(self):
        """Reset execution state"""
        self.vm.reset()
        self.current_instruction = 0
        self.current_section = None
        self.step_mode = False


if __name__ == "__main__":
    # Test execution engine
    from machine_loader import MachineConfig, load_machine_config
    
    config = MachineConfig()
    vm = VirtualMachine(config)
    prog = Program()
    
    engine = ExecutionEngine(vm, prog)
    print("Execution Engine Test")
