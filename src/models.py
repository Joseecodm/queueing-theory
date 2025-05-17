import math

# models.py
# Simplified M/M/1 and M/M/S queueing models without unit conversion

# By: José Manuel Cortes Cerón - TI Student - ITSOEH

def mm1(lambda_, mu, n=None):
    """
    Calculates metrics for the M/M/1 queueing model:
      rho = λ/μ
      P0  = 1 − rho
      Ls  = λ/(μ − λ)
      Ws  = 1/(μ − λ)
      Lq  = λ² / [μ(μ − λ)]
      Wq  = λ / [μ(μ − λ)]
      Pn  = (1 − rho)·rho^n  (if n is provided)

    Args:
      lambda_ (float): arrival rate λ (clients per hour)
      mu      (float): service rate μ (clients per hour)
      n       (int, optional): for Pn calculation

    Returns:
      dict with keys 'rho', 'P0', 'Ls', 'Ws', 'Lq', 'Wq', and 'Pn' if n provided.
    """
    # Stability check
    if lambda_ >= mu:
        raise ValueError("Unstable system: arrival rate (λ) must be less than service rate (μ).")

    rho = lambda_ / mu
    P0  = 1 - rho
    Ls  = lambda_ / (mu - lambda_)
    Ws  = 1.0 / (mu - lambda_)
    Lq  = lambda_**2 / (mu * (mu - lambda_))
    Wq  = lambda_ / (mu * (mu - lambda_))

    results = {
        'rho': rho,
        'P0' : P0,
        'Ls' : Ls,
        'Ws' : Ws,
        'Lq' : Lq,
        'Wq' : Wq,
    }

    if n is not None:
        if not isinstance(n, int) or n < 0:
            raise ValueError("n must be a non-negative integer.")
        results['Pn'] = (1 - rho) * (rho**n)

    return results


def mms(lambda_, mu, s):
    """
    Calculates metrics for the M/M/S queueing model:
      rho = λ/(s·μ)
      P0  = [∑_{n=0}^{s-1}(λ/μ)^n/n! + (λ/μ)^s/(s!·(1−rho))]⁻¹
      Lq  = [(λ/μ)^s·rho] / [s!·(1−rho)^2] · P0
      Ls  = Lq + λ/μ
      Wq  = Lq / λ
      Ws  = Wq + 1/μ

    Args:
      lambda_ (float): arrival rate λ (clients per hour)
      mu      (float): service rate μ (clients per hour)
      s       (int):   number of servers

    Returns:
      dict with keys 'rho', 'P0', 'Lq', 'Ls', 'Wq', 'Ws'.
    """
    if lambda_ <= 0 or mu <= 0:
        raise ValueError("Arrival and service rates must be positive.")
    if not isinstance(s, int) or s < 1:
        raise ValueError("Number of servers (s) must be a positive integer.")

    rho = lambda_ / (s * mu)
    if rho >= 1:
        raise ValueError("Unstable system: load (λ/(s·μ)) must be less than 1.")

    a = lambda_ / mu
    sum_terms = sum((a**n) / math.factorial(n) for n in range(s))
    last_term = (a**s) / (math.factorial(s) * (1 - rho))
    P0 = 1.0 / (sum_terms + last_term)

    Lq = ((a**s) * rho) / (math.factorial(s) * (1 - rho)**2) * P0
    Ls = Lq + a
    Wq = Lq / lambda_
    Ws = Wq + 1.0 / mu

    return {
        'rho': rho,
        'P0' : P0,
        'Lq' : Lq,
        'Ls' : Ls,
        'Wq' : Wq,
        'Ws' : Ws,
    }
