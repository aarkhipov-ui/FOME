from irvin import calculate_point, irvin_curve, mobility_curve

print("Проверка 1. Собственное сопротивление (почти без примесей) при 300 К")
IOFFE_RHO = {"Si": 3.2e5, "Ge": 46, "GaAs": 3.3e8}
for key in ["Si", "Ge", "GaAs"]:
    r = calculate_point(key, 300, 1.0, 0.01)
    ratio = r["rho"] / IOFFE_RHO[key]
    if 0.3 < ratio < 3:
        result = "OK"
    else:
        result = "ОШИБКА"
    print("  ", key, ": rho = %.2e Ом*см, на ioffe %.1e ->" % (r["rho"], IOFFE_RHO[key]), result)

print()
print("Кривая Ирвина для кремния, 300 К, фосфор (временные константы подвижности):")
curve = irvin_curve("Si", 300, 0.045, points=11)
print("    Nd0        n, см^-3     mu_n     rho, Ом*см")
for i in range(len(curve["Nd0"])):
    print("  %.0e    %.3e    %6.0f    %.3e"
          % (curve["Nd0"][i], curve["n"][i], curve["mu_n"][i], curve["rho"][i]))

print()
print("Подвижность электронов в кремнии от температуры, Nd0 = 1e17:")
curve = mobility_curve("Si", 1e17, 0.045, T_min=100, T_max=500, points=5)
for i in range(len(curve["T"])):
    print("   T = %3.0f К   mu_n = %.0f" % (curve["T"][i], curve["mu_n"][i]))