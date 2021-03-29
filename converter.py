# -*- coding: utf-8 -*-
import json
import os

# https://github.com/Cockatrice/Cockatrice/wiki/Custom-Cards-&-Sets

# globals
tablerow = {"Follower": 2, "Spell": 3, "Amulet": 1}
# 1 → non-creature, non-land permanents (like Planeswalkers, Enchantments, and Artifacts)
# 2 → creatures
# 3 → non-permanent cards (like Instants and Sorceries)
rarities = {"Bronze": "basic",
            "Silver": "uncommon",
            "Gold": "rare",
            "Legendary": "mythic"}
sets = {"Token": ("TK", "1970-01-01"),
        "Basic": ("Basic", "2016-06-21"),
        "Standard Card Pack": ("STD", "2016-06-21"),
        "Darkness Evolved": ("DE", "2016-09-29"),
        "Rise of Bahamut": ("ROB", "2016-12-29"),
        "Tempest of the Gods": ("TOTG", "2017-03-30"),
        "Wonderland Dreams": ("WLD", "2017-06-29"),
        "Starforged Legends": ("SL", "2017-09-28"),
        "Chronogenesis": ("CG", "2017-12-28"),
        "Dawnbreak Nightedge": ("DN", "2018-03-28"),
        "Brigade of the Sky": ("BOTS", "2018-06-27"),
        "Omen of the Ten": ("OOT", "2018-09-26"),
        "Altersphere": ("AS", "2018-12-26"),
        "Steel Rebellion": ("SR", "2019-03-27"),
        "Rebirth of Glory": ("ROG", "2019-06-27"),
        "Verdant Conflict": ("VC", "2019-09-25"),
        "Ultimate Colosseum": ("UC", "2019-12-27"),
        "World Uprooted": ("WU", "2020-03-29"),
        "Fortune's Hand": ("FH", "2020-06-29"),
        "Storm Over Rivayle": ("SOR", "2020-09-23"),
        "Eternal Awakening": ("EA", "2020-12-28"),
        "Darkness Over Vellsar": ("DOV", "2021-03-29")
        }

# https://github.com/user6174/shadowverse-json
with open("shadowverse-json/en/all.json", 'r') as f:
    data = json.load(f)

# end globals
c = open("sv_cards.xml", 'w+')
t = open("sv_tokens.xml", 'w+')

c.write('''<?xml version="1.0" encoding="UTF-8"?>\n
        <cockatrice_carddatabase version="4">\n
        <sets>\n''')
t.write('''<?xml version="1.0" encoding="UTF-8"?>\n
            <cockatrice_carddatabase version="4">\n
            <cards>\n''')
for s in sets:
    c.write('\t<set>\n')
    c.write(f'\t\t<name>{sets[s][0]}</name>\n')
    c.write(f'\t\t<longname>{s}</longname>\n')
    c.write('\t\t<settype>Custom</settype>\n')
    c.write(f'\t\t<releasedate>{sets[s][1]}</releasedate>')
    c.write('\t</set>\n')
c.write('</sets>\n<cards>\n')


def clean(txt):
    try:
        return txt.replace('Ofcr.', "Officer").replace('Cmdr.', "Commander") \
            .replace('Nat.', 'Natura').replace('Mach.', 'Machina') \
            .strip(' /').replace('<br>', '\n').replace('&', 'and')
    except AttributeError:
        return txt


for i in list(data):
    card = data[i]
    if card["expansion_"] == "Promo": continue
    card["trait_"] = card["trait_"].strip("-")

    def xml(field, val):
        try:
            return clean(f'\t\t<{field}>{card[val]}</{field}>\n')
        except KeyError:
            return clean(f'\t\t<{field}>{val}</{field}>\n')

    out = ['\t<card>\n',
           xml('name', 'name_'),
           xml('text', 'baseEffect_'),
           '\t\t<prop>\n',
           '\t' + xml('layout', 'normal'),
           '\t' + xml('side', 'front'),
           '\t' + xml('type', f'{clean(card["trait_"])} {card["type_"]}'),
           '\t' + xml('maintype', 'type_'),
           '\t' + xml('manacost', 'pp_'),
           '\t' + xml('cmc', 'pp_'),
           '\t' + xml('colors', 'craft_'),
           '\t' + xml('coloridentity', 'craft_'),
           '\t' + xml('pt', f'{card["baseAtk_"]}/{card["baseDef_"]}') if card["baseDef_"] != 0 else '',
           '\t' + xml('format-standard', 'legal' if card["rotation_"] else "banned"),
           '\t\t</prop>\n',
           f'\t\t<set rarity="{rarities[card["rarity_"]]}" uuid="{card["id_"]}" num="{card["id_"]}" muid="{card["id_"]}" '
           f'picurl="https://svgdb.me/assets/cards/C_{card["id_"]}.png"> {sets[clean(card["expansion_"])][0]}</set>\n']
    for j in data:
        if data[j]["name_"][:-1] in card["baseEffect_"]:
            out.append(xml('related', data[j]["name_"]))
    if card["type_"] == "Follower":
        out.append(f'<related attach="1">{clean(card["name_"]) + " Evolved"}</related>')
    out.append(xml('token', '1' if card["expansion_"] == "Token" else '0'))
    out.append(xml('tablerow', tablerow[card["type_"]]))
    out.append('</card>\n')
    if card["expansion_"] == 'Token':
        for i in range(len(out)):
            t.write(out[i])
    else:
        for i in range(len(out)):
            c.write(out[i])
        if card["type_"] == "Follower":
            out[1] = xml('name', card["name_"] + " Evolved")
            out[2] = xml('text', card["evoEffect_"])
            out[5] = out[5].replace('front', 'back')
            out[12] = xml('pt', f'{card["evoAtk_"]}/{card["evoDef_"]}')
            out[15] = f'\t\t<set rarity="{rarities[card["rarity_"]]}" uuid="{card["id_"]}" num="{card["id_"]}" ' \
                      f'muid="{card["id_"]}" picurl="https://svgdb.me/assets/cards/E_{card["id_"]}.png">TK</set>\n'
            for idx, line in enumerate(out):
                if "Evolved</related>" in line:
                    out.pop(idx)
                if "<token>" in line:
                    out[idx] = xml('token', '1')
            for i in range(len(out)):
                t.write(out[i])

c.write('</cards>\n</cockatrice_carddatabase>')
t.write('</cards>\n</cockatrice_carddatabase>')
c.close()
t.close()
