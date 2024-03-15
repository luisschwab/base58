import coincurve
from hashlib import sha256

# secp256k1 values
p = int('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F', 16)
n = int('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141', 16)


def sign(message: str, privkey: int) -> tuple[int, int]:
    message = message.encode('utf-8')
    digest = int(sha256(sha256(message).digest()).hexdigest(), 16)
    z = digest
    
    # add random nonce later
    k = 42
    
    while (1):
        # R(x, y) = nonce*G
        Rx = coincurve.PrivateKey.from_int(k).public_key.point()[0]

        # inverse of k
        k1 = pow(k, -1, n)

        # r
        r = Rx % n
        if r == 0: break

        # signature
        s = (k1 * (z + r*privkey)) % n
        if s == 0: break
        
        return (r, s)


def verify(message: str, r: int, s: int, pubkey: str) -> bool:
    if r > n: return False

    if s > n: return False

    message = message.encode('utf-8')
    digest = sha256(sha256(message).digest()).hexdigest()
    z = int(digest, 16)

    s1 = pow(s, -1, n)

    # u = z * r^-1
    u = (z * s1) % n
    
    # v = z * r^-1
    v = (r * s1) % n

    U = coincurve.PrivateKey.from_int(u).public_key

    P = coincurve.PublicKey(bytes.fromhex(pubkey))
    V = P.multiply(v.to_bytes(32, 'big'))

    R = coincurve.PublicKey.combine_keys([V, U])

    if r == R.point()[0]: return True


if __name__ == "__main__":
    message = "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks"
    privkey = 888
    pubkey = coincurve.PrivateKey.from_int(privkey).public_key.format().hex()

    (r, s) = sign(message, privkey)

    verify(message, r, s, pubkey)
