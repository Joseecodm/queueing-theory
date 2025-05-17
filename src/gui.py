import tkinter as tk
from tkinter import ttk, messagebox
from models import mm1, mms

class QueueApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Queueing Theory Calculator")
        self.geometry("800x600")
        self.minsize(600, 400)
        self._build_frames()
        self.show_frame("MainMenu")

    def _build_frames(self):
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MainMenu, MM1Frame, MMSFrame, ConverterFrame):
            page = F(self.container, self)
            self.frames[F.__name__] = page
            page.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, name):
        self.frames[name].tkraise()

class MainMenu(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        content = ttk.Frame(self)
        content.grid(row=0, column=0)

        title = ttk.Label(content, text="Queueing Theory Calculator",
                          font=("Segoe UI", 24, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 30))

        models_frame = ttk.Labelframe(content, text="Models", padding=15)
        models_frame.grid(row=1, column=0, padx=20)
        btn_mm1 = ttk.Button(models_frame, text="M/M/1", width=20,
                             command=lambda: controller.show_frame("MM1Frame"))
        btn_mm1.grid(row=0, column=0, pady=(0,10), ipadx=10, ipady=10)
        btn_mms = ttk.Button(models_frame, text="M/M/S", width=20,
                             command=lambda: controller.show_frame("MMSFrame"))
        btn_mms.grid(row=1, column=0, pady=(0,10), ipadx=10, ipady=10)

        util_frame = ttk.Frame(content)
        util_frame.grid(row=1, column=1, padx=20)
        btn_about = ttk.Button(util_frame, text="About", width=20,
                               command=self._show_about)
        btn_about.grid(row=0, column=0, pady=(0,10), ipadx=10, ipady=10)
        btn_exit = ttk.Button(util_frame, text="Exit", width=20,
                              command=controller.destroy)
        btn_exit.grid(row=1, column=0, pady=(0,10), ipadx=10, ipady=10)
        btn_conv = ttk.Button(util_frame, text="Converter", width=20,
                              command=lambda: controller.show_frame("ConverterFrame"))
        btn_conv.grid(row=2, column=0, ipadx=10, ipady=10)

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
        for i in range(2): self.grid_columnconfigure(i, weight=1)

        ttk.Label(self, text="M/M/1 Model", font=("Segoe UI", 18, "bold")) \
            .grid(row=0, column=0, columnspan=2, pady=(0,20))

        ttk.Label(self, text="Arrival rate (λ):").grid(row=1, column=0, sticky="e", pady=5)
        self.e_lambda = ttk.Entry(self)
        self.e_lambda.grid(row=1, column=1, sticky="w", pady=5)

        ttk.Label(self, text="Service rate (μ):").grid(row=2, column=0, sticky="e", pady=5)
        self.e_mu = ttk.Entry(self)
        self.e_mu.grid(row=2, column=1, sticky="w", pady=5)

        ttk.Label(self, text="n (for Pₙ):").grid(row=3, column=0, sticky="e", pady=5)
        self.e_n = ttk.Entry(self)
        self.e_n.grid(row=3, column=1, sticky="w", pady=5)

        calc = ttk.Button(self, text="Calculate", command=self.calculate)
        calc.grid(row=4, column=0, columnspan=2, pady=20, ipadx=20, ipady=10)

        self.txt = tk.Text(self, width=60, height=10, state="disabled", wrap="word")
        self.txt.grid(row=5, column=0, columnspan=2, pady=10)

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
        for i in range(2): self.grid_columnconfigure(i, weight=1)

        ttk.Label(self, text="M/M/S Model", font=("Segoe UI", 18, "bold")) \
            .grid(row=0, column=0, columnspan=2, pady=(0,20))

        ttk.Label(self, text="Arrival rate (λ):").grid(row=1, column=0, sticky="e", pady=5)
        self.e_lambda = ttk.Entry(self)
        self.e_lambda.grid(row=1, column=1, sticky="w", pady=5)

        ttk.Label(self, text="Service rate (μ):").grid(row=2, column=0, sticky="e", pady=5)
        self.e_mu = ttk.Entry(self)
        self.e_mu.grid(row=2, column=1, sticky="w", pady=5)

        ttk.Label(self, text="Servers (S):").grid(row=3, column=0, sticky="e", pady=5)
        self.e_s = ttk.Entry(self)
        self.e_s.grid(row=3, column=1, sticky="w", pady=5)

        calc = ttk.Button(self, text="Calculate", command=self.calculate)
        calc.grid(row=4, column=0, columnspan=2, pady=20, ipadx=20, ipady=10)

        self.txt = tk.Text(self, width=60, height=10, state="disabled", wrap="word")
        self.txt.grid(row=5, column=0, columnspan=2, pady=10)

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
class ConverterFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=30)
        self.controller = controller

        # Configuramos 2 columnas con igual peso para centrar
        for col in range(2):
            self.columnconfigure(col, weight=1)

        # Título
        ttk.Label(self, text="Rate Converter",
                  font=("Segoe UI", 24, "bold")) \
            .grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Entrada: clientes por minuto
        ttk.Label(self, text="Clients / minute:") \
            .grid(row=1, column=0, sticky="e", padx=(0,10), pady=5)
        self.e_rate_min = ttk.Entry(self, width=20)
        self.e_rate_min.grid(row=1, column=1, sticky="w", pady=5)
        
        # Entrada: clientes por hora
        ttk.Label(self, text="Clients / hour:") \
            .grid(row=2, column=0, sticky="e", padx=(0,10), pady=5)
        self.e_rate_hr = ttk.Entry(self, width=20)
        self.e_rate_hr.grid(row=2, column=1, sticky="w", pady=5)

        # Botones en una sub‐fila centrada
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        btn_frame.columnconfigure((0,1), weight=1)

        ttk.Button(btn_frame, text="Convert → per hour",
                   command=self.min_to_hour) \
            .grid(row=0, column=0, padx=10, ipadx=10, ipady=5, sticky="ew")
        ttk.Button(btn_frame, text="Convert → per minute",
                   command=self.hour_to_min) \
            .grid(row=0, column=1, padx=10, ipadx=10, ipady=5, sticky="ew")

        # Label de resultado centralizado
        self.lbl_result = ttk.Label(self, text="", font=("Segoe UI", 14))
        self.lbl_result.grid(row=4, column=0, columnspan=2, pady=10)

        # Separador
        ttk.Separator(self, orient="horizontal") \
            .grid(row=5, column=0, columnspan=2, sticky="ew", pady=15)

        # Botón volver
        ttk.Button(self, text="Back to Menu",
                   command=lambda: controller.show_frame("MainMenu")) \
            .grid(row=6, column=0, columnspan=2, pady=10, ipadx=20, ipady=10)

    def min_to_hour(self):
        try:
            rate_min = float(self.e_rate_min.get())
            rate_hr = rate_min * 60.0
            self.e_rate_hr.delete(0, tk.END)
            self.e_rate_hr.insert(0, f"{rate_hr:.4f}")
            self.lbl_result.config(text="")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number for clients per minute")

    def hour_to_min(self):
        try:
            rate_hr = float(self.e_rate_hr.get())
            rate_min = rate_hr / 60.0
            self.e_rate_min.delete(0, tk.END)
            self.e_rate_min.insert(0, f"{rate_min:.4f}")
            self.lbl_result.config(text="")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number for clients per hour")
