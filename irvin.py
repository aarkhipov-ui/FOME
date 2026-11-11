# Проводимость и кривая Ирвина: сопротивление от концентрации доноров.

import math
from constants import E_CHARGE
from materials import MATERIALS
from equilibrium import solve
from mobility import mobility_n, mobility_p


def calculate_point(key, T, Nd0, Ed, Na0=0.0, Ea=0.045):
    # одна точка: key - "Si", "Ge" или "GaAs"; T в К; Nd0, Na0 в см^-3; Ed, Ea в эВ
    r = solve(MATERIALS[key], T, Nd0, Ed, Na0, Ea)
    mu_n = mobility_n(key, T, r["Nd_plus"], r["Na_minus"])
    mu_p = mobility_p(key, T, r["Nd_plus"], r["Na_minus"])
    sigma = E_CHARGE * (r["n"] * mu_n + r["p"] * mu_p)   # 1/(Ом*см)
    r["mu_n"] = mu_n
    r["mu_p"] = mu_p
    r["sigma"] = sigma
    r["rho"] = 1 / sigma                                  # Ом*см
    return r


def irvin_curve(key, T, Ed, Nd_min=1e10, Nd_max=1e20, points=201, Na0=0.0, Ea=0.045):
    # кривая Ирвина: возвращает словарь списков одинаковой длины
    if Nd_min <= 0 or Nd_max <= Nd_min:
        raise ValueError("Нужно 0 < Nd_min < Nd_max.")
    if points < 2:
        raise ValueError("Число точек должно быть не меньше 2.")

    curve = {"Nd0": [], "mu": [], "n": [], "p": [], "Nd_plus": [],
             "mu_n": [], "mu_p": [], "sigma": [], "rho": []}

    log_min = math.log10(Nd_min)
    log_step = (math.log10(Nd_max) - log_min) / (points - 1)
    for i in range(points):
        Nd0 = 10 ** (log_min + i * log_step)
        r = calculate_point(key, T, Nd0, Ed, Na0, Ea)
        curve["Nd0"].append(Nd0)
        curve["mu"].append(r["mu"])
        curve["n"].append(r["n"])
        curve["p"].append(r["p"])
        curve["Nd_plus"].append(r["Nd_plus"])
        curve["mu_n"].append(r["mu_n"])
        curve["mu_p"].append(r["mu_p"])
        curve["sigma"].append(r["sigma"])
        curve["rho"].append(r["rho"])
    return curve


def mobility_curve(key, Nd0, Ed, T_min=100, T_max=500, points=81, Na0=0.0, Ea=0.045):
    # подвижность от температуры при заданной Nd0: возвращает словарь списков
    if T_min <= 0 or T_max <= T_min:
        raise ValueError("Нужно 0 < T_min < T_max.")
    if points < 2:
        raise ValueError("Число точек должно быть не меньше 2.")

    curve = {"T": [], "mu_n": [], "mu_p": [], "n": [], "sigma": [], "rho": []}
    T_step = (T_max - T_min) / (points - 1)
    for i in range(points):
        T = T_min + i * T_step
        r = calculate_point(key, T, Nd0, Ed, Na0, Ea)
        curve["T"].append(T)
        curve["mu_n"].append(r["mu_n"])
        curve["mu_p"].append(r["mu_p"])
        curve["n"].append(r["n"])
        curve["sigma"].append(r["sigma"])
        curve["rho"].append(r["rho"])
    return curve