# Подвижность по формулам (3.1) и (3.2) задачи 4, см^2/(В*с).
# ВРЕМЕННЫЕ константы: C = 1, T0_phonon даёт подвижность чистого материала при 300 К (ioffe),
# T0 подобрана так, что при Nd+ + Na- = 1e17 см^-3 подвижность падает вдвое.
# Потом заменим их на подобранные по эксперименту.

MOBILITY = {
    "Si":   {"Cn": 1.0, "T0n_phonon": 3.754e4, "T0n": 1.113e-11,
             "Cp": 1.0, "T0p_phonon": 1.762e4, "T0p": 2.371e-11},
    "Ge":   {"Cn": 1.0, "T0n_phonon": 7.433e4, "T0n": 5.620e-12,
             "Cp": 1.0, "T0p_phonon": 4.602e4, "T0p": 9.077e-12},
    "GaAs": {"Cn": 1.0, "T0n_phonon": 1.249e5, "T0n": 3.343e-12,
             "Cp": 1.0, "T0p_phonon": 1.629e4, "T0p": 2.565e-11},
}


def mobility_n(key, T, Nd_plus, Na_minus):
    # подвижность электронов; key - "Si", "Ge" или "GaAs"; концентрации в см^-3
    c = MOBILITY[key]
    return c["Cn"] / ((T / c["T0n_phonon"]) ** 1.5 + (Nd_plus + Na_minus) * (c["T0n"] / T) ** 1.5)


def mobility_p(key, T, Nd_plus, Na_minus):
    # подвижность дырок
    c = MOBILITY[key]
    return c["Cp"] / ((T / c["T0p_phonon"]) ** 1.5 + (Nd_plus + Na_minus) * (c["T0p"] / T) ** 1.5)
