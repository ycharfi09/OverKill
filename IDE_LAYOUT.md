# OverKill IDE Visual Layout

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ OverKill IDE - Sandboxed Programming Language                    [_][□][X]  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ File  Edit  Run  Help                                                        ║
╠════════════════════════════════════════╦═════════════════════════════════════╣
║                                        ║ Execution Controls                  ║
║  Code Editor                           ║ ┌─────────────────────────────────┐ ║
║  ┌──────────────────────────────────┐  ║ │ [▶ Run] [→ Step] [⏸ Pause]    │ ║
║  │run on "machine.okt"              │  ║ │ [⟲ Reset]                      │ ║
║  │                                  │  ║ └─────────────────────────────────┘ ║
║  │First                             │  ║                                     ║
║  │    mode warn                     │  ║ ┌─ Registers ─────────────────────┐ ║
║  │    set reg 0;0 = int 10 named   │  ║ │ === Registers & Memory ===      │ ║
║  │        counter                   │  ║ │                                 │ ║
║  │    set reg 1;0 = int 0 named    │  ║ │ (  0,   0) = 10        [*]      │ ║
║  │        result                    │  ║ │ (  1,   0) = 0                  │ ║
║  │    watch reg 0;0 on write       │  ║ │ (  2,   0) = 10        [*]      │ ║
║  │                                  │  ║ │ (  3,   0) = 1         [*]      │ ║
║  │Second                            │  ║ │                                 │ ║
║  │    read 0;0 into value          │  ║ └─────────────────────────────────┘ ║
║  │    read 1;0 into current        │  ║                                     ║
║  │    write value into 2;0         │  ║ ┌─ Variables ─────────────────────┐ ║
║  │    wait 100                      │  ║ │ === Variables ===               │ ║
║  │                                  │  ║ │                                 │ ║
║  │                                  │  ║ │ value = 10                      │ ║
║  │                                  │  ║ │ current = 0                     │ ║
║  └──────────────────────────────────┘  ║ │                                 │ ║
║                                        ║ └─────────────────────────────────┘ ║
║                                        ║                                     ║
║                                        ║ ┌─ Console / Warnings ────────────┐ ║
║                                        ║ │ === Starting execution ===      │ ║
║                                        ║ │ Mode set to: warn               │ ║
║                                        ║ │ Write: (0, 0) = 10              │ ║
║                                        ║ │ ⚠ WARNING: Watchpoint hit:      │ ║
║                                        ║ │   write at (0, 0)               │ ║
║                                        ║ │ === Execution completed ===     │ ║
║                                        ║ └─────────────────────────────────┘ ║
╠════════════════════════════════════════╩═════════════════════════════════════╣
║ Status: Execution completed                                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## IDE Features

### Left Panel - Code Editor
- Syntax-highlighted text editor (planned)
- Line numbers
- Edit .ok program files
- File operations: New, Open, Save, Save As

### Right Panel - VM Visualization

#### Execution Controls
- **▶ Run**: Execute the entire program
- **→ Step**: Execute one instruction at a time
- **⏸ Pause**: Pause execution
- **⟲ Reset**: Clear VM state and start over

#### Registers Tab
- Shows all initialized memory locations
- Format: (X, Y) = Value
- `[*]` indicates recently changed locations
- Real-time updates during execution

#### Variables Tab
- Shows all program variables
- Format: variable_name = value
- Updated as program executes

#### Console/Warnings Tab
- Execution logs
- Warnings (⚠) highlighted
- Errors (✗) highlighted
- Step-by-step instruction trace

### Status Bar
- Shows current execution state
- File path being edited
- Mode indicators

## Usage Flow

1. **Write/Load Program**: Edit code in the left panel
2. **Run/Step**: Use execution controls to run program
3. **Observe**: Watch memory changes in real-time
4. **Debug**: Use watchpoints and step mode to understand execution
5. **Learn**: See consequences of each instruction clearly

## Educational Benefits

- **Visual Feedback**: See exactly what each instruction does
- **Safe Exploration**: No risk to real hardware
- **Step-by-Step**: Understand execution flow
- **Error Visibility**: Clear warnings and errors
- **Memory Observation**: Watch how programs modify state
