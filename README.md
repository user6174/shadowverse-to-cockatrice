### How to use
* grab `sv_cards.xml`, `sv_tokens.xml` and `empty.json`.
* Install [Cockatrice](https://github.com/Cockatrice/Cockatrice/releases/latest).
* Open Cockatrice and follow the setup instructions. Skip the MTG database download in `Source selection` by passing `empty.json`, and in `Tokens import` by typing in any site (e.g. google.com).
* When prompted to the `Card Database section`, hit `Disable all sets`.
* `Cockatrice > Settings > General > Path > Token Database`: select `sv_tokens.xml`.
* `Cockatrice > Settings > General > Path > Card Database`: select`sv_cards.xml`.
* `Cockatrice > Settings > General > Card Sources`: remove the default Download URLs (if any).
* `Cockatrice > Card Database > Manage Sets`: disable the Token set.

### Tips for filtering cards
![](https://github.com/user6174/Shadowverse-to-Cockatrice/blob/master/card_filter.png)
* the `standard` condition filters for Rotation legal cards.
