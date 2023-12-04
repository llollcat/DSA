import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import DSA
from DSA import *


class CheckSignGUI(tk.Tk):
    def __init__(self, L, N):
        super().__init__()
        self.sign = None
        self.wm_title("DSA")
        messagebox.showinfo('Info', 'Выберите сертификат для проверки подписи')
        self.cert_path = filedialog.askopenfilename()

        self.param = DSA.load_public_certificate(self.cert_path)

        self.dsa = DSA(L, N, self.param['p'], self.param['q'], self.param['g'])

        messagebox.showinfo('Info', 'Выберите файл для проверки подписи')
        self.filename = filedialog.askopenfilename()
        self.file_hash = DSA.get_file_hash(self.filename)

        verify = self.dsa.check_sign(self.file_hash, self.param['y'], self.param['r'], self.param['s'])

        messagebox.showinfo('Проверка подписи', "Подпись верна" if verify else "Подпись не верна")

        self.mainloop()
