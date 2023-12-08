import tkinter as tk
from tkinter import scrolledtext

import hashlib
from LCGRandom import *


class DSA:

    def _fermat_test(self, num):
        tests = list()

        for _ in range(5):
            a = self._rand.random_num(1, num - 1)
            if pow(a, num - 1, num) != 1:
                tests.append(f"pow({a}, {num - 1}, {num}) != 1\n")
                tests.insert(0, False)
                return tests
            tests.append(f"pow({a}, {num - 1}, {num}) == 1\n")
        tests.insert(0, True)
        return tests

    # noinspection PyShadowingNames
    def _is_prime_rabin_miller(self, num):
        tests = list()

        s = num - 1
        t = 0

        while s % 2 == 0:
            s = s // 2
            t += 1

        for _ in range(5):
            a = self._rand.random_num(2, num - 1)
            v = pow(a, s, num)
            if v != 1:
                i = 0
                while v != (num - 1):
                    if i == t - 1:
                        tests.append(f"{i} == {t}-1\n")
                        tests.insert(0, False)

                        return tests
                    else:
                        i = i + 1
                        v = (v ** 2) % num

            tests.append(f"{v} == {num}-1\n")

        tests.insert(0, True)
        return tests

    def is_prime(self, num):
        if num < 2:
            return [False, f"{num}<2\n"]

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
                return [False, f"{num} делится на простое {prime}\n"]

        t1 = self._fermat_test(num)
        t2 = self._is_prime_rabin_miller(num)
        return [(t1[0] and t2[0]), ''.join(t1[1:]), ''.join(t2[1:])]

    def _ex_gcd(self, a, b, arr):
        if b == 0:
            arr[0] = 1
            arr[1] = 0
            return a
        g = self._ex_gcd(b, a % b, arr)
        t = arr[0]
        arr[0] = arr[1]
        arr[1] = t - int(a / b) * arr[1]
        return g

    def get_new_q(self, n_bit_size):
        window = tk.Tk()
        window.title('Получение q')
        window.grid_rowconfigure(0, weight=1)
        text_area = scrolledtext.ScrolledText(window)
        text_area.pack(expand=True, fill='both')
        while True:
            num = self._rand.random_num(2 ** (n_bit_size - 1), 2 ** n_bit_size)

            is_prime = self.is_prime(num)

            text_area.insert(tk.INSERT, ''.join(is_prime[1:]))

            if is_prime[0]:
                text_area.insert(tk.INSERT, 'Число подошло!!!\n\n')
                return num
            text_area.insert(tk.INSERT, '===Поиск другого числа===\n\n')

    def get_new_p_from_q(self, q, L, N):
        window = tk.Tk()
        window.title('Получение p')
        window.grid_rowconfigure(0, weight=1)
        text_area = scrolledtext.ScrolledText(window)
        text_area.pack(expand=True, fill='both')

        while True:
            t = self._rand.random_num(2 << (L - N - 1), (2 << (L - N)) - 1)
            p = t * q + 1

            is_prime = self.is_prime(p)
            text_area.insert(tk.INSERT, ''.join(is_prime[1:]))

            if len(str(bin(p))) - 2 == L and is_prime[0]:
                text_area.insert(tk.INSERT, 'Число подошло!!!\n\n')
                return p
            text_area.insert(tk.INSERT, '===Поиск другого числа===\n\n')

    def get_new_g(self, p, q):
        while True:
            a = self._rand.random_num(1, q - 1)
            g = pow(a, (p - 1) // q, p)

            if g > 1:
                return g

    def mod_reverse(self, a, n):  # ax = 1 (mod n) Нахождение обратного
        arr = [0, 1]
        gcd = self._ex_gcd(a, n, arr)
        if gcd == 1:
            return (arr[0] % n + n) % n
        else:
            return -1

    def __init__(self, p_n_bit_size, q_n_bit_size, seed=0, p=None, q=None, g=None):
        self._rand = LCGRandom()
        self._rand.change_seed(seed)

        self._L = p_n_bit_size
        self._N = q_n_bit_size

        self._q = q or self.get_new_q(self._N)
        self._p = p or self.get_new_p_from_q(self._q, self._L, self._N)
        self._g = g or self.get_new_g(self._p, self._q)

    def get_crypto_parameters(self) -> dict:
        return {'p': self._p, 'q': self._q, 'g': self._g}

    def generate_new_keys(self) -> dict:
        # x - закрытый ключ
        x = self._rand.random_num(1, self._q - 1)
        # y - открытый ключ
        y = pow(self._g, x, self._p)
        return {'x': x, 'y': y}

    def sign(self, file_hash: int, x) -> dict:
        # хеш

        k = self._rand.random_num(1, self._q - 1)
        r = pow(self._g, k, self._p) % self._q
        s = self.mod_reverse(k, self._q) * (file_hash + x * r) % self._q

        return {'r': r, 's': s}

    def check_sign(self, file_hash: int, y: int, r: int, s: int):

        w = self.mod_reverse(s, self._q) % self._q
        u1 = file_hash * w % self._q
        u2 = (r * w) % self._q
        v = (pow(self._g, u1, self._p) * pow(y, u2, self._p)) % self._p % self._q

        return v == r

    def save_public_certificate(self, filename, y, r, s):
        with (open(filename, 'w')) as cert:
            cert.write(f'{self._p}\n')
            cert.write(f'{self._q}\n')
            cert.write(f'{self._g}\n')
            cert.write(f'{y}\n')
            cert.write(f'{r}\n')
            cert.write(f'{s}\n')
            cert.close()

    @staticmethod
    def load_public_certificate(filename):
        out = dict()
        with (open(filename, 'r')) as cert:
            out['p'] = int(cert.readline()[:-1])
            out['q'] = int(cert.readline()[:-1])
            out['g'] = int(cert.readline()[:-1])
            out['y'] = int(cert.readline()[:-1])
            out['r'] = int(cert.readline()[:-1])
            out['s'] = int(cert.readline()[:-1])
        return out

    def save_private_certificate(self, filename, x):
        with (open(filename, 'w')) as cert:
            cert.write(f'{self._p}\n')
            cert.write(f'{self._q}\n')
            cert.write(f'{self._g}\n')
            cert.write(f'{x}\n')
            cert.close()

    @staticmethod
    def load_private_certificate(filename):
        out = dict()
        with (open(filename, 'r')) as cert:
            out['p'] = int(cert.readline()[:-1])
            out['q'] = int(cert.readline()[:-1])
            out['g'] = int(cert.readline()[:-1])
            out['x'] = int(cert.readline()[:-1])
        return out

    @staticmethod
    def get_file_hash(path):
        sha1 = hashlib.sha1()

        with open(path, 'rb') as f:
            while True:
                data = f.read(65536)
                if not data:
                    break
                sha1.update(data)

        return int(sha1.hexdigest(), 16)

    def set_random_seed(self, seed):
        self._rand.change_seed(seed)
