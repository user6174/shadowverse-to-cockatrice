# -*- coding: utf-8 -*-
import json

with open("en.json", 'r') as f:
    data = json.load(f)
g = open("sv_cards.xml", 'w+')
h = open("sv_tokens.xml", 'w+')
tablerow = {"Follower": 2, "Spell": 3, "Amulet": 1}
# 1 → non-creature, non-land permanents (like Planeswalkers, Enchantments, and Artifacts)
# 2 → creatures (this includes all cards that have the "creature" type like "Enchantment Creature")
# 3 → non-permanent cards (like Instants and Sorceries)
sets = ["Basic", "Standard Card Pack", "Darkness Evolved", "Rage of Bahamut", "Tempest of the Gods",
        "Wonderland Dreams", "Starforged Legends", "Chronogenesis", "Dawnbreak Nightedge",
        "Brigade of the Sky","Omen of the Ten", "Altersphere", "Steel Rebellion", "Rebirth of Glory",
        "Verdant Conflict", "Ultimate Colosseum"]
rarity = {"Bronze": "common",
          "Silver" : "uncommon",
          "Gold" : "rare",
          "Legendary" : "mythic"}
g.write('''<?xml version="1.0" encoding="UTF-8"?>\n<cockatrice_carddatabase version="4">\n\t<sets>\n''')
h.write('''<?xml version="1.0" encoding="UTF-8"?>\n<cockatrice_carddatabase version="4">\n\t<cards>\n''')
odin_string = "<<{me.deck_self.count}+1 ??<br>(Times evolved: <<{me.evolved_card_list.count}>>)>><br>"
for i in sets:
    g.write("\t\t<set>\n")
    g.write("\t\t\t<name>{}</name>\n".format(i))
    g.write("\t\t\t<longname>{}</longname>\n".format(i))
    g.write("\t\t\t<settype>Custom</settype>\n")
    g.write("\t\t</set>\n")
g.write("\t</sets>\t<cards>\n")
for i in data:
    token = False
    out = []
    out.append('\t\t<card>\n')
    out.append(
        '\t\t\t<name>{}</name>\n'.format(str(data[i]["name"].replace('&', 'and'))))
    out.append('\t\t\t<text>{}</text>\n'.format(str(data[i]["baseData"]["description"].replace(
        odin_string, '').replace('<br>', '\n').replace('&', 'and'))))
    if data[i]["expansion"] == "Token":
        out.append('\t\t\t<token>1</token>')
        token = True
    out.append(
        '\t\t\t<tablerow>{}</tablerow>\n'.format(str(tablerow[data[i]["type"]])))
    out.append('\t\t\t<set rarity="{}" picurl="https://sv.bagoum.com/cardF/en/c/{}">{}</set>\n'.format(
        rarity[str(data[i]["rarity"])], str(data[i]["id"]), str(data[i]["expansion"])))
    for j in data:
        if data[j]["name"][:-1] in data[i]["baseData"]["description"]:
            out.append(
                '\t\t\t<related>{}</related>\n'.format(str(data[j]["name"].replace('&', 'and'))))
    if data[i]["type"] == "Follower":
        out.append('\t\t\t<related>{} Evolved</related>\n'.format(
            str(data[i]["name"].replace('&', 'and'))))
    # trait, like machina
    out.append(
        '\t\t\t<prop>\n\t\t\t\t<type>{}</type>\n'.format(str(data[i]["race"])))
    # type, like follower
    out.append(
        '\t\t\t\t<maintype>{}</maintype>\n'.format(str(data[i]["type"])))
    out.append(
        '\t\t\t\t<manacost>{}</manacost>\n'.format(str(data[i]["manaCost"])))
    out.append('\t\t\t\t<cmc>{}</cmc>\n'.format(str(data[i]["manaCost"])))
    out.append('\t\t\t\t<colors>{}</colors>\n'.format(str(data[i]["faction"])))
    out.append(
        '\t\t\t\t<coloridentity>{}</coloridentity>\n'.format(str(data[i]["faction"])))
    out.append('\t\t\t\t<format-standard>{}</format-standard>\n'.format('legal' *
                                                                        (str(data[i]["rot"]) == 'Rotation')))
    out.append('\t\t\t\t<pt>{}</pt>\n\t\t\t</prop>\n'.format(
        str(data[i]["baseData"]["attack"]) + "/" + str(data[i]["baseData"]["defense"])))
    out.append('\t\t</card>\n')

    if data[i]["type"] == "Follower":
        evo_out = list()
        evo_out.append('\t\t<card>\n')
        evo_out.append('\t\t\t<name>{} Evolved</name>\n'.format(
            str(data[i]["name"].replace('&', 'and'))))
        evo_out.append('\t\t\t<text>{}</text>\n'.format(str(data[i]["evoData"]["description"].replace(
            odin_string, '').replace('<br>', '\n').replace('&', 'and'))))
        evo_out.append('\t\t\t<token>1</token>')
        evo_out.append(
            '\t\t\t<tablerow>{}</tablerow>\n'.format(str(tablerow[data[i]["type"]])))
        evo_out.append('\t\t\t<set rarity="{}" picurl="https://sv.bagoum.com/cardF/en/e/{}">Token</set>\n'.format(
            rarity[str(data[i]["rarity"])], str(data[i]["id"])))
        for j in data:
            if data[j]["name"][:-1] in data[i]["evoData"]["description"]:
                evo_out.append(
                    '\t\t\t<related>{}</related>\n'.format(str(data[j]["name"].replace('&', 'and'))))
        evo_out.append(
            '\t\t\t<prop>\n\t\t\t\t<type>{}</type>\n'.format(str(data[i]["race"])))
        evo_out.append(
            '\t\t\t\t<maintype>{}</maintype>\n'.format(str(data[i]["type"])))
        evo_out.append(
            '\t\t\t\t<cmc>{}</cmc>\n'.format(str(data[i]["manaCost"])))
        evo_out.append(
            '\t\t\t\t<colors>{}</colors>\n'.format(str(data[i]["faction"])))
        evo_out.append('\t\t\t\t<pt>{}</pt>\n\t\t\t</prop>\n'.format(
            str(data[i]["evoData"]["attack"]) + "/" + str(data[i]["evoData"]["defense"])))
        evo_out.append('\t\t</card>\n')
        for i in range(len(evo_out)):
            h.write(evo_out[i])
    if token:
        for i in range(len(out)):
            h.write(out[i])
    else:
        for i in range(len(out)):
            g.write(out[i])
g.write('\t\t</cards>\n</cockatrice_carddatabase>')
h.write('\t\t</cards>\n</cockatrice_carddatabase>')
g.close()
h.close()
