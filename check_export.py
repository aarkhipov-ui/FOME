from irvin import irvin_curve
from export import save_two_columns

curve = irvin_curve("Si", 300, 0.045, points=11)
save_two_columns("test_irvin_Si.txt", curve["Nd0"], curve["rho"],
                 "Nd0 [cm^-3]", "rho [Ohm*cm]", "Si, T = 300 K, Ed = 0.045 eV")

print("Файл test_irvin_Si.txt сохранён. Его содержимое:")
file = open("test_irvin_Si.txt", "r")
print(file.read())
file.close()