# OverKill Tutorial

## Introduction

OverKill is a sandboxed programming language designed to teach beginners how machines work at a low level, without the risk of affecting real hardware. It simulates memory, registers, and storage in a safe, controlled environment.

## Getting Started

### Running Programs

**Using the Command-Line Interface:**
```bash
python overkill_cli.py your_program.ok
```

**Using the GUI IDE (requires tkinter):**
```bash
python overkill_ide.py
```

## Language Basics

### Program Structure

Every OverKill program has this structure:

```
run on "machine.okt"

First
    # Initialization code - runs once
    
Second
    # Main code - runs once or repeats forever
```

### Sections

- **First**: Runs once at program start. Use for initialization.
- **Second**: Main program logic. Can repeat forever if `repeat forever` is included.

### Comments

```
# This is a comment
```

## Instructions

### 1. Set Register

Set a register to a value:

```
set reg X;Y = int N [named name]
```

Examples:
```
set reg 0;0 = int 42
set reg 1;0 = int 100 named counter
set reg 2;0 = bool true
```

### 2. Read from Memory

Read a value from a memory location into a variable:

```
read X;Y into variable_name
```

Examples:
```
read 0;0 into value
read 1;0 into counter
read temp into result
```

### 3. Write to Memory

Write a variable's value to a memory location:

```
write variable_name into X;Y
```

Examples:
```
write value into 0;0
write counter into 1;0
```

### 4. Conditional Execution

Execute code based on conditions:

```
when condition
    # code if true

when condition
    # code if true
otherwise
    # code if false
```

Supported operators:
- `==` (equal)
- `!=` (not equal)
- `<` (less than)
- `>` (greater than)
- `<=` (less than or equal)
- `>=` (greater than or equal)
- `and` (logical AND)
- `or` (logical OR)

Examples:
```
when counter > 10
    set reg 0;0 = int 0

when value == 42 and flag == true
    write result into 5;5
```

### 5. Wait

Simulate a delay (for teaching purposes, doesn't actually wait):

```
wait N
```

Example:
```
wait 100    # Wait 100 milliseconds
```

### 6. Repeat Forever

Make the Second section repeat indefinitely:

```
repeat forever
```

Example:
```
Second
    read 0;0 into counter
    write counter into 1;0
    wait 50
    repeat forever
```

## Watchpoints

Monitor when specific memory locations are accessed:

```
watch reg X;Y on read
watch reg X;Y on write
watch reg X;Y on both
```

When a watchpoint is triggered, a warning is logged.

Example:
```
First
    set reg 0;0 = int 10
    watch reg 0;0 on write

Second
    write value into 0;0    # Triggers watchpoint!
```

## Execution Modes

### Warn Mode (Default)

Warnings are printed but execution continues:

```
mode warn
```

### Strict Mode

Execution stops on any error:

```
mode strict
```

Example:
```
First
    mode strict
    set reg 0;0 = int 100

Second
    write value into 20;250    # ERROR! Read-only location
    # Following code won't execute
```

## Machine Definition Files (.okt)

Machine files define the virtual hardware:

```
# Memory size
memory 256x256

# Define regions with permissions
region registers 0;0 to 15;15 rw
region storage 16;0 to 255;255 rw
region readonly_area 16;240 to 31;255 readonly

# Named registers with types
reg 0;0 int counter
reg 1;0 int result
reg 2;0 bool flag
```

Permissions:
- `rw` - read/write
- `r` - read-only
- `readonly` - read-only

Types:
- `int` - integer
- `bool` - boolean

## Complete Examples

### Example 1: Simple Counter

```
run on "machine.okt"

First
    mode warn
    set reg 0;0 = int 0 named counter

Second
    read 0;0 into count
    write count into 1;0
```

### Example 2: Conditional Logic

```
run on "machine.okt"

First
    set reg 0;0 = int 10 named value

Second
    read 0;0 into x
    
    when x > 5
        set reg 1;0 = int 1
    otherwise
        set reg 1;0 = int 0
```

### Example 3: Loop with Watchpoint

```
run on "machine.okt"

First
    mode warn
    set reg 0;0 = int 0 named counter
    watch reg 0;0 on write

Second
    read 0;0 into count
    write count into 1;0
    wait 100
    repeat forever
```

### Example 4: Strict Mode Error Handling

```
run on "machine.okt"

First
    mode strict
    set reg 0;0 = int 100

Second
    # This will cause execution to stop
    write value into 20;250    # Read-only location!
    set reg 1;0 = int 999      # Won't execute
```

## Common Errors and Warnings

### Uninitialized Read
```
WARNING: Reading uninitialized location: (5, 5)
```
Solution: Initialize the location before reading.

### Read-Only Write
```
ERROR: Write to read-only location: (20, 250)
```
Solution: Don't write to read-only regions.

### Out of Bounds
```
ERROR: Out of bounds access: (300, 300)
```
Solution: Use coordinates within the memory size.

### Uninitialized Variable
```
WARNING: Variable 'x' not initialized
```
Solution: Read into the variable before using it.

## Teaching Tips

1. **Start Simple**: Begin with basic set/read/write operations
2. **Use Watchpoints**: Help students understand when memory is accessed
3. **Strict Mode**: Enforce good practices
4. **Step Mode**: Use the step execution to see each instruction's effect
5. **Visualize**: Watch the memory and register changes in real-time

## Troubleshooting

### Program Won't Run

- Check that the machine file exists
- Verify all coordinates are within bounds
- Ensure proper syntax (use examples as templates)

### Infinite Loop

- `repeat forever` causes the Second section to loop up to 10,000 iterations
- Use conditions to break loops
- Check loop logic carefully

### Permission Errors

- Review the machine definition file
- Ensure you're not writing to read-only regions
- Use warn mode during development

## Next Steps

1. Try the provided examples
2. Create your own machine definitions
3. Experiment with watchpoints
4. Build progressively complex programs
5. Use step mode to understand execution flow

Happy coding with OverKill!
