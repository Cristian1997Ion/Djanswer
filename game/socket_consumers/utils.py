from typing import Final

def get_game_channel_name(roomCode: str) -> str:
    return 'room_{roomCode}_game'.format(roomCode=roomCode)

def get_lobby_channel_name(roomCode: str) -> str:
    return 'room_{roomCode}_lobby'.format(roomCode=roomCode)

GAME_ENGINE_NAME: Final = 'game_engine'