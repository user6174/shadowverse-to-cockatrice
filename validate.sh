xmllint --schema ./validator.xsd ./sv_cards.xml
read  -n 1 -p "Press any for validating tokens." var
xmllint --schema ./validator.xsd ./sv_tokens.xml