import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

from DSA import DSA

if __name__ == '__main__':
    # Create the main window
    root = tk.Tk()

    x = None
    y = None
    h = None
    message = None

    seed = simpledialog.askinteger("Seed", "Введите seed для генерации", initialvalue=0)

    dsa = DSA(512, 160, seed)

    root.title("Отправитель")

    # Set the size of the window
    root.geometry("1600x400")

    # Add labels, entries, and buttons
    label_sign = ttk.Label(root, text="Параметры системы")
    label_sign.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

    label_p = ttk.Label(root, text="p")
    label_p.grid(column=0, row=1, sticky=tk.W, padx=5)

    label_q = ttk.Label(root, text="q")
    label_q.grid(column=0, row=2, sticky=tk.W, padx=5)

    label_g = ttk.Label(root, text="g")
    label_g.grid(column=0, row=3, sticky=tk.W, padx=5)

    label_p_key = ttk.Label(root, text="---")
    label_p_key.grid(column=1, row=1, sticky=tk.W, padx=5)

    label_q_key = ttk.Label(root, text="---")
    label_q_key.grid(column=1, row=2, sticky=tk.W, padx=5)

    label_g_key = ttk.Label(root, text="---")
    label_g_key.grid(column=1, row=3, sticky=tk.W, padx=5)

    label_h = ttk.Label(root, text="hash:")
    label_h.grid(column=0, row=4, sticky=tk.W, padx=5)

    label_r = ttk.Label(root, text="r")
    label_r.grid(column=0, row=5, sticky=tk.W, padx=5)

    label_s = ttk.Label(root, text="s")
    label_s.grid(column=0, row=6, sticky=tk.W, padx=5)

    label_h_key = ttk.Label(root, text="---")
    label_h_key.grid(column=1, row=4, sticky=tk.W, padx=5)

    label_r_key = ttk.Label(root, text="---")
    label_r_key.grid(column=1, row=5, sticky=tk.W, padx=5)

    label_s_key = ttk.Label(root, text="---")
    label_s_key.grid(column=1, row=6, sticky=tk.W, padx=5)

    label_x = ttk.Label(root, text="закрытый ключ x")
    label_x.grid(column=0, row=7, sticky=tk.W, padx=5)

    label_y = ttk.Label(root, text="открытый ключ y")
    label_y.grid(column=0, row=8, sticky=tk.W, padx=5)

    label_x_key = ttk.Label(root, text="---")
    label_x_key.grid(column=1, row=7, sticky=tk.W, padx=5)

    label_y_key = ttk.Label(root, text="---")
    label_y_key.grid(column=1, row=8, sticky=tk.W, padx=5)

    frame_message_box = ttk.LabelFrame(root, text="Окно сообщения", height=100)
    frame_message_box.grid(column=0, row=10, columnspan=3, sticky=tk.EW, padx=5, pady=5)
    frame_message_box.grid_propagate(False)

    # Text box for the message
    text_message = tk.Text(frame_message_box, height=5, width=50)
    text_message.pack(expand=True, padx=5, pady=5)

    param = dsa.get_crypto_parameters()
    label_p_key.config(text=param['p'])
    label_q_key.config(text=param['q'])
    label_g_key.config(text=param['g'])


    def calc_hash():
        global text_message, label_h, h, message
        message = text_message.get("1.0", "end-1c")
        h = dsa.get_str_hash(message)
        label_h_key.config(text=h)


    button_calculate_hash = ttk.Button(root, text="Подсчитать хеш сообщение", command=calc_hash)
    button_calculate_hash.grid(column=3, row=1, sticky=tk.W, padx=5, pady=5)


    def gen_param():
        global dsa, x, y
        p = dsa.generate_new_keys()
        x = p['x']
        y = p['y']
        label_x_key.config(text=str(x))
        label_y_key.config(text=str(y))


    button_keys_generate = ttk.Button(root, text="Сгенерировать открытый и закрытый ключ", command=gen_param)
    button_keys_generate.grid(column=3, row=2, sticky=tk.W, padx=5, pady=5)

    r = None
    s = None
    def sign():
        global label_r_key, label_s_key, h, r, s
        out = dsa.sign(h, x)
        label_r_key.config(text=out['r'])
        label_s_key.config(text=out['s'])

        r = out['r']
        s = out['s']


    button_sign = ttk.Button(root, text="Подписать сообщение", command=sign)
    button_sign.grid(column=3, row=3, sticky=tk.W, padx=5, pady=5)

    is_send = False


    def send():
        global is_send
        is_send = True


    button_send = ttk.Button(root, text="Отправить")
    button_send.grid(column=3, row=4, sticky=tk.W, padx=5, pady=5)

    # Start the main loop

    # Create the main window
    root1 = tk.Tk()
    root1.title("Получатель")

    # Set the size of the window
    root1.geometry("1600x400")

    # Add labels, entries, and buttons
    label_sign = ttk.Label(root1, text="Параметры системы")
    label_sign.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

    label_p_s = ttk.Label(root1, text="p")
    label_p_s.grid(column=0, row=1, sticky=tk.W, padx=5)

    label_q_s = ttk.Label(root1, text="q")
    label_q_s.grid(column=0, row=2, sticky=tk.W, padx=5)

    label_g_s = ttk.Label(root1, text="g")
    label_g_s.grid(column=0, row=3, sticky=tk.W, padx=5)

    label_p_key_s = ttk.Label(root1, text="---")
    label_p_key_s.grid(column=1, row=1, sticky=tk.W, padx=5)

    label_q_key_s = ttk.Label(root1, text="---")
    label_q_key_s.grid(column=1, row=2, sticky=tk.W, padx=5)

    label_g_key_s = ttk.Label(root1, text="---")
    label_g_key_s.grid(column=1, row=3, sticky=tk.W, padx=5)

    label_h_s = ttk.Label(root1, text="hash:")
    label_h_s.grid(column=0, row=4, sticky=tk.W, padx=5)

    label_r_s = ttk.Label(root1, text="r")
    label_r_s.grid(column=0, row=5, sticky=tk.W, padx=5)

    label_s_s = ttk.Label(root1, text="s")
    label_s_s.grid(column=0, row=6, sticky=tk.W, padx=5)

    label_h_key_s = ttk.Label(root1, text="---")
    label_h_key_s.grid(column=1, row=4, sticky=tk.W, padx=5)

    label_r_key_s = ttk.Label(root1, text="---")
    label_r_key_s.grid(column=1, row=5, sticky=tk.W, padx=5)

    label_s_key_s = ttk.Label(root1, text="---")
    label_s_key_s.grid(column=1, row=6, sticky=tk.W, padx=5)

    label_y_s = ttk.Label(root1, text="открытый ключ y")
    label_y_s.grid(column=0, row=8, sticky=tk.W, padx=5)

    label_y_key_s = ttk.Label(root1, text="---")
    label_y_key_s.grid(column=1, row=8, sticky=tk.W, padx=5)

    frame_message_box_s = ttk.LabelFrame(root1, text="Окно сообщения", height=100)
    frame_message_box_s.grid(column=0, row=10, columnspan=3, sticky=tk.EW, padx=5, pady=5)
    frame_message_box_s.grid_propagate(False)

    # Text box for the message
    text_message_s = tk.Text(frame_message_box_s, height=5, width=50)
    text_message_s.pack(expand=True, padx=5, pady=5)


    def get_mess_param():
        global text_message_s, label_p_key_s, label_q_key_s, label_g_key_s, label_r_key_s, label_s_key_s, label_y_key_s
        text_message_s.delete("1.0", "end-1c")
        text_message_s.insert("1.0", message)
        pqg = dsa.get_crypto_parameters()
        label_p_key_s.config(text=pqg['p'])
        label_q_key_s.config(text=pqg['q'])
        label_g_key_s.config(text=pqg['g'])
        label_r_key_s.config(text=str(r))
        label_s_key_s.config(text=str(s))
        label_y_key_s.config(text=str(y))


    button_generate_param_s = ttk.Button(root1, text="Получить параметры и сообщение", command=get_mess_param)
    button_generate_param_s.grid(column=3, row=0, sticky=tk.W, padx=5, pady=5)

    H_s = None


    def hash_s():
        global text_message_s, H_s, label_h_key_s
        mess = text_message_s.get("1.0", "end-1c")
        H_s = dsa.get_str_hash(mess)
        label_h_key_s.config(text=H_s)


    button_calculate_hash_s = ttk.Button(root1, text="Подсчитать хеш сообщение", command=hash_s)
    button_calculate_hash_s.grid(column=3, row=1, sticky=tk.W, padx=5, pady=5)

    def verify():
        global text_message_s
        mess = text_message_s.get("1.0", "end-1c")

        p = dsa.get_str_hash(mess)
        verify = dsa.check_sign(H_s, y, r, s)
        messagebox.showinfo('Проверка подписи', "Подпись верна" if verify else "Подпись не верна")


    button_keys_generate_s = ttk.Button(root1, text="Проверить подпись", command=verify)
    button_keys_generate_s.grid(column=3, row=2, sticky=tk.W, padx=5, pady=5)

    # Start the main loop
    root1.mainloop()
