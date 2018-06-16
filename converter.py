# -*- coding: utf-8 -*-
import json

tablerow = {"Follower":2,"Spell":3,"Amulet":1}
#1 → non-creature, non-land permanents (like Planeswalkers, Enchantments, and Artifacts)
#2 → creatures (this includes all cards that have the "creature" type like "Enchantment Creature")
#3 → non-permanent cards (like Instants and Sorceries)

f = open("/home/sv_database.json")
g = open("/home/sv_database.xml",'w')
g.write( '<cockatrice_carddatabase version="3">')
g.write( '<cards>')

data = json.load(f)
for i in data:
  g.write( '<card>')
  g.write( '<name>' + str(data[i]["name"]) + '</name>')
  g.write( '<set>' + str(data[i]["expansion"]) + '</set>')
  g.write( '<set picURL="https://shadowverse-portal.com/image/card/en/C_' + str(data[i]["id"]) + '.png"></set>')
  g.write( '<related>' + str(data[i]["name"]) + ' EVOLVED</related>')
  g.write( '<color>' + str(data[i]["faction"]) + '</color>')
  g.write( '<manacost>'+str(data[i]["manaCost"])+'</manacost>')
  g.write( '<cmc>'+str(data[i]["manaCost"])+'</cmc>')
  g.write( '<type>' + str(data[i]["race"]) + '</type>') 
  g.write( '<pt>' + str(data[i]["baseData"]["attack"]) + "/" + str(data[i]["baseData"]["defense"]) + '</pt>')
  g.write( '<tablerow>' + str(tablerow[data[i]["type"]]) + '</tablerow>')
  g.write( '<text>' + str(data[i]["baseData"]["description"].replace('<br>',' ')) + '</text>')
  g.write( '<token></token>')
  g.write( '</card>')
  g.write( '<card>')
  g.write( '<name>' + str(data[i]["name"]) + ' EVOLVED</name>')
  g.write( '<set picURL="https://shadowverse-portal.com/image/card/en/E_' + str(data[i]["id"]) + '.png"></set>')
  g.write( '<color>' + str(data[i]["faction"]) + '</color>')
  g.write( '<manacost>'+str(data[i]["manaCost"])+'</manacost>')
  g.write( '<cmc>'+str(data[i]["manaCost"])+'</cmc>')
  g.write( '<type>' + str(data[i]["race"]) + '</type>') 
  g.write( '<pt>' + str(data[i]["evoData"]["attack"]) + "/" + str(data[i]["evoData"]["defense"]) + '</pt>')
  g.write( '<tablerow>' + str(tablerow[data[i]["type"]]) + '</tablerow>')
  g.write( '<text>' + str(data[i]["evoData"]["description"].replace('<br>',' ')) + '</text>')
  g.write( '<token></token>')
  g.write( '</card>')
g.write( '</cards>')
g.write( '</cockatrice_carddatabase>')
g.close()





                                                                                                                                               
