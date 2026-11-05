# Проверка: формула Варшни при 300 К должна дать значения Eg с сайта ioffe.
from materials import MATERIALS, band_gap

# Табличные значения Eg при 300 К с ioffe.ru, эВ
IOFFE_EG = {"Si": 1.12, "Ge": 0.661, "GaAs": 1.424}

for key in MATERIALS:
    material = MATERIALS[key]
    eg = band_gap(material, 300)
    difference = abs(eg - IOFFE_EG[key])
    if difference < 0.005:
        result = "OK"
    else:
        result = "ОШИБКА"
    print(material["name"], ": Eg(300 K) =", round(eg, 4), "эВ, на ioffe", IOFFE_EG[key], "эВ ->", result)