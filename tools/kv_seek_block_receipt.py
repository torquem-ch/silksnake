#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The kv_seek_block_receipt command allows to query the turbo-geth/silkworm KV 'Receipts' bucket."""

import argparse

import context # pylint: disable=unused-import

from silksnake.db.cbor import receipt
from silksnake.rlp import sedes
from silksnake.helpers.dbutils import tables
from silksnake.remote import kv_remote
from silksnake.remote import kv_utils
from silksnake.remote.kv_remote import DEFAULT_TARGET

def kv_seek_block_receipt(kv_view: kv_remote.RemoteView, block_height: int, count: int = 1):
    """ Search for the provided block range in KV 'Receipts' bucket of turbo-geth/silkworm running at target.
    """
    for index, block_number in enumerate(range(block_height, block_height + count)):
        encoded_canonical_block_number = sedes.encode_canonical_block_number(block_number)
        print('CANONICAL HEADER\nREQ1 block_number:', block_number, '(key: ' + str(encoded_canonical_block_number.hex()) + ')')
        key, block_hash = kv_view.get(tables.BLOCK_HEADERS_LABEL, encoded_canonical_block_number)
        decoded_block_number = sedes.decode_canonical_block_number(key)
        assert decoded_block_number == block_number, 'ERR block number {} does not match!'.format(decoded_block_number)
        print('RSP1 block_hash:', block_hash.hex(), '\n')

        encoded_block_key = sedes.encode_block_key(block_number, block_hash)
        print('RECEIPT\nREQ2 block_number:', block_number, '(key: ' + str(encoded_block_key.hex()) + ')')
        key, value = kv_view.get(tables.BLOCK_RECEIPTS_LABEL, encoded_block_key)
        decoded_block_number, decoded_block_hash = sedes.decode_block_key(key)
        block_receipt_list = receipt.TransactionReceipt.from_bytes(value)
        assert decoded_block_number == block_number, 'ERR block number {} does not match!'.format(decoded_block_number)
        assert decoded_block_hash == block_hash, 'ERR block hash {} does not match!'.format(decoded_block_hash)
        print('RSP2 block_receipts(' + str(len(block_receipt_list)) + '): [')
        for block_receipt in block_receipt_list:
            print('receipt#' + str(block_receipt_list.index(block_receipt)), block_receipt)
        print(']' if index == count - 1 else ']\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('block_number', help='the block number as integer')
    parser.add_argument('-c', '--count', default=1, help='the number of blocks to seek as integer')
    parser.add_argument('-t', '--target', default=DEFAULT_TARGET, help='the server location as string <address>:<port>')
    args = parser.parse_args()

    kv_utils.kv_func(args.target, kv_seek_block_receipt, int(args.block_number), int(args.count))
