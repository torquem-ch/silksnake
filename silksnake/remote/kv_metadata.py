# -*- coding: utf-8 -*-
"""The turbo-geth/silkworm KV application protocol metadata."""

from silksnake.core.constants import ADDRESS_SIZE

ACCOUNTS_HISTORY_LABEL: str = 'hAT'
BLOCK_BODIES_LABEL: str = 'b'
BLOCK_HEADERS_LABEL: str = 'h'
BLOCK_HEADER_NUMBERS_LABEL: str = 'H'
BLOCK_RECEIPTS_LABEL: str = 'r'
PLAIN_STATE_LABEL: str = 'PLAIN-CST2'
TRANSACTION_LOOKUP_LABEL: str = 'l'
TRANSACTION_SENDERS_LABEL: str = 'txSenders'

ACCOUNTS_HISTORY_NAME: str = 'History Of Accounts'
BLOCK_BODIES_NAME: str = 'Block Bodies'
BLOCK_HEADERS_NAME: str = 'Headers'
BLOCK_HEADER_NUMBERS_NAME: str = 'Header Numbers'
BLOCK_RECEIPTS_NAME: str = 'Receipts'
PLAIN_STATE_NAME: str = 'Plain State'
TRANSACTION_LOOKUP_NAME: str = 'Transaction Index'
TRANSACTION_SENDERS_NAME: str = 'Senders'

bucketLabels: [str] = [
    BLOCK_BODIES_LABEL,
    BLOCK_HEADERS_LABEL,
    BLOCK_HEADER_NUMBERS_LABEL,
    BLOCK_RECEIPTS_LABEL,
    PLAIN_STATE_LABEL,
    TRANSACTION_LOOKUP_LABEL,
    TRANSACTION_SENDERS_LABEL,
]

bucketDescriptors: [str] = {
    BLOCK_BODIES_LABEL: BLOCK_BODIES_NAME,
    BLOCK_HEADERS_LABEL: BLOCK_HEADERS_NAME,
    BLOCK_HEADER_NUMBERS_LABEL: BLOCK_HEADER_NUMBERS_NAME,
    BLOCK_RECEIPTS_LABEL: BLOCK_RECEIPTS_NAME,
    PLAIN_STATE_LABEL: PLAIN_STATE_NAME,
    TRANSACTION_LOOKUP_LABEL: TRANSACTION_LOOKUP_NAME,
    TRANSACTION_SENDERS_LABEL: TRANSACTION_SENDERS_NAME,
}

INVALID_BLOCK_NUMBER = -1

def encode_account_address(account_address: str) -> bytes:
    """ Encode the given hex account address as 20-byte buffer.
    """
    account_address = account_address[2:] if account_address.startswith('0x') else account_address
    return bytes.fromhex(account_address)

def encode_account_history_key(account_address: str, block_number: int = INVALID_BLOCK_NUMBER) -> bytes:
    """ Encode the given hex account address and block number as 28-byte BigEndian buffer.
    """
    account_address_bytes = encode_account_address(account_address)
    if block_number >= 0:
        block_number_bytes = int.to_bytes(block_number, 8, 'big')
        account_history_key = account_address_bytes + block_number_bytes
    else:
        account_history_key = account_address_bytes
    return account_history_key

def encode_incarnation(incarnation: int, *, signed: bool = False) -> bytes:
    """ Encode the given incarnation integer as 8-byte BigEndian buffer.
    """
    return int.to_bytes(incarnation, 8, 'big', signed=signed)

def encode_storage_location(storage_location: str) -> bytes:
    """ Encode the given storage_location integer as 32-byte BigEndian buffer.
    """
    storage_location = storage_location[2:] if storage_location.startswith('0x') else storage_location
    return int.to_bytes(int(storage_location), 32, 'big')

def decode_account_address_list(address_list_bytes: bytes):
    """ Decode the given data bytes as concatenated list of 20-byte addresses.
    """
    num_addresses = len(address_list_bytes) // ADDRESS_SIZE
    account_address_list = []
    for i in range(num_addresses):
        account_address = address_list_bytes[i : i + ADDRESS_SIZE]
        account_address_list.append(account_address)
    return account_address_list
