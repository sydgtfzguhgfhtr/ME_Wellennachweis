import cadquery as cq


l_AB = 290
l_z22 = 115
l_z21 = 95

Festlager = 0
Loslager  = -l_AB
B_fl = 31
B_ll = 12
B_Zahnrad = 60
B_Ritzel = 80


geometrie = (
    (-l_AB-30,30),
    # Loslager
    (-l_AB+B_ll/2,35),
    (-l_AB+B_ll/2,35),
    (-l_z22-B_Ritzel/2-2,42),
    (-l_z22,42),# Ritzel
    (-B_fl/2,42),
    (-B_fl/2,40),
    # Festlager
    (l_z21,40),# Zahnrad
    (l_z21+B_Zahnrad/2+5,40)
)

results = []

for i in range(len(geometrie)-2):
    if i == 0:
        result = cq.Workplane('XY').circle(geometrie[0][1]).workplane(offset=geometrie[1][0]-geometrie[0][0]).circle(geometrie[1][1]).loft(combine=True)
    else:
        result = cq.Workplane('XY').workplane(offset=geometrie[i][0]-geometrie[i-1][0]).circle(geometrie[i][1]).workplane(offset=geometrie[i+2][0]-geometrie[i+1][0]).circle(geometrie[i+1][1]).loft(combine=True)

    results.append(result)