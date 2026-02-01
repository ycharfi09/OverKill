# OverKill - Sandboxed Programming Language and IDE

OverKill is a **sandboxed programming language and IDE** designed to **teach beginners how machines work safely**. It simulates memory, registers, storage, loops, and reads/writes **without touching real hardware**.

## Features

- **Safe Virtual Machine**: Executes code in a sandboxed environment
- **Memory Visualization**: See registers and memory in real-time
- **Step-by-Step Execution**: Debug and understand each instruction
- **Watchpoints**: Monitor specific registers and variables
- **Educational Focus**: Explicit errors and warnings for learning

## File Types

- `.ok` - OverKill program files
- `.okt` - Machine definition files (defines memory layout, registers, permissions)

## Quick Start

```bash
python overkill_ide.py
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

## License

MIT License - See LICENSE file for details
