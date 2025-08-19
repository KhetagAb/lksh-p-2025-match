import pytest
from lkshmatch.adapters.base import Player

@pytest.fixture
def alice() -> Player:
    return Player(tg_id=1, tg_username="alice", core_id=1, name="alice")

@pytest.fixture
def bob() -> Player:
    return Player(tg_id=2, tg_username="bob", core_id=2, name="bob")

def test_players_are_not_equal(alice: Player, bob: Player) -> None:
    assert alice != bob

def test_player_fields(alice: Player) -> None:
    assert alice.tg_id == 1
    assert alice.tg_username == "alice"