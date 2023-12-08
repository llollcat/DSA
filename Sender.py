import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import DSA
from DSA import *


class Sender(tk.Tk):
    def __init__(self, L, N):
        super().__init__()
        self.title('Sender')
        self.geometry('')