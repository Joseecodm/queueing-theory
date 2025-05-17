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

    # Check system stability: λ must be less than μ (ρ < 1)
    if lambda_ >= mu:
        raise ValueError("λ must be less than μ for a stable system (ρ<1).")

    # System utilization (ρ)
    rho = lambda_ / mu
    # Probability of zero customers in the system (P0)
    P0  = 1 - rho
    # Average number of customers in the system (Ls)
    Ls  = lambda_ / (mu - lambda_)
    # Average time a customer spends in the system (Ws)
    Ws  = 1.0  / (mu - lambda_)
    # Average number of customers in the queue (Lq)
    Lq  = lambda_**2 / (mu * (mu - lambda_))
    # Average time a customer spends waiting in the queue (Wq)
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