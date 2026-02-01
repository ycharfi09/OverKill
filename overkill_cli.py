#!/usr/bin/env python3
"""
OverKill Command-Line Interface
For testing without GUI
"""

import sys
import os
from machine_loader import load_machine_config
from language_parser import parse_program
from virtual_machine import VirtualMachine
from execution_engine import ExecutionEngine


def print_separator():
    print("=" * 60)


def print_vm_state(vm):
    """Print the current VM state"""
    print_separator()
    print("VM STATE")
    print_separator()
    
    print("\nMemory & Registers:")
    if vm.initialized:
        for (x, y) in sorted(vm.initialized):
            value = vm.memory.get((x, y), 0)
            is_recent = (x, y) in vm.recent_changes
            marker = " [CHANGED]" if is_recent else ""
            print(f"  ({x:3d}, {y:3d}) = {value}{marker}")
    else:
        print("  (No initialized memory)")
    
    print("\nVariables:")
    if vm.variables:
        for var_name, value in vm.variables.items():
            print(f"  {var_name} = {value}")
    else:
        print("  (No variables)")
    
    print("\nWatchpoints:")
    if vm.watchpoints:
        for (x, y), watch_type in vm.watchpoints.items():
            print(f"  ({x}, {y}) -> {watch_type}")
    else:
        print("  (No watchpoints)")
    
    print(f"\nMode: {vm.mode}")
    print(f"Warnings: {len(vm.warnings)}")
    print(f"Errors: {len(vm.errors)}")


def run_program(program_file, step_mode=False):
    """Run an OverKill program"""
    print_separator()
    print(f"LOADING PROGRAM: {program_file}")
    print_separator()
    
    try:
        # Parse program
        program = parse_program(program_file)
        print(f"\n✓ Program parsed successfully")
        print(f"  Machine file: {program.machine_file}")
        print(f"  Mode: {program.mode}")
        print(f"  First section: {len(program.first_section)} instructions")
        print(f"  Second section: {len(program.second_section)} instructions")
        
        # Load machine config
        machine_file = program.machine_file or "machine.okt"
        if not os.path.exists(machine_file):
            print(f"\n! Machine file '{machine_file}' not found, using default config")
            from machine_loader import MachineConfig
            config = MachineConfig()
        else:
            config = load_machine_config(machine_file)
            print(f"\n✓ Machine config loaded")
            print(f"  Memory: {config.memory_size[0]}x{config.memory_size[1]}")
            print(f"  Regions: {len(config.regions)}")
            print(f"  Named registers: {len(config.named_registers)}")
        
        # Create VM and engine
        vm = VirtualMachine(config, mode=program.mode)
        engine = ExecutionEngine(vm, program)
        
        print_separator()
        print("STARTING EXECUTION")
        print_separator()
        
        # Run the program
        engine.run()
        
        # Show results
        print_separator()
        print("EXECUTION COMPLETED")
        print_separator()
        
        print_vm_state(vm)
        
        # Show logs
        print("\n" + "=" * 60)
        print("EXECUTION LOG")
        print("=" * 60)
        for log_entry in vm.log:
            if "WARNING" in log_entry:
                print(f"⚠ {log_entry}")
            elif "ERROR" in log_entry:
                print(f"✗ {log_entry}")
            else:
                print(f"  {log_entry}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("OverKill Command-Line Interface")
        print("\nUsage:")
        print("  python overkill_cli.py <program.ok>")
        print("\nExamples:")
        print("  python overkill_cli.py example.ok")
        print("  python overkill_cli.py loop_example.ok")
        return
    
    program_file = sys.argv[1]
    
    if not os.path.exists(program_file):
        print(f"Error: File '{program_file}' not found")
        return
    
    run_program(program_file)


if __name__ == "__main__":
    main()
