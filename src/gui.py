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