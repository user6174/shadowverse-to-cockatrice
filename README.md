Thanks to [Bagoum](https://sv.bagoum.com/) for providing the card database.

### How to use

1) Check if the provided `en.json` is up to date (ctrl+F a card name from the newest expansion). 
2) If it is, grab `sv_cards.xml` and `sv_tokens.xml` and go to `4.`
3) Else, get the updated json [here](https://sv.bagoum.com/cardsFullJSON/en). 
- Download and unzip the repository.
- Run `converter.py`. `sv_cards.xml` and `sv_tokens.xml` should appear in that same folder. 
- Make sure that they're parsable by Cockatrice by running `validate.sh`.
4) Install [Cockatrice](https://github.com/Cockatrice/Cockatrice/releases/latest).
5) Follow the instructions. If you wish, you can skip the MTG database download in `Source selection` by passing `empty.json`, and in `Tokens import` by typing in any site (e.g. google.com).
6) When prompted to the `Card Database section`, hit `Disable all sets`.
7) `Cockatrice > Settings > General > Path > Token Database`: select `sv_tokens.xml`.
8) `Cockatrice > Settings > General > Path > Card Database`: select`sv_cards.xml`.
9) `Cockatrice > Settings > General > Card Sources`: remove the default Download URLs (if any).
10) `Cockatrice > Card Database > Manage Sets`: disable the Token set.

### Tips for filtering cards

* the `standard` condition filters for Rotation legal cards.
