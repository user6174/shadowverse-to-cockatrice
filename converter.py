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
g.write('''<?xml version="1.0" encoding="UTF-8"?>\n<cockatrice_carddatabase version="4">\n<cards>\n''')
h.write('''<?xml version="1.0" encoding="UTF-8"?>\n<cockatrice_carddatabase version="4">\n<cards>\n''')
odin_string = "<<{me.deck_self.count}+1 ??<br>(Times evolved: <<{me.evolved_card_list.count}>>)>><br>"
for i in data:
    istoken = False
    out = []
    out.append('<card>\n')
    out.append(
        '    <name>{}</name>\n'.format(str(data[i]["name"].encode('utf8').replace('&', 'and'))))
    out.append('    <text>{}\n\n'.format(str(data[i]["baseData"]["description"].replace(
        odin_string, '').replace('<br>', '\n').encode('utf8').replace('&', 'and'))))
    out.append('{}</text>\n'.format(str(data[i]["evoData"]["description"].replace(
        odin_string, '').replace('<br>', '\n').encode('utf8').replace('&', 'and'))))
    if data[i]["expansion"] == "Token":
        out.append('    <token>1</token>')
        istoken = True
    out.append(
        '   <tablerow>{}</tablerow>\n'.format(str(tablerow[data[i]["type"]])))
    out.append('    <set rarity="{}" picurl="https://sv.bagoum.com/cardF/en/c/{}">{}</set>\n'.format(
        str(data[i]["rarity"]), str(data[i]["id"]), str(data[i]["expansion"])))
    for j in data:
        if data[j]["name"][:-1] in data[i]["baseData"]["description"]:
            out.append(
                '   <related>{}</related>\n'.format(str(data[j]["name"].encode('utf8').replace('&', 'and'))))
    if data[i]["type"] == "Follower":
        out.append('    <related>{} Evolved</related>\n'.format(
            str(data[i]["name"].encode('utf8').replace('&', 'and'))))
    # trait, like machina
    out.append(
        '    <prop>\n        <type>{}</type>\n'.format(str(data[i]["race"])))
    # type, like follower
    out.append(
        '        <maintype>{}</maintype>\n'.format(str(data[i]["type"])))
    out.append(
        '        <manacost>{}</manacost>\n'.format(str(data[i]["manaCost"])))
    out.append('        <cmc>{}</cmc>\n'.format(str(data[i]["manaCost"])))
    out.append('        <colors>{}</colors>\n'.format(str(data[i]["faction"])))
    out.append(
        '       <coloridentity>{}</coloridentity>\n'.format(str(data[i]["faction"])))
    out.append('        <format-standard>{}</format-standard>\n'.format('legal' *
                                                                        (str(data[i]["rot"]) == 'Rotation')))
    out.append('        <pt>{}</pt>\n    </prop>\n'.format(
        str(data[i]["baseData"]["attack"]) + "/" + str(data[i]["baseData"]["defense"])))
    out.append('</card>')

    if data[i]["type"] == "Follower":
        evo_out = list()
        evo_out.append('<card>\n')
        evo_out.append('    <name>{} Evolved</name>\n'.format(
            str(data[i]["name"].encode('utf8').replace('&', 'and'))))
        evo_out.append('    <text>{}</text>\n'.format(str(data[i]["evoData"]["description"].replace(
            odin_string, '').replace('<br>', '\n').encode('utf8').replace('&', 'and'))))
        evo_out.append('    <token>1</token>')
        evo_out.append(
            '   <tablerow>{}</tablerow>\n'.format(str(tablerow[data[i]["type"]])))
        evo_out.append('    <set rarity="{}" picurl="https://sv.bagoum.com/cardF/en/e/{}">Token</set>\n'.format(
            str(data[i]["rarity"]), str(data[i]["id"])))
        for j in data:
            if data[j]["name"][:-1] in data[i]["evoData"]["description"]:
                evo_out.append(
                    '   <related>{}</related>\n'.format(str(data[j]["name"].encode('utf8').replace('&', 'and'))))
        evo_out.append(
            '   <prop>\n        <type>{}</type>\n'.format(str(data[i]["race"])))
        evo_out.append(
            '       <maintype>{}</maintype>\n'.format(str(data[i]["type"])))
        evo_out.append(
            '        <cmc>{}</cmc>\n'.format(str(data[i]["manaCost"])))
        evo_out.append(
            '        <colors>{}</colors>\n'.format(str(data[i]["faction"])))
        evo_out.append('        <pt>{}</pt>\n    </prop>\n'.format(
            str(data[i]["evoData"]["attack"]) + "/" + str(data[i]["evoData"]["defense"])))
        evo_out.append('</card>\n')
        for i in range(len(evo_out)):
            h.write(evo_out[i])
    if istoken:
        for i in range(len(out)):
            h.write(out[i])
    else:
        for i in range(len(out)):
            g.write(out[i])

g.write('</cards>\n</cockatrice_carddatabase>')
h.write('</cards>\n</cockatrice_carddatabase>')
g.close()
h.close()
