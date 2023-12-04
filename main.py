import random
import hashlib

L = 512  # p size
N = 160  # q size


def rabin_miller(num):
    s = num - 1
    t = 0

    # заменить
    while s % 2 == 0:
        s = s // 2
        t += 1

    for trials in range(5):
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1:
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % num
    return True


def is_prime(num):
    if num < 2:
        return False

    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
                    103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
                    211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
                    331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443,
                    449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577,
                    587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
                    709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839,
                    853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983,
                    991, 997]

    for prime in small_primes:
        if num % prime == 0:
            return False

    return rabin_miller(num)


def get_prime(n_bit_size):
    while True:
        num = random.randrange(2 ** (n_bit_size - 1), 2 ** n_bit_size)
        if is_prime(num):
            return num


def get_p_from_q(q):
    while True:
        t = random.randint(2 << (L - N - 1), (2 << (L - N)) - 1)
        p = t * q + 1
        if len(str(bin(p))) - 2 == L and is_prime(p):
            return p


def get_g(p, q):
    while True:
        a = random.randrange(1, q - 1)
        g = pow(a, (p - 1) // q, p)

        if g > 1:
            return g


def ex_gcd(a, b, arr):
    if b == 0:
        arr[0] = 1
        arr[1] = 0
        return a
    g = ex_gcd(b, a % b, arr)
    t = arr[0]
    arr[0] = arr[1]
    arr[1] = t - int(a / b) * arr[1]
    return g


def mod_reverse(a, n):  # ax = 1 (mod n) Нахождение обратного
    arr = [0, 1]
    gcd = ex_gcd(a, n, arr)
    if gcd == 1:
        return (arr[0] % n + n) % n
    else:
        return -1


if __name__ == '__main__':
    q = get_prime(160)
    p = get_p_from_q(q)
    g = get_g(p, q)
    # x - закрытый ключ
    x = random.randrange(1, q - 1)
    # y - открытый ключ
    y = pow(g, x, p)

    # сообщение
    m = "hello"

    # хеш
    h = int(hashlib.sha1(m.encode('utf-8')).hexdigest(), 16)

    k = random.randint(1, q - 1)

    # Подпись информации m
    print("p:" + str(len(str(bin(p)))))
    print("q:" + str(len(str(bin(q)))))
    print("g:" + str(g))
    print("y:" + str(len(str(bin(y)))))
    r = pow(g, k, p) % q

    s = mod_reverse(k, q) * (h + x * r) % q

    print("Подпись (R, S):" + str(r), str(s))

    s_1 = mod_reverse(s, q)
    w = s_1 % q
    u1 = h * w % q
    u2 = (r * w) % q
    v = (pow(g, u1, p) * pow(y, u2, p)) % p % q
    if v == r:
        print("Подпись верна")
    else:
        print("Подпись неверна")
