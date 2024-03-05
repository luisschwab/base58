#!/bin/python3

from coincurve import PrivateKey, PublicKey

# Challenge #1
def find_pubkey_point(priv_int):
    return PrivateKey.from_int(priv_int).public_key.point()


# Challenge #2
def find_compressed_key(priv_int):
    return PrivateKey.from_int(priv_int).public_key.format().hex()


# Challenge #3
def find_uncompressed_key(priv_int):
    point = find_pubkey_point(priv_int)

    x_int = point[0]
    y_int = point[1]

    return (bytes([0x04]) + x_int.to_bytes(32, 'big') + y_int.to_bytes(32, 'big')).hex()
    

# Challenge #4
def point_to_compressed(point):
    x, y = point

    if y % 2 == 0:
        parity = 0x02
    else:
        parity = 0x03

    return (bytes([parity]) + x.to_bytes(32, 'big')).hex()


secp256k1_field_size = 115792089237316195423570985008687907853269984665640564039457584007908834671663
def find_y(x_int, parity_value, p=secp256k1_field_size):
    y2 = (x_int**3 + 7) % p

    y = pow(y2, (p + 1) // 4, p)

    if (y % 2) != (parity_value % 2):
        y = p - y

    return y

# Challenge #5
def compressed_to_point(compressed_key):
    parity = int(compressed_key[0:2], 16)
    x_int = int(compressed_key[2:], 16)
    y_int = find_y(x_int, parity)

    return (x_int, y_int)

# Challenge #6
def find_privkey(compressed_key):
    # psa: max value for privkey is 2^16-1,
    # so let's bruteforce it

    for privkey in range(2**16-1):

        if privkey == 0: 
            continue

        pubkey = PrivateKey.from_int(privkey).public_key

        if pubkey.format().hex() == compressed_key:
            return privkey




if __name__ == "__main__":

    # privkey
    k = 777

    # point
    P = find_pubkey_point(k)

    # compressed
    c = find_compressed_key(k)

    print("\npubkey point (k*G):")
    print(find_pubkey_point(k))

    print("\ncompressed pubkey:")
    print(find_compressed_key(k))

    print("\nuncompressed pubkey:")
    print(find_uncompressed_key(k))

    print("\npoint to compressed:")
    print(point_to_compressed(P))

    print("\ncompressed to point:")
    print(compressed_to_point(c))

    print("\nfind privkey:")
    print(find_privkey(c))