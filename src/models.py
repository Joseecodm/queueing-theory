import math

# This module contains functions to calculate metrics for M/M/1 and M/M/S queueing models.
# Supports optional unit conversion between per-minute and per-hour rates.

# By: José Manuel Cortes Cerón - TI Student - ITSOEH

def mm1(lambda_, mu, n=None, lam_in_minutes=False, mu_in_minutes=False):
    """
    Calculates the metrics for the M/M/1 queueing model with optional unit conversion.

    If lam_in_minutes=True, lambda_ is interpreted as arrivals per minute and converted to per hour.
    If mu_in_minutes=True, mu is interpreted as services per minute and converted to per hour.

    Metrics:
      rho = λ/μ
      P0  = 1 − rho
      Ls  = λ/(μ − λ)
      Ws  = 1/(μ − λ)
      Lq  = λ² / [μ(μ − λ)]
      Wq  = λ / [μ(μ − λ)]
      Pn  = (1 − rho)·rho^n  (if n is not None)

    Args:
      lambda_ (float): arrival rate (per hour or per minute)
      mu      (float): service rate (per hour or per minute)
      n       (int, optional): number of customers for Pn
      lam_in_minutes (bool): if True, convert lambda_ from per-minute to per-hour
      mu_in_minutes  (bool): if True, convert mu from per-minute to per-hour

    Returns:
      dict with keys 'rho', 'P0', 'Ls', 'Ws', 'Lq', 'Wq' and, if n given, 'Pn'.
    """
    # Convert units if specified
    if lam_in_minutes:
        lambda_ = lambda_ * 60.0
    if mu_in_minutes:
        mu = mu * 60.0

    # Check stability: lambda_ < mu
    if lambda_ >= mu:
        raise ValueError("λ must be less than μ for a stable system (ρ<1).")

    rho = lambda_ / mu
    P0  = 1 - rho
    Ls  = lambda_ / (mu - lambda_)
    Ws  = 1.0 / (mu - lambda_)
    Lq  = lambda_**2 / (mu * (mu - lambda_))
    Wq  = lambda_ / (mu * (mu - lambda_))

    results = {
        'rho': rho,
        'P0':  P0,
        'Ls':  Ls,
        'Ws':  Ws,
        'Lq':  Lq,
        'Wq':  Wq,
    }

    if n is not None:
        if not isinstance(n, int) or n < 0:
            raise ValueError("n must be a non-negative integer.")
        Pn = (1 - rho) * (rho**n)
        results['Pn'] = Pn

    return results


def mms(lambda_, mu, s, lam_in_minutes=False, mu_in_minutes=False):
    """
    Calculates the metrics for the M/M/S queueing model with optional unit conversion.

    If lam_in_minutes=True, lambda_ is interpreted as arrivals per minute and converted to per hour.
    If mu_in_minutes=True, mu is interpreted as services per minute and converted to per hour.

    Metrics:
      rho = λ/(s·μ)
      P0  = [ ∑_{n=0}^{s-1} (λ/μ)^n/n!  +  (λ/μ)^s/(s!·(1−ρ)) ]⁻¹
      Lq  = ( (λ/μ)^s·ρ ) / [s!·(1−ρ)^2] · P0
      Ls  = Lq + λ/μ
      Wq  = Lq / λ
      Ws  = Wq + 1/μ

    Args:
      lambda_ (float): arrival rate (per hour or per minute)
      mu      (float): service rate per server (per hour or per minute)
      s       (int):   number of servers
      lam_in_minutes (bool): if True, convert lambda_ from per-minute to per-hour
      mu_in_minutes  (bool): if True, convert mu from per-minute to per-hour

    Returns:
      dict with keys 'rho', 'P0', 'Lq', 'Ls', 'Wq', 'Ws'.
    """
    # Convert units if specified
    if lam_in_minutes:
        lambda_ = lambda_ * 60.0
    if mu_in_minutes:
        mu = mu * 60.0

    if lambda_ <= 0 or mu <= 0:
        raise ValueError("λ and μ must be greater than 0.")
    if not isinstance(s, int) or s < 1:
        raise ValueError("s must be a positive integer (number of servers).")

    rho = lambda_ / (s * mu)
    if rho >= 1:
        raise ValueError("Unstable system: λ/(s·μ) must be < 1.")

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
        'P0':  P0,
        'Lq':  Lq,
        'Ls':  Ls,
        'Wq':  Wq,
        'Ws':  Ws,
    }
