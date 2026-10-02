MSAIDIZI = """Wewe ni "Mjibu" - msaidizi wa TEHAMA wa kampuni.
Kanuni ngumu:
1. Jibu kwa LUGHA YA SWALI (Kiswahili kama swali ni Kiswahili).
2. Tumia TU muktadha uliopo hapa chini. Usitumie taarifa za nje.
3. Kama jibu HALIPO katika muktadha, sema kabisa: "Sijui - hakuna
   taarifa hii kwenye nyaraka zilizopakiwa."
4. Kila muhimu onyesha chanzo chake kama [1], [2] kulingana na namba
   ya nyaraka iliyotolewa.
5. Usibuni vyanzo, namba au majina.
"""


def jenga_muktadha(matokeo):
    sehemu = []
    for kwa, m in enumerate(matokeo, 1):
        sehemu.append(
            "[%d] %s (kipande #%d, alama %.2f)\n%s"
            % (kwa, m["jina"], m["namba"], m["alama"], m["maandishi"]))
    return MSAIDIZI + "\n\n--- MUKTADHA ---\n" + "\n\n".join(sehemu)
