file_cd = open("tmp_custom_cd.xml", 'a+')
file_tk = open("tmp_custom_tk.xml", 'a+')
tablerow = {"f":2, "s":3, "a":1}
fulltype = {"f":"Follower", "s":"Spell", "a":"Amulet"}

f = raw_input
def g(par, s):
    return '<{}>{}</{}>\n'.format(par, s, par)   

while True:
    out = []
    istoken = False
    x = f("next card? (y/done): ")
    if x == 'done':
        break
    elif x == 'y':
        out.append('<card>\n')
        cardname = f("card name: ")
        out.append(g('name', cardname)) # do not include '&' and other special characters in the name
        out.append(g('text', f('card text: ')))
        if f("token? (y/Enter): ") == 'y':
            istoken = True
            out.append('<token>1</token>')
        while True:
            try:
                cardtype = f("follower/spell/amulet? (f/s/a): ")
                break
            except KeyError:
                pass
        out.append(g('tablerow', tablerow[cardtype]))
        out.append('<set rarity="new" picurl="{}">0</set>\n'.format (f('image link: ')))
        y = f("related card names? (name/Enter)")
        while y != '':
            out.append(g('related', y))
            y = f("related card names? (name/Enter)")
        out.append('<prop>\n')
        out.append(g('type', f('trait? (trait/Enter):')))
        out.append(g('maintype', fulltype[cardtype]))
        pp = f("pp? ")
        out.append(g('manacost', pp))
        out.append(g('cmc', pp))
        craft = f("craft? ")
        out.append(g('colors', craft))
        out.append(g('coloridentity', craft))
        if cardtype == 'f':
            atk=f('atk? ')
            deff=f('def? ')
            out.append(g('pt', '{}/{}'.format(atk, deff)))
        else:
            out.append(g('pt', '0/0'))
        out.append('</prop></card>')

        if istoken:
            for i in out:
                file_tk.write(i)
        else:
            for i in out:
                file_cd.write(i)
file_cd.close()
file_tk.close()

file_cd = open("tmp_custom_cd.xml", 'r')
l = file_cd.read()
with open("custom_cd.xml", 'w') as cd:
    cd.write('''<?xml version="1.0" encoding="UTF-8"?>\n<cockatrice_carddatabase version="4">\n<cards>\n''')
    cd.write(l)
    cd.write('</cards>\n</cockatrice_carddatabase>')

file_tk = open("tmp_custom_tk.xml", 'r')
m = file_tk.read()
with open("custom_tk.xml", 'w') as cd:
    cd.write('''<?xml version="1.0" encoding="UTF-8"?>\n<cockatrice_carddatabase version="4">\n<cards>\n''')
    cd.writelines(m)
    cd.write('</cards>\n</cockatrice_carddatabase>')
