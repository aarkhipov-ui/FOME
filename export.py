# Сохранение графика в текстовый файл (ASCII), два столбца.


def save_two_columns(filename, x_values, y_values, x_name, y_name, comment=""):
    # x_name, y_name, comment - латиницей, например "Nd0 [cm^-3]", "rho [Ohm*cm]"
    if len(x_values) != len(y_values):
        raise ValueError("Столбцы X и Y должны быть одинаковой длины.")

    file = open(filename, "w", encoding="ascii", errors="replace")
    if comment != "":
        file.write("# " + comment + "\n")
    file.write("# " + x_name + "\t" + y_name + "\n")
    for i in range(len(x_values)):
        file.write("%.6e\t%.6e\n" % (x_values[i], y_values[i]))
    file.close()