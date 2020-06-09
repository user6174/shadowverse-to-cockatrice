# -*- coding: utf-8 -*-
import json

#### globals ################################################################################
tablerow = {"Follower": 2, "Spell": 3, "Amulet": 1}
# 1 → non-creature, non-land permanents (like Planeswalkers, Enchantments, and Artifacts)
# 2 → creatures
# 3 → non-permanent cards (like Instants and Sorceries)
sets = ["Basic", "Standard Card Pack", "Darkness Evolved", "Rage of Bahamut",
        "Tempest of the Gods", "Wonderland Dreams", "Starforged Legends", "Chronogenesis",
        "Dawnbreak Nightedge", "Brigade of the Sky","Omen of the Ten", "Altersphere",
        "Steel Rebellion", "Rebirth of Glory", "Verdant Conflict", "Ultimate Colosseum",
        "World Uprooted"]
rarity = {"Bronze": "common",
          "Silver" : "uncommon",
          "Gold" : "rare",
          "Legendary" : "mythic"}
modesty_string = "<<{me.inplay.class.count}+1??<br>(Artifacts destroyed: \
<<{me.destroyed_card_list.race=artifact.unique_base_card_id_card.count}>>)>>"
shiva_string = "<<{me.inplay.class.count}+1??<br>(Current turn: )>>"
with open("en.json", 'r') as f:
    data = json.load(f)
#############################################################################################

g = open("sv_cards.xml", 'w+')
h = open("sv_tokens.xml", 'w+')

g.write('''<?xml version="1.0" encoding="UTF-8"?>\n\
    <cockatrice_carddatabase version="4">\n<sets>\n''')
h.write('''<?xml version="1.0" encoding="UTF-8"?>\n\
    <cockatrice_carddatabase version="4">\n<cards>\n''')
for s in sets:
    g.write('  <set>\n')
    g.write(f'    <name>{s}</name>\n')
    g.write(f'    <longname>{s}</longname>\n')
    g.write('    <settype>Custom</settype>\n')
    g.write('  </set>\n')
g.write('</sets>\n<cards>\n')

def clean(s):
    try:
        return s.replace(modesty_string , '').replace(shiva_string, '')\
               .replace('<br>', '\n').replace('&', 'and')
    except AttributeError:
        return s

print(data["Robogoblin"].keys())
print(data["Robogoblin"].values())
for i in data:
    card = data[i]
    if card["expansion"] == "Token":
        card["manaCost"] += 100
    out = []

    def xml(field, attr, val=None):
        if val is None:
            val = clean(card[attr])
        else:
            try:
                val = clean(val[attr])
            except TypeError:
                val = clean(val)
        return f'<{field}>{val}</{field}>\n'
        
    out.append('<card>\n')
    out.append(xml('name', 'name'))
    out.append(xml('text', 'description', card["baseData"]))
    if card["expansion"] == "Token":
        out.append(xml('token', '/', 1))
    out.append(xml('tablerow', '/', tablerow[card['type']]))
    out.append(f'<set rarity="{rarity[card["rarity"]]}" \
        picurl="https://sv.bagoum.com/cardF/en/c/{card["id"]}">\
        {clean(card["expansion"])}</set>\n')
    for j in data:
        if data[j]["name"][:-1] in card["baseData"]["description"]:
            out.append(xml('related', 'name', data[j]))
    if card["type"] == "Follower":
        out.append(xml('related', '/', card["name"] + ' Evolved'))
    out.append('<prop>\n')
    # e.g. machina
    out.append(xml('type', 'race'))
    # e.g. follower
    out.append(xml('maintype', 'type'))
    out.append(xml('manacost', 'manaCost'))
    out.append(xml('cmc', 'manaCost'))
    # e.g. neutral
    out.append(xml('colors', 'faction'))
    out.append(xml('coloridentity', 'faction'))
    out.append(xml('format-standard', '/', "legal" if card["rot"]=="Rotation" else "banned"))
    out.append(xml('pt', '/', f'{card["baseData"]["attack"]}/{card["baseData"]["defense"]}'))
    out.append('</prop>\n')
    out.append('</card>\n')

    if card["type"] == "Follower":
        card["manaCost"] += 100
        evo_out = []
        evo_out.append('<card>\n')
        evo_out.append(xml('name', '/', card["name"] + ' Evolved'))
        evo_out.append(xml('text', 'description', card["evoData"]))
        evo_out.append(xml('token', '/', 1))
        evo_out.append(xml('tablerow', '/', tablerow[card['type']]))
        evo_out.append(f'<set rarity="{rarity[card["rarity"]]}" \
        picurl="https://sv.bagoum.com/cardF/en/e/{card["id"]}">\
        Token</set>\n')
        for j in data:
            if data[j]["name"][:-1] in card["evoData"]["description"]:
                evo_out.append(xml('related', 'name', data[j]))
        evo_out.append('<prop>\n')
        evo_out.append(xml('type', 'race'))
        evo_out.append(xml('maintype', 'type'))
        evo_out.append(xml('manacost', 'manaCost'))
        evo_out.append(xml('cmc', 'manaCost'))
        evo_out.append(xml('colors', 'faction'))
        evo_out.append(xml('coloridentity', 'faction'))
        evo_out.append(xml('format-standard', '/', "legal" if card["rot"]=="Rotation" else "banned"))
        evo_out.append(xml('pt', '/', f'{card["evoData"]["attack"]}/{card["evoData"]["defense"]}'))
        evo_out.append('</prop>\n')
        evo_out.append('</card>\n')
        for i in range(len(evo_out)):
                h.write(evo_out[i])
    if card["expansion"]=='Token':
        for i in range(len(out)):
            h.write(out[i])
    else:
        for i in range(len(out)):
            g.write(out[i])
g.write('</cards>\n</cockatrice_carddatabase>')
h.write('</cards>\n</cockatrice_carddatabase>')
g.close()

h.close()
