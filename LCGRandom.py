class LCGRandom:

    def __init__(self, seed=0,
                 const=155229902547946559768364455795513512670675597892115756896506985123931082767047955648944895487967835745478328129432250014441876138159683012069943751236736450095365516430337940798673559806703032087720573217658988954917232370798314234938509091539554354034402410431378912468558035048681263268068907507291689610089):
        self._seed = seed
        self._num = self._seed
        self._const = const

    # не больше 2049
    def random_num(self, start, end):
        while True:
            self._num = (self._num * self._const + 3567823253) % (1 << 2048)
            out = self._num % (end + 1)
            if out >= start:
                return out

    def change_seed(self, seed):
        self._seed = seed
