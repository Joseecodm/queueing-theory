import math
import pytest
from models import mm1, mms

def test_mm1_core_metrics():
    # Parámetros básicos: λ=0.75, μ=1.0
    lam, mu = 0.75, 1.0
    res = mm1(lam, mu)
    assert pytest.approx(0.75, rel=1e-3) == res['rho']
    assert pytest.approx(0.25, rel=1e-3) == res['P0']
    assert pytest.approx(3.0, rel=1e-3)  == res['Ls']
    assert pytest.approx(4.0, rel=1e-3)  == res['Ws']
    assert pytest.approx(2.25, rel=1e-3) == res['Lq']
    assert pytest.approx(3.0, rel=1e-3)  == res['Wq']

def test_mm1_Pn():
    # Probabilidad Pn para n=2
    lam, mu, n = 0.75, 1.0, 2
    res = mm1(lam, mu, n=n)
    expected = (1 - lam/mu) * (lam/mu)**n
    assert 'Pn' in res
    assert pytest.approx(expected, rel=1e-4) == res['Pn']

def test_car_wash_basic_metrics():
    # Lava carros: λ=9/h, μ=1 car/5min = 12/h
    lam, mu = 9.0, 12.0
    res = mm1(lam, mu)
    assert pytest.approx(0.75, rel=1e-3) == res['rho']
    assert pytest.approx(0.25, rel=1e-3) == res['P0']
    assert pytest.approx(3.0, rel=1e-3)  == res['Ls']
    assert pytest.approx(1/3, rel=1e-3)  == res['Ws']
    assert pytest.approx(2.25, rel=1e-3) == res['Lq']
    assert pytest.approx(0.25, rel=1e-3) == res['Wq']

def test_car_wash_probabilities():
    lam, mu = 9.0, 12.0
    res = mm1(lam, mu)
    rho = res['rho']
    delta = mu - lam  # 3
    # P(cola > 3) = rho^4
    assert pytest.approx(rho**4, rel=1e-4) == rho**4
    # P(Wq > 0.5h) = exp(-delta * 0.5)
    expected_wait_q = math.exp(-delta * 0.5)
    assert pytest.approx(expected_wait_q, rel=1e-4) == expected_wait_q

def test_mms_core_metrics():
    # Caso M/M/2: λ=2/h, μ=3/h, s=2
    lam, mu, s = 2.0, 3.0, 2
    res = mms(lam, mu, s)
    assert pytest.approx(2/(2*3), rel=1e-4) == res['rho']
    assert pytest.approx(0.5, rel=1e-4) == res['P0']
    assert pytest.approx(0.08333, rel=1e-3) == res['Lq']
    assert pytest.approx(0.75, rel=1e-3)    == res['Ls']
    assert pytest.approx(0.04167, rel=1e-3) == res['Wq']
    assert pytest.approx(0.375, rel=1e-3)   == res['Ws']
