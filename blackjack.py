import random

# create deck
suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
deck = [(rank, suit) for rank in ranks for suit in suits]

def create_hand_name(hand):
    suit_symbols = {'Spades': '♠', 'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣'}
    handName = []
    for item in hand:
        if item[0] == "10":
            handName.append(f"{item[0]}{suit_symbols.get(item[1])}")
        else:
            handName.append(f"{item[0][0]}{suit_symbols.get(item[1])}")
    return handName

def get_card_count(deck):
    card_values = {
        '2': -1,
        '3': -1,
        '4': -1,
        '5': -1,
        '6': -1,
        '7': 0,
        '8': 0,
        '9': 0,
        '10': 1,
        'J': 1,
        'Q': 1,
        'K': 1,
        'A': 1
    }
    count = 0
    for card in deck:
        if (card[0]=="10"):
            count += int(card_values.get(card[0]))
        else:
            count += int(card_values.get(card[0][0]))
    return count

def get_value(card):
    if card[0] in ['Jack', 'Queen', 'King']:
        return 10
    elif card[0] == 'Ace':
        return 11
    else:
        return int(card[0])

def get_hand_value(hand):
    value = sum([get_value(card) for card in hand])
    aces = sum([1 for card in hand if card[0] == 'Ace'])
    while value > 21 and aces > 0:
        value -= 10
        aces -= 1
    return value

def play_blackjack(n_decks):
    cardsLeft = n_decks*52
    roundCount = 1
    numberWins = 0
    numberLoss = 0
    playerChips = 10000
    deck = [(rank, suit) for rank in ranks for suit in suits] * n_decks
    random.shuffle(deck)
    while cardsLeft >=10:
        
        # break game
        if playerChips<=0:
            print("End game! Out of chips")
            return

        # betting turn
        startBet = -1
        while int(startBet)<=0 or int(startBet)>int(playerChips):
            startBet = input(f'\n How many chips you wanna bet? ( máx. {playerChips}) :  ')

        # start game
        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]
        cardsLeft -= 4
        print(f"------------------------------------------------")
        print(f"-----                ROUND {roundCount}               -----")
        print(f"-----           CARD COUNT {-1*get_card_count(deck)}               -----")
        print(f"-----  Cartas restantes: {cardsLeft} , W: {numberWins} / L: {numberLoss} -----")   
        print(f"-----            YOUR BET: {startBet}         -----")
        print(f"------------------------------------------------")

        # player turn
        while get_hand_value(player_hand) < 21:
            print(f"Player hand: {create_hand_name(player_hand)} ( {get_hand_value(player_hand)} )  |  Dealer hand: ['{create_hand_name(dealer_hand)[0]}', ? ] ( ? )", end="\r")
            choice = input('\n Hit, stand or double? (h/s/d)')
            match choice.lower():
                case 'h':
                    player_hand.append(deck.pop())
                    cardsLeft -= 1
                case 'd':
                    if int(playerChips) >= 2*int(startBet):
                        startBet = int(startBet)*2
                        player_hand.append(deck.pop())
                        cardsLeft -= 1
                        break
                    else:
                        print("You don't have enought chips to double")
                case 's':
                    break

        # dealer turn
        while get_hand_value(dealer_hand) < 17:
            dealer_hand.append(deck.pop())
            cardsLeft -= 1

        # check who won
        player_hand_value = get_hand_value(player_hand)
        dealer_hand_value = get_hand_value(dealer_hand)
        print(f'Player hand: {create_hand_name(player_hand)} ( {player_hand_value} )  |  Dealer hand: {create_hand_name(dealer_hand)} ( {dealer_hand_value} )', end="\r" )
        if player_hand_value > 21:
            print('Player busts! Dealer wins.')
            playerChips -= int(startBet)
            numberLoss += 1
        elif dealer_hand_value > 21:
            print('Dealer busts! Player wins.')
            playerChips += int(startBet)
            numberWins += 1
        elif player_hand_value > dealer_hand_value:
            print('Player wins!')
            playerChips += int(startBet)
            numberWins += 1
        elif player_hand_value < dealer_hand_value:
            print('Dealer wins!')
            playerChips -= int(startBet)
            numberLoss += 1
        else:
            print('Push.')
        print("\n\n\n")
        roundCount += 1

n_decks = int(input("How many decks you wanna play?  "))
play_blackjack(n_decks)
print("Thank you for playing")