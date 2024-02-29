def find_y(x, parity_value, p):
    y2 = (x**3 + 7) % p

    y = pow(y2, (p + 1) // 4, p)

    if (y % 2) != (parity_value % 2):
        y = p - y

    return y

