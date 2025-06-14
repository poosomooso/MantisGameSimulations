import random

mantis_colors = ["red", "blue", "green", "yellow", "pink", "purple"]
num_players = 4

class GameLogger:
    def __init__(self, players, printing=False):
        self.printing=printing
        self.num_players = len(players)
        self.players = players
        self.num_cards = { i: [len(players[i].contained_cards)] for i in range(self.num_players)}
        self.num_points = { i: [players[i].points()] for i in range(self.num_players)}
        self.actions = {i: [{"action": "deal"}] for i in range(self.num_players)}

    def post_turn(self, player_num, action_obj):
        p = self.players[player_num]
        self.actions[player_num].append(action_obj)
        self.num_cards[player_num].append(len(p.contained_cards))
        self.num_points[player_num].append(p.points())
        
    def log(self, line):
        if self.printing:
            print(line)

class Card:
    def __init__(self, color, back_colors = None):
        self.color = color
        if back_colors:
            self.back_colors = back_colors.copy()
        else:
            pass # TODO

    def __str__(self):
        return f"Card: {self.color}, ({str(self.back_colors)})"
    
    def __repr__(self):
        return str(self)

class Player:
    def __init__(self):
        self.contained_cards = []
        self.point_cards = []

    def receive_card(self, c):
        self.contained_cards.append(c)

    def points(self):
        return len(self.point_cards)
    
    def get_action(self, other_players, card_back):
        return {
            "action": random.choice(["steal", "score"]), 
            "from": random.choice(list(other_players.keys()))
        }

    def score(self, card):
        same_color = self.get_same_colored_cards(card.color)
        if len(same_color) > 0:
            self.point_cards.extend(same_color)
            self.point_cards.append(card)
            self.remove_color(card.color)
        else:
            self.receive_card(card)

    def remove_color(self, color_name):
        self.contained_cards = [x 
                                for x in self.contained_cards 
                                if x.color != color_name]
        
    def get_same_colored_cards(self, color_name):
        return [x
                for x in self.contained_cards
                if x.color == color_name]
    
    def __str__(self):
        return f"Player\tHand: {str(self.contained_cards)}\n\tPoints: {str(self.point_cards)} ({self.points()})\n"
    
    def __repr__(self):
        return str(self)



def create_deck():
    deck = []
    perms = [(a, b, c) 
            for a in range(len(mantis_colors) -1) 
            for b in range(len(mantis_colors) -1) 
            for c in range(len(mantis_colors) -1)
            if a != b and b != c and a != c]

    for c in mantis_colors:
        # TODO: current color needs to be included in the mantis colors
        remaining = [a for a in mantis_colors if a != c]
        for p in perms:
            deck.append(Card(c, [remaining[p[0]], remaining[p[1]], remaining[p[2]]]))

    return deck

def shuffle(deck):
    random.shuffle(deck)
    
def play(specified_players=None, num_players = 4):
    deck = create_deck()
    shuffle(deck)

    if specified_players:
        players = specified_players
        num_players = len(players)
    else:
        players = []
        for _ in range(num_players):
            players.append(Player())

    # deal initial cards
    for _ in range(4):
        for i in range(num_players):
            players[i].receive_card(deck.pop(0))

    gl = GameLogger(players)

    turn = 0
    while len(deck) > 0: 
        gl.log(f"Player {turn}'s turn")
        gl.log(players)
        draw = deck.pop(0)
        action = players[turn].get_action({i : 
                                  players[i]
                                  for i in range(num_players) 
                                  if i != turn
                                  },
                                  draw.back_colors)
        
        # get points
        if action['action'] == "score":
            gl.log(f"Player {turn} scores")
            players[turn].score(draw)
            
        # steal
        elif action['action'] == "steal":
            victim = action['from']
            gl.log(f'Player {turn} steals from player {victim}')
            stolen = players[victim].get_same_colored_cards(draw.color)
            if len(stolen) > 0:
                players[victim].remove_color(draw.color)
                for c in stolen:
                    players[turn].receive_card(c)
                players[turn].receive_card(draw)
            else:
                players[victim].receive_card(draw)

        else:
            raise ValueError(f"{action['action']} is not a valid action!")
        
        gl.post_turn(turn, action)
        if players[turn].points() >= 10:
                break
        
        turn += 1
        turn %= num_players

    for p in players:
        print(p.points())
    return gl


if __name__ == "__main__":
    print(str(Player()))
    play()

