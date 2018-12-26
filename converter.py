# -*- coding: utf-8 -*-
import json, Tkinter, tkFileDialog

tablerow = {"Follower":2, "Spell":3, "Amulet":1}
#1 → non-creature, non-land permanents (like Planeswalkers, Enchantments, and Artifacts)
#2 → creatures (this includes all cards that have the "creature" type like "Enchantment Creature")
#3 → non-permanent cards (like Instants and Sorceries)

root = Tkinter.Tk()
root.withdraw()
path = tkFileDialog.askdirectory()

f = open ("en.json".format (path + str ("/")))
g = open ("sv_database.xml".format (path + str ("/")), 'w')
h = open ("sv_tokens.xml".format (path + str ("/")), 'w')
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
  for j in data:
    if data [j] ["name"] [:-1] in data [i] ["baseData"] ["description"]:
      out.append ('<related>{}</related>\n'.format (  str( data [j] ["name"]).replace ('&', 'and')))
  out.append ('<color>{}</color>\n'.format (str (data [i] ["faction"])))
  out.append ('<manacost>{}</manacost>\n'.format (str (data [i] ["manaCost"])))
  out.append ('<cmc>{}</cmc>\n'.format (str (data [i] ["manaCost"])))
  out.append ('<type>{}</type>\n'.format (str (data [i] ["race"]))) 
  out.append ('<pt>{}</pt>\n'.format (str (data [i] ["baseData"] ["attack"]) + "/" + str (data [i] ["baseData"] ["defense"])))
  out.append ('<tablerow>{}</tablerow>\n'.format ( str (tablerow [data [i] ["type"]])))
  out.append ('<text>{}</text>\n'.format (str (data [i] ["baseData"] ["description"].replace ('<br>', ' ').replace ('&', 'and'))))
  out.append ('</card>')
  if data [i] ["type"] == "Follower":
    evo_out = list ()
    evo_out.append ('<card>')
    evo_out.append ('<name>{} EVOLVED</name>\n'.format ( str (data [i] ["name"]).replace ('&', 'and')))
    evo_out.append ('<set picURL="https://shadowverse-portal.com/image/card/en/E_{}.png"></set>\n'.format (str (data [i] ["id"])))
    evo_out.append ('<color>{}</color>\n'.format (str (data [i] ["faction"])))
    evo_out.append ('<manacost>{}</manacost>\n'.format (str (data [i] ["manaCost"])))
    evo_out.append ('<cmc>{}</cmc>\n'.format (str (data [i] ["manaCost"])))
    evo_out.append ('<type>{}</type>\n'.format (str (data [i] ["race"]))) 
    evo_out.append ('<pt>{}</pt>\n'.format (str (data [i] ["evoData"] ["attack"]) + "/" + str (data [i] ["evoData"] ["defense"])))
    evo_out.append ('<tablerow>{}</tablerow>\n'.format (str (tablerow [data [i] ["type"]])))
    evo_out.append ('<text>{}</text>\n'.format (str (data [i] ["evoData"] ["description"].replace ('<br>', ' ').replace ('&', 'and'))))
    evo_out.append ('<token>1</token>')
    evo_out.append ('</card>')
    for i in range (len (evo_out)):
      h.write (evo_out [i])
  if istoken:
    for i in range (len (out)):
      h.write (out [i])
  else:
    for i in range (len (out)):
      g.write (out [i])
g.write ('</cards>')
g.write ('</cockatrice_carddatabase>')
h.write ('</cards>')
h.write ('</cockatrice_carddatabase>')
g.close ()
h.close ()



                                                                                                                                               
