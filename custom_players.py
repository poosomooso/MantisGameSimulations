from mantis_game import Player
import random

_score_obj = {
            "action": "score", 
            "from": ""
        }

# check if f1 is greater than f2
# epsilon is 1/500 -- if someone has more than 500 cards, well too bad
def floatGT(f1, f2):
    if abs(f1-f2) < (1/20):
        return False
    return f1 > f2

class AlwaysScore(Player):
    def get_action(self, other_players, card_back):
        return _score_obj

class AlwaysStealRandom(Player):
    def get_action(self, other_players, card_back):
        have_matching = []
        for i, p in other_players.items():
            matches = 0
            for c in card_back:
                matches += len(p.get_same_colored_cards(c))
            if matches > 0:
                have_matching.append(i)
        if len(have_matching) <= 0:
            return _score_obj
        return {
            "action": "steal", 
            "from": random.choice(have_matching)
        }
    
class AlwaysStealMostMatching(Player):
    def get_action(self, other_players, card_back):
        max_matches = 0
        max_match_player = -1
        # shuffle list so we're not stealing from the same person
        shuffled_player_list = list(other_players.items())
        random.shuffle(shuffled_player_list) 
        for i, p in shuffled_player_list:
            matches = 0
            for c in card_back:
                matches += len(p.get_same_colored_cards(c))
            if matches > max_matches:
                max_match_player = i
        if max_match_player < 0:
            return _score_obj
        return {
            "action": "steal", 
            "from": max_match_player
        }
    
class AlwaysStealMaxMatchingRatio(Player):
    def get_action(self, other_players, card_back):
        max_matches = 0.0
        max_match_player = -1
        # shuffle list so we're not stealing from the same person
        shuffled_player_list = list(other_players.items())
        random.shuffle(shuffled_player_list) 
        for i, p in shuffled_player_list:
            matches = 0
            for c in card_back:
                matches += len(p.get_same_colored_cards(c))
            match_ratio = matches / len(p.contained_cards)
            if floatGT(match_ratio, max_matches):
                max_match_player = i
        if max_match_player < 0:
            return _score_obj
        return {
            "action": "steal", 
            "from": max_match_player
        }
    
class AlwaysStealMaxDiversity(Player):
    def get_action(self, other_players, card_back):
        max_matches = 0
        max_match_player = -1
        # shuffle list so we're not stealing from the same person
        shuffled_player_list = list(other_players.items())
        random.shuffle(shuffled_player_list) 
        for i, p in shuffled_player_list:
            matches = 0
            for c in card_back:
                if len(p.get_same_colored_cards(c)) > 0:
                    matches += 1
            
            if matches > max_matches:
                max_match_player = i
        if max_match_player < 0:
            return _score_obj
        return {
            "action": "steal", 
            "from": max_match_player
        }
    
class SafetySteal(Player):
    def get_action(self, other_players, card_back):
        max_match_player = -1
        # shuffle list so we're not stealing from the same person
        shuffled_player_list = list(other_players.items())
        random.shuffle(shuffled_player_list) 
        for i, p in shuffled_player_list:
            matches = 0
            for c in card_back:
                if len(p.get_same_colored_cards(c)) > 0:
                    matches += 1
            
            if matches >= len(card_back):
                max_match_player = i
        if max_match_player < 0:
            return _score_obj
        return {
            "action": "steal", 
            "from": max_match_player
        }