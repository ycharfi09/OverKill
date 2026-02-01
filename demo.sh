#!/bin/bash
# Demonstration script for OverKill
# Shows all features in action

echo "================================================================"
echo "         OverKill - Sandboxed Programming Language"
echo "                     Demonstration"
echo "================================================================"
echo ""

echo "1. Running Basic Example"
echo "================================================================"
python overkill_cli.py example.ok
echo ""
echo "Press Enter to continue..."
read

echo ""
echo "2. Running Simple Demo (with conditionals)"
echo "================================================================"
python overkill_cli.py simple_demo.ok
echo ""
echo "Press Enter to continue..."
read

echo ""
echo "3. Running Strict Mode Demo (shows error handling)"
echo "================================================================"
python overkill_cli.py strict_demo.ok
echo ""
echo "Press Enter to continue..."
read

echo ""
echo "4. Running Watchpoint Demo"
echo "================================================================"
python overkill_cli.py watchpoint_demo.ok
echo ""
echo "Press Enter to continue..."
read

echo ""
echo "5. Running Comprehensive Demo (all features)"
echo "================================================================"
python overkill_cli.py comprehensive_demo.ok
echo ""
echo "Press Enter to continue..."
read

echo ""
echo "6. Running Test Suite"
echo "================================================================"
python test_overkill.py
echo ""

echo "================================================================"
echo "                  Demonstration Complete"
echo "================================================================"
echo ""
echo "To try OverKill yourself:"
echo "  1. Edit or create a .ok program file"
echo "  2. Run: python overkill_cli.py your_program.ok"
echo "  3. Or use the GUI: python overkill_ide.py (requires tkinter)"
echo ""
echo "See TUTORIAL.md for complete language reference"
echo "================================================================"
