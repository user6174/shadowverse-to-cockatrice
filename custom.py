g = open("/home/makra/SV_COCKATRICE/sv_custom.xml",'a')
#g.write( '<cockatrice_carddatabase version="3">')
#g.write( '<cards>')
while(raw_input("0 when completely done\n"))!='0':
  isfollower=0
  g.write('<card>')
  x=raw_input("name")
  g.write( '<name>' + str(x) + '</name>')
  g.write( '<set>' + 'Brigade of the Sky' + '</set>')
  if raw_input("follower? y/n:\n")=='y':
    isfollower=1
  y = raw_input("craft?")
  g.write( '<color>' + str(y) + '</color>')
  w = raw_input("cost?")
  g.write( '<manacost>'+str(w)+'</manacost>')
  z = raw_input("officer/commander/mysteria/ER/etc")
  g.write( '<type>' + str(z) + '</type>') 
  g.write( '<pt>' + str(raw_input("attack")) + "/" + str(raw_input("defense")) + '</pt>')
  if isfollower==1:
          g.write('<tablerow>2</tablerow>')
  else:
      g.write( '<tablerow>' + str(raw_input("1 amulet, 3 spell") + '</tablerow>'))
  g.write( '<text>' + str(raw_input("description")) + '</text>')
  e = raw_input("token?y/n")=='y'
  if e:             
    g.write( '<token>1</token>')
  g.write( '</card>')
  if isfollower==1:
    g.write( '<card>')
    g.write( '<name>' + str(x) + ' EVOLVED</name>')
    g.write( '<color>' + str(y) + '</color>')
    g.write( '<manacost>'+str(w)+'</manacost>')
    g.write( '<type>' + str(z) + '</type>') 
    g.write( '<pt>' + str(raw_input("evo atk")) + "/" + str(raw_input("evo def") + '</pt>'))
    g.write( '<tablerow>2</tablerow>')
    g.write( '<text>' + str(raw_input("evo description")) + '</text>')
    if e:             
      g.write( '<token>1</token>')
    g.write( '</card>')
g.close()
