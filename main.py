from tkinter import *
from tkinter import ttk
import pyperclip
import sqlite3
import math
conn = sqlite3.connect('orders.db')
cur = conn.cursor()

def validate(new_value):     
    """Проверка на ввод цифр в поле ввода"""                                           
    return new_value == "" or new_value.isnumeric()

def copy(val, buffer = None):
    """
    Копирование данных в буфер обмена
    
    val - Копируемый текст
    buffer - Текстовое поле где отражен скопированный текст

    pyperclip.copy - копирует val в буфер обмена
    """

    pyperclip.copy(val.format(
        aut_text = main.aut_text_entry.get()))

    if buffer != None:
        buffer.delete("1.0", END)
        buffer.insert("2.0", val.format(
        aut_text = main.aut_text_entry.get()))


def add_copy(val, buffer):
    """
    Добавление к копированным данным в буфер обмена
    
    val - Копируемый текст
    buffer - Текстовое поле где отражен скопированный текст

    text - Соединяет содержание буфера обмена с val
    pyperclip.copy - копирует text в буфер обмена
    buffer.insert - Вставляет в текстовое поле val
    """
        
    text = pyperclip.paste() + val.format(
        aut_text = main.aut_text_entry.get())

    pyperclip.copy(text)

    buffer.insert(END, val.format(
        aut_text = main.aut_text_entry.get()))


def past(empty):

    """
    Вставляет в текстовое поле содержимое буфера обмена
    
    empty - Поле в которое нужно вставить текст

    empty_str - Содержание буфера обмена
    empty_new - Новый текст если в конце empty_str есть пробел
    """

    empty_str = pyperclip.paste()
    empty_new = str()
    
    if empty_str[-1] == " ":
        empty_new = empty_str[0:len(empty_str)-1]
    else:
        empty_new = empty_str

    empty.delete(0, END)
    empty.insert(0, empty_new)


def f_counter_plus(empty):

    """
    Добавляет к счетчику значение 1
    empty - поле ввода

    cur.execute - Увеличивает счетчик в БД
    """

    cur.execute("""
    UPDATE counter 
    SET count = count + 1""")
    conn.commit()

    if empty.get() != "":
        new_empty = str(int(empty.get()) + 1)
        empty.delete(0, END)
        empty.insert(0, new_empty)
    else:
        empty.insert(0, "1")

def f_counter_minus(empty):
    
    """
    Убавляет значение 1 со счетчика
    empty - поле ввода

    cur.execute - Уменьшает счетчик в БД
    """

    if empty.get() > "0":

        cur.execute("""
        UPDATE counter 
        SET count = count - 1""")
        conn.commit()

        new_empty = str(int(empty.get()) - 1)
        empty.delete(0, END)
        empty.insert(0, new_empty)
    else:
        pass

def f_counter_null(empty):
    
    """
    Обнуляет счетчик
    empty - поле ввода

    cur.execute - Обнуляет счетчик в БД
    """

    cur.execute("""
    UPDATE counter 
    SET count = 0""")
    conn.commit()

    empty.delete(0, END)
    empty.insert(0, "0")


def assembling_next_page():
    if Assembling.page != Assembling.len_assembling_list:
        Assembling.page += 1
        Assembling.page_list += 14
        Assembling.center_btn.configure(text = f"{Assembling.page}/{Assembling.len_assembling_list}")

        cur.execute(f"SELECT title, text FROM assembling_list LIMIT 14 OFFSET {Assembling.page_list - 1};")
        val_list = cur.fetchall()

        for i_num, i_val in enumerate(Assembling.label_list):
            try:
                i_val.configure(text = val_list[i_num][0])
            except IndexError:
                i_val.configure(text = "")
        
        for i_num, i_val in enumerate(Assembling.btn_assembling_list):
            try:
                val = val_list[i_num][1]
                i_val.configure(command = lambda val=val: copy(val, buffer_assembling))
            except IndexError:
                i_val.configure(state='disabled')

        for i_num, i_val in enumerate(Assembling.add_btn_assembling_list):
            try:
                val = val_list[i_num][1]
                i_val.configure(command = lambda val=val: add_copy(val, buffer_assembling))
            except IndexError:
                i_val.configure(state='disabled')
        
    

def assembling_back_page():
    if Assembling.page != 1:
        Assembling.page -= 1
        Assembling.page_list -= 14
        Assembling.center_btn.configure(text = f"{Assembling.page}/{Assembling.len_assembling_list}")

        cur.execute(f"SELECT title, text FROM assembling_list LIMIT 14 OFFSET {Assembling.page_list - 1};")
        val_list = cur.fetchall()

        for i_num, i_val in enumerate(Assembling.label_list):
            i_val.configure(text = val_list[i_num][0])

        for i_num, i_val in enumerate(Assembling.btn_assembling_list):
                val = val_list[i_num][1]
                i_val.configure(state='normal', command = lambda val=val: copy(val, buffer_assembling))

        for i_num, i_val in enumerate(Assembling.add_btn_assembling_list):
                val = val_list[i_num][1]
                i_val.configure(state='normal', command = lambda val=val: add_copy(val, buffer_assembling))

def assembling_first_page():
    Assembling.page = 1
    Assembling.page_list = 1
    Assembling.center_btn.configure(text = f"{Assembling.page}/{Assembling.len_assembling_list}")

    cur.execute(f"SELECT title, text FROM assembling_list LIMIT 14 OFFSET {Assembling.page_list - 1};")
    val_list = cur.fetchall()

    for i_num, i_val in enumerate(Assembling.label_list):
        i_val.configure(text = val_list[i_num][0])

    for i_num, i_val in enumerate(Assembling.btn_assembling_list):
            val = val_list[i_num][1]
            i_val.configure(state='normal', command = lambda val=val: copy(val, buffer_assembling))

    for i_num, i_val in enumerate(Assembling.add_btn_assembling_list):
            val = val_list[i_num][1]
            i_val.configure(state='normal', command = lambda val=val: add_copy(val, buffer_assembling))

def ready_next_page(category):
    attributes = Ready.attributes_list[category]
    btn_list = Ready.btn_ready_list[category]

    if attributes["page"] != attributes["len_ready_text"]:
        attributes["page"] += 1
        attributes["page_list"] += 10

        len_page = attributes["len_ready_text"]
        page = attributes["page"]
        page_list = attributes["page_list"]

        attributes["|"].configure(text = f"{page}/{len_page}")
        
        cur.execute(f"""
                    SELECT ready_text.title, ready_text.text
                    FROM ready_text
                    JOIN ready_category ON ready_category.id = ready_text.id_category
                    WHERE ready_category.title = "{category[0]}"
                    LIMIT 10 OFFSET {page_list};
                    """)
        val_list = cur.fetchall()
        for i_num, i_val in enumerate(btn_list):
            try:
                val = val_list[i_num][1]
                i_val.configure(text = val_list[i_num][0], command = lambda val=val: copy(val))
            except IndexError:
                i_val.configure(text = "", state='disabled')


def ready_back_page(category):
    attributes = Ready.attributes_list[category]
    btn_list = Ready.btn_ready_list[category]

    if attributes["page"] != 1:
        attributes["page"] -= 1
        attributes["page_list"] -= 10

        len_page = attributes["len_ready_text"]
        page = attributes["page"]
        page_list = attributes["page_list"]

        attributes["|"].configure(text = f"{page}/{len_page}")
        
        cur.execute(f"""
                    SELECT ready_text.title, ready_text.text
                    FROM ready_text
                    JOIN ready_category ON ready_category.id = ready_text.id_category
                    WHERE ready_category.title = "{category[0]}"
                    LIMIT 10 OFFSET {page_list};
                    """)
        val_list = cur.fetchall()
        for i_num, i_val in enumerate(btn_list):
            val = val_list[i_num][1]
            i_val.configure(state='normal', text = val_list[i_num][0], command = lambda val=val: copy(val))


def ready_first_page(category):
    attributes = Ready.attributes_list[category]
    btn_list = Ready.btn_ready_list[category]

    attributes["page"] = 1
    attributes["page_list"] = 1

    len_page = attributes["len_ready_text"]
    page = attributes["page"]
    page_list = attributes["page_list"]

    attributes["|"].configure(text = f"{page}/{len_page}")
    
    cur.execute(f"""
                SELECT ready_text.title, ready_text.text
                FROM ready_text
                JOIN ready_category ON ready_category.id = ready_text.id_category
                WHERE ready_category.title = "{category[0]}"
                LIMIT 10 OFFSET {page_list};
                """)
    val_list = cur.fetchall()
    for i_num, i_val in enumerate(btn_list):
        val = val_list[i_num][1]
        i_val.configure(state='normal', text = val_list[i_num][0], command = lambda val=val: copy(val))

root = Tk()
root.title("TCRM+")
root.geometry("218x640")
root.resizable(width=False, height=False)
root.attributes("-topmost",True)
root.iconbitmap("icon.ico")

class VerticalScrolledFrame(ttk.Frame):

    "Скролл бар"

    def __init__(self, parent, *args, **kw):
        ttk.Frame.__init__(self, parent, *args, **kw)

        vscrollbar = ttk.Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Tk.Canvas(self, bd=0, highlightthickness=0,
                           yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        self.interior = interior = ttk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        def _configure_interior(event):
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

class main:

    """
    Основная панель, содержит: 
    Поле вставки из буфера, 
    счетчик,
    Вкладки.

    frame - Основной фрейм растянутый на все поле
    frame_up - Фрейм шапки приложения
    frame_up_aut_text - Фрейм для вставки
    frame_up_counter - Фрейм счетчика

    frame_bot - Фрейм Вкладок - растянут на всю доступную высоту

    frame_Ready, frame_assembling, frame_rare - Фреймы для закладок

    aut_text_btn - Кнопка вставки в поле aut_text_entry

    counter_plus, counter_minus, counter_null - Кнопки контроля счетчика

    counter - Поле ввода счетчика
    """

    frame = Frame(root)
    frame.place(rely=0, relheight=1, relwidth=1)

    frame_up = Frame(frame)
    frame_up.place(rely=0, relheight=0.08, relwidth=1)

    frame_up_aut_text = Frame(frame_up)
    frame_up_aut_text.place(rely=0, relheight=0.5, relwidth=1)

    frame_up_counter = Frame(frame_up)
    frame_up_counter.place(rely=0.5, relheight=0.5, relwidth=1)

    frame_bot = Frame(frame)
    frame_bot.place(rely=0.08, relheight=1, relwidth=1)

    aut_text_btn = Button(frame_up_aut_text, text = "Вставить", width=10, command= lambda: past(main.aut_text_entry))
    aut_text_btn.grid(column=0, row = 0)

    aut_text_entry = Entry(frame_up_aut_text, width=100)
    aut_text_entry.grid(column=1, row = 0)

    counter_plus = Button(frame_up_counter, text = "+", width=10, command= lambda: f_counter_plus(main.counter))
    counter_plus.grid(column=0, row = 0, sticky="nswe")

    counter_minus = Button(frame_up_counter, text = "-", width=10, command= lambda: f_counter_minus(main.counter))
    counter_minus.grid(column=1, row = 0, sticky="nswe")

    counter_null = Button(frame_up_counter, text = "0", width=1, command= lambda: f_counter_null(main.counter))
    counter_null.grid(column=2, row = 0)

    vcmd = (root.register(validate), '%P')  
    counter = Entry(frame_up_counter, name="counter", width= 100, validate="key", validatecommand=vcmd)
    counter.grid(column=3, row = 0)
    cur.execute("SELECT count FROM counter")
    count = cur.fetchone()[0]
    counter.insert(0, count)
    counter.bind("<Key>", lambda e: "break") 
    

    # создаем набор вкладок
    notebook = ttk.Notebook(frame_bot)
    notebook.pack(expand=True, fill=BOTH)

    # создаем пару фреймвов
    frame_Ready = ttk.Frame(notebook)
    frame_assembling = ttk.Frame(notebook)
    frame_rare = ttk.Frame(notebook)

    frame_Ready.pack(fill=BOTH, expand=True)
    frame_assembling.pack(fill=BOTH, expand=True)
    frame_rare.pack(fill=BOTH, expand=True)

    # добавляем фреймы в качестве вкладок
    notebook.add(frame_Ready, text="Г")
    notebook.add(frame_assembling, text="С")
    notebook.add(frame_rare, text="Р")



class Ready:
    
    """
    Вкладка готовых скриптов. Содержит вкладки категорий скриптов и кнопки для копирования скриптов

    select_title - Список всех категорий
    select_text - Список всех значений с выбранной категории

    frame_Ready - Вкладка категории
    btn_readys - Кнопка для копирования скрипта
    """

    notebook_ready = ttk.Notebook(main.frame_Ready)
    notebook_ready.pack(expand=True, fill=BOTH)
    
    select_title = cur.execute("""
    SELECT title 
    FROM ready_category;
    """)
    ready_category = cur.fetchall()

    btn_ready_list = dict()
    attributes_list = dict()

    for i_category in ready_category:
        frame_Ready = ttk.Frame(notebook_ready)
        frame_Ready.pack(fill=BOTH, expand=True)
        notebook_ready.add(frame_Ready, text=i_category)

        select_text = cur.execute(f"""
        SELECT ready_text.title, ready_text.text 
        FROM ready_text
        JOIN ready_category ON 
        ready_category.id = ready_text.id_category
        WHERE ready_category.title = "{i_category[0]}";
        """)
        ready_text = cur.fetchall()

        page = 1
        page_list = 1
        len_ready_text = math.ceil(len(ready_text) / 10)

        btn_ready_list[i_category] = list()
        attributes_list[i_category] = {
            "<--": None,
            "|": None,
            "-->": None,
            "page": page,
            "page_list": page_list,
            "len_ready_text": len_ready_text,
            }
        for i_val in range(10):
            try:
                key = ready_text[i_val][0]
                val = ready_text[i_val][1]

                btn_readys = Button(frame_Ready, text = key, bg = "yellow", command= lambda val=val: copy(val)) 
                btn_readys.pack(fill = X, pady = 10)
                btn_ready_list[i_category].append(btn_readys)
                
            except IndexError:
                btn_readys = Button(frame_Ready, text = "", bg = "yellow", state='disabled') 
                btn_readys.pack(fill = X, pady = 10)

        left_btn = Button(frame_Ready, width = 11, text = "<--", bg = "yellow", command = lambda i_category=i_category: ready_back_page(i_category))
        left_btn.pack(side=LEFT)
        attributes_list[i_category]["<--"] = left_btn

        center_btn = Button(frame_Ready, width = 4, text = f"{page}/{len_ready_text}", bg = "yellow", command = lambda i_category=i_category: ready_first_page(i_category))
        center_btn.pack(side=LEFT)
        attributes_list[i_category]["|"] = center_btn

        right_btn = Button(frame_Ready, width = 11, text = "-->", bg = "yellow", command = lambda i_category=i_category: ready_next_page(i_category))
        right_btn.pack(side=LEFT)
        attributes_list[i_category]["-->"] = right_btn

class Assembling:
    """
    Вкладка сборочных скриптов. Имеет Кнопки:
    Копировать,
    Добавить к скопированному,
    Вперед X скриптов
    Назад X скриптов

    Имеет текстовое поле для просмотра скопированного

    frame_assembling_left - Фрейм для кнопок копировать и добавить
    frame_assembling_right - Фрейм для титульников для кнопок копирования

    frame_assembling_bot - Фрейм для кнопок переключения и текстового поля буфера
    frame_assembling_bot_arrow - Фрейм для кнопок переключения
    frame_assembling_bot_text - Фрейм для текстового поля буфера

    count - счетчик для столбцов
    assembling_list - список титульников и текстов сборочных скриптов

    btn_assembling - Кнопка копировать
    add_btn_assembling - кнопка добавить к скопированному
    frame_lb - фрейм для текста
    lb - титульник для кнопок копирования
    """

    frame_assembling_left = Frame(main.frame_assembling, width=43.6, height=600)
    frame_assembling_left.pack(side=LEFT, anchor="nw")

    frame_assembling_right = Frame(main.frame_assembling, width=174.8, height=600)
    frame_assembling_right.pack(side=LEFT, anchor="nw")

    frame_assembling_bot = Frame(main.frame_assembling, width=218, height=100)
    frame_assembling_bot.place(y = 400)

    frame_assembling_bot_arrow = Frame(frame_assembling_bot, width=218, height=25, background="red")
    frame_assembling_bot_arrow.grid(column=0, row = 0)

    frame_assembling_bot_text = Frame(frame_assembling_bot, width=218, height=100, background="green")
    frame_assembling_bot_text.grid(column=0, row = 1)

    count = 0
    page = 1
    page_list = 1

    cur.execute("SELECT title, text FROM assembling_list;")
    assembling_list = cur.fetchall()
    len_assembling_list = math.ceil(len(assembling_list) / 14)

    btn_assembling_list = []
    add_btn_assembling_list = []
    label_list = []

    for i_val in assembling_list[page_list - 1: page_list + 13]:
        global btn_assembling, add_btn_assembling, buffer_assembling

        key = i_val[0]
        val = i_val[1]

        btn_assembling = Button(frame_assembling_left, width = 2, text = "С", bg = "yellow", command = lambda val=val: copy(val, buffer_assembling))
        btn_assembling.grid(column=0, row = count)
        btn_assembling_list.append(btn_assembling)

        add_btn_assembling = Button(frame_assembling_left, width = 2, text = "+", bg = "yellow", command = lambda val=val: add_copy(val, buffer_assembling))
        add_btn_assembling.grid(column=1, row = count)
        add_btn_assembling_list.append(add_btn_assembling)

        frame_lb = Frame(frame_assembling_right)
        frame_lb.place(rely=0.043 * count, relheight=1, relwidth=1)

        lb = Label(frame_lb,  text = key)
        lb.grid(column=0, row = count)
        label_list.append(lb)

        count += 1


    left_btn = Button(frame_assembling_bot_arrow, width = 11, text = "<--", bg = "yellow", command = assembling_back_page)
    left_btn.pack(side=LEFT)

    center_btn = Button(frame_assembling_bot_arrow, width = 4, text = f"{page}/{len_assembling_list}", bg = "yellow", command = assembling_first_page)
    center_btn.pack(side=LEFT)

    right_btn = Button(frame_assembling_bot_arrow, width = 11, text = "-->", bg = "yellow", command = assembling_next_page)
    right_btn.pack(side=LEFT)

    buffer_assembling = Text(frame_assembling_bot_text, width=25, height=7, wrap=WORD)
    buffer_assembling.pack()
    buffer_assembling.bind("<Key>", lambda e: "break") 

root.mainloop()

input()