import random
import string
from typing import Annotated, Any, Dict, List, Optional, Union

from fastapi import Depends, FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from random import choices, randint
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime

from database import Account, AccountBase, AccountCreate, AccountRead, AccountUpdate, get_session

from character import Character, StatModifier, Ability, Spell
from game_loop_test_1 import action_attack
from websocket import ConnectionManager

from utils import *



import json



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

games: dict[str, dict[str, list[Character]]] = {}

manager = ConnectionManager()

SessionDep = Annotated[Session, Depends(get_session)]




class GameBase(SQLModel):
    game_code: str = Field(unique = True, index = True)
    host_id: str
    player_count: int
    created_at: datetime = Field(default_factory = datetime.now)

class Game(GameBase, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)

class GameCreate(GameBase):
    game_code: Optional[str] = None

class GameRead(GameBase):
    id: int

class GameUpdate(GameBase):
    player_id: str

class JoinGame(SQLModel):
    game_code: str
    player_id: str




def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/get-character/")
async def get_character(request: Request) -> dict:
    data = await request.json()
    characterID = data.get('characterID')
    
    print("char\n", characterID)
    try:
        with open("characters.json", "r") as f:
            characters = json.load(f)
    except FileNotFoundError:
        return {"char": None, "error": True, "message": "Characters file not found"}
    
    try:
        character = characters[characterID]
        return {
            "char": character,
            "error": False
        }
    except KeyError:
        return {"char": None, "error": True, "message": "Character not found"}


@app.post("/generate-code")
async def generate_code(request: Request, session: SessionDep) -> GameBase:

    data = await request.json()

    # player_id: str, character: PydanticCharacter

    player_id = data.get('player_id')
    characterID = data.get('character_id')
    
    character: Character = getDefaultCharacterFromStr(characterID, True)
    
    # print(type(character))
    current_code = ''.join(choices(string.ascii_uppercase + string.digits, k=6))
    gb = GameBase(
        game_code=current_code,
        host_id=player_id,
        player_count=1
    )
    db_game = Game.model_validate(gb)

    
    games = readGames()

    games[current_code] = {
        "characters": [character.character_to_json()],
        "playerCharacters": [character.character_to_json()],
        "enemyCharacters": [],
        "current_turn": [0],
        "players": [player_id],
        "locked_players": [],
        "active_player": [player_id]
    }

    writeGames(games)
    



    

    print(db_game)

    session.add(db_game)
    session.commit()
    session.refresh(db_game)

    return db_game

@app.post("/get-account")
async def get_account(request: Request, session: SessionDep):
    data = await request.json()

    username = data.get('username')
    hashed_password = data.get('hashed_password')

    account = session.exec(
        select(Account).where(Account.username == username).where(Account.hashed_password == hashed_password).with_for_update()
    ).one()


    if not account:
        raise HTTPException(status_code=404, detail="Account Not Found")

    return account

@app.post("/create-account")
async def create_account(request: Request, session: SessionDep):
    data = await request.json()

    username = data.get('username')
    hashed_password = data.get('hashed_password')

    print("username: ", username)
    print("hashed_password: ", hashed_password)

    account = Account(
        username=username,
        hashed_password=hashed_password
    )

    db_account = Account.model_validate(account)

    print(db_account)

    session.add(db_account)
    session.commit()
    session.refresh(db_account)




    

@app.post("/join")
# def join_game(jg: JoinGame, character: PydanticCharacter, session: SessionDep):
async def join_game(request: Request, session: SessionDep) -> dict:
    data = await request.json()
    characterID = data.get('characterID')
    gameCode = data.get('game_code')
    playerID = data.get('player_id')
    
    character: Character = getDefaultCharacterFromStr(characterID, True)
    jg = JoinGame(
        game_code=gameCode,
        player_id=playerID
    )

    print(jg.game_code)
    
    gameBase: Game = session.exec(
        select(Game).where(Game.game_code == jg.game_code).with_for_update()
    ).one()

    if not gameBase:
        print("No Game Found")
        raise HTTPException(status_code=404, detail="Game Not Found")

    games = readGames()
    games[jg.game_code]["characters"].append(character.character_to_json())
    games[jg.game_code]["enemyCharacters"].append(character.character_to_json())
    games[jg.game_code]["players"].append(jg.player_id)
    games[jg.game_code]["locked_players"].append(jg.player_id)

    writeGames(games)

    print(gameBase.__dict__)
    gameBase.player_count += 1
    # gameBase.id += 1
    # db_joingame = Game.model_validate(gameBase, from_attributes=True)

    print(gameBase)

    session.add(gameBase)

    session.commit()
    session.refresh(gameBase)

    return {}



@app.post('/update-user-stats')
def update_user_stats(stat_key: str, value: float, account_name: str, session: SessionDep):
    account: Account = session.exec(
        select(Account).where(Account.username == account_name).with_for_update()
    ).one()

@app.post('/game')
async def get_game(request: Request):
    data = await request.json()
    game_code: str = data.get('game_code')
    with Session(engine) as session:
        game = session.exec(
            select(Game).where(Game.game_code == game_code)
        )

        if not game:
            raise HTTPException(status_code=404, detail="Game Not Found")
        
        return game
    pass

@app.post('/game-data')
async def game_data(request: Request):
    data = await request.json()
    game_code: str = data.get('game_code')
    games = readGames()
    print(game_code)
    try:
        game = games[game_code]
    except KeyError:
        print("cant find game")
        raise HTTPException(status_code=404,detail="Incorrect Game Code")

    return game

@app.post("/action")
async def select_action(request: Request, session: SessionDep, useData: bool = True):
    if useData:
        data = await request.json()
        action: str = data.get('action')
        player_id: str = data.get('player_id')
        game_code: str = data.get('game_code')
        params: dict[str, str] = data.get('params')

    games = readGames()
    
    
    if player_id != games[game_code]["players"][games[game_code]["current_turn"][0]]:
        print(games[game_code]["current_turn"][0])
        print(games[game_code]["players"][games[game_code]["current_turn"][0]])
        return "wrong player"
    
    currentCharacter = games [game_code] ["characters"] [games[game_code]["current_turn"][0]]

    characterKey: str = "enemyCharacters" if not currentCharacter in games[game_code]["playerCharacters"] else "playerCharacters"
    opponentsKey: str = "enemyCharacters" if currentCharacter in games[game_code]["playerCharacters"] else "playerCharacters"
    opponentCharacters: List[Character] = games[game_code][opponentsKey]

    print("current character\n", currentCharacter)

    print("palyer id\n" + player_id)
    
    match action:
        case "attack":
            if not params["target"]:
                params["target"] = random.choice([opponentCharacter["name"] for opponentCharacter in opponentCharacters])
                pass
            
            for char in opponentCharacters:
                if char["name"] == params["target"]:
                    target = char
                    break

            # action_attack(currentCharacter, target_name=params["target"])
            print('attack')

            res = action_attack(currentCharacter["name"], game_code, params["target"], opponentsKey, characterKey)
            turnEnded = res
            if turnEnded:
                games = readGames()
                games[game_code]["current_turn"][0] = (games[game_code]["current_turn"][0] + 1) % 2
                writeGames(games)

            
            pass
    

    return "correct player"

@app.get('/get-all-characters')
async def get_all_characters():

    with open("characters.json", "r") as f:
        characters = json.load(f)

    return list(characters.keys())


@app.post('/get-cards')
async def get_cards(request: Request, session: SessionDep):
    data = await request.json()
    character_id = data.get('character_id')
    game_code = data.get('game_code')

    games = readGames()
    try:
        game = games[game_code]
    except KeyError:
        raise HTTPException(status_code=404, detail="Incorrect or Invalid Game Code!")
    

    char_index = 0 if game["players"][0] == character_id else 1
    character = getCharacterFromDict(game["characters"][char_index])
    
    return character.get_cards()

@app.post('/turn-options')
async def turn_options(request: Request, session: SessionDep):
    # should return only possible turns; not all

    data = await request.json()

    player_id = data.get('player_id')
    game_code = data.get('game_code')

    print(f"Requested Turn Options by {player_id} with code {game_code}")

    games = readGames()

    game = games[game_code]

    active_player = game["players"][game["current_turn"][0]]

    print(f"The active player is {active_player}")

    if active_player == player_id:
        print("Request is from the Correct Player")

        current_turn = game["current_turn"][0]

        current_character = game["characters"][current_turn]

        character = getCharacterFromDict(current_character)

        turn_options = character.get_available_options()

        return turn_options

    return []

def run_action(action: str, player_id: str, game_code: str, params: Dict[str, str]) -> Dict[str, str]:

    games = readGames()

    game = games[game_code]
    
    if player_id != game["players"][game["current_turn"][0]]:
        print(games[game_code]["current_turn"][0])
        print(games[game_code]["players"][games[game_code]["current_turn"][0]])
        print(player_id)
        return {"message": "wrong player"}
    
    currentCharacter = games [game_code] ["characters"] [games[game_code]["current_turn"][0]]

    characterKey: str = "enemyCharacters" if not currentCharacter in games[game_code]["playerCharacters"] else "playerCharacters"
    opponentsKey: str = "enemyCharacters" if currentCharacter in games[game_code]["playerCharacters"] else "playerCharacters"
    opponentCharacters: List[Character] = games[game_code][opponentsKey]

    print("current character\n", currentCharacter)

    print("palyer id\n" + player_id)
    
    match action:
        case "Attack":
            if not params["target"]:
                params["target"] = random.choice([opponentCharacter["name"] for opponentCharacter in opponentCharacters])
                pass
            
            for char in opponentCharacters:
                if char["name"] == params["target"]:
                    target = char
                    break

            # action_attack(currentCharacter, target_name=params["target"])
            print('attack')

            res = action_attack(currentCharacter["name"], game_code, params["target"], opponentsKey, characterKey)
            turnEnded = res
            if turnEnded:
                games = readGames()
                games[game_code]["current_turn"][0] = (games[game_code]["current_turn"][0] + 1) % 2
                writeGames(games)

            
            pass
        
        case "Skip Turn":

            print(f"{player_id} has skipped their turn.")
            pass
    

    return {"message": "correct player"}


@app.websocket("/game-ws")
async def game_websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    print("message")
    try:
        while True:
            data = await websocket.receive_text()
            

            data_json: dict = json.loads(data)

            print(f"action: {data_json["action"]}")
            print(f"params: {data_json["params"]}")
            print(f"game code: {data_json["game_code"]}")
            

            ret_msg: Dict[str, str] = run_action(
                action=data_json["action"],
                player_id=data_json["player_id"],
                game_code=data_json["game_code"],
                params=data_json["params"]
            )

            print(ret_msg)

            await websocket.send_text(ret_msg["message"])
            # match data_json["action"]:
            #     case "Attack":
                    
            #         pass
            #     case "Forfeit":
            #         pass
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Close")
        print("disconnected")