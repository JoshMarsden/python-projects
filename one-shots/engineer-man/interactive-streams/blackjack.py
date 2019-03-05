#!/usr/bin/env python

"""

Author: Engineer Man 
  <github.com/engineer-man/youtube/blob/master/stream014/blackjack.py>

Modified by: Josh Marsden
  <github.com/OddAlgorithm>

blackjack.py

A console-based game application by which the user can play the well-known 
card game Blackjack. This version includes the ability to place fake bets 
that have no standing in the real world. Also, the dealers are humanized. 
I say **dealers** because there is also an API in use that returns randomly 
generated names.

"""

import random           # for random.shuffle()
import os               # for os.system()
import time             # for time.sleep()

# All for getting a random first name, lol
import urllib.request   # for urllib.request.urlopen()
import contextlib       # for contextlib.closing()
import json             # for json.loads()


def clear_screen():
    """Clears console output in Windows, Linux, and Mac."""

    os.system('cls' if os.name == 'nt' else 'clear')


def get_random_dealer_name():
    """Travels across the internet to grab and return a random first name.

    returns:
        dealer_name: str
            First name received from the API or selected from the list.
    """

    # URL follows guidelines at <randomuser.me/documentation>
    api_url = "https://randomuser.me/api/?inc=name&noinfo"
    results = None  # This will hold the JSON response from the API

    try:
        # Recommended way to auto-close an open URL
        with contextlib.closing(urllib.request.urlopen(api_url)) as web_response:
            results = web_response.read().decode('utf-8')  # Decode to str

        # Finally, something usable in python
        results = dict(json.loads(results))
        results = results['results'][0]  # Which is another dictionary of info

        dealer_name = results['name']['first']
    except Exception:
        # Just in case something goes wrong :}
        dealer_name = random.choice(['Jule', 'Kris', 'Mell', 'Odie', 
                                     'Sage', 'Olie', 'Cleo',])

    return dealer_name.capitalize()


def calc_hand(hand):
    """Returns the integer score of a card hand using simple Blackjack rules.

    params:
        hand (list): List of strings representing card values and suits
    """

    sum = 0

    non_aces = [card for card in hand if card[0] != 'A']
    aces = [card for card in hand if card[0] == 'A']

    for card in non_aces:
        if card[0] in 'JQK' or card[0:2] == '10':
            sum += 10
        else:
            sum += int(card[0])

    for card in aces:
        if sum <= 10:
            sum += 11
        else:
            sum += 1

    return sum


# My own addition :}
def print_hand(hand):
    """Returns a cute, mini Unicode version of a hand of cards as a str.

    If a card is not meant to be revealed, a '?' is expected in its place. 
    This will cause a blank card to be printed, representing a face-down 
    card.

    params:
        hand (list): List of strings representing card values and suits
    """

    #           .-  .---  ---.              -.
    # corners = |   | 0 ,  1 |, | 2 ,  3 |   |
    #           '-              '---  ---'  -'
    corners = [
            '\u250c',  #'\N{Box Drawings Light Down and Right}' (upper-left)
            '\u2510',  #'\N{Box Drawings Light Down and Left}' (upper-right)
            '\u2514',  #'\N{Box Drawings Light Up and Right}' (lower-left)
            '\u2518',  #'\N{Box Drawings Light Up and Left}' (lower-right)
            # (upper-middle)
            '\u2565',  #'\N{Box Drawings Down Double and Horizontal Single}
            # (lower-middle)
            '\u2568',  #'\N{Box Drawings Up Double and Horizontal Single}
    ]

    suits = {
            'S': '\u2660',  # Black Spade Suit
            'C': '\u2663',  # Black Club Suit
            'H': '\u2665',  # Black Heart Suit
            'D': '\u2666',  # Black Diamond Suit
    }

    card_str = ''
    line1 = []      # Top halves of cards...
    line2 = ['\n']  # ...bottom halves

    for card in hand:
        # Insert card value between upper corners
        line1.append(corners[0])
        line1.append(card[0] if card[0] != '?' else corners[4])
        # Some fancy checking if 10 is card value (double digits)
        line1.append(card[1] if len(card) > 2 else corners[1])

        # Insert card suit between lower corners
        line2.append(corners[2])
        line2.append(suits[card[-1]] if card[0] != '?' else corners[5])
        line2.append(corners[3])

    card_str = ''.join(line1 + line2)

    return card_str


def play_round(dealer_name, initial_bet, min_bet, max_bet):
    """Plays a single round of Blackjack between one player and a dealer.

    Each round lasts until one of the following end conditions are met:
      * Either party busts (status = -1 or 1)
      * Both parties stand (status = 0)
      * Player gets Blackjack first hand (status = 2)

    params:
        dealer_name: str
            Name of the Blackjack host NPC. Can be an empty string.
        initial_bet: int
            Player's starting bet. They can choose to up it as the round
            gets more interesting.
        min_bet: int
            Session's minimum allowed to bet.
        max_bet: int
            Session's maximum allowed to bet, usually based on player's 
            bank.

    returns:
        status: int
            Value is one of (-1, 0, 1, 2) corresponding to the status of 
            the player at the end of the round.
        final_bet: int
            Player's final bet factor at the end of the round. To be 
            multiplied with status and minimum bet.
    """

    status = 0
    final_bet = initial_bet

    # Start with a fresh deck of 52 cards
    deck = [
        '2S','3S','4S','5S','6S','7S','8S','9S','10S','JS','QS','KS','AS',
        '2C','3C','4C','5C','6C','7C','8C','9C','10C','JC','QC','KC','AC',
        '2H','3H','4H','5H','6H','7H','8H','9H','10H','JH','QH','KH','AH',
        '2D','3D','4D','5D','6D','7D','8D','9D','10D','JD','QD','KD','AD',
    ]

    # Shuffle the deck
    random.shuffle(deck)

    # Both players start with empty hands
    dealer = []
    player = []

    # Each player gets two cards
    for _ in range(2):
        # Deal first to player, then to dealer
        player.append(deck.pop())
        dealer.append(deck.pop())

    standing = False
    first_hand = True

    while True:
        clear_screen()

        player_score = calc_hand(player)
        dealer_score = calc_hand(dealer)

        if standing:
            print()
            print('Dealer Cards:')
            print(print_hand(dealer))
            print('Value: ({})'.format(dealer_score))
        else:
            print('Dealer Cards:')
            print(print_hand([dealer[0], '?']))

        print()
        print('Your Cards:')
        print(print_hand(player))
        print('Value: ({})'.format(player_score))
        print()

        # Check to see who won
        if standing:
            if dealer_score > 21:
                print('> Dealer busts, you win!')
                status = 1
                break
            elif player_score == dealer_score:
                print('> Push, no one wins or loses')
                status = 0
                break
            elif player_score > dealer_score:
                print('> You beat the dealer, you win!')
                status = 1
                break
            else:
                print('> You lose')
                status = -1
                break


        if first_hand and player_score == 21:
            print('> Blackjack! You get an extra ${}'.format(final_bet))
            status = 2
            break

        first_hand = False

        if player_score > 21:
            print('> You busted!')
            status = -1
            break

        # Take the player's bet again
        print('Current bet: ${}\n'.format(final_bet))
        answer = 'N'
        if min_bet + final_bet <= max_bet:
            text = ['> Feeling lucky?']
            dealer_says(text, dealer_name)
            answer = input('> Feel free to up the ante (Y/n): ')
        if not answer or answer[0] in 'Yy':
            prompt = '> How much more will you bet (${})? +$'.format(min_bet)
            new_bet = 0
            new_bet = how_much(prompt, default=min_bet)
            if new_bet + final_bet > max_bet:
                print("> Looks like you don't have enough in your bank.")
            else:
                final_bet += new_bet
                print('> You are now betting ${}'.format(final_bet))

        print()
        text = ['> What would you like to do?\n',
                '>  [1] (H)it\n',
                '>  [2] (s)tand']
        dealer_says(text, dealer_name)

        choice = input('\nYour choice: ')

        # Default choice is for player to hit
        if not choice or choice[0] in '1Hh':
            player.append(deck.pop())
        elif choice[0] in '2Ss':
            standing = True
            while calc_hand(dealer) <= 16:
                dealer.append(deck.pop())

    return status, final_bet


def how_much(prompt, default=None):
    """Prompts user for integer amount in betting and banking.

    params:
        prompt: str
            Text supplied to the user to ask for an integer.
        maximum: int
            User cannot enter an integer larger than this number.
        default: int
            If programmer has a default value already, no need to 
            enforce the user actually entering anything.

    returns:
        number: int
            The integer the user has replied with.
    """

    number = 0

    # Input catch-all for unexpected answers
    while True:
        try:
            number = input(prompt)
            # Check if user only hit enter
            number = default if number == '' else number
            number = abs(int(number))
            break
        except Exception:
            print("Sorry, didn't catch that.")

    return number


def dealer_says(words, dealer_name):
    """Prints dialogue from the Blackjack table dealer.

    params:
        words: list
            A list (for readability) of prompt strings.
        dealer_name: str
            Name of the dealer reading the strings. Can be blank.
    """

    print()
    print('{}(dealer):'.format(dealer_name))
    print('{}'.format(''.join(words)))


if __name__ == '__main__':
    # Humanize the game :P
    dealer_name = get_random_dealer_name()

    player_bank = 0
    winnings = 0
    min_bet = 5
    player_bet = 0
    keep_playing = True
    response = ""

    clear_screen()
    text = ['> Welcome to Blackjack!\n',
            '> House rules are as follows:\n',
            '>  * No splitting aces or eights, stick with what ya got\n',
            '>  * Bets are made in whole dollar amounts\n',
            '>  * Minimum bet is ${}\n'.format(min_bet),
            '>  * Getting Blackjack doubles your rewards!\n',
            '>  * Tap the table (<Enter>) to make the SUGGESTED action\n',
            '>  * No hitting the dealer, jk, jk. We are all ',
            'here to have fun']
    dealer_says(text, dealer_name)

    while keep_playing:
        print()
        print('Your Bank: ${}'.format(player_bank))
        print('Miminum Bet: ${}'.format(min_bet))

        while player_bank < min_bet:
            text = ['> Your bank value is below the minimum bet.']
            dealer_says(text, dealer_name)
            prompt = '> Would you like to put more money in your bank to continue playing? (Y/n): '
            # Default to "Yes" so that the player only has to push <Enter>
            response = input(prompt)
            if response and response[0] in 'Nn':
                # Break if this is the player's "breaking point"
                print("Sorry to see you go. Come back soon!")
                keep_playing = False
                break

            player_bank += how_much('> How many dollars? $')
            print()
            print('Your Bank: ${}'.format(player_bank))
            print('Miminum Bet: ${}'.format(min_bet))

        # Because of the above while loop, the if inside can't break twice
        if keep_playing == False:
            break

        # Take the player's bet
        text = ['> Time for the starting bet!']
        dealer_says(text, dealer_name)
        new_bet = 0
        while new_bet < min_bet:
            prompt = '> What will you bet? '
            if player_bet > 0:  # Skip this if playing first round
                prompt += 'Tap the table to bet the same as last time ' \
                        + '(${}) $'.format(player_bet)
            else:  # Very first time betting
                prompt += 'Tap the table to bet the minimum. $'

            player_bet = min_bet if player_bet < min_bet else player_bet
            new_bet = how_much(prompt, default=player_bet)

            if new_bet > player_bank:
                print('> That is more than what is in your bank. '
                      'Please enter a smaller value.')
                new_bet = 0
                player_bet = 0  # Start betting over again
                continue

            if new_bet < min_bet:
                print('> No lower than the minimum bet please.')
            else:
                player_bet = new_bet
                print('> You have bet ${}'.format(player_bet))

        time.sleep(.5)
        input('> Shall I deal? ')  # Dummy input so player has time to read

        # Play a round of Blackjack
        round_status, player_bet = play_round(dealer_name, player_bet, min_bet, player_bank)
        # Update bank and winnings with round winning pot or lost bet
        player_bank += player_bet * round_status
        winnings += player_bet * round_status

        # Default to "Yes" so that the player only has to push <Enter>
        response = input('> Keep playing? (Y/n): ')
        if response and response[0] in 'Nn':
            keep_playing = False

    # End of keep_playing loop

    # Wrap things up
    print("Winnings: ${}, Cashout: ${}".format(winnings, player_bank))
