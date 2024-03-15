# secp256k1 values
p = int('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F', 16)
n = int('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141', 16)


# s must have a value in the lower half 
# of n. why? because the additive inverse
# of s is also a valid signature (r, -s mod n)
# this way, you can have 2 different txid's
# with the same signature. that's not very
# interesting; that's why we flip the s
def flip_s(s_int):
    if s_int > n/2:
        s_int = n - s_int

    return s_int


# basically, in order to be explicit about the sign of 
# the value, the first bit cannot be one. this is true 
# for values over 0x80. so, when this is the case, an 0x00
# byte is prepended to the byte array. this is why the
# data field will either be 0x20 (32) or 0x21 (33) bytes long
def convert_bytes(val_int):
    val_bytes = (val_int).to_bytes(32, 'big')

    if val_bytes[0] > 0x80:
        val_bytes = bytes([0x00]) + val_bytes
    
    return val_bytes


def build_tlv(type_val, val_bytes):
    return \
        bytes([type_val]) + \
        bytes([len(val_bytes)]) + \
        val_bytes

# wraps r and s in a TLV, then wraps
# this TLV in another TLV
def sig_to_der(r_int, s_int):
    s_int = flip_s(s_int)

    r = convert_bytes(r_int)
    s = convert_bytes(s_int)

    r_tlv = build_tlv(0x02, r)
    s_tlv = build_tlv(0x02, s)

    rs_tlv = r_tlv + s_tlv

    der = build_tlv(0x30, rs_tlv)

    return der


def sig_from_der(der_hex):
    data = bytes.fromhex(der_hex)

    assert data[0] == 0x30
    
    data_len = data[1]
    assert data_len == len(data[2:])

    assert data[2] == 0x02
    r_len = data[3]
    r_data = data[4:4+r_len]
    r = int.from_bytes(r_data, 'big')

    assert data[4+r_len] == 0x02
    s_len = data[5+r_len]
    s_data = data[6+r_len:6+r_len+s_len]
    s = int.from_bytes(s_data, 'big')

    return (r, s)