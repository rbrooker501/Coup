"""Program to play a game of Coup
Luna Brooker, 2023
"""

import random
import utils
import time


HAND_SIZE = 2
NUMBER_CARDS = 3
STARTING_COINS = 2
INQUISITOR = False
MOVES = ['income', 'foreign aid', 'tax', 'exchange', 'steal', 'assassinate']

ASSASSINATE_AMOUNT = 3
COUP_AMOUNT = 7
MUST_COUP = 10

class Player:
  def __init__(self, deck, coins, name):
    """Initializes an instance of the player class. 
    Arguments:
      `deck` (list) - The deck of remaining cards
      `coins` (int) - The number of coins a user has
      `name` (string) - The user's name
    """
    self.hand = self.generate_hand(deck)
    self.displayed_cards = ['---', '---']
    self.coins = coins
    self.name = name
    self.lives = HAND_SIZE

  def generate_hand(self, deck):
    """Generates a 2 card hand for the user given a deck of remaining cards
    Arguments:
      `deck` (list) - The deck of remaining cards
    Returns:
      `hand` (list) - The user's hand
    """
    hand = []
    for i in range(HAND_SIZE):
      idx = random.randint(0, len(deck)-1)
      hand.append(deck[idx])
      del deck[idx]
    return hand

  def has_duke(self):
    """Checks if the user has a Duke in their hand"""
    return 'duke' in self.hand
  
  def has_ambassador(self):
    """Checks if the user has an Ambassador in their hand"""
    return 'ambassador' in self.hand
  
  def has_captain(self):
    """Checks if the user has a Captain in their hand"""
    return 'captain' in self.hand

  def has_assassin(self):
    """Checks if the user has an Assassin in their hand"""
    return 'assassin' in self.hand

  def has_contessa(self):
    """Checks if the user has a Contessa in their hand"""
    return 'contessa' in self.hand
  
  def is_alive(self):
    if len(self.hand) != 0:
      return True
    return False

class Game:
  def __init__(self, n_players):
    self.players = n_players
    self.deck = self.generate_deck()

  def generate_deck(self):
    deck = []
    if not INQUISITOR:
      cards = ['duke', 'ambassador', 'captain', 'assassin', 'contessa']
    else:
      cards = ['duke', 'inquisitor', 'captain', 'assassin', 'contessa']
    
    for i in cards:
      for j in range(NUMBER_CARDS):
        deck.append(i)
    
    random.shuffle(deck)
    return deck

def exchange(hand, deck):
  cards = []
  for card in hand:
    cards.append(card)
  kept = []
  for i in range(2):
    cards.append(deck[i])
  del deck[0]
  del deck[0]
  for j in range(len(hand)):
    for k in range(len(cards)):
      print(f'{k}: {cards[k]}')
    keep = int(input('Which card do you want to keep? (enter an index) '))
    kept.append(cards[keep])
    del cards[keep]

  for l in cards:
    deck.append(l)
  random.shuffle(deck)


  return (kept, deck)

def steal(player, target):
  if target.coins < 2:
    player.coins += target.coins
    target.coins = 0
  else:
    player.coins += 2
    target.coins -= 2
  
def lose_life(player):
  for i, card in enumerate(player.hand):
    print(f"{i}: {card} ")

  discard = int(input("Which card would you like to discard (enter an index)? "))
  while discard > len(player.hand) - 1 or discard < 0:
    print("Please enter a valid index.")
    discard = input("Which card would you like to discard (enter an index)? ")
  discarded = player.hand.pop(discard)
  del player.displayed_cards[0]
  player.displayed_cards.append(discarded)

def block(player, other_player, action):
  print(f'{player.name} is attempting to {action}.')
  utils.cls()
  print(f'Your hand: {other_player.hand}')
  block = input(f"{other_player.name}: Would you like to block this action (yes or no)? ").lower()
  if block == 'yes':
    return True
  else: 
    return False

def challenge_result(player, other_player, result, card):
  if card == 'ambassador':
    article = 'an'
  else:
    article = 'a'
    
  if result:
    print(f'Nice job! {other_player.name} doesn\'t have {article} {card.title()}!')
    time.sleep(3)
    utils.cls()
    print(other_player.name)
    lose_life(other_player)
  else:
    print(f'Bad news!! {other_player.name} has {article} {card.title()}!')
    print(player.name)
    lose_life(player)
  return result

def challenge(player, other_player, action, card=None):
  """Challenges an action or a block.
  Arguments:
    `player` (Player object) - The player challenging
    `other_player` (Player object) - The player being challenged
    `action` (string) - The action being challenged
    `card` (string) - The card being challenged (defaults to 'None')
  Returns:
    `True` if challenge was successful
    `False` if challenge was not successful
    `None` if user decides not to challenge
  """
  match card:
    case 'ambassador':
      if action == 'block':
        print(f'{other_player.name} is attempting to block your steal with their {card}')
      else:
        print(f'{other_player.name} is attempting to {action}.')
      
      challenge = input('Would you like to challenge this (yes or no) ').lower()
      if challenge == 'yes':
        if other_player.has_ambassador():
          return challenge_result(player, other_player, False, card)
        else:
          return challenge_result(player, other_player, True, card)
    case 'assassin':
      print(f'{other_player.name} is attempting to {action} you.')

      challenge = input('Would you like to challenge this (yes or no) ').lower()
      if challenge == 'yes':
        if other_player.has_assassin():
          return challenge_result(player, other_player, False, card)
        else:
          return challenge_result(player, other_player, True, card)
    case 'captain':
      if action == 'block':
        print(f'{other_player.name} is attempting to block your steal with their {card}')
      else:
        print(f'{other_player.name} is attempting to {action}.')

      challenge = input('Would you like to challenge this (yes or no) ').lower()
      if challenge == 'yes':
        if other_player.has_captain():
          return challenge_result(player, other_player, False, card)
        else:
          return challenge_result(player, other_player, True, card)
    case 'contessa':
      print(f'{other_player.name} is attempting to block your {action} with their {card}')
      challenge = input('Would you like to challenge this (yes or no) ').lower()
      if challenge == 'yes':
        if other_player.has_contessa():
          return challenge_result(player, other_player, False, card)
        else:
          return challenge_result(player, other_player, True, card)
    case 'duke':
        if action == 'foreign aid':
          print(f'{other_player.name} is attempting to block your {action}.')
        elif action == 'tax':
          print(f'{other_player.name} is attempting to {action}.')

        challenge = input('Would you like to challenge this (yes or no) ').lower()
        if challenge == 'yes':
          if other_player.has_duke():
            return challenge_result(player, other_player, False, card)
          else:
            return challenge_result(player, other_player, True, card)

def challenge_ask(player, player_list, action, card):
  """Loops through each player and asks if they want to challenge an action.
  If yes, challenges the action by calling the challenge() function
  (use help challenge() for implementation details.)
  Arguments:
    `player` (Player object) - The player being challenged
    `player_list` (list) - A list of player objects to iterate through
    `action` (string) - The action being challenged
    `card` (string) - The card being challenged
  Returns:
    `True` if the challenge was successful
    `False` otherwise
  """
  for other_player in player_list:
    utils.cls()
    challenged = challenge(other_player, player, action, card)
    print(challenged)
    if challenged is not None:
      break

  return challenged == True

if __name__ == "__main__":
  players_list = []
  players = int(input('Enter a number of players (up to 6): '))
  while players > 6 or players < 2:
    print("Error: You cannot play with more than 6 or less than 2 players!")
    players = int(input('Enter a number of players (up to 6): '))
  game = Game(players)
  for i in range(players):
    name = input('Enter your name: ')
    player = Player(game.deck, STARTING_COINS, name)
    players_list.append(player)
    utils.cls()
  alive_players = players_list
  while True:
    for i in range(len(alive_players)):
      player = alive_players.pop(0)
      if player.is_alive():
        print(f'{player.name}\'s hand = {player.hand}')
        print(f'{player.name}\'s coins = {player.coins}')

        for person in players_list:
          print(f'Player: {person.name}, Hand: {person.displayed_cards}, Coins: {person.coins}')
        
        if player.coins >= COUP_AMOUNT:
          action = 'coup'
        action = input(f'What would you like to do, {player.name}? ').lower()
        while action not in MOVES:
          if action == 'help':
            print('Valid moves:\n')
            for j in MOVES:
              print(j)
          else:
            print('Invalid action! Please select a valid action.')
          action = input(f'What would you like to do, {player.name}? ').lower()

        if action == 'income':
          player.coins += 1
        elif action == 'foreign aid':
          for other_player in alive_players:
            if block(player, other_player, action):
              utils.cls()
              # Only one person gets to challenge this
              challenge(player, other_player, action, 'duke')
              break
          else:
            player.coins += 2
        elif action == 'tax':
          if not challenge_ask(player, alive_players, action, 'duke'):
            player.coins += 3
        elif action == 'exchange':
          if not challenge_ask(player, alive_players, action, 'ambassador'):
            hand, deck = exchange(player.hand, game.deck)
            player.hand = hand
            game.deck = deck     
        elif action == 'steal':
          for j in range(len(alive_players)):
            print(f"{j}: {alive_players[j].name}")
          target = int(input('Who would you like to steal from? (enter an index) '))
          if block(player, alive_players[target], action):
            card = input('Which card would you like to block with (ambassador or captain)? ').lower()
            challenge(player, alive_players[target], 'block', card)
          else:
            if not challenge(alive_players[target], player, action, 'captain'):
              steal(player, alive_players[target])
        elif action == 'assassinate':
          if player.coins > ASSASSINATE_AMOUNT:
            for j in range(len(alive_players)):
              print(f"{j}: {alive_players[j].name}")
            target = int(input('Who would you like to assassinate? (enter an index) '))
            player.coins -= ASSASSINATE_AMOUNT
            if block(player, alive_players[target], action):
              challenged = challenge(player, alive_players[target], action, 'contessa')
              if challenged is not None:
                if challenged:
                  lose_life(alive_players[target])
            else:
              challenge(alive_players[target], player, action, 'assassin')
          else:
            print('Sorry, you do not have enough coins to assassinate anybody!')
        elif action == 'coup':
          if player.coins > COUP_AMOUNT:
            for j in range(len(alive_players)):
              print(f"{j}: {alive_players[j].name}")
            target = int(input('Who would you like to coup? (enter an index) '))
            player.coins -= COUP_AMOUNT
            lose_life(alive_players[target])
          else:
            print('Sorry, you do not have enough coins to coup anybody!')
      else:
        del alive_players[0]
      players_list.append(player)
      utils.cls()

      if len(alive_players) < 2:
        print('Game over!')
        print(f'The winner is: {alive_players[0].name}!')
        exit()
  
  