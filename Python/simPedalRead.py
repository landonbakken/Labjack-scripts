import tkinter as tk
from tkinter import ttk
from labjack import ljm
import threading
import time

class LabJackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LabJack AIN0 Reader")

        # Initialize LabJack
        try:
            self.handle = ljm.openS("ANY", "ANY", "ANY")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Could not open LabJack: {e}")
            raise

        # Variables
        self.zero_value = 0.0
        self.ratio = tk.DoubleVar(value=1.0)
        self.display_value = tk.StringVar(value="0.0000")

        # Layout
        ttk.Label(root, text="Ratio:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(root, textvariable=self.ratio, width=10).grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(root, text="Zero Value", command=self.zero_reading).grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(root, text="Scaled Value:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(root, textvariable=self.display_value, font=("Consolas", 16, "bold")).grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="w")

        # Start reading thread
        self.running = True
        threading.Thread(target=self.read_loop, daemon=True).start()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def zero_reading(self):
        """Set current AIN0 value as zero offset."""
        self.zero_value = ljm.eReadName(self.handle, "AIN0")

    def read_loop(self):
        """Continuously read from AIN0 and update display."""
        while self.running:
            try:
                raw_value = ljm.eReadName(self.handle, "AIN0")
                adjusted_value = (raw_value - self.zero_value) * self.ratio.get()
                self.display_value.set(f"{adjusted_value:.4f}")
            except Exception as e:
                self.display_value.set(f"Error: {e}")
            time.sleep(0.1)

    def on_close(self):
        """Cleanup on exit."""
        self.running = False
        time.sleep(0.2)
        try:
            ljm.close(self.handle)
        except Exception:
            pass
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = LabJackApp(root)
    root.mainloop()
