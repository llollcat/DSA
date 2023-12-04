from DSA import *

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
