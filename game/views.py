from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Game
import random, json

def home_view(request):
    return render(request, 'home.html')

def blackjack_view(request):
    
    deck = create_deck()

    player_hand = deal_initial_cards(deck)
    dealer_hand = deal_initial_cards(deck)

    player_score = 0
    dealer_score = 0

    player_chips_v = 500
    player_chips = chips_display(player_chips_v)
    dealer_chips_v = 500
    dealer_chips = chips_display(dealer_chips_v)

    player_bet_v = 0
    player_bet = chips_display(player_bet_v)
    dealer_bet_v = 0
    dealer_bet = chips_display(dealer_bet_v)
    round_bet_v = 0
    round_bet = chips_display(round_bet_v)

    game = Game.objects.create (
        
        deck=deck,
        
        player_hand=player_hand,
        dealer_hand=dealer_hand,

        player_chips=player_chips,
        player_chips_v = player_chips_v,
        dealer_chips=dealer_chips,
        dealer_chips_v=dealer_chips_v,

        dealer_score=dealer_score,
        player_score=player_score,

        player_bet_v=player_bet_v,
        player_bet=player_bet,
        dealer_bet_v=dealer_bet_v,
        dealer_bet=dealer_bet,
        round_bet_v=round_bet_v,
        round_bet=round_bet

    )

    # Store game details in session
    request.session['game_id'] = game.id

    context = {
        
        'game':game,
        'player_hand': player_hand,
        'dealer_hand': dealer_hand,
        'player_chips_v': player_chips_v,
        'player_chips': player_chips,
        'dealer_chips_v':dealer_chips_v,
        'dealer_chips':dealer_chips
    }

    return render(request, 'game.html', context)
    

def create_deck():
    symbols = ['diamond', 'heart', 'club', 'spade']
    numbers = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = [(x, y) for x in numbers for y in symbols] * 5
    random.shuffle(deck)
    return deck

def deal_initial_cards(deck):
    hand = [deck.pop(0), deck.pop(0)]  
    return hand

def chips_display(chips_v):

    chips = []

    if chips_v == 0:
        return chips
    else:
        v_0 = chips_v/100

        while v_0 >= 2.5:
            chips.append(100)
            chips_v -= 100
            v_0 = int(chips_v/100)

        v_1 = chips_v/50

        while v_1 >= 1.5 and chips_v > 75:
            chips.append(50)
            chips_v -= 50
            v_1 = chips_v/50

        while chips_v > 0:
            chips.append(25)
            chips_v -=25

        chips = chips[::-1]

    return chips

def calculate_score(hand):
    
    game_dict = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
    result = 0
    aces = 0

    for card in hand:
        if card[0] == 'A':
            aces += 1
        result += game_dict[card[0]]

    while result > 21 and aces:
        result -= 10
        aces -= 1

    return result

def place_bet_view(request, game_id):
    
    game_dict = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
    
    game = Game.objects.get(id=game_id)
    
    if request.method == 'POST':

        data = json.loads(request.body)

        game.player_score = calculate_score(game.player_hand)
        game.dealer_score = game_dict[game.dealer_hand[0][0]]
        
        # Get bet values
        game.player_bet_v = data.get('playerBetV',0)
        game.player_chips_v = data.get('playerChipV',0)

        # Calculate dealer's bet and round bet
        if game.player_bet_v > game.dealer_chips_v:
            game.dealer_bet_v = game.dealer_chips_v
            game.player_chips_v += game.player_bet_v - game.dealer_chips_v
            game.player_bet_v = game.dealer_bet_v
            game.dealer_chips_v = 0
        else:
            game.dealer_bet_v = game.player_bet_v
            game.dealer_chips_v -= game.dealer_bet_v

        game.round_bet_v = game.player_bet_v + game.dealer_bet_v

        # Ajust chip display
        game.dealer_chips = chips_display(game.dealer_chips_v)
        game.player_chips = chips_display(game.player_chips_v)
        game.round_bet = chips_display(game.round_bet_v)
        
        game.save()
    
        return JsonResponse({
            'playerChips': game.player_chips,
            'playerChipsV': game.player_chips_v,
            'dealerChips': game.dealer_chips,
            'dealerChipsV': game.dealer_chips_v,
            'roundBet': game.round_bet,
            'roundBetV': game.round_bet_v,
            'playerScoreV': game.player_score,
            'dealerScoreV': game.dealer_score
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def hit_view(request, game_id):

    game = Game.objects.get(id=game_id)

    deck = game.deck
    player_hand = game.player_hand
    player_score = game.player_score
    dealer_hand = game.dealer_hand

    new_card = deck.pop(0)
    player_hand.append(new_card)

    player_score = calculate_score(player_hand)

    game.player_hand = player_hand
    game.player_score = player_score
    game.deck = deck

    if player_score > 21:
        dealer_score = calculate_score(dealer_hand)
        game.dealer_score = dealer_score 
        game.dealer_hand = dealer_hand
        game.dealer_chips_v += game.round_bet_v
        game.round_bet_v = 0
        game.dealer_chips = chips_display(game.dealer_chips_v)
        game.game_result = "Dealer wins!"

    game.save()

    return JsonResponse({
        'player_hand': game.player_hand,
        'playerChipsV': game.player_chips_v,
        'player_score': game.player_score,
        'dealer_hand': game.dealer_hand,
        'dealer_score': game.dealer_score,
        'dealerChipsV': game.dealer_chips_v,
        'dealerChips': game.dealer_chips,
        'roundBetV': game.round_bet_v,
        'gameResult': game.game_result

    })


def stand_view(request, game_id):
    
    game = Game.objects.get(id=game_id)

    dealer_hand = game.dealer_hand
    dealer_score = calculate_score(dealer_hand)
    deck = game.deck

    while dealer_score < 17:
        new_card = deck.pop(0)
        dealer_hand.append(new_card)
        dealer_score = calculate_score(dealer_hand)

    if dealer_score > 21 or game.player_score > dealer_score:
        game.player_chips_v += game.round_bet_v
        game.round_bet_v = 0
        game.player_chips = chips_display(game.player_chips_v)
        game.game_result = "You win!"
    elif dealer_score <= 21 and game.player_score < dealer_score:
        game.dealer_chips_v += game.round_bet_v
        game.round_bet_v = 0
        game.dealer_chips = chips_display(game.dealer_chips_v)
        game.game_result = "Dealer wins!"
    elif dealer_score == game.player_score:
        game.dealer_chips_v += game.round_bet_v/2
        game.player_chips_v += game.round_bet_v/2
        game.round_bet_v = 0
        game.player_chips = chips_display(game.player_chips_v)
        game.dealer_chips = chips_display(game.dealer_chips_v)
        game.game_result = "It's a draw!"
    else:
        game.game_result = "Check!"


    game.dealer_hand = dealer_hand
    game.dealer_score = dealer_score
    game.save()

    return JsonResponse({
        'player_hand': game.player_hand,
        'player_score': game.player_score,
        'dealer_hand': game.dealer_hand,
        'dealer_score': game.dealer_score,
        'playerChipsV': game.player_chips_v,
        'playerChips': game.player_chips,
        'dealerChipsV': game.dealer_chips_v,
        'dealerChips': game.dealer_chips,
        'roundBetV': game.round_bet_v,
        'gameResult': game.game_result

    })


def newround_view(request, game_id):
    
    game = Game.objects.get(id=game_id)

    game.player_hand = deal_initial_cards(game.deck)
    game.dealer_hand = deal_initial_cards(game.deck)
    game.player_score = 0
    game.dealer_score = 0
    game.round_bet_v = 0

    game.save()

    return JsonResponse({
        'player_hand': game.player_hand,
        'player_score': game.player_score,
        'dealer_hand': game.dealer_hand,
        'dealer_score': game.dealer_score,
        'playerChipsV': game.player_chips_v,
        'playerChips': game.player_chips,
        'dealerChipsV': game.dealer_chips_v,
        'dealerChips': game.dealer_chips,
        'roundBetV': game.round_bet_v

    })
