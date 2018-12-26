# -*- coding: utf-8 -*-
import json

tablerow = {"Follower":2, "Spell":3, "Amulet":1}
#1 → non-creature, non-land permanents (like Planeswalkers, Enchantments, and Artifacts)
#2 → creatures (this includes all cards that have the "creature" type like "Enchantment Creature")
#3 → non-permanent cards (like Instants and Sorceries)

f = open ("your/directory/cockatrice/en.json")
g = open ("your/directory/cockatrice/sv_database.xml", 'w')
h = open ("your/directory/cockatrice/sv_tokens.xml", 'w')
g.write ('<cockatrice_carddatabase version="3">')
g.write ('<cards>')
h.write ('<cockatrice_carddatabase version="3">')
h.write ('<cards>')

data = json.load (f)
for i in data:
  istoken = False
  out = list ()
  out.append ('<card>')
  out.append ('<name>{}</name>\n'.format (str (data [i] ["name"]).replace ('&', 'and')))
  if data [i] ["expansion"] != "Token":
    out.append ('<set>{}</set>\n'.format (str (data [i] ["expansion"])))
  else:
    out.append ('<token>1</token>')
    istoken = True
  out.append ('<set picURL="https://shadowverse-portal.com/image/card/en/C_{}.png"></set>\n'.format (str( data [i] ["id"])))
  if data [i] ["type"] == "Follower":
    out.append ('<related>{} EVOLVED</related>\n'.format (str (data [i] ["name"]).replace ('&', 'and')))
  else:
    for j in data:
      if data [j] ["name"] [:-1] in data [i] ["baseData"] ["description"]:
        out.append ('<related>{}</related>\n'.format (  str( data [j] ["name"]).replace ('&', 'and')))
        break
  out.append ('<color>{}</color>\n'.format (str (data [i] ["faction"])))
  out.append ('<manacost>{}</manacost>\n'.format (str (data [i] ["manaCost"])))
  out.append ('<cmc>{}</cmc>\n'.format (str (data [i] ["manaCost"])))
  out.append ('<type>{}</type>\n'.format (str (data [i] ["race"]))) 
  out.append ('<pt>{}</pt>\n'.format (str (data [i] ["baseData"] ["attack"]) + "/" + str (data [i] ["baseData"] ["defense"])))
  out.append ('<tablerow>{}</tablerow>\n'.format ( str (tablerow [data [i] ["type"]])))
  out.append ('<text>{}</text>\n'.format (str (data [i] ["baseData"] ["description"].replace ('<br>', ' ').replace ('&', 'and'))))
  out.append ('</card>')
  if data [i] ["type"] == "Follower":
    out.append ('<card>')
    out.append ('<name>{} EVOLVED</name>\n'.format ( str (data [i] ["name"]).replace ('&', 'and')))
    out.append ('<set picURL="https://shadowverse-portal.com/image/card/en/E_{}.png"></set>\n'.format (str (data [i] ["id"])))
    out.append ('<color>{}</color>\n'.format (str (data [i] ["faction"])))
    out.append ('<manacost>{}</manacost>\n'.format (str (data [i] ["manaCost"])))
    out.append ('<cmc>{}</cmc>\n'.format (str (data [i] ["manaCost"])))
    out.append ('<type>{}</type>\n'.format (str (data [i] ["race"]))) 
    out.append ('<pt>{}</pt>\n'.format (str (data [i] ["evoData"] ["attack"]) + "/" + str (data [i] ["evoData"] ["defense"])))
    out.append ('<tablerow>{}</tablerow>\n'.format (str (tablerow [data [i] ["type"]])))
    out.append ('<text>{}</text>\n'.format (str (data [i] ["evoData"] ["description"].replace ('<br>', ' ').replace ('&', 'and'))))
    if istoken:
      out.append ('<token>1</token>')
    out.append ('</card>')
    for i in range(len(out)):
      h.write(out[i])
  else:
    for i in range(len(out)):
      g.write(out[i])
g.write( '</cards>')
g.write( '</cockatrice_carddatabase>')
h.write( '</cards>')
h.write( '</cockatrice_carddatabase>')
g.close()
h.close()



                                                                                                                                               
