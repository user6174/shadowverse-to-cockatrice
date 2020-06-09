### How to use

Should you find that the .json isn't up to date, you can get it [here](https://sv.bagoum.com/cardsFullJSON/en). Run `converter.py` in the same folder you placed `en.json` in. 
`sv_cards.xml` and `sv_tokens.xml` should appear in that same folder.

* Install [Cockatrice](https://github.com/Cockatrice/Cockatrice/releases/latest)
* Follow the instructions. If you wish, you can skip the MTG database download in `Source selection` by passing `empty.json`, and in `Tokens import` by typing in any site (e.g. google.com).
* When prompted to the `Card Database section`, hit `Disable all sets`.
* `Cockatrice > Settings... > General > Path > Token Database`: select `sv_tokens.xml`.
* `Cockatrice > Settings... > General > Path > Card Database`: select`sv_cards.xml`.
* `Cockatrice > Settings... > General > Card Sources`: remove the default Download URLs (if any).

### Tips for filtering cards
![](https://github.com/user6174/Shadowverse-to-Cockatrice/blob/master/card_filter_example.png)
* the CMC condition excludes token cards (the sets filters don't work as expected).
* the standard condition filters for Rotation legal cards.
