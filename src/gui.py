feature/add-user-interface
import tkinter as tk
from tkinter import ttk, messagebox
from models import mm1, mms

class QueueApp(tk.Tk):
    """
    Main application class for the Queueing Theory Calculator.
    Sets up the main window and manages navigation between frames.
    """
    def __init__(self):
        super().__init__()
        self.title("Queueing Theory Calculator")
        self.geometry("600x600")
        self.minsize(600, 400)
        self._build_frames()
        self.show_frame("MainMenu")

    def _build_frames(self):
        """
        Create and store all frames (pages) used in the application.
        """
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
        """
        Bring the frame with the given name to the front.
        """
        self.frames[name].tkraise()

class MainMenu(ttk.Frame):
    """
    Main menu frame. Allows navigation to the different models and utilities.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        content = ttk.Frame(self)
        content.grid(row=0, column=0)

        # Application title
        title = ttk.Label(content, text="Queueing Theory Calculator",
                          font=("Segoe UI", 24, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 30))

        # Model selection frame
        models_frame = ttk.Labelframe(content, text="Models", padding=15)
        models_frame.grid(row=1, column=0, padx=20)
        btn_mm1 = ttk.Button(models_frame, text="M/M/1", width=20,
                             command=lambda: controller.show_frame("MM1Frame"))
        btn_mm1.grid(row=0, column=0, pady=(0,10), ipadx=10, ipady=10)
        btn_mms = ttk.Button(models_frame, text="M/M/S", width=20,
                             command=lambda: controller.show_frame("MMSFrame"))
        btn_mms.grid(row=1, column=0, pady=(0,10), ipadx=10, ipady=10)

        # Utility buttons frame
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
        """
        Show an About dialog with application information.
        """
        message = (
            "Queueing Theory Calculator\n"
            "Models: M/M/1 & M/M/S\n"
            "Author: José Manuel Cortes Cerón\n"
            "2025"
        )
        messagebox.showinfo("About", message)

class MM1Frame(ttk.Frame):
    """
    Frame for the M/M/1 queueing model.
    Allows the user to input parameters and displays results.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        self.ctrl = controller
        for i in range(2): self.grid_columnconfigure(i, weight=1)

        # Title
        ttk.Label(self, text="M/M/1 Model", font=("Segoe UI", 18, "bold")) \
            .grid(row=0, column=0, columnspan=2, pady=(0,20))

        # Input fields for lambda, mu, and n
        ttk.Label(self, text="Arrival rate (λ):").grid(row=1, column=0, sticky="e", pady=5)
        self.e_lambda = ttk.Entry(self)
        self.e_lambda.grid(row=1, column=1, sticky="w", pady=5)

        ttk.Label(self, text="Service rate (μ):").grid(row=2, column=0, sticky="e", pady=5)
        self.e_mu = ttk.Entry(self)
        self.e_mu.grid(row=2, column=1, sticky="w", pady=5)

        ttk.Label(self, text="n (for Pₙ):").grid(row=3, column=0, sticky="e", pady=5)
        self.e_n = ttk.Entry(self)
        self.e_n.grid(row=3, column=1, sticky="w", pady=5)

        # Calculate button
        calc = ttk.Button(self, text="Calculate", command=self.calculate)
        calc.grid(row=4, column=0, columnspan=2, pady=20, ipadx=20, ipady=10)

        # Results display
        self.txt = tk.Text(self, width=60, height=10, state="disabled", wrap="word")
        self.txt.grid(row=5, column=0, columnspan=2, pady=10)

        # Back to menu button
        back = ttk.Button(self, text="Back to Menu",
                          command=lambda: controller.show_frame("MainMenu"))
        back.grid(row=6, column=0, columnspan=2, pady=10, ipadx=20, ipady=10)

    def calculate(self):
        """
        Reads user input, performs M/M/1 calculations, and displays results.
        """
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
        """
        Formats and displays the results in the text widget.
        """
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
    """
    Frame for the M/M/S queueing model.
    Allows the user to input parameters and displays results.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        self.ctrl = controller
        for i in range(2): self.grid_columnconfigure(i, weight=1)

        # Title
        ttk.Label(self, text="M/M/S Model", font=("Segoe UI", 18, "bold")) \
            .grid(row=0, column=0, columnspan=2, pady=(0,20))

        # Input fields for lambda, mu, and s
        ttk.Label(self, text="Arrival rate (λ):").grid(row=1, column=0, sticky="e", pady=5)
        self.e_lambda = ttk.Entry(self)
        self.e_lambda.grid(row=1, column=1, sticky="w", pady=5)

        ttk.Label(self, text="Service rate (μ):").grid(row=2, column=0, sticky="e", pady=5)
        self.e_mu = ttk.Entry(self)
        self.e_mu.grid(row=2, column=1, sticky="w", pady=5)

        ttk.Label(self, text="Servers (S):").grid(row=3, column=0, sticky="e", pady=5)
        self.e_s = ttk.Entry(self)
        self.e_s.grid(row=3, column=1, sticky="w", pady=5)

        # Calculate button
        calc = ttk.Button(self, text="Calculate", command=self.calculate)
        calc.grid(row=4, column=0, columnspan=2, pady=20, ipadx=20, ipady=10)

        # Results display
        self.txt = tk.Text(self, width=60, height=10, state="disabled", wrap="word")
        self.txt.grid(row=5, column=0, columnspan=2, pady=10)

        # Back to menu button
        back = ttk.Button(self, text="Back to Menu",
                          command=lambda: controller.show_frame("MainMenu"))
        back.grid(row=6, column=0, columnspan=2, pady=10, ipadx=20, ipady=10)

    def calculate(self):
        """
        Reads user input, performs M/M/S calculations, and displays results.
        """
        try:
            lam = float(self.e_lambda.get())
            mu  = float(self.e_mu.get())
            s   = int(self.e_s.get())
            res = mms(lam, mu, s)
            self._show_results(res)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _show_results(self, res):
        """
        Formats and displays the results in the text widget.
        """
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
    """
    Frame for converting rates between clients per minute and clients per hour.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, padding=30)
        self.controller = controller

        # Configure two columns for centering widgets
        for col in range(2):
            self.columnconfigure(col, weight=1)

        # Title
        ttk.Label(self, text="Rate Converter",
                  font=("Segoe UI", 24, "bold")) \
            .grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Input for clients per minute
        ttk.Label(self, text="Clients / minute:") \
            .grid(row=1, column=0, sticky="e", padx=(0,10), pady=5)
        self.e_rate_min = ttk.Entry(self, width=20)
        self.e_rate_min.grid(row=1, column=1, sticky="w", pady=5)
        
        # Input for clients per hour
        ttk.Label(self, text="Clients / hour:") \
            .grid(row=2, column=0, sticky="e", padx=(0,10), pady=5)
        self.e_rate_hr = ttk.Entry(self, width=20)
        self.e_rate_hr.grid(row=2, column=1, sticky="w", pady=5)

        # Buttons for conversion
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        btn_frame.columnconfigure((0,1), weight=1)

        ttk.Button(btn_frame, text="Convert → per hour",
                   command=self.min_to_hour) \
            .grid(row=0, column=0, padx=10, ipadx=10, ipady=5, sticky="ew")
        ttk.Button(btn_frame, text="Convert → per minute",
                   command=self.hour_to_min) \
            .grid(row=0, column=1, padx=10, ipadx=10, ipady=5, sticky="ew")

        # Result label
        self.lbl_result = ttk.Label(self, text="", font=("Segoe UI", 14))
        self.lbl_result.grid(row=4, column=0, columnspan=2, pady=10)

        # Separator
        ttk.Separator(self, orient="horizontal") \
            .grid(row=5, column=0, columnspan=2, sticky="ew", pady=15)

        # Back to menu button
        ttk.Button(self, text="Back to Menu",
                   command=lambda: controller.show_frame("MainMenu")) \
            .grid(row=6, column=0, columnspan=2, pady=10, ipadx=20, ipady=10)

    def min_to_hour(self):
        """
        Converts the rate from clients per minute to clients per hour.
        """
        try:
            rate_min = float(self.e_rate_min.get())
            rate_hr = rate_min * 60.0
            self.e_rate_hr.delete(0, tk.END)
            self.e_rate_hr.insert(0, f"{rate_hr:.4f}")
            self.lbl_result.config(text="")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number for clients per minute")

    def hour_to_min(self):
        """
        Converts the rate from clients per hour to clients per minute.
        """
        try:
            rate_hr = float(self.e_rate_hr.get())
            rate_min = rate_hr / 60.0
            self.e_rate_min.delete(0, tk.END)
            self.e_rate_min.insert(0, f"{rate_min:.4f}")
            self.lbl_result.config(text="")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number for clients per hour")
=======
import math

def mm1(lambda_, mu, n=None):
    """
    Calculates the metrics for the M/M/1 queueing model:
      ρ    = λ/μ
      P0   = 1 − ρ
      Ls   = λ/(μ − λ)
      Ws   = 1/(μ − λ)
      Lq   = λ²/[μ(μ − λ)]
      Wq   = λ/[μ(μ − λ)]
      Pn   = (1 − ρ) ρ^n  (if n is not None)
    Args:
      lambda_ (float): arrival rate λ
      mu      (float): service rate μ
      n       (int, optional): number of customers for Pn
    Returns:
      dict with keys 'rho','P0','Ls','Ws','Lq','Wq' and, if n is given, 'Pn'.
    """

    # Check if the system is stable: λ must be less than μ (ρ < 1)
    if lambda_ >= mu:
        raise ValueError("λ must be less than μ for a stable system (ρ<1).")

    # Calculate system utilization (ρ)
    rho = lambda_ / mu
    # Calculate the probability of zero customers in the system (P0)
    P0  = 1 - rho
    # Calculate the average number of customers in the system (Ls)
    Ls  = lambda_ / (mu - lambda_)
    # Calculate the average time a customer spends in the system (Ws)
    Ws  = 1.0  / (mu - lambda_)
    # Calculate the average number of customers in the queue (Lq)
    Lq  = lambda_**2 / (mu * (mu - lambda_))
    # Calculate the average time a customer spends waiting in the queue (Wq)
    Wq  = lambda_      / (mu * (mu - lambda_))

    # Store results in a dictionary
    resultados = {
        'rho': rho,
        'P0':  P0,
        'Ls':  Ls,
        'Ws':  Ws,
        'Lq':  Lq,
        'Wq':  Wq,
    }

    # If requested, calculate the probability of having exactly n customers in the system (Pn)
    if n is not None:
        if n < 0 or not isinstance(n, int):
            raise ValueError("n must be an integer ≥ 0")
        Pn = (1 - rho) * (rho**n)
        resultados['Pn'] = Pn

    return resultados

def mms(lambda_, mu, s):
    """
    Calculates the metrics for the M/M/S queueing model:
      ρ   = λ / (s·μ)
      P0  = [ ∑_{n=0}^{s-1} (λ/μ)^n / n!  +  (λ/μ)^s / (s!·(1−ρ)) ]⁻¹
      Lq  = ( (λ/μ)^s · ρ ) / ( s!·(1−ρ)^2 ) · P0
      Ls  = Lq + λ/μ
      Wq  = Lq / λ
      Ws  = Wq + 1/μ

    Args:
      lambda_ (float): arrival rate λ
      mu      (float): service rate per server μ
      s       (int):   number of servers

    Returns:
      dict with keys 'rho','P0','Lq','Ls','Wq','Ws'
    """

    # Basic validation for input parameters
    if lambda_ <= 0 or mu <= 0:
        raise ValueError("λ and μ must be greater than 0.")
    if not isinstance(s, int) or s < 1:
        raise ValueError("s must be a positive integer (number of servers).")

    # Calculate system utilization (ρ)
    rho = lambda_ / (s * mu)
    if rho >= 1:
        raise ValueError("Unstable system: λ/(s·μ) must be < 1.")

    # a is the traffic intensity (λ/μ)
    a = lambda_ / mu

    # Calculate P0: probability that there are zero customers in the system
    sum_terms = sum((a**n) / math.factorial(n) for n in range(s))
    last_term = (a**s) / (math.factorial(s) * (1 - rho))
    P0 = 1.0 / (sum_terms + last_term)

    # Calculate queue and system metrics
    # Lq: average number of customers in the queue
    Lq = ((a**s) * rho) / (math.factorial(s) * (1 - rho)**2) * P0
    # Ls: average number of customers in the system
    Ls = Lq + a
    # Wq: average waiting time in the queue
    Wq = Lq / lambda_
    # Ws: average time a customer spends in the system
    Ws = Wq + 1.0 / mu

    # Return results as a dictionary
    return {
        'rho': rho,
        'P0':  P0,
        'Lq':  Lq,
        'Ls':  Ls,
        'Wq':  Wq,
        'Ws':  Ws,
    }
main
