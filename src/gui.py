import tkinter as tk
from tkinter import ttk, messagebox
from models import mm1, mms

class QueueApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Queueing Theory Calculator")
        self.geometry("600x600")
        self.minsize(600, 400)
        self._build_frames()
        self.show_frame("MainMenu")

    def _build_frames(self):
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        # Configure grid so child frames center adaptively
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MainMenu, MM1Frame, MMSFrame):
            page = F(self.container, self)
            self.frames[F.__name__] = page
            page.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, name):
        self.frames[name].tkraise()

class MainMenu(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # Center content frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        content = ttk.Frame(self)
        content.grid(row=0, column=0)
        # Title
        title = ttk.Label(content, text="Queueing Theory Calculator",
                          font=("Segoe UI", 24, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 30))
        # Model selection
        models_frame = ttk.Labelframe(content, text="Models", padding=15)
        models_frame.grid(row=1, column=0, padx=20)
        btn_mm1 = ttk.Button(models_frame, text="M/M/1", width=20,
                             command=lambda: controller.show_frame("MM1Frame"))
        btn_mm1.grid(row=0, column=0, pady=(0,10), ipadx=10, ipady=10)
        btn_mms = ttk.Button(models_frame, text="M/M/S", width=20,
                             command=lambda: controller.show_frame("MMSFrame"))
        btn_mms.grid(row=1, column=0, pady=(0,10), ipadx=10, ipady=10)
        # Utilities
        util_frame = ttk.Frame(content)
        util_frame.grid(row=1, column=1, padx=20)
        btn_about = ttk.Button(util_frame, text="About", width=20,
                               command=self._show_about)
        btn_about.grid(row=0, column=0, pady=(0,10), ipadx=10, ipady=10)
        btn_exit = ttk.Button(util_frame, text="Exit", width=20,
                              command=controller.destroy)
        btn_exit.grid(row=1, column=0, ipadx=10, ipady=10)

    def _show_about(self):
        message = (
            "Queueing Theory Calculator\n"
            "Models: M/M/1 & M/M/S\n"
            "Author: José Manuel Cortes Cerón\n"
            "2025"
        )
        messagebox.showinfo("About", message)

class MM1Frame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        self.ctrl = controller

        # Columnas adaptativas
        for i in range(2):
            self.grid_columnconfigure(i, weight=1)

        # Título
        ttk.Label(self, text="M/M/1 Model", font=("Segoe UI", 18, "bold")) \
            .grid(row=0, column=0, columnspan=2, pady=(0,20))

        # Parámetros λ y μ
        ttk.Label(self, text="Arrival rate (λ):").grid(row=1, column=0, sticky="e", pady=5)
        self.e_lambda = ttk.Entry(self)
        self.e_lambda.grid(row=1, column=1, sticky="w", pady=5)

        ttk.Label(self, text="Service rate (μ):").grid(row=2, column=0, sticky="e", pady=5)
        self.e_mu = ttk.Entry(self)
        self.e_mu.grid(row=2, column=1, sticky="w", pady=5)

        # Parámetro n para Pn
        ttk.Label(self, text="n (for Pₙ):").grid(row=3, column=0, sticky="e", pady=5)
        self.e_n = ttk.Entry(self)
        self.e_n.grid(row=3, column=1, sticky="w", pady=5)

        # Botón Calculate
        calc = ttk.Button(self, text="Calculate", command=self.calculate)
        calc.grid(row=4, column=0, columnspan=2, pady=20, ipadx=20, ipady=10)

        # Área de resultados
        self.txt = tk.Text(self, width=60, height=10, state="disabled", wrap="word")
        self.txt.grid(row=5, column=0, columnspan=2, pady=10)

        # Botón Back to Menu
        back = ttk.Button(self, text="Back to Menu",
                          command=lambda: controller.show_frame("MainMenu"))
        back.grid(row=6, column=0, columnspan=2, pady=10, ipadx=20, ipady=10)

    def calculate(self):
        try:
            lam = float(self.e_lambda.get())
            mu  = float(self.e_mu.get())
            n_txt = self.e_n.get().strip()
            n_val = int(n_txt) if n_txt else None

            res = mm1(lam, mu, n=n_val)
            self._show_results(res, n_val)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _show_results(self, res, n_val):
        mapping = {
            'rho': ("Utilization", 'percent'),
            'P0':  ("Prob. System Empty", 'percent'),
            'Ls':  ("Avg. # in System", 'value'),
            'Ws':  ("Avg. Time in System", 'value'),
            'Lq':  ("Avg. # in Queue", 'value'),
            'Wq':  ("Avg. Waiting Time in Queue", 'value'),
        }
        if n_val is not None:
            mapping['Pn'] = (f"Prob. of exactly {n_val} customers", 'percent')

        self.txt.config(state="normal")
        self.txt.delete("1.0", tk.END)
        for key, (label, kind) in mapping.items():
            val = res.get(key)
            if val is None: continue
            if kind == 'percent':
                self.txt.insert(tk.END, f"{label}: {val*100:.2f}%\n")
            else:
                self.txt.insert(tk.END, f"{label}: {val:.4f}\n")
        self.txt.config(state="disabled")
class MMSFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        self.ctrl = controller

        # Columnas adaptativas
        for i in range(2):
            self.grid_columnconfigure(i, weight=1)

        # Título
        ttk.Label(self, text="M/M/S Model", font=("Segoe UI", 18, "bold")) \
            .grid(row=0, column=0, columnspan=2, pady=(0,20))

        # Parámetros λ, μ y S
        ttk.Label(self, text="Arrival rate (λ):").grid(row=1, column=0, sticky="e", pady=5)
        self.e_lambda = ttk.Entry(self)
        self.e_lambda.grid(row=1, column=1, sticky="w", pady=5)

        ttk.Label(self, text="Service rate (μ):").grid(row=2, column=0, sticky="e", pady=5)
        self.e_mu = ttk.Entry(self)
        self.e_mu.grid(row=2, column=1, sticky="w", pady=5)

        ttk.Label(self, text="Servers (S):").grid(row=3, column=0, sticky="e", pady=5)
        self.e_s = ttk.Entry(self)
        self.e_s.grid(row=3, column=1, sticky="w", pady=5)

        # Botón Calculate
        calc = ttk.Button(self, text="Calculate", command=self.calculate)
        calc.grid(row=4, column=0, columnspan=2, pady=20, ipadx=20, ipady=10)

        # Área de resultados
        self.txt = tk.Text(self, width=60, height=10, state="disabled", wrap="word")
        self.txt.grid(row=5, column=0, columnspan=2, pady=10)

        # Botón Back to Menu
        back = ttk.Button(self, text="Back to Menu",
                          command=lambda: controller.show_frame("MainMenu"))
        back.grid(row=6, column=0, columnspan=2, pady=10, ipadx=20, ipady=10)

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
        # Mapeo de clave -> (texto, tipo)
        mapping = {
            'rho': ("Utilization", 'percent'),
            'P0':  ("Prob. System Empty", 'percent'),
            'Lq':  ("Avg. # in Queue", 'value'),
            'Ls':  ("Avg. # in System", 'value'),
            'Wq':  ("Avg. Waiting Time in Queue", 'value'),
            'Ws':  ("Avg. Time in System", 'value'),
        }

        self.txt.config(state="normal")
        self.txt.delete("1.0", tk.END)
        for key, (label, kind) in mapping.items():
            val = res.get(key)
            if val is None:
                continue
            if kind == 'percent':
                self.txt.insert(tk.END, f"{label}: {val*100:.2f}%\n")
            else:
                self.txt.insert(tk.END, f"{label}: {val:.4f}\n")
        self.txt.config(state="disabled")
