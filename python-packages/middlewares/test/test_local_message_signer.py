"""Tests of 0x.middlewares.local_message_signer."""

from eth_utils import to_checksum_address
from web3 import Web3
from zero_ex.contract_addresses import NETWORK_TO_ADDRESSES, NetworkId
from zero_ex.middlewares.local_message_signer import (
    construct_local_message_signer,
)
from zero_ex.order_utils import (
    generate_order_hash_hex,
    is_valid_signature,
    make_empty_order,
    sign_hash,
)


def test_local_message_signer__sign_order():
    """Test signing order with the local_message_signer middleware"""
    expected_signature = (
        "0x1cd17d75b891accf16030c572a64cf9e7955de63bcafa5b084439cec630ade2d7"
        "c00f47a2f4d5b6a4508267bf4b8527100bd97cf1af9984c0a58e42d25b13f4f0a03"
    )
    address = "0x5409ED021D9299bf6814279A6A1411A7e866A631"
    exchange = NETWORK_TO_ADDRESSES[NetworkId.GANACHE].exchange
    private_key = (
        "f2f48ee19680706196e2e339e5da3491186e0c4c5030670656b0e0164837257d"
    )
    web3_rpc_url = "http://127.0.0.1:8545"
    web3_instance = Web3.HTTPProvider(web3_rpc_url)
    web3_instance.middlewares.add(construct_local_message_signer(private_key))
    order = make_empty_order()
    order_hash = generate_order_hash_hex(order, exchange)
    signature = sign_hash(
        web3_instance, to_checksum_address(address), order_hash
    )
    assert signature == expected_signature
    is_valid = is_valid_signature(
        web3_instance, order_hash, signature, address
    )[0]
    assert is_valid is True
