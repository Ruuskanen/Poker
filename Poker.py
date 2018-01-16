import random
import sys
import copy

class Player:
	def __init__(self, name):
		self.name = name
		self.position = 0
		self.holeCards = []
		self.allCards = []
		self.bestHand = []
		self.lastHand = []
		self.valuesOfHands = []
		self.namesOfHands = []
		
class Card:
	def __init__(self, value, suit, name):
		self.value = value
		self.suit = suit
		self.name = name
		
def makePlayingCards():
	cards = []
	suits = ["h", "d", "s", "c"]
	for i in range(0, 4):
		for j in range(2, 15):
			if j <= 10:
				name = str(j)
			elif j == 11:
				name = "J"
			elif j == 12:
				name = "Q"
			elif j == 13:
				name = "K"
			elif j == 14:
				name = "A"
			card = Card(j, suits[i], name)
			cards.append(card)
	return cards
	
def shuffleTheDeck(cards):
	deck = []
	ints = []
	for i in range(0, 52):
		ints.append(i)
	while len(ints)	> 0:
		number = random.choice(ints)
		deck.append(cards[number])
		ints.remove(number)
	return deck

def dealAHand(player): # Funktio lisää argumenttina olevalle pelaajalle aloituskäden
	holeCards = []
	for i in range(0, 2):
		holeCards.append(deck[0])
		del deck[0]
		player.holeCards = holeCards
	
def dealCommunityCards():
	burnCards.append(deck[0])
	del deck[0]
	if len(communityCards) == 0: # Flop
		for i in range(0, 3):
			communityCards.append(deck[0])
			del deck[0]
	elif len(communityCards) == 3: # Turn
		communityCards.append(deck[0])
		del deck[0]
	elif len(communityCards) == 4: # River
		communityCards.append(deck[0])
		del deck[0]
					
def calculateCardAmounts():
	cardsInHands = 2 * len(players)
	print("Kortteja käsissä: " + str(cardsInHands) + ", pöydällä: " + str(len(communityCards)) + ", pakassa: " + str(len(deck)) + ", poistettu pelistä: " + str(len(burnCards)))
	print("Yhteensä: " + str((cardsInHands + len(communityCards) + len(deck) + len(burnCards))))
	
def combineHoleCardsWithCommunity(player):
	player.allCards = []
	combined = []
	for card in player.holeCards:
		combined.append(card)
	for card in communityCards:
		combined.append(card)
	i = len(combined)
	for i in range(0, i):
		highest = combined[0].value
		index = 0
		for j, card in enumerate(combined):
			if card.value > highest:
				highest = card.value
				index = j
		player.allCards.append(combined[index])
		del combined[index]
		
def checkForStraightFlush(player): #1
	x = copy.deepcopy(player.allCards)
	player.lastHand = []
	suits = [[], [], [], []]
	for card in x:
		if card.suit == "h":
			suits[0].append(card)
		elif card.suit == "s":
			suits[1].append(card)
		elif card.suit == "d":
			suits[2].append(card)
		elif card.suit == "c":
			suits[3].append(card)
	for suit in suits:
		if len(suit) >= 5:
			if suit[0].value == 14:
				suit.append(Card(1, suit[0].suit, suit[0].name))
			for i in range(0, len(suit) - 4):
				if suit[i].value == suit[i + 1].value + 1:
					if suit[i + 1].value == suit[i + 2].value + 1:
						if suit[i + 2].value == suit[i + 3].value + 1:
							if suit[i + 3].value == suit[i + 4].value + 1:
								player.namesOfHands.append("a straight flush")
								player.valuesOfHands.append(1)
								for j in range(0, 5):
									player.lastHand.append(suit[i + j])
								break
	if player.bestHand == []:
		player.bestHand = copy.deepcopy(player.lastHand)
		
def checkForFourOfAKind(player): #2
	x = copy.deepcopy(player.allCards)
	player.lastHand = []
	for i in range(0, len(x) - 3):
		if x[i].value == x[i + 1].value:
			if x[i + 1].value == x[i + 2].value:
				if x[i + 2].value == x[i + 3].value:
					player.namesOfHands.append("four of a kind")
					player.valuesOfHands.append(2)
					for j in range(0, 4):
						player.lastHand.append(x[i + j])
					for k in range(0, 4):
						del x[i]
					highest = x[0].value
					index = 0
					for l, card in enumerate(x):
						if card.value > highest:
							highest = card.value
							index = j
					player.lastHand.append(x[index])
					break
	if player.bestHand == []:
		player.bestHand = copy.deepcopy(player.lastHand)
	
def checkForFullHouse(player): #3
	x = copy.deepcopy(player.allCards)
	player.lastHand = []
	for i in range(0, len(x) - 2):
		if x[i].value == x[i + 1].value:
			if x[i + 1].value == x[i + 2].value:
				for j in range(0, 3):
					player.lastHand.append(x[i])
					del x[i]
				for k in range(0, len(x) - 1):
					if x[k].value == x[k + 1].value:
						player.lastHand.append(x[k])
						player.lastHand.append(x[k + 1])
						player.namesOfHands.append("a full house")
						player.valuesOfHands.append(3)
						if player.bestHand == []:
							player.bestHand = copy.deepcopy(player.lastHand)
						break
				break
	
def checkForFlush(player): #4
	x = copy.deepcopy(player.allCards)
	player.lastHand = []
	suits = [[], [], [], []]
	for card in x:
		if card.suit == "h":
			suits[0].append(card)
		elif card.suit == "s":
			suits[1].append(card)
		elif card.suit == "d":
			suits[2].append(card)
		elif card.suit == "c":
			suits[3].append(card)
	for suit in suits:
		if len(suit) >= 5:
			for i in range(0, 5):
				player.lastHand.append(suit[i])
			player.namesOfHands.append("a flush")
			player.valuesOfHands.append(4)
	if player.bestHand == []:
		player.bestHand = copy.deepcopy(player.lastHand)
	
def checkForStraight(player): #5
	x = copy.deepcopy(player.allCards)
	player.lastHand = []
	removeDuplicateValues(x)
	if x[0].value == 14:
		x.append(Card(1, x[0].suit, x[0].name))
	if len(x) >= 5:
		for i in range(0, len(x) - 4):
			if x[i].value == x[i + 1].value + 1:
				if x[i + 1].value == x[i + 2].value + 1:
					if x[i + 2].value == x[i + 3].value + 1:
						if x[i + 3].value == x[i + 4].value + 1:
							player.namesOfHands.append("a straight")
							player.valuesOfHands.append(5)
							for j in range(0, 5):
								player.lastHand.append(x[i + j])
						break
	if player.bestHand == []:
		player.bestHand = copy.deepcopy(player.lastHand)
		
def checkForThreeOfAKind(player): #6
	x = copy.deepcopy(player.allCards)
	player.lastHand = []
	for i in range(0, len(x) - 2):
		if x[i].value == x[i + 1].value:
			if x[i + 1].value == x[i + 2].value:
				for j in range(0, 3):
					player.lastHand.append(x[i])
					del x[i]
				for k in range(0, 2):
					player.lastHand.append(x[0])
					del x[0]
				player.namesOfHands.append("three of a kind")
				player.valuesOfHands.append(6)
				break	
	if player.bestHand == []:
		player.bestHand = copy.deepcopy(player.lastHand)
						
def checkForTwoPair(player): #7
	x = copy.deepcopy(player.allCards)
	player.lastHand = []
	for i in range(0, len(x) - 1):
		if x[i].value == x[i + 1].value:
			for j in range(0, 2):
				player.lastHand.append(x[i])
				del x[i]
			for k in range(0, len(x) - 1):
				if x[k].value == x[k + 1].value:
					for l in range(0, 2):
						player.lastHand.append(x[k])
						del x[k]
					player.lastHand.append(x[0])
					player.namesOfHands.append("two pair")
					player.valuesOfHands.append(7)
					if player.bestHand == []:
						player.bestHand = copy.deepcopy(player.lastHand)
					break
			break

def checkForPair(player): #8
	x = copy.deepcopy(player.allCards)
	player.lastHand = []
	for i in range(0, len(x) - 1):
		if x[i].value == x[i + 1].value:
			for j in range(0, 2):
				player.lastHand.append(x[i])
				del x[i]
			for k in range(0, 3):
				player.lastHand.append(x[0])
				del x[0]
			player.namesOfHands.append("a pair")
			player.valuesOfHands.append(8)
			break	
	if player.bestHand == []:
		player.bestHand = copy.deepcopy(player.lastHand)

def checkForHighHard(player): #9
	x = copy.deepcopy(player.allCards)
	player.lastHand = []
	for i in range(0, 5):
		player.lastHand.append(x[0])
		del x[0]
	player.namesOfHands.append("a high card")
	player.valuesOfHands.append(9)
	if player.bestHand == []:
		player.bestHand = copy.deepcopy(player.lastHand)

def determineBestHand(player):
	player.namesOfHands = []
	player.valuesOfHands = []
	player.bestHand = []
	combineHoleCardsWithCommunity(player)
	checkForStraightFlush(player) #1
	checkForFourOfAKind(player) #2
	checkForFullHouse(player) #3
	checkForFlush(player) #4
	checkForStraight(player) #5
	checkForThreeOfAKind(player) #6
	checkForTwoPair(player) #7
	checkForPair(player) #8
	checkForHighHard(player) #9
			
def removeDuplicateValues(list):
	duplicates = []
	for i in range(0, len(list) - 1):
		if list[i].value == list[i + 1].value:
			duplicates.append(i)
	j = len(duplicates) - 1
	while j >= 0:
		index = duplicates[j]
		del list[index]
		j -= 1

def printCards(cards): # Funktio tulostaa argumenttina olevassa listassa olevat kortit.
	for card in cards:
		sys.stdout.write((card.name + card.suit).ljust(4))
	print()
	
def printBestHands():
	for i, player in enumerate(players):
		sys.stdout.write((player.name + " has " + player.namesOfHands[0] + ".").ljust(30))
		if player.position != 0:
			sys.stdout.write("(" + str(player.position) + ")".ljust(2))
			if player.position == 1:
				print("Winner!")
			else:
				print()
		else:
			print()
		for card in player.bestHand:
			sys.stdout.write((card.name + card.suit).ljust(4))
		if i != len(players) - 1:
			if players[i].position == players[i + 1].position:
				print("|".rjust(12))
				print("|".rjust(32))
			else:
				print()
				print()
	
def printHoleAndCommunityCards():
	for player in players:
		sys.stdout.write(player.name.ljust(12))
		for card in player.holeCards:
			sys.stdout.write((card.name + card.suit).ljust(4))
		print()
	print()
	sys.stdout.write("Community:  ")
	printCards(communityCards)
	print()

# Deal hands for players and determine the best hand.

cards = makePlayingCards()
deck = shuffleTheDeck(cards)
communityCards = []
burnCards = []
players = []

names = ["P1", "P2", "P3", "P4", "P5", "P6", "P7"]
	
for name in names:
	players.append(Player(name))

for player in players:
	dealAHand(player)

dealCommunityCards()
dealCommunityCards()
dealCommunityCards()

printHoleAndCommunityCards()

for player in players:
	determineBestHand(player)
						
while True:
	change = False
	for i in range(0, len(players) - 1):
		if players[i + 1].valuesOfHands[0] < players[i].valuesOfHands[0]:
			players[i], players[i + 1] = players[i + 1], players[i]
			change = True
		elif players[i + 1].valuesOfHands[0] == players[i].valuesOfHands[0]:
			for j in range(0, 5):
				if players[i + 1].bestHand[j].value != players[i].bestHand[j].value:
					if players[i + 1].bestHand[j].value > players[i].bestHand[j].value:
						players[i], players[i + 1] = players[i + 1], players[i]
						change = True
						break
					else:
						break
	if change == False:
		break
		
for i in range(0, len(players)):
	if i == 0:
		players[i].position = 1
	else:
		difference = False
		for j in range(0, 5):
			if players[i].bestHand[j].value != players[i - 1].bestHand[j].value:
				difference = True
				break
		if difference == True:
			players[i].position = players[i - 1].position + 1
		else:
			players[i].position = players[i - 1].position

printBestHands()
