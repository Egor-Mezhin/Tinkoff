from tkinter import *
from tkinter import ttk
import pyperclip
import sqlite3

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
        for i_val in ready_text:
            key = i_val[0]
            val = i_val[1]
            btn_readys = Button(frame_Ready, text = key, bg = "yellow", command= lambda val=val: copy(val)) 
            btn_readys.pack(fill = X, pady = 10)


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

    cur.execute("SELECT title, text FROM assembling_list;")
    assembling_list = cur.fetchall()

    for i_val in assembling_list:
        global btn_assembling, add_btn_assembling, buffer_assembling

        key = i_val[0]
        val = i_val[1]

        btn_assembling = Button(frame_assembling_left, width = 2, text = "С", bg = "yellow", command = lambda val=val: copy(val, buffer_assembling))
        btn_assembling.grid(column=0, row = count)

        add_btn_assembling = Button(frame_assembling_left, width = 2, text = "+", bg = "yellow", command = lambda val=val: add_copy(val, buffer_assembling))
        add_btn_assembling.grid(column=1, row = count)

        frame_lb = Frame(frame_assembling_right)
        frame_lb.place(rely=0.043 * count, relheight=1, relwidth=1)

        lb = Label(frame_lb,  text = key)
        lb.grid(column=0, row = count)

        count += 1


    left_btn = Button(frame_assembling_bot_arrow, width = 11, text = "<--", bg = "yellow")
    left_btn.pack(side=LEFT)

    right_btn = Button(frame_assembling_bot_arrow, width = 4, text = "1/1", bg = "yellow")
    right_btn.pack(side=LEFT)

    right_btn = Button(frame_assembling_bot_arrow, width = 11, text = "-->", bg = "yellow")
    right_btn.pack(side=LEFT)

    buffer_assembling = Text(frame_assembling_bot_text, width=25, height=7, wrap=WORD)
    buffer_assembling.pack()
    buffer_assembling.bind("<Key>", lambda e: "break") 
    
root.mainloop()