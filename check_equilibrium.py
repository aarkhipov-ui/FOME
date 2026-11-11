# Проверка блока 2: правильно ли считаются уровень Ферми и концентрации.
from materials import MATERIALS, SI
from equilibrium import solve


def report(name, ok):
    if ok:
        print("  OK      ", name)
    else:
        print("  ОШИБКА  ", name)


# Табличные значения ioffe при 300 К (для сравнения)
IOFFE = {
    "Si":   {"Nc": 3.2e19, "Nv": 1.8e19, "ni": 1.0e10},
    "Ge":   {"Nc": 1.0e19, "Nv": 5.0e18, "ni": 2.0e13},
    "GaAs": {"Nc": 4.7e17, "Nv": 9.0e18, "ni": 2.1e6},
}

print("Проверка 1. Nc, Nv и ni при 300 К сравниваем с ioffe")
for key in MATERIALS:
    r = solve(MATERIALS[key], 300, 1e10, 0.01)
    print(" ", key, ": Nc =", "%.2e" % r["Nc"], " Nv =", "%.2e" % r["Nv"], " ni =", "%.2e" % r["ni"],
          "   (ioffe: ni =", "%.1e" % IOFFE[key]["ni"], ")")
    ratio = r["ni"] / IOFFE[key]["ni"]
    report(key + ": ni совпадает с ioffe по порядку величины", 0.2 < ratio < 5)

print()
print("Проверка 2. Закон действующих масс: n * p = ni^2")
for key in MATERIALS:
    for Nd0 in [1e10, 1e14, 1e18, 1e20]:
        r = solve(MATERIALS[key], 300, Nd0, 0.01)
        error = abs(r["n"] * r["p"] / r["ni"] ** 2 - 1)
        report(key + ", Nd0 = " + "%.0e" % Nd0, error < 1e-6)

print()
print("Проверка 3. Электронейтральность: p + Nd+ = n + Na-")
for key in MATERIALS:
    for Nd0 in [1e10, 1e15, 1e20]:
        r = solve(MATERIALS[key], 300, Nd0, 0.01, Na0=1e14, Ea=0.03)
        plus = r["p"] + r["Nd_plus"]
        minus = r["n"] + r["Na_minus"]
        report(key + ", Nd0 = " + "%.0e" % Nd0, abs(plus / minus - 1) < 1e-9)

print()
print("Проверка 4. Кремний, Nd0 = 1e16, 300 К: все доноры ионизованы, n = Nd0")
r = solve(SI, 300, 1e16, 0.045)
report("n = " + "%.3e" % r["n"] + " (ожидаем 1.0e16)", abs(r["n"] / 1e16 - 1) < 0.01)

print()
print("Таблица для кремния, 300 К, донор фосфор (Ed = 0.045 эВ):")
print("    Nd0       Ec - mu, эВ    n, см^-3     p, см^-3    доля Nd+")
for power in range(10, 21):
    Nd0 = 10.0 ** power
    r = solve(SI, 300, Nd0, 0.045)
    print("  %.0e      %.3f        %.3e    %.3e    %.3f"
          % (Nd0, r["Eg"] - r["mu"], r["n"], r["p"], r["Nd_plus"] / Nd0))