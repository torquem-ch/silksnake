# -*- coding: utf-8 -*-
"""The unit test for changeset module."""

import pytest

from silksnake.core.changeset import AccountChangeSet, Change, ChangeSet

# pylint: disable=line-too-long,no-self-use

class TestChange:
    """ Unit test case for Change.
    """
    @pytest.mark.parametrize("key_hex,value_hex,should_pass", [
        # Valid test list
        ('0000000000000000', '00', True),

        # Invalid test list
        (None, None, False),
        ('', '', False),
    ])
    def test_init(self, key_hex: str, value_hex: str, should_pass: bool):
        """ Unit test for __init__. """
        key = bytes.fromhex(key_hex) if key_hex is not None else None
        value = bytes.fromhex(value_hex) if value_hex is not None else None
        if should_pass:
            change = Change(key, value)
            assert change.key == key
            assert change.value == value
            assert str(change)
        else:
            with pytest.raises((TypeError, ValueError)):
                Change(key, value)

class TestChangeSet:
    """ Unit test case for ChangeSet.
    """
    def test_init(self):
        """ Unit test for __init__. """
        changeset = ChangeSet()
        assert len(changeset.changes) == 0
        assert str(changeset)

    def test_add(self):
        """ Unit test for add. """
        changeset = ChangeSet()
        change = Change(b'\x00', b'')
        changeset.add(change)
        assert len(changeset.changes) == 1
        assert changeset.changes.pop() is change

    def test_iter(self):
        """ Unit test for iter. """
        changeset = ChangeSet()
        change1 = Change(b'\x00', b'')
        change2 = Change(b'\x01', b'')
        changeset.add(change1)
        changeset.add(change2)
        for change in changeset:
            assert change

class TestAccountChangeSet:
    """ Unit test case for AccountChangeSet.
    """
    @pytest.mark.parametrize("buffer_hex,key_length,should_pass", [
        # Valid test list
        ('00000000', 0, True),
        ('00000000', 1, True),
        ('00000000', 20, True),
        ('00000000', 32, True),

        # Invalid test list
        (None, 0, False),
        ('0000000000000000', None, False),
        (None, None, False),
        ('', 0, False),
        ('00', 0, False),
        ('0000', 0, False),
        ('000000', 0, False),
        ('00000000', -1, False),
        ('00000000', '0', False),
    ])
    def test_init(self, buffer_hex: str, key_length: int, should_pass: bool):
        """ Unit test for __init__. """
        buffer = bytes.fromhex(buffer_hex) if buffer_hex is not None else None
        if should_pass:
            changeset = AccountChangeSet(buffer, key_length)
            assert changeset.buffer == buffer
            assert changeset.key_length == key_length
        else:
            with pytest.raises((TypeError, ValueError)):
                AccountChangeSet(buffer, key_length)
