from random import choice
from json import load
from os.path import dirname, realpath


def initCardLib(craft='Shadow'):
    """Initializes the card library that the various decks will be based on.

    :param craft: the craft whose card library you want to initialize - options: 'Rune', 'Sword', Shadow', Forest',
    'Haven', 'Blood', 'Portal' (case sensitive!)
    :returns lib, data
    :rtype lib: a list of card names
    :rtype data: a dictionary mapping the name of every card in the library to its various attributes.
    Example of the structure of an element:

    >>> card_data["Robogoblin"].keys()
    dict_keys(['name', 'faction', 'race', 'expansion', 'type', 'manaCost', 'baseData', 'evoData', 'rot', 'pps', 'tags'])

    >>> card_data["Robogoblin"].values()
    dict_values(['Robogoblin', 'Neutral', 'Machina', 'Steel Rebellion', 'Follower', 2,
    {'description': 'Last Words: Put a Repair Mode into your hand.', 'attack': 2, 'defense': 2},
    {'description': '(Same as the unevolved form.)', 'attack': 4, 'defense': 4}, 'Rotation', [2], ['mech', 'lw']])
    """
    with open("{}/Neutral.json".format(dirname(realpath(__file__))), 'r') as f:
        data = load(f)
        f.close()
    with open("{}/{}craft.json".format(dirname(realpath(__file__)), craft), 'r') as f:
        tmp = load(f)
        for i in list(tmp):
            data[i] = tmp[i]
        f.close()
    tmp = list(data)
    sorted_indexes = sorted(range(len(tmp)), key=lambda x: (data[tmp[x]]["manaCost"],
                                                            data[tmp[x]]["tags"],
                                                            data[tmp[x]]["type"]))
    '''
    This sorting phase encourages the creation of low-order schemata (in this case, synergistic card packages) by 
    clumping similar cards in the same genetic locus.
    '''
    lib = [tmp[i] for i in sorted_indexes]
    return lib, data


card_lib, card_data = initCardLib()


def indexToName(index):
    return card_lib[index]


def indexToAttrs(index):
    return card_data[card_lib[index]]


def nameToIndex(name):
    matches = []
    for i in card_lib:
        if name in i.lower():
            matches.append(i)
    if len(matches) == 1:
        return card_lib.index(matches[0])
    x = int(input('matches: {}\n'.format(matches)))
    print(matches[x])
    return card_lib.index(matches[x])


def nameToAttrs(name):
    return card_data[card_lib.index(name)]


class Deck:
    def __init__(self, other=[0] * len(card_lib)):
        """Initializes the deck to one passed by the user or to a random one.

        :param other: a list of ints between 0 and 3, the ith element represents the number of copies of the ith card
        in the library that are included in the deck
        .. warning:: len(other) == len(card_lib), -1 < other[i] < 4
        """
        self.setCards(other)
        self.setRandDeck()  # this does nothing if other is already a 40-cards sized deck
        self.setUsedCards()

    cards = []
    '''the structure of this variable is explained in the init'''

    def getCards(self):
        return self.cards

    def setCards(self, cards):
        self.cards = cards

    def __len__(self):
        """
        :return: the deck size
        .. note:: in order not to confuse len(self) with len(self.cards), len(card_lib) is called when the second
        quantity is needed
        """
        return sum(self.cards)

    def __getitem__(self, item):
        return self.cards[item]

    def __setitem__(self, item, value):
        """
        .. note:: doesn't update used_cards
        """
        self.cards[item] = value

    used_cards = []
    '''
    A list of ints representing the library indexes of the cards that are being used in the deck, each one appearing 
    n times, where n is the number of copies of that card included in the deck (for example if the 6th card in the 
    library is a 2of this list will contain 2 instances of 6). 
    '''

    def getUsedCards(self):
        return self.used_cards

    def setUsedCards(self):
        result = []
        for i in range(len(card_lib)):
            if self[i] > 0:
                for j in range(self[i]):
                    result.append(i)
        self.used_cards = result

    def addSingle(self, card):
        """Increases the number of copies of self[card] by 1 if possible.

        :param card: a library index
        :returns True or False, whether, respectively, adding that card was possible or not.
        """
        if self[card] < 3:
            self[card] += 1
            self.used_cards.append(card)
            return True
        return False

    def removeSingle(self, card):
        """Decreases the number of copies of self[card] by 1 if possible.

        :param card: a library index
        """
        if self[card] > 0:
            self[card] -= 1
            self.used_cards.remove(card)

    def addRandSingle(self):
        """Adds a random card to the deck."""
        added = False
        while not added:
            card = choice([i for i in range(len(card_lib))])
            added = self.addSingle(card)

    def removeRandSingle(self):
        """Removes a random card from the deck."""
        self.removeSingle(choice(self.used_cards))

    rating = 0  # an integer between 0 and 1 representing how good the deck is according to some arbitrary parameters

    def getRating(self):
        return self.rating

    def rate(self, tag=''):
        """
        :param tag: possible options so far:
            > 'evo'
            > 'nat'
        .. note:: it's recommended to call rate as few times as possible, as in its target implementation it will
        be the most computationally expensive part of the algorithm
        .. todo:: more rating parameters
        """
        # rating based on consistency, 14 being the least number of unique cards that one can make a deck with
        consistency = 14 / len([i for i in self.cards if i > 0])
        # rating based on the number of cards with a certain tag in the deck
        tags = len([i for i in self.used_cards if tag in indexToAttrs(i)["tags"]]) / 40
        self.rating = (consistency + tags) / 2

    def setRandDeck(self):
        """Completes a deck of less than 40 cards by adding random cards."""
        while len(self) < 40:
            self.addRandSingle()

    def __str__(self):
        """Prints out the deck in a readable format."""
        card_list = list(dict.fromkeys(self.used_cards))
        card_list.sort()  # stripping self.used_cards from repetitions and sorting
        for i in card_list:
            print("[{}] {}x {}".format(i, self.used_cards.count(i), card_lib[i]))
        return '\n'

    def readjust(self, deck1, deck2):
        candidates = deck1.used_cards + deck2.used_cards
        while len(self) != 40:
            if len(self) > 40:
                self.removeRandSingle()
            elif len(self) < 40:
                random_candidate = choice(candidates)
                self.addSingle(random_candidate)
                candidates.remove(random_candidate)

    def mix(self, other, method='SPC'):
        """Recombines two decks into a third one.

        :type other: Deck
        :param method: the kind of crossover to be used - the options are:
            > 'RP' (random picker)
            > 'SPC' (single point crossover)
            > 'DSPC' (dense single point crossover) (made on used_cards instead that on cards)
        :rtype result: Deck
        """
        dummy_deck = [1] * 40 + [0] * (len(card_lib) - 40)
        result = Deck(dummy_deck)
        result.setCards([0] * len(card_lib))  # as it's not allowed to initialize empty decks
        result.setUsedCards()
        if method == 'RP':
            '''Random cards are picked from a shared pool of the parents'.'''
            result.readjust(self, other)
        elif method == 'SPC':
            '''
            The parent cards lists are split into two segments along a randomly chosen point, and a child is created by 
            appending the second segment of one to the first of the other. Cards are randomly removed or added to
            readjust the deck size.
            '''
            crossover = choice([i for i in range(len(card_lib))])
            result.setCards(self[crossover:] + other[:crossover])
            result.readjust(self, other)
        elif method == 'DSPC':
            crossover = choice([i for i in range(len(card_lib))])
            for i in self.used_cards[:crossover]:
                result.addSingle(i)
            for i in other.used_cards[crossover:]:
                result.addSingle(i)
            result.readjust(self, other)
        # elif method == 'PMX':
        #     start = choice([i for i in range(40)])
        #     end = choice([i for i in range(40)])
        #     start, end = min(start, end), max(start, end)
        #     for i in range(start, end):
        #         result.addSingle(self.used_cards[i])  # 1
        #     candidates = []
        #     for i in range(start, end):
        #         if other.used_cards[i] not in result.used_cards:
        #             candidates.append(other.used_cards[i])  # 2
        #     for i in candidates:
        #         index = other.used_cards.index(i)
        #         while True:
        #             if self.used_cards[index] in other.used_cards:  # i
        #                 lookup_index = other.used_cards.index(self.used_cards[index])  # ii
        #                 if start < other.used_cards[lookup_index] < end:
        #                     index = lookup_index
        #                     pass  # iii
        #                 else:
        #                     result.addSingle(i)
        #                     break  # iv
        #     result.readjust(other, other)
        return result

    def mutate(self, method='PM'):
        """Stochastically modifies a part of the deck.

        :param method: the mutation algorithm to be used - the options are:
            >'PM' (plain mutation)
        """
        if method == 'PM':
            '''
            Removes a random card from the deck and replaces it with a random card from the library.
            '''
            self.removeRandSingle()
            self.addRandSingle()
