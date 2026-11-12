MOBILITY = {
    "Si":   {"Cn": 1328, "T0n_phonon": 300, "T0n": 1.072e-9,
             "Cp": 429,  "T0p_phonon": 300, "T0p": 9.814e-10},
    "Ge":   {"Cn": 3260, "T0n_phonon": 300, "T0n": 8.657e-10,
             "Cp": 2057, "T0p_phonon": 300, "T0p": 8.801e-10},
    "GaAs": {"Cn": 7379, "T0n_phonon": 300, "T0n": 5.056e-10,
             "Cp": 390,  "T0p_phonon": 300, "T0p": 4.027e-10},
}

def mobility_n(key, T, Nd_plus, Na_minus):
    # подвижность электронов; key - "Si", "Ge" или "GaAs"; концентрации в см^-3
    c = MOBILITY[key]
    return c["Cn"] / ((T / c["T0n_phonon"]) ** 1.5 + (Nd_plus + Na_minus) * (c["T0n"] / T) ** 1.5)


def mobility_p(key, T, Nd_plus, Na_minus):
    # подвижность дырок
    c = MOBILITY[key]
    return c["Cp"] / ((T / c["T0p_phonon"]) ** 1.5 + (Nd_plus + Na_minus) * (c["T0p"] / T) ** 1.5)
