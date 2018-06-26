# -*- coding: utf-8 -*-
import json

tablerow = {"Follower":2,"Spell":3,"Amulet":1}
#1 → non-creature, non-land permanents (like Planeswalkers, Enchantments, and Artifacts)
#2 → creatures (this includes all cards that have the "creature" type like "Enchantment Creature")
#3 → non-permanent cards (like Instants and Sorceries)

f = open("/PATH/TO/sv_database.json")
g = open("/PATH/TO/sv_database.xml",'w')
h = open("/PATH/TO/sv_tokens.xml",'w')
g.write( '<cockatrice_carddatabase version="3">')
g.write( '<cards>')
h.write( '<cockatrice_carddatabase version="3">')
h.write( '<cards>')

data = json.load(f)
for i in data:
  out=list()
  out.append( '<card>')
  out.append( '<name>' + str(data[i]["name"]) + '</name>')
  out.append( '<set>' + str(data[i]["expansion"]) + '</set>')
  out.append( '<set picURL="https://shadowverse-portal.com/image/card/en/C_' + str(data[i]["id"]) + '.png"></set>')
  if data[i]["type"]=="Follower":
    out.append( '<related>' + str(data[i]["name"]) + ' EVOLVED</related>')
  for j in data:
    if data[j]["name"] in data[i]["baseData"]["description"]:
      out.append( '<related>' + str(data[j]["name"]) + ' </related>')
  out.append( '<color>' + str(data[i]["faction"]) + '</color>')
  out.append( '<manacost>'+str(data[i]["manaCost"])+'</manacost>')
  out.append( '<cmc>'+str(data[i]["manaCost"])+'</cmc>')
  out.append( '<type>' + str(data[i]["race"]) + '</type>') 
  out.append( '<pt>' + str(data[i]["baseData"]["attack"]) + "/" + str(data[i]["baseData"]["defense"]) + '</pt>')
  out.append( '<tablerow>' + str(tablerow[data[i]["type"]]) + '</tablerow>')
  out.append( '<text>' + str(data[i]["baseData"]["description"].replace('<br>',' ')) + '</text>')
  if data[i]["expansion"] == "Token":
    out.append( '<token>1</token>')
  out.append( '</card>')
  if data[i]["type"]=="Follower":
    out.append( '<card>')
    out.append( '<name>' + str(data[i]["name"]) + ' EVOLVED</name>')
    out.append( '<set picURL="https://shadowverse-portal.com/image/card/en/E_' + str(data[i]["id"]) + '.png"></set>')
    out.append( '<color>' + str(data[i]["faction"]) + '</color>')
    out.append( '<manacost>'+str(data[i]["manaCost"])+'</manacost>')
    out.append( '<cmc>'+str(data[i]["manaCost"])+'</cmc>')
    out.append( '<type>' + str(data[i]["race"]) + '</type>') 
    out.append( '<pt>' + str(data[i]["evoData"]["attack"]) + "/" + str(data[i]["evoData"]["defense"]) + '</pt>')
    out.append( '<tablerow>' + str(tablerow[data[i]["type"]]) + '</tablerow>')
    out.append( '<text>' + str(data[i]["evoData"]["description"].replace('<br>',' ')) + '</text>')
    if data[i]["expansion"] == "Token":
      out.append( '<token>1</token>')
    out.append( '</card>')
  if data[i]["expansion"]=="Token":
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



                                                                                                                                               
