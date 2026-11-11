from mobility import mobility_n, mobility_p

print("Подвижность при 300 К без примесей (ioffe: Si 1400/450, Ge 3900/1900, GaAs 8500/400):")
for key in ["Si", "Ge", "GaAs"]:
    print("  ", key, ": mu_n =", round(mobility_n(key, 300, 0, 0)), "  mu_p =", round(mobility_p(key, 300, 0, 0)))

print()
print("Кремний, электроны, от концентрации примеси при 300 К:")
for N in [1e14, 1e16, 1e17, 1e18, 1e19]:
    print("   N = %.0e   mu_n = %.0f" % (N, mobility_n("Si", 300, N, 0)))

print()
print("Кремний, электроны, от температуры:")
print("   T, К     чистый    N = 1e17")
for T in [100, 200, 300, 400, 500]:
    print("   %4d     %6.0f     %6.0f" % (T, mobility_n("Si", T, 0, 0), mobility_n("Si", T, 1e17, 0)))
