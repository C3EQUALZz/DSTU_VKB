#!/usr/bin/env python
#  Copyright 2011 Sybren A. Stüvel <sybren@stuvel.eu>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import pytest
import rsa.key
from rsa.pem import _markers

# 512-bit key. Too small for practical purposes, but good enough for testing with.
public_key_pem = """
-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAKH0aYP9ZFuctlPnXhEyHjgc8ltKKx9M
0c+h4sKMXwjhjbQAZdtWIw8RRghpUJnKj+6bN2XzZDazyULxgPhtax0CAwEAAQ==
-----END PUBLIC KEY-----
"""

private_key_pem = """
-----BEGIN RSA PRIVATE KEY-----
MIIBOwIBAAJBAKH0aYP9ZFuctlPnXhEyHjgc8ltKKx9M0c+h4sKMXwjhjbQAZdtW
Iw8RRghpUJnKj+6bN2XzZDazyULxgPhtax0CAwEAAQJADwR36EpNzQTqDzusCFIq
ZS+h9X8aIovgBK3RNhMIGO2ThpsnhiDTcqIvgQ56knbl6B2W4iOl54tJ6CNtf6l6
zQIhANTaNLFGsJfOvZHcI0WL1r89+1A4JVxR+lpslJJwAvgDAiEAwsjqqZ2wY2F0
F8p1J98BEbtjU2mEZIVCMn6vQuhWdl8CIDRL4IJl4eGKlB0QP0JJF1wpeGO/R76l
DaPF5cMM7k3NAiEAss28m/ck9BWBfFVdNjx/vsdFZkx2O9AX9EJWoBSnSgECIQCa
+sVQMUVJFGsdE/31C7wCIbE3IpB7ziABZ7mN+V3Dhg==
-----END RSA PRIVATE KEY-----
"""

# Private key components
prime1 = 96275860229939261876671084930484419185939191875438854026071315955024109172739
prime2 = 88103681619592083641803383393198542599284510949756076218404908654323473741407


def test_markers():
    assert _markers("RSA PRIVATE KEY") == (
        b"-----BEGIN RSA PRIVATE KEY-----",
        b"-----END RSA PRIVATE KEY-----",
    )


@pytest.mark.parametrize(
    "pem_data", [public_key_pem.encode(), public_key_pem.encode("ascii")]
)
def test_public_key_loading(pem_data):
    key = rsa.key.PublicKey.load_pkcs1_openssl_pem(pem_data)
    assert key.n == prime1 * prime2


@pytest.mark.parametrize(
    "pem_data", [private_key_pem.encode(), private_key_pem.encode("ascii")]
)
def test_private_key_loading(pem_data):
    key = rsa.key.PrivateKey.load_pkcs1(pem_data)
    assert key.p == prime1
    assert key.q == prime2


def test_byte_output_public():
    key = rsa.key.PublicKey.load_pkcs1_openssl_pem(public_key_pem.encode())
    assert isinstance(key.save_pkcs1(file_format="DER"), bytes)
    assert isinstance(key.save_pkcs1(file_format="PEM"), bytes)


def test_byte_output_private():
    key = rsa.key.PrivateKey.load_pkcs1(private_key_pem.encode())
    assert isinstance(key.save_pkcs1(file_format="DER"), bytes)
    assert isinstance(key.save_pkcs1(file_format="PEM"), bytes)


def test_byte_input_public():
    key = rsa.key.PublicKey.load_pkcs1_openssl_pem(public_key_pem.encode("ascii"))
    assert isinstance(key.save_pkcs1(file_format="DER"), bytes)
    assert isinstance(key.save_pkcs1(file_format="PEM"), bytes)


def test_byte_input_private():
    key = rsa.key.PrivateKey.load_pkcs1(private_key_pem.encode("ascii"))
    assert isinstance(key.save_pkcs1(file_format="DER"), bytes)
    assert isinstance(key.save_pkcs1(file_format="PEM"), bytes)
