import random
import hashlib


class DSA:

    # noinspection PyShadowingNames
    @staticmethod
    def _is_prime_rabin_miller(num):
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

    @staticmethod
    def _is_prime(num):
        if num < 2:
            return False

        small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
                        101,
                        103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197,
                        199,
                        211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313,
                        317,
                        331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439,
                        443,
                        449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571,
                        577,
                        587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691,
                        701,
                        709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829,
                        839,
                        853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977,
                        983,
                        991, 997]

        for prime in small_primes:
            if num % prime == 0:
                return False

        return DSA._is_prime_rabin_miller(num)

    @staticmethod
    def _ex_gcd(a, b, arr):
        if b == 0:
            arr[0] = 1
            arr[1] = 0
            return a
        g = DSA._ex_gcd(b, a % b, arr)
        t = arr[0]
        arr[0] = arr[1]
        arr[1] = t - int(a / b) * arr[1]
        return g

    @staticmethod
    def _get_new_prime(n_bit_size):
        while True:
            num = random.randrange(2 ** (n_bit_size - 1), 2 ** n_bit_size)
            if DSA._is_prime(num):
                return num

    @staticmethod
    def get_new_q(n_bit_size):
        return DSA._get_new_prime(n_bit_size)

    @staticmethod
    def get_new_p_from_q(q, L, N):
        while True:
            t = random.randint(2 << (L - N - 1), (2 << (L - N)) - 1)
            p = t * q + 1
            if len(str(bin(p))) - 2 == L and DSA._is_prime(p):
                return p

    @staticmethod
    def get_new_g(p, q):
        while True:
            a = random.randrange(1, q - 1)
            g = pow(a, (p - 1) // q, p)

            if g > 1:
                return g

    @staticmethod
    def mod_reverse(a, n):  # ax = 1 (mod n) Нахождение обратного
        arr = [0, 1]
        gcd = DSA._ex_gcd(a, n, arr)
        if gcd == 1:
            return (arr[0] % n + n) % n
        else:
            return -1

    def __init__(self, p_n_bit_size, q_n_bit_size, p=None, q=None, g=None):

        self._L = p_n_bit_size
        self._N = q_n_bit_size

        self._q = q or DSA.get_new_q(self._N)
        self._p = p or DSA.get_new_p_from_q(self._q, self._L, self._N)
        self._g = g or DSA.get_new_g(self._p, self._q)

    def get_crypto_parameters(self) -> dict:
        return {'p': self._p, 'q': self._q, 'g': self._g}

    def generate_new_keys(self) -> dict:
        # x - закрытый ключ
        x = random.randrange(1, self._q - 1)
        # y - открытый ключ
        y = pow(self._g, x, self._p)
        return {'x': x, 'y': y}

    def sign_str(self, message: str, x) -> dict:
        # хеш
        h = int(hashlib.sha1(message.encode('utf-8')).hexdigest(), 16)

        k = random.randint(1, self._q - 1)
        r = pow(self._g, k, self._p) % self._q
        s = DSA.mod_reverse(k, self._q) * (h + x * r) % self._q

        return {'r': r, 's': s}

    def check_sign_str(self, message: str, y: int, r: int, s: int):
        h = int(hashlib.sha1(message.encode('utf-8')).hexdigest(), 16)

        w = DSA.mod_reverse(s, self._q) % self._q
        u1 = h * w % self._q
        u2 = (r * w) % self._q
        v = (pow(self._g, u1, self._p) * pow(y, u2, self._p)) % self._p % self._q

        return v == r


if __name__ == '__main__':
    L = 512
    N = 160

    m = 'Hello world'
    dsa = DSA(L, N)
    keys = dsa.generate_new_keys()
    sign = dsa.sign_str(m, keys['x'])
    print(sign)
    print(keys)
    print(dsa.get_crypto_parameters())
    verify = dsa.check_sign_str(m, keys['y'], **sign)

    print(verify)
