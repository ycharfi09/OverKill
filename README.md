# OverKill - Sandboxed Programming Language and IDE

OverKill is a **sandboxed programming language and IDE** designed to **teach beginners how machines work safely**. It simulates memory, registers, storage, loops, and reads/writes **without touching real hardware**.

## Features

- **Safe Virtual Machine**: Executes code in a sandboxed environment
- **Memory Visualization**: See registers and memory in real-time
- **Step-by-Step Execution**: Debug and understand each instruction
- **Watchpoints**: Monitor specific registers and variables
- **Educational Focus**: Explicit errors and warnings for learning
- **Execution Modes**: Warn mode for learning, strict mode for enforcing correctness
- **Permission System**: Read-only and read-write regions
- **Named Registers**: Use descriptive names instead of coordinates

## File Types

- `.ok` - OverKill program files
- `.okt` - Machine definition files (defines memory layout, registers, permissions)

## Quick Start

### Command-Line Interface (Recommended for Testing)

```bash
# Run a program
python overkill_cli.py example.ok

# Run other examples
python overkill_cli.py simple_demo.ok
python overkill_cli.py strict_demo.ok
python overkill_cli.py watchpoint_demo.ok
```

### GUI IDE (Requires tkinter)

```bash
python overkill_ide.py
```

### Run Tests

```bash
python test_overkill.py
```

## Language Syntax

### Program Structure

```
run on "machine.okt"

First
    # Runs once at program start
    set reg 0;0 = int 10 named counter

Second
    # May repeat forever
    read 0;0 into value
    write value into 1;0
    repeat forever
```

### Instructions

- `set reg X;Y = int N [named name]` - Set register value
- `read X;Y into variable` - Read from memory/register
- `write variable into X;Y` - Write to memory/register
- `when condition ... otherwise ...` - Conditional execution
- `repeat forever` - Loop Second section indefinitely
- `wait N` - Simulated delay in milliseconds

### Watchpoints

```
watch reg 0;0 on read
watch reg 1;0 on write
```

### Modes

- `mode warn` - Print warnings, continue execution
- `mode strict` - Stop on any invalid operation

## Machine Definition (.okt)

```
memory 256x256
region registers 0;0 to 15;15 rw
region storage 16;0 to 255;255 rw
reg 12;4 int led
reg 34;1 int counter
```

## Project Structure

```
OverKill/
├── machine_loader.py      # Loads .okt machine definition files
├── virtual_machine.py     # Virtual machine implementation
├── language_parser.py     # Parses .ok program files
├── execution_engine.py    # Executes instructions on VM
├── overkill_ide.py        # GUI IDE (requires tkinter)
├── overkill_cli.py        # Command-line interface
├── test_overkill.py       # Test suite
├── machine.okt            # Default machine definition
├── example.ok             # Basic example program
├── simple_demo.ok         # Simple demonstration
├── strict_demo.ok         # Strict mode demonstration
├── watchpoint_demo.ok     # Watchpoint demonstration
├── loop_example.ok        # Loop example
├── README.md              # This file
└── TUTORIAL.md            # Comprehensive tutorial
```

## Examples Included

1. **example.ok** - Basic read/write operations with watchpoints
2. **simple_demo.ok** - Demonstrates conditional logic
3. **strict_demo.ok** - Shows strict mode error handling
4. **watchpoint_demo.ok** - Demonstrates watchpoint triggers
5. **loop_example.ok** - Infinite loop with repeat forever

## Documentation

- **README.md** (this file) - Quick start and overview
- **TUTORIAL.md** - Comprehensive language tutorial with examples

## Testing

The project includes a comprehensive test suite that validates:
- Machine configuration loading
- Virtual machine operations
- Language parsing
- Instruction execution
- Error handling and warnings
- Watchpoints
- Conditional execution
- Strict mode enforcement

Run tests with:
```bash
python test_overkill.py
```

## Requirements

- Python 3.7 or higher
- tkinter (for GUI IDE, optional)

No external dependencies required - uses only Python standard library!

## Architecture

1. **Machine Loader**: Parses `.okt` files to define virtual hardware
2. **Virtual Machine**: Manages memory, enforces permissions, tracks state
3. **Language Parser**: Parses `.ok` program files into instruction objects
4. **Execution Engine**: Executes instructions on the VM with proper error handling
5. **IDE/CLI**: User interfaces for writing and running programs

## Educational Use

OverKill is designed for teaching:
- How memory and registers work
- Assembly-like low-level programming
- Debugging with step execution
- Memory safety and permissions
- Consequences of uninitialized reads
- Watchpoint-based debugging

## Contributing

This project is designed to be easily extensible:
- Add new instruction types in `language_parser.py` and `execution_engine.py`
- Enhance VM features in `virtual_machine.py`
- Improve visualization in `overkill_ide.py`
- Add new machine configurations (`.okt` files)
- Create more example programs (`.ok` files)

## License

MIT License - See LICENSE file for details
