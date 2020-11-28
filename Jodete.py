import random
import names
from itertools import cycle, islice, chain
import time

initial_decks = 3
initial_players = 4
initial_hand = 7
game_suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
special_values = {
	"A": 15,
	"2": 20,
	"8": 30,
	"J": 10,
	"Q": 10,
	"K": 10,
	"Joker": 50
}


class Card:
	def __init__(self, rank, suit):
		self.rank = rank
		self.suit = suit
		self.card = (rank, suit)
		if self.rank in special_values:
			self.points = special_values[rank]
		else:
			self.points = int(rank)

	def __repr__(self):
		if self.rank == "Joker":
			return f"|{self.rank}|"
		else:
			return f"|{self.rank} of {self.suit}|"

	def __add__(self, p):
		return self.points + p.points


class Player:
	def __init__(self, name):
		self.name = name
		self.hand = []

	def __repr__(self):
		return self.name

	def play_card(self, card):
		if not is_valid(card):
			print("The play is not valid. JODETE! --> You draw 3 cards.")
			self.draw(3)
			return
		else:
			self.hand.remove(card)
			table.append(card)
			return card

	def draw(self, x):
		if len(deck) - 6 < x:
			shuffle()
		drawn = draw_from_deck(x)
		self.hand.extend(drawn)
		return drawn

	def calculate_points(self):
		points = 0
		for card in self.hand:
			points = points + card.points
		return points

	def next_play(self):
		""" Automation of plays by CP."""
		for card in self.hand:
			if is_valid(card):
				self.play_card(card)
				return card
		global forced_rank
		if forced_rank == "2":
			global two_multiplier
			self.draw(two_multiplier)
			print(f"{self.name} draws {str(two_multiplier)} cards.")
			two_multiplier = 0
			forced_rank = False
			return None
		card = self.draw(1)[0]
		print(self.name + " draws a card.")
		if is_valid(card):
			self.play_card(card)
			return card
		print(self.name + " passes the turn.")


def shuffle():
	tabletop = table[-1]
	deck.extend(table[0:-1])
	random.shuffle(deck)
	table.clear()
	table.append(tabletop)
	print("--> The table has been shuffled into de the deck. <--")


def choose_suit():
	return random.choice(game_suits)


def create_players(n):
	players = list()
	for i in range(n):
		players.append(Player(names.get_full_name()))
	return players


def create_deck(boxes, suits):
	a_deck = []
	special = {1: "A", 11: "J", 12: "Q", 13: "K"}

	for a in range(boxes):
		for i in range(1, 14):
			for suit in suits:
				if i in special:
					i = special[i]
				card = Card(str(i), suit)
				a_deck.append(card)
		jokers = [Card("Joker", "Joker")] * 2
		a_deck.extend(jokers)
	return a_deck


def draw_from_deck(y):
	cards_drawn = []
	for i in range(1, y+1):
		cards_drawn.append(deck.pop(random.randrange(len(deck)-1)))
	return cards_drawn


def start_game():
	players = create_players(initial_players - 1)
	user = input("What's your name? \n")
	players.append(Player(user))
	random.shuffle(players)

	for player in players:
		player.draw(initial_hand)

	table.extend(draw_from_deck(1))

	print("The game is starting. Players are, in order of the round:")
	time.sleep(2)
	for player in players:
		time.sleep(1)
		print("-- " + player.name)
	time.sleep(1)
	print("The top card of the deck is revealed:")
	time.sleep(1)
	print(table[-1])
	time.sleep(2)
	print(f"{players[0]} will begin.")

	return players, user


def is_valid(card):
	top = table[-1]
	valid_ranks = [top.rank, "8", "Joker"]
	if forced_rank:
		if card.rank != forced_rank:
			return False
	if card.rank in valid_ranks:
		return True

	if forced_suit:
		if card.suit == forced_suit:
			return True
		else:
			return False
	elif top.suit == card.suit:
		return True
	elif top.rank == card.rank:
		return True
	return False


def user_turn(user):
	print("It's your turn. what card will you play?")
	time.sleep(1)
	print("Tabletop:" + str(table[-1]))
	time.sleep(1)
	print("Your hand:")
	print(user.hand)
	global forced_rank
	global two_multiplier

	while True:
		user_play = input('Type the card as shown in your hand, or "pass" to draw a card. \n')
		if user_play.lower() == "pass":
			if forced_rank == "2":
				draw = user.draw(two_multiplier)
				print(f"You drew {str(two_multiplier)} cards: {draw}.")
				forced_rank = False
				two_multiplier = 0
				return
			else:
				draw = user.draw(1)[0]
				play_last_draw = input(f"You drew a {draw}. Want to play it? Y or N. \n")
				if play_last_draw.lower() == "y":
					print(f"You play a {draw}")
					play = user.play_card(draw)
					return play
				else:
					return
		else:
			card_input = user_play.split(" ")
			if len(card_input) == 3 or card_input[0].lower() == "joker":
				for card in user.hand:
					is_correct = card_input[0].lower() == "joker" and card.rank == "Joker"
					if not is_correct:
						is_correct = card_input[0].lower() == card.rank.lower() and card_input[2].lower() == card.suit.lower()
					if is_correct:
						print(f"You play a {card}")
						play = user.play_card(card)
						if forced_rank == "2" and not play:
							draw = user.draw(two_multiplier)
							print(f"You drew {str(two_multiplier)} cards: {draw}.")
							forced_rank = False
							two_multiplier = 0
							return
						return play
				print("Input not valid! Try again.")


def cp_turn(player):
	play = player.next_play()
	if play is not None:
		print(f"-- {player.name} plays a {play}.")
	return play


def end_of_game(winner, players):
	print(f" {winner.name} has no more cards in hand. The game ended!")
	print("The final points are:")
	for player in players:
		print(player.name + ": " + str(player.calculate_points()))
	exit()


def reverse_round(current_player):
	'''Returns a reversed cycle object starting with current player.'''
	players.reverse()
	reverse_players = cycle(players)
	while True:
		if next(reverse_players) == current_player:
			return reverse_players


def main(players_, user_):
	players_cycle = cycle(players_)
	global forced_suit
	global forced_rank
	current_player = next(players_cycle)

	while True:
		print("The length of the deck is " + str(len(deck)))
		if user_ == current_player.name:
			played = user_turn(current_player)
			if len(current_player.hand) == 0:
				end_of_game(current_player, players_)
			if played:
				if played.rank == "8" or played.rank == "Joker":
					suit = input("--> Choose a suit. \n")
					while True:
						lower_suits = [i.lower() for i in game_suits]
						if suit.lower() in lower_suits:
							forced_suit = game_suits[lower_suits.index(suit.lower())]
							break
						else:
							suit = input("Suit is not valid. Type a valid suit.\n")
				else:
					forced_suit = False

		else:
			played = cp_turn(current_player)
			time.sleep(1)
			if len(current_player.hand) == 0:
				end_of_game(current_player, players_)
			if played:
				if played.rank == "8" or played.rank == "Joker":
					forced_suit = choose_suit()
					print(f"-- {current_player.name} chose {forced_suit}.")
				else:
					forced_suit = False

		if played:
			if played.rank == "2":
				global forced_rank
				forced_rank = "2"
				global two_multiplier
				two_multiplier += 2

			if played.rank == "K":
				players_cycle = reverse_round(current_player)
			if played.rank == "J":
				next(players_cycle)
			if played.rank == "Q":
				next(players_cycle)
				next(players_cycle)
			if played.rank == "Joker":
				current_player = next(players_cycle)
				current_player.draw(4)
				print(f"{current_player} draws 4 cards.")
				continue
		current_player = next(players_cycle)


deck = create_deck(initial_decks, game_suits)
table = []

forced_rank = False
forced_suit = False
two_multiplier = 0

players, user = start_game()

main(players, user)


# todo shuffle deck

