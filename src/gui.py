import tkinter as tk
from tkinter import ttk, messagebox
from models import mm1, mms  # import the functions you implemented

class QueueApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Queueing Theory Calculator")
        self.geometry("450x400")
        self._build_frames()
        self.show_frame("MainMenu")

    def _build_frames(self):
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MainMenu, MM1Frame, MMSFrame):
            page = F(container, self)
            self.frames[F.__name__] = page
            page.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, name):
        self.frames[name].tkraise()

class MainMenu(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        ttk.Label(self, text="Queueing Theory", font=("Segoe UI", 20, "bold")).pack(pady=20)
        ttk.Button(self, text="M/M/1 Model", command=lambda: controller.show_frame("MM1Frame")).pack(fill="x", pady=10, padx=50)
        ttk.Button(self, text="M/M/S Model", command=lambda: controller.show_frame("MMSFrame")).pack(fill="x", pady=10, padx=50)

class MM1Frame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        self.ctrl = controller
        ttk.Label(self, text="M/M/1 Model", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self, text="Arrival rate (λ):").grid(row=1, column=0, sticky="e", pady=5)
        self.e_lambda = ttk.Entry(self); self.e_lambda.grid(row=1, column=1, pady=5)

        ttk.Label(self, text="Service rate (μ):").grid(row=2, column=0, sticky="e", pady=5)
        self.e_mu = ttk.Entry(self); self.e_mu.grid(row=2, column=1, pady=5)

        ttk.Button(self, text="Calculate", command=self.calculate).grid(row=3, column=0, columnspan=2, pady=15)

        self.txt = tk.Text(self, width=50, height=8, state="disabled", wrap="word")
        self.txt.grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(self, text="Back to Menu", command=lambda: controller.show_frame("MainMenu")).grid(row=5, column=0, columnspan=2)

    def calculate(self):
        try:
            lam = float(self.e_lambda.get())
            mu  = float(self.e_mu.get())
            res = mm1(lam, mu)
            self._show_results(res)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _show_results(self, res):
        self.txt.config(state="normal")
        self.txt.delete("1.0", tk.END)
        for k, v in res.items():
            self.txt.insert(tk.END, f"{k}: {v:.4f}\n")
        self.txt.config(state="disabled")

class MMSFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        self.ctrl = controller
        ttk.Label(self, text="M/M/S Model", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self, text="Arrival rate (λ):").grid(row=1, column=0, sticky="e", pady=5)
        self.e_lambda = ttk.Entry(self); self.e_lambda.grid(row=1, column=1, pady=5)

        ttk.Label(self, text="Service rate (μ):").grid(row=2, column=0, sticky="e", pady=5)
        self.e_mu = ttk.Entry(self); self.e_mu.grid(row=2, column=1, pady=5)

        ttk.Label(self, text="Servers (S):").grid(row=3, column=0, sticky="e", pady=5)
        self.e_s = ttk.Entry(self); self.e_s.grid(row=3, column=1, pady=5)

        ttk.Button(self, text="Calculate", command=self.calculate).grid(row=4, column=0, columnspan=2, pady=15)

        self.txt = tk.Text(self, width=50, height=10, state="disabled", wrap="word")
        self.txt.grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Button(self, text="Back to Menu", command=lambda: controller.show_frame("MainMenu")).grid(row=6, column=0, columnspan=2)

    def calculate(self):
        try:
            lam = float(self.e_lambda.get())
            mu  = float(self.e_mu.get())
            s   = int(self.e_s.get())
            res = mms(lam, mu, s)
            self._show_results(res)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _show_results(self, res):
        self.txt.config(state="normal")
        self.txt.delete("1.0", tk.END)
        for k, v in res.items():
            self.txt.insert(tk.END, f"{k}: {v:.4f}\n")
        self.txt.config(state="disabled")
