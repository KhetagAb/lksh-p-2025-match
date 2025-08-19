import pytest
from lkshmatch.adapters.base import Player

@pytest.fixture
def alice() -> Player:
    return Player(tg_id=1, tg_username="alice")

@pytest.fixture
def bob() -> Player:
    return Player(tg_id=2, tg_username="bob")

def test_players_are_not_equal(alice: Player, bob: Player) -> None:
    assert alice != bob

def test_player_fields(alice: Player) -> None:
    assert alice.tg_id == 1
    assert alice.tg_username == "alice"

@pytest.mark.parametrize(
    "tg_id, username",
    [
        (10, "charlie"),
        (11, "diana"),
    ],
)
def test_parametrized_players(tg_id: int, username: str) -> None:
    player = Player(tg_id=tg_id, tg_username=username)
    assert player.tg_id == tg_id
    assert player.tg_username == username
