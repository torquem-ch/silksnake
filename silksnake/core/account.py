# -*- coding: utf-8 -*-
"""The storage encoding/decoding for accounts."""

import enum

from .constants import HASH_SIZE

class AccountFieldSet(enum.IntFlag):
    """ This class represents the account fields.
    """
    NONE = 0
    NONCE = 1
    BALANCE = 2
    INCARNATION = 4
    CODE_HASH = 8
    STORAGE_ROOT = 16

class Account:
    """ This class represents the blockchain account.
    """
    @classmethod
    def from_storage(cls, account_bytes: bytes):
        """ Create an account from serialized account_bytes."""
        if len(account_bytes) == 0:
            raise ValueError('zero length account_bytes')

        def read_next(pos: int, length: int) -> (int, bytes):
            value_bytes = account_bytes[pos + 1 : pos + length + 1]
            value_length = len(value_bytes)
            if value_length != length:
                raise ValueError('expected length ' + str(length) + ', actual ' + str(value_length))
            return pos + length + 1, value_bytes

        fieldset = AccountFieldSet(account_bytes[0])
        pos = 1

        nonce = 0
        if fieldset & AccountFieldSet.NONCE:
            pos, nonce_bytes = read_next(pos, account_bytes[pos])
            nonce = int.from_bytes(nonce_bytes, 'big')

        balance = 0
        if fieldset & AccountFieldSet.BALANCE:
            pos, balance_bytes = read_next(pos, account_bytes[pos])
            balance = int.from_bytes(balance_bytes, 'big')

        incarnation = 0
        if fieldset & AccountFieldSet.INCARNATION:
            pos, incarnation_bytes = read_next(pos, account_bytes[pos])
            incarnation = int.from_bytes(incarnation_bytes, 'big')

        code_hash = ''
        if fieldset & AccountFieldSet.CODE_HASH:
            pos, code_hash_bytes = read_next(pos, account_bytes[pos])
            code_hash = code_hash_bytes.hex()

        return Account(nonce, balance, incarnation, code_hash, '')

    def __init__(self, nonce: int, balance: int, incarnation: int, code_hash: str, storage_root: str):
        self.nonce = nonce
        self.balance = balance
        self.incarnation = incarnation
        self.code_hash = code_hash
        self.storage_root = storage_root

    def length_for_storage(self):
        """ length_for_storage """
        length = 1 # always 1 byte for fieldset

        if self.nonce > 0:
            num_nonce_bytes = (self.nonce.bit_length() + 7) // 8
            length += 1 + num_nonce_bytes

        if self.balance > 0:
            num_balance_bytes = (self.balance.bit_length() + 7) // 8
            length += 1 + num_balance_bytes

        if self.incarnation > 0:
            num_incarnation_bytes = (self.incarnation.bit_length() + 7) // 8
            length += 1 + num_incarnation_bytes

        if self.code_hash:
            length += 1 + HASH_SIZE

        return length

    def to_storage(self, account_bytes: bytes) -> None:
        """ to_storage """
        if len(account_bytes) == 0:
            raise ValueError('zero length account_bytes')
        if len(account_bytes) != self.length_for_storage():
            raise ValueError('invalid account_bytes length, expected {} got {}'.format(self.length_for_storage(), len(account_bytes)))

        fieldset = AccountFieldSet.NONE
        pos = 1

        if self.nonce > 0:
            fieldset = AccountFieldSet.NONCE
            num_nonce_bytes = (self.nonce.bit_length() + 7) // 8
            account_bytes[pos] = num_nonce_bytes
            nonce = self.nonce
            for i in range(num_nonce_bytes, 0, -1):
                account_bytes[pos+i] = nonce
                nonce >>= 8
            pos += num_nonce_bytes + 1

        if self.balance > 0:
            fieldset |= AccountFieldSet.BALANCE
            num_balance_bytes = (self.balance.bit_length() + 7) // 8
            account_bytes[pos] = num_balance_bytes
            pos += 1
            account_bytes[pos : pos+num_balance_bytes] = self.balance.to_bytes(num_balance_bytes, 'big') # TBD: check
            pos += num_balance_bytes

        if self.incarnation > 0:
            fieldset |= AccountFieldSet.INCARNATION
            num_incarnation_bytes = (self.incarnation.bit_length() + 7) // 8
            account_bytes[pos] = num_incarnation_bytes
            incarnation = self.incarnation
            for i in range(num_incarnation_bytes, 0, -1):
                account_bytes[pos+i] = incarnation
                incarnation >>= 8
            pos += num_incarnation_bytes + 1

        if self.code_hash:
            fieldset |= AccountFieldSet.CODE_HASH
            account_bytes[pos] = HASH_SIZE
            account_bytes[pos+1:] = bytes.fromhex(self.code_hash)

        account_bytes[0] = fieldset

    def __str__(self):
        beautify = (lambda v: v.hex() if isinstance(v, bytes) else v)
        fields = tuple('{}={!r}'.format(k, beautify(v)) for k, v in self.__dict__.items())
        return '({})'.format(", ".join(fields))
