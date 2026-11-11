# Уровень Ферми и концентрации носителей.
# Энергии от потолка валентной зоны; Ed - вниз от дна зоны проводимости.

import math
from constants import K_B, EV, N_PREFACTOR
from materials import band_gap


def safe_exp(x):
    # защита от переполнения
    if x > 700:
        x = 700
    return math.exp(x)


def fermi_function(x):
    # 1 / (1 + exp(x)) без переполнения
    if x > 0:
        return math.exp(-x) / (1 + math.exp(-x))
    else:
        return 1 / (1 + math.exp(x))


def density_of_states(mass, T):
    # Nc или Nv, см^-3
    return N_PREFACTOR * mass ** 1.5 * (T / 300) ** 1.5


def solve(material, T, Nd0, Ed, Na0=0.0, Ea=0.045):
    # T в К, концентрации в см^-3, энергии Ed и Ea в эВ
    Eg_ev = band_gap(material, T)
    if T <= 0:
        raise ValueError("Температура должна быть больше 0 К.")
    if Nd0 < 0 or Na0 < 0:
        raise ValueError("Концентрации примесей не могут быть отрицательными.")
    if Ed <= 0 or Ed >= Eg_ev:
        raise ValueError("Энергия донора Ed должна быть больше 0 и меньше Eg.")
    if Na0 > 0 and (Ea <= 0 or Ea >= Eg_ev):
        raise ValueError("Энергия акцептора Ea должна быть больше 0 и меньше Eg.")

    # перевод в СГС
    kT = K_B * T
    Eg = Eg_ev * EV
    Ed_erg = Ed * EV
    Ea_erg = Ea * EV
    Nc = density_of_states(material["mc"], T)
    Nv = density_of_states(material["mv"], T)

    def concentrations(mu):
        n = Nc * safe_exp(-(Eg - mu) / kT)
        p = Nv * safe_exp(-mu / kT)
        Nd_plus = Nd0 * fermi_function(-(Eg - Ed_erg - mu) / kT)
        Na_minus = Na0 * fermi_function(-(mu - Ea_erg) / kT)
        return n, p, Nd_plus, Na_minus

    # бисекция: ищем mu, при котором p + Nd+ = n + Na-
    mu_low = -0.5 * EV
    mu_high = Eg + 0.5 * EV
    for step in range(100):
        mu_mid = (mu_low + mu_high) / 2
        n, p, Nd_plus, Na_minus = concentrations(mu_mid)
        if p + Nd_plus > n + Na_minus:
            mu_low = mu_mid
        else:
            mu_high = mu_mid
    mu = (mu_low + mu_high) / 2

    n, p, Nd_plus, Na_minus = concentrations(mu)
    ni = math.sqrt(Nc * Nv) * math.exp(-Eg / (2 * kT))

    return {
        "Eg": Eg_ev,          # эВ
        "mu": mu / EV,        # эВ
        "n": n,
        "p": p,
        "Nd_plus": Nd_plus,
        "Na_minus": Na_minus,
        "Nc": Nc,
        "Nv": Nv,
        "ni": ni,
    }