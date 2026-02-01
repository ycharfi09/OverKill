#!/usr/bin/env python3
"""
Test suite for OverKill
Validates all core functionality
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from machine_loader import MachineConfig, load_machine_config, parse_coordinate
from language_parser import parse_program
from virtual_machine import VirtualMachine, VMError
from execution_engine import ExecutionEngine


class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def add_pass(self, test_name):
        self.passed += 1
        self.tests.append((test_name, True, None))
        print(f"  ✓ {test_name}")
    
    def add_fail(self, test_name, error):
        self.failed += 1
        self.tests.append((test_name, False, error))
        print(f"  ✗ {test_name}: {error}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Test Results: {self.passed}/{total} passed")
        if self.failed > 0:
            print(f"FAILED: {self.failed} tests failed")
            return False
        else:
            print("SUCCESS: All tests passed!")
            return True


def test_machine_loader(results):
    """Test machine configuration loader"""
    print("\n=== Testing Machine Loader ===")
    
    # Test default config
    try:
        config = MachineConfig()
        assert config.memory_size == (256, 256)
        assert config.is_valid_coordinate(0, 0)
        assert not config.is_valid_coordinate(300, 300)
        results.add_pass("Default machine config")
    except Exception as e:
        results.add_fail("Default machine config", str(e))
    
    # Test coordinate parsing
    try:
        coord = parse_coordinate("12;34")
        assert coord == (12, 34)
        coord = parse_coordinate("1A;2B")
        assert coord == (26, 43)
        results.add_pass("Coordinate parsing")
    except Exception as e:
        results.add_fail("Coordinate parsing", str(e))
    
    # Test loading machine file
    try:
        config = load_machine_config("machine.okt")
        assert config.memory_size == (256, 256)
        assert "counter" in config.named_registers
        assert config.get_permission(0, 0) == "rw"
        assert config.get_permission(20, 250) == "readonly"
        results.add_pass("Load machine config file")
    except Exception as e:
        results.add_fail("Load machine config file", str(e))


def test_virtual_machine(results):
    """Test virtual machine"""
    print("\n=== Testing Virtual Machine ===")
    
    config = MachineConfig()
    
    # Test basic read/write
    try:
        vm = VirtualMachine(config, mode="warn")
        vm.write_memory(0, 0, 42)
        value = vm.read_memory(0, 0)
        assert value == 42
        assert (0, 0) in vm.initialized
        results.add_pass("Basic read/write")
    except Exception as e:
        results.add_fail("Basic read/write", str(e))
    
    # Test uninitialized read warning
    try:
        vm = VirtualMachine(config, mode="warn")
        value = vm.read_memory(5, 5)
        assert len(vm.warnings) > 0
        assert "uninitialized" in vm.warnings[0].lower()
        results.add_pass("Uninitialized read warning")
    except Exception as e:
        results.add_fail("Uninitialized read warning", str(e))
    
    # Test bounds checking
    try:
        vm = VirtualMachine(config, mode="warn")
        vm.write_memory(300, 300, 42)
        assert len(vm.errors) > 0
        assert "bounds" in vm.errors[0].lower()
        results.add_pass("Bounds checking")
    except Exception as e:
        results.add_fail("Bounds checking", str(e))
    
    # Test watchpoints
    try:
        vm = VirtualMachine(config, mode="warn")
        vm.set_watchpoint(0, 0, "write")
        vm.write_memory(0, 0, 42)
        assert len(vm.warnings) > 0
        assert "watchpoint" in vm.warnings[0].lower()
        results.add_pass("Watchpoints")
    except Exception as e:
        results.add_fail("Watchpoints", str(e))
    
    # Test strict mode
    try:
        vm = VirtualMachine(config, mode="strict")
        config.permissions[(0, 0)] = "readonly"
        error_raised = False
        try:
            vm.write_memory(0, 0, 42)
        except VMError:
            error_raised = True
        assert error_raised
        results.add_pass("Strict mode")
    except Exception as e:
        results.add_fail("Strict mode", str(e))


def test_parser(results):
    """Test language parser"""
    print("\n=== Testing Language Parser ===")
    
    # Test parsing example program
    try:
        program = parse_program("example.ok")
        assert program.machine_file == "machine.okt"
        assert program.mode == "warn"
        assert len(program.first_section) > 0
        assert len(program.second_section) > 0
        results.add_pass("Parse example program")
    except Exception as e:
        results.add_fail("Parse example program", str(e))
    
    # Test instruction types
    try:
        program = parse_program("example.ok")
        from language_parser import (SetRegInstruction, ReadInstruction, 
                                     WriteInstruction, WatchInstruction)
        
        has_set = any(isinstance(i, SetRegInstruction) for i in program.first_section)
        has_read = any(isinstance(i, ReadInstruction) for i in program.second_section)
        has_write = any(isinstance(i, WriteInstruction) for i in program.second_section)
        has_watch = any(isinstance(i, WatchInstruction) for i in program.first_section)
        
        assert has_set and has_read and has_write and has_watch
        results.add_pass("Instruction parsing")
    except Exception as e:
        results.add_fail("Instruction parsing", str(e))


def test_execution_engine(results):
    """Test execution engine"""
    print("\n=== Testing Execution Engine ===")
    
    # Test basic execution
    try:
        config = load_machine_config("machine.okt")
        program = parse_program("example.ok")
        vm = VirtualMachine(config, mode=program.mode)
        engine = ExecutionEngine(vm, program)
        
        engine.run()
        
        assert len(vm.initialized) > 0
        assert len(vm.variables) > 0
        results.add_pass("Basic program execution")
    except Exception as e:
        results.add_fail("Basic program execution", str(e))
    
    # Test conditional execution
    try:
        config = load_machine_config("machine.okt")
        program = parse_program("simple_demo.ok")
        vm = VirtualMachine(config, mode=program.mode)
        engine = ExecutionEngine(vm, program)
        
        engine.run()
        
        # Check that conditional was executed
        assert (3, 0) in vm.initialized
        results.add_pass("Conditional execution")
    except Exception as e:
        results.add_fail("Conditional execution", str(e))
    
    # Test strict mode errors
    try:
        config = load_machine_config("machine.okt")
        program = parse_program("strict_demo.ok")
        vm = VirtualMachine(config, mode=program.mode)
        engine = ExecutionEngine(vm, program)
        
        engine.run()
        
        # Should have an error from readonly write
        assert len(vm.errors) > 0
        results.add_pass("Strict mode error handling")
    except Exception as e:
        results.add_fail("Strict mode error handling", str(e))
    
    # Test watchpoint triggers
    try:
        config = load_machine_config("machine.okt")
        program = parse_program("watchpoint_demo.ok")
        vm = VirtualMachine(config, mode=program.mode)
        engine = ExecutionEngine(vm, program)
        
        engine.run()
        
        # Should have warnings from watchpoints and uninitialized read
        assert len(vm.warnings) > 0
        results.add_pass("Watchpoint triggers")
    except Exception as e:
        results.add_fail("Watchpoint triggers", str(e))


def main():
    """Run all tests"""
    print("="*60)
    print("OverKill Test Suite")
    print("="*60)
    
    results = TestResults()
    
    test_machine_loader(results)
    test_virtual_machine(results)
    test_parser(results)
    test_execution_engine(results)
    
    print("\n" + "="*60)
    success = results.summary()
    print("="*60)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
