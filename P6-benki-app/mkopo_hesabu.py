def hesabu(aina, kiasi, riba, miezi):
    if aina not in ("flat", "reducing"):
        raise ValueError("Aina isiyojulikana: %s" % aina)
    if kiasi <= 0:
        raise ValueError("Kiasi lazima liwe zaidi ya 0")
    if riba < 0 or riba > 100:
        raise ValueError("Riba lazima iwe kati ya 0 na 100")
    if miezi < 1 or miezi > 360:
        raise ValueError("Miezi lazima iwe kati ya 1 na 360")
    if aina == "flat":
        return _flat(kiasi, riba, miezi)
    return _reducing(kiasi, riba, miezi)


def _flat(kiasi, riba, miezi):
    riba_jumla = kiasi * riba / 100 * (miezi / 12)
    jumla = kiasi + riba_jumla
    malipo_mwezi = jumla / miezi
    riba_mwezi = riba_jumla / miezi
    salio = kiasi
    jedwali = []
    for n in range(1, miezi + 1):
        if n == miezi:
            marejesho = salio
            malipo = marejesho + riba_mwezi
            salio = 0.0
        else:
            marejesho = malipo_mwezi - riba_mwezi
            malipo = malipo_mwezi
            salio = salio - marejesho
        jedwali.append({"mwezi": n, "malipo": malipo, "riba": riba_mwezi,
                        "marejesho": marejesho, "salio": salio})
    return {"aina": "flat", "kiasi": kiasi, "riba_ya_jumla": riba_jumla,
            "jumla": jumla, "malipo_mwezi": malipo_mwezi, "jedwali": jedwali}


def _reducing(kiasi, riba, miezi):
    i = riba / 100 / 12
    if i == 0:
        malipo = kiasi / miezi
    else:
        malipo = kiasi * i / (1 - (1 + i) ** (-miezi))
    salio = kiasi
    riba_jumla = 0.0
    jedwali = []
    for n in range(1, miezi + 1):
        riba_mwezi = salio * i
        if n == miezi:
            marejesho = salio
            malipo_sasa = marejesho + riba_mwezi
            salio = 0.0
        else:
            marejesho = malipo - riba_mwezi
            malipo_sasa = malipo
            salio = salio - marejesho
        riba_jumla = riba_jumla + riba_mwezi
        jedwali.append({"mwezi": n, "malipo": malipo_sasa, "riba": riba_mwezi,
                        "marejesho": marejesho, "salio": salio})
    return {"aina": "reducing", "kiasi": kiasi, "riba_ya_jumla": riba_jumla,
            "jumla": kiasi + riba_jumla, "malipo_mwezi": malipo,
            "jedwali": jedwali}
