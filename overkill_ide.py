"""
OverKill IDE - Graphical Interface
Minimal GUI with code editor, VM visualization, and execution controls
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import os
import tempfile
from machine_loader import load_machine_config, MachineConfig
from language_parser import parse_program
from virtual_machine import VirtualMachine
from execution_engine import ExecutionEngine
import threading


class OverKillIDE:
    """Main IDE window for OverKill"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("OverKill IDE - Sandboxed Programming Language")
        self.root.geometry("1200x800")
        
        # State
        self.vm = None
        self.engine = None
        self.program = None
        self.current_file = None
        self.execution_thread = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open...", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As...", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Main container with paned window
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - Code editor
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=2)
        
        # Editor label and toolbar
        editor_toolbar = ttk.Frame(left_frame)
        editor_toolbar.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(editor_toolbar, text="Code Editor", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        
        # Code editor
        self.code_editor = scrolledtext.ScrolledText(
            left_frame,
            wrap=tk.WORD,
            width=60,
            height=30,
            font=("Courier New", 10)
        )
        self.code_editor.pack(fill=tk.BOTH, expand=True)
        
        # Right panel - VM and controls
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=1)
        
        # Execution controls
        controls_frame = ttk.LabelFrame(right_frame, text="Execution Controls", padding=10)
        controls_frame.pack(fill=tk.X, pady=(0, 5))
        
        btn_frame = ttk.Frame(controls_frame)
        btn_frame.pack(fill=tk.X)
        
        self.run_btn = ttk.Button(btn_frame, text="▶ Run", command=self.run_program)
        self.run_btn.pack(side=tk.LEFT, padx=2)
        
        self.step_btn = ttk.Button(btn_frame, text="→ Step", command=self.step_program)
        self.step_btn.pack(side=tk.LEFT, padx=2)
        
        self.pause_btn = ttk.Button(btn_frame, text="⏸ Pause", command=self.pause_program)
        self.pause_btn.pack(side=tk.LEFT, padx=2)
        
        self.reset_btn = ttk.Button(btn_frame, text="⟲ Reset", command=self.reset_program)
        self.reset_btn.pack(side=tk.LEFT, padx=2)
        
        # VM Panel with tabs
        vm_notebook = ttk.Notebook(right_frame)
        vm_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Registers tab
        registers_frame = ttk.Frame(vm_notebook)
        vm_notebook.add(registers_frame, text="Registers")
        
        # Registers display (scrollable)
        reg_scroll_frame = ttk.Frame(registers_frame)
        reg_scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        self.registers_text = scrolledtext.ScrolledText(
            reg_scroll_frame,
            wrap=tk.WORD,
            width=40,
            height=15,
            font=("Courier New", 9)
        )
        self.registers_text.pack(fill=tk.BOTH, expand=True)
        
        # Variables tab
        variables_frame = ttk.Frame(vm_notebook)
        vm_notebook.add(variables_frame, text="Variables")
        
        self.variables_text = scrolledtext.ScrolledText(
            variables_frame,
            wrap=tk.WORD,
            width=40,
            height=15,
            font=("Courier New", 9)
        )
        self.variables_text.pack(fill=tk.BOTH, expand=True)
        
        # Console/Warnings
        console_frame = ttk.LabelFrame(right_frame, text="Console / Warnings", padding=5)
        console_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        self.console_text = scrolledtext.ScrolledText(
            console_frame,
            wrap=tk.WORD,
            width=40,
            height=10,
            font=("Courier New", 9),
            bg="#1e1e1e",
            fg="#d4d4d4"
        )
        self.console_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Load example program
        self.load_example()
    
    def load_example(self):
        """Load an example program"""
        example = '''run on "machine.okt"

First
    mode warn
    set reg 0;0 = int 10 named counter
    set reg 1;0 = int 0 named result
    watch reg 0;0 on write

Second
    read 0;0 into value
    read 1;0 into current
    write value into 2;0
    wait 100
'''
        self.code_editor.delete(1.0, tk.END)
        self.code_editor.insert(1.0, example)
        self.log_console("Example program loaded")
    
    def new_file(self):
        """Create a new file"""
        self.code_editor.delete(1.0, tk.END)
        self.current_file = None
        self.status_bar.config(text="New file")
    
    def open_file(self):
        """Open an existing file"""
        filename = filedialog.askopenfilename(
            title="Open OverKill Program",
            filetypes=[("OverKill Files", "*.ok"), ("All Files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    content = f.read()
                self.code_editor.delete(1.0, tk.END)
                self.code_editor.insert(1.0, content)
                self.current_file = filename
                self.status_bar.config(text=f"Opened: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {e}")
    
    def save_file(self):
        """Save the current file"""
        if self.current_file:
            try:
                content = self.code_editor.get(1.0, tk.END)
                with open(self.current_file, 'w') as f:
                    f.write(content)
                self.status_bar.config(text=f"Saved: {self.current_file}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
        else:
            self.save_file_as()
    
    def save_file_as(self):
        """Save the file with a new name"""
        filename = filedialog.asksaveasfilename(
            title="Save OverKill Program",
            defaultextension=".ok",
            filetypes=[("OverKill Files", "*.ok"), ("All Files", "*.*")]
        )
        if filename:
            self.current_file = filename
            self.save_file()
    
    def log_console(self, message):
        """Add a message to the console"""
        self.console_text.insert(tk.END, message + "\n")
        self.console_text.see(tk.END)
    
    def clear_console(self):
        """Clear the console"""
        self.console_text.delete(1.0, tk.END)
    
    def update_vm_display(self):
        """Update the VM visualization"""
        if not self.vm:
            return
        
        # Update registers display
        self.registers_text.delete(1.0, tk.END)
        self.registers_text.insert(tk.END, "=== Registers & Memory ===\n\n")
        
        # Show initialized memory locations
        for (x, y) in sorted(self.vm.initialized):
            value = self.vm.memory.get((x, y), 0)
            is_recent = (x, y) in self.vm.recent_changes
            marker = " [*]" if is_recent else ""
            self.registers_text.insert(tk.END, f"({x:3d}, {y:3d}) = {value}{marker}\n")
        
        if not self.vm.initialized:
            self.registers_text.insert(tk.END, "(No initialized memory)\n")
        
        # Update variables display
        self.variables_text.delete(1.0, tk.END)
        self.variables_text.insert(tk.END, "=== Variables ===\n\n")
        
        for var_name, value in self.vm.variables.items():
            self.variables_text.insert(tk.END, f"{var_name} = {value}\n")
        
        if not self.vm.variables:
            self.variables_text.insert(tk.END, "(No variables)\n")
        
        # Update console with logs
        if self.vm.log:
            for log_entry in self.vm.log[-50:]:  # Show last 50 entries
                if "WARNING" in log_entry or "ERROR" in log_entry:
                    self.log_console(log_entry)
    
    def prepare_execution(self):
        """Prepare the VM and program for execution"""
        try:
            # Save code to temporary file
            code = self.code_editor.get(1.0, tk.END)
            # Use tempfile to ensure reliable temp file creation
            with tempfile.NamedTemporaryFile(mode='w', suffix='.ok', delete=False) as f:
                temp_ok_file = f.name
                f.write(code)
            
            # Parse program
            self.program = parse_program(temp_ok_file)
            
            # Clean up temporary file after parsing
            try:
                os.unlink(temp_ok_file)
            except FileNotFoundError:
                pass  # File already deleted, ignore
            except OSError as e:
                self.log_console(f"Warning: Failed to clean up temp file: {e}")
            
            # Check if machine file exists, create default if not
            if self.program.machine_file:
                machine_file = self.program.machine_file
            else:
                machine_file = "machine.okt"
            
            # Try to find machine file
            search_paths = [
                machine_file,
                os.path.join("/home/runner/work/OverKill/OverKill", machine_file),
                os.path.join("/tmp", machine_file)
            ]
            
            config = None
            for path in search_paths:
                if os.path.exists(path):
                    config = load_machine_config(path)
                    break
            
            if not config:
                # Create default machine config
                self.log_console(f"Machine file '{machine_file}' not found, using default config")
                config = MachineConfig()
            
            # Create VM and engine
            self.vm = VirtualMachine(config, mode=self.program.mode)
            self.engine = ExecutionEngine(self.vm, self.program)
            
            self.status_bar.config(text="Ready to execute")
            return True
            
        except Exception as e:
            self.log_console(f"ERROR: Failed to prepare execution: {e}")
            messagebox.showerror("Error", f"Failed to prepare execution: {e}")
            return False
    
    def run_program(self):
        """Run the program"""
        self.clear_console()
        self.log_console("=== Starting execution ===")
        
        if not self.prepare_execution():
            return
        
        self.status_bar.config(text="Running...")
        
        # Run in a separate thread to keep UI responsive
        def run_thread():
            try:
                self.engine.run()
                self.root.after(0, lambda: self.on_execution_complete())
            except Exception as e:
                self.root.after(0, lambda: self.log_console(f"ERROR: {e}"))
        
        self.execution_thread = threading.Thread(target=run_thread, daemon=True)
        self.execution_thread.start()
        
        # Update display periodically
        self.root.after(100, self.check_execution)
    
    def check_execution(self):
        """Check execution status and update display"""
        if self.vm:
            self.update_vm_display()
        
        if self.execution_thread and self.execution_thread.is_alive():
            self.root.after(100, self.check_execution)
    
    def on_execution_complete(self):
        """Called when execution completes"""
        self.update_vm_display()
        self.log_console("=== Execution completed ===")
        self.status_bar.config(text="Execution completed")
    
    def step_program(self):
        """Execute one step"""
        if not self.engine:
            if not self.prepare_execution():
                return
            self.clear_console()
            self.log_console("=== Step mode ===")
        
        self.status_bar.config(text="Step mode...")
        self.engine.step()
        self.update_vm_display()
        self.status_bar.config(text="Step completed")
    
    def pause_program(self):
        """Pause execution"""
        if self.engine:
            self.engine.pause()
            self.log_console("=== Paused ===")
            self.status_bar.config(text="Paused")
    
    def reset_program(self):
        """Reset the VM"""
        if self.engine:
            self.engine.reset()
        self.vm = None
        self.engine = None
        self.program = None
        self.clear_console()
        self.log_console("=== Reset ===")
        self.status_bar.config(text="Reset")
        
        # Clear displays
        self.registers_text.delete(1.0, tk.END)
        self.variables_text.delete(1.0, tk.END)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = OverKillIDE(root)
    root.mainloop()


if __name__ == "__main__":
    main()
