from pony.orm import db_session, delete
from server.db.database import *
from server.db.crud.exception_crud import *
from server.db.dicts import *

@db_session
def delete_data(table): 
    delete(p for p in table)

@db_session
def delete_user(email: str, username: str, password: str): 
    user = User.get(Email=email, Username=username, Password=password)
    if user is not None:
        user.delete()
    return user

@db_session
def make_minister(player_id: int):
    Player[player_id].GovRol = MINISTER

@db_session
def make_ex_minister(player_id: int):
    Player[player_id].GovRol = EX_MINISTER

@db_session
def make_magician(player_id: int):
    Player[player_id].GovRol = MAGICIAN

@db_session
def make_director(player_id: int):
    Player[player_id].GovRol = DIRECTOR

@db_session
def make_voldemort(player_id: int):
    Player[player_id].SecretRol = VOLDEMORT

@db_session
def make_phoenix(player_id: int):
    Player[player_id].SecretRol = PHOENIX

@db_session
def get_player_gov_rol(player_id: int):
    return GovRolDiccionary[Player[player_id].GovRol]

@db_session
def get_exdirector_username(match_id: int):
    director = Match[match_id].Players.filter(lambda p: p.GovRol == EX_DIRECTOR).first()
    if director is None:
        return "No director yet"
    return director.UserId.Username 

@db_session
def set_candidate_director_test(match_id: int, position: int):
    Match[match_id].CandidateDirector = position

@db_session
def set_current_minister(match_id: int, position: int):
    Match[match_id].CurrentMinister = position

@db_session
def set_current_director(match_id: int, position: int):
    Match[match_id].CurrentDirector = position 

@db_session
def get_candidate_director(match_id: int):
    return Match[match_id].CandidateDirector

@db_session
def reset_proclamation(match_id: int):
    Match[match_id].Board.PhoenixProclamations = 0
    Match[match_id].Board.DeathEaterProclamations = 0

@db_session
def change_last_minister(match_id: int, position: int):
    Match[match_id].CurrentMinister = position

@db_session
def change_last_director(match_id: int, position: int):
    Match[match_id].Currentdirector = position

@db_session
def change_last_director_govrol(player_id: int):
    Player[player_id].GovRol = EX_DIRECTOR

@db_session
def change_selected_deck_phoenix(board_id: int):
    deck = Board[board_id].Proclamations
    for card in deck.Cards['selected']:
        deck.Cards['selected'].pop()
    for i in range (0,3):
        deck.Cards['selected'].append(PHOENIX_STR)

@db_session
def change_selected_deck_death_eater(board_id: int):
    deck = Board[board_id].Proclamations
    for card in deck.Cards['selected']:
        deck.Cards['selected'].pop()
    for i in range (0,3):
        deck.Cards['selected'].append(DEATH_EATER_STR)

@db_session
def show_available_deck(board_id: int):
    if Board.exists(Id=board_id):
        deck = Board[board_id].Proclamations
        if deck is not None:
            return deck.Cards['available']
        else:
            raise DeckNotFound
    else:
        raise BoardNotFound

@db_session
def show_discarded_deck(board_id: int):
    if Board.exists(Id=board_id):
        deck = Board[board_id].Proclamations
        if deck is not None:
            return deck.Cards['discarded']
        else:
            raise DeckNotFound
    else:
        raise BoardNotFound

@db_session
def show_deck(board_id: int):
    if Deck.exists(Board=board_id):
        deck = Deck.get(Board=board_id)
        print(f'Available: {deck.Available}')
        print(f'Discarded: {deck.Discarded}')
        return deck.Cards

@db_session
def get_position(player_id: int):
    return Player[player_id].Position

@db_session
def kill_player(player_id: int):
    Player[player_id].IsDead = True


@db_session
def get_failed_election_count(board_id: int):
    if not Board.exists(Id=board_id):
        raise BoardNotFound
    return Board[board_id].FailedElectionsCount

@db_session
def get_players_from_match(match_id: int):
    return Match[match_id].Players


@db_session
def get_num_phoenix(match_id: int): 
    n = 0       
    if Match.exists(Id=match_id):
        players = Match[match_id].Players
        for p in players:
            if (p.SecretRol == PHOENIX):
                n = n + 1 
    return n 

@db_session
def get_num_magicians(match_id: int): 
    n = 0       
    if Match.exists(Id=match_id):
        players = Match[match_id].Players
        for p in players:
            if (p.GovRol == MAGICIAN or p.GovRol == EX_MINISTER or p.GovRol == EX_DIRECTOR):
                n = n + 1 
    return n    


@db_session
def get_num_death(match_id: int): 
    n = 0       
    if Match.exists(Id=match_id):
        players = Match[match_id].Players
        for p in players:
            if (p.SecretRol == DEATH_EATER):
                n = n + 1 
    return n     

@db_session
def get_num_minister(match_id: int): 
    n = 0       
    if Match.exists(Id=match_id):
        players = Match[match_id].Players
        for p in players:
            if (p.GovRol == MINISTER):
                n = n + 1 
    return n    

@db_session
def get_num_voldemort(match_id: int): 
    n = 0       
    if Match.exists(Id=match_id):
        players = Match[match_id].Players
        for p in players:
            if (p.SecretRol == VOLDEMORT):
                n = n + 1 
    return n 

@db_session
def change_player_rol(player_id: int, rol: int):
    Player[player_id].SecretRol = rol
