from pony.orm import db_session, select, count
from backend.db.database import *
from backend.db.dicts import *

@db_session #Bool
def user_is_registred(name, upassword):
    try:
        u = User.get(Username = name, Password = upassword)
        if u:
            return True
        else: 
            return False
    except Exception:
        return False

@db_session
def check_username(username):
    try: 
        u = User.exists(Username=username)
        return u 
    except Exception:
        return False

@db_session
def check_email(email):
    try: 
        u = User.exists(Email=email)
        return u 
    except Exception:
        return False

@db_session #get the User object.
def get_user(username, password):
    user = User.get(Username=username, Password=password)
    if user is not None:
        user = user.to_dict("Id Username")
    return user


@db_session
def create_user(email: str, username: str, password: str):
    try:
        User(Email=email, Username=username, Password=password)
        return True
    except Exception:
        return False

@db_session
def add_match(minp,maxp,creator):
    try:
        newmatch = Match(MaxPlayers=maxp,
            MinPlayers=minp,
            Status=0,
            BoardType=0, #hardcoded
            LastMinister = 0, #Changes when the match starts
            Creator = creator)
        return newmatch
    except :
        return None

@db_session
def add_board(newmatch):
    newboard = Board(BoardType = newmatch.BoardType,
        PhoenixProclamations = 0,
        DeathEaterProclamations = 0,
        FailedElectionsCount = 0,
        Match = newmatch)
    return newboard

@db_session
def add_user_in_match(userid, matchid, position):
    try:
        mymatch = Match[matchid]
        myuser= User[userid]
    except :
        return None
    newplayer = Player(Position = position,
        SecretRol = 0, #Changes when the match starts
        GovRol = 2, #Changes when the match starts
        IsDead = False,
        UserId = myuser,
        MatchId = mymatch)
    return newplayer

@db_session
def check_player_in_match(gid: int, pid: int): # need testing
    if Match.exists(Id=gid):
        return exists(p for p in Match[gid].Players if p.PlayerId == pid)
    return False

@db_session
def add_match_db(minp,maxp,uhid):
    if(minp>maxp):
        return None
    try:
        creator= User[uhid]
    except :
        return None
    
    match = add_match(minp,maxp,creator)
    if match is not None:
        matchId= match.to_dict("Id")["Id"]
        add_board(match)
        player = add_user_in_match(uhid, matchId, 0)# add the creator to player table 
        player.GovRol = 1
        match_and_player = {
            "Match_id": matchId,
            "Player_id": player.to_dict("PlayerId")["PlayerId"]
        }
        return match_and_player
    else:
        return None

@db_session
def there_is_space(mid):
    try: 
        players = Match[mid].Players
        MaxPlayers = Match[mid].MaxPlayers
        if (len(players) < MaxPlayers):
            return True
        else:
            return False
    except :
        return False

@db_session
def vote_director(player_id: int, vote: str): # need testing
    if vote == 'nox':
        Player[player_id].Vote = 0
    elif vote == 'lumos':
        Player[player_id].Vote = 1
    elif vote == 'missing vote':
        Player[player_id].Vote = 2


@db_session
def delete_data(table): # needed for testing
    delete(p for p in table)

@db_session
def delete_user(email, username, password): # needed for testing
    user = User.get(Email=email, Username=username, Password=password)
    if user is not None:
        user.delete()

    return user

@db_session
def get_minister_username(ID: int): # need testing
    minister = Match[ID].Players.filter(lambda p: p.GovRol == 1).first()
    return minister.UserId.Username 

@db_session
def get_match_status(ID: int): # need testing
    return Status[Match[ID].Status] 

@db_session
def get_board_status(ID: int): # need testing
    board_attr = ["PhoenixProclamations", "DeathEaterProclamations"]
    board_status = Match[ID].Board.to_dict(board_attr)
    board_status['boardtype'] = BoardType[Match[ID].Board.BoardType]
    return board_status    

@db_session
def check_match(mid): # need testing
    return Match.exists(Id=mid)


@db_session
def get_player_votes(match_id: int): # need testing
    def replace(vote: int):
        result = 'missing vote'
        if vote == 0:
            result = 'nox'
        elif vote == 1:
            result = 'lumos'
        return result

    if Match.exists(Id=match_id):
        players = Match[match_id].Players.order_by(Player.Position)
        return {x.UserId.Username: replace(x.Vote) for x in players}        

@db_session
def get_player_id(match_id: int, user_id: int): # need testing
    if Match.exists(Id=match_id):
        player = get(p for p in Match[match_id].Players if p.UserId.Id == user_id)
        return player.PlayerId

@db_session
def set_next_minister(match_id: int): # need testing
    if Match.exists(Id=match_id):
        query = Match[match_id].Players.order_by(Player.Position)
        players = [x for x in query]
        last_minister = Match[match_id].LastMinister
        players[last_minister].GovRol = 2
        current_minister = (last_minister + 1) % len(players)
        players[current_minister].GovRol = 1
        Match[match_id].LastMinister = current_minister
        return current_minister

@db_session
def compute_election_result(match_id: int): # need testing
    if Match.exists(Id=match_id):
        players = Match[match_id].Players
        lumos = 0
        voting_cutoff = 0.5000001
        result = 'nox'
        if not exists(p for p in players if p.Vote == 2):
            total = count(p for p in players)
            lumos = count(p for p in players if p.Vote == 1)
            lumos = lumos/total

        if lumos > voting_cutoff:
            result = 'lumos'

        return result

@db_session
def restore_election(match_id: int): # need testing
    if Match.exists(Id=match_id):
        players = Match[match_id].Players
        for p in players:
            p.Vote = 2

@db_session
def enact_proclamation(match_id: int, proclamation: str): # need testing
    if proclamation == "phoenix":
        Match[match_id].Board.PhoenixProclamations += 1
    elif proclamation == "death eater":
        Match[match_id].Board.DeathEaterProclamations += 1

@db_session
def get_phoenix_proclamations(match_id: int): # need testing
    return Match[match_id].Board.PhoenixProclamations

@db_session
def get_death_eater_proclamations(match_id): # need testing
    return Match[match_id].Board.DeathEaterProclamations

@db_session
def is_victory_from(match_id: int): # need testing
    if Match.exists(Id=match_id):
        winner = "no winner yet"
        if get_death_eater_proclamations(match_id) == 6:
            winner = "death eater"
            Match[match_id].Status = 2
        elif get_phoenix_proclamations(match_id) == 5:
            winner = "phoenix"
            Match[match_id].Status = 2

        return winner
