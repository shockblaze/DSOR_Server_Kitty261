"""The server serves the release261_192 client unless told otherwise."""

import os
from unittest.mock import patch

from dso_server.protocol import command_ids


def test_release261_192_table_is_the_default():
    with patch.dict(os.environ):
        os.environ.pop(command_ids.ENVIRONMENT_VARIABLE, None)
        assert command_ids.active_table_path() == command_ids.DEFAULT_TABLE
    assert command_ids.DEFAULT_TABLE.is_file()
    table = command_ids._table(str(command_ids.DEFAULT_TABLE))
    # Ids up to 346 match dro_client64-patch5 ...
    assert table["Commands::HitCommand"] == 107
    assert table["Commands::TimedChallengesInfoCommand"] == 131
    # ... and the commands release261_192 inserts from 347 move the rest.
    assert table["Commands::GetSeasonPassAwardCommand"] == 0x0160 + 3
    assert table["Commands::ServerToClientMsgCommand"] == 381


def test_builtin_keeps_the_patch5_numbers():
    for value in ("builtin", "patch5"):
        with patch.dict(os.environ, {command_ids.ENVIRONMENT_VARIABLE: value}):
            assert command_ids.active_table_path() is None
