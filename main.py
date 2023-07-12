from tkinter import *
from tkinter import ttk
import pyperclip
import sqlite3
import ctypes
import math
conn = sqlite3.connect('orders.db')
cur = conn.cursor()
        
def is_ru_lang_keyboard():
    """
    Функция для работы функции keys. Для работы блокнота в русской раскладке
    """
    u = ctypes.windll.LoadLibrary("user32.dll")
    pf = getattr(u, "GetKeyboardLayout")
    return hex(pf(0)) == '0x4190419'

def keys(event):
    """
    Функция для работы блокнота в русской раскладке. Закрепляет за кнопками команты копировать вставить и тд
    """
    if is_ru_lang_keyboard():
        if event.keycode==86:
            event.widget.event_generate("<<Paste>>")
        elif event.keycode==67: 
            pyperclip.copy(event.widget.selection_get())
        elif event.keycode==88:  
            pyperclip.copy(event.widget.selection_get())
            event.widget.delete("sel.first", "sel.last")
        elif event.keycode==65535: 
            event.widget.event_generate("<<Clear>>")
        elif event.keycode==65: 
            event.widget.event_generate("<<SelectAll>>")
        elif event.keycode == 90 and (event.state & 0x4):
            event.widget.edit_undo()
        # TODO: Добавить Ctrl + backstase

def copy(val, buffer = None):
    """
    Копирование данных в буфер обмена
    
    val - Копируемый текст
    buffer - Текстовое поле где отражен скопированный текст

    pyperclip.copy - копирует val в буфер обмена
    """

    pyperclip.copy(val.format(main.aut_text_entry.get()))

    if buffer != None:
        buffer.delete("1.0", END)
        buffer.insert("2.0", val.format(main.aut_text_entry.get()))


def add_copy(val, buffer):
    """
    Добавление к копированным данным в буфер обмена
    
    val - Копируемый текст
    buffer - Текстовое поле где отражен скопированный текст

    text - Соединяет содержание буфера обмена с val
    pyperclip.copy - копирует text в буфер обмена
    buffer.insert - Вставляет в текстовое поле val
    """
        
    text = pyperclip.paste() + val.format(main.aut_text_entry.get())

    pyperclip.copy(text)

    buffer.insert(END, val.format(main.aut_text_entry.get()))


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


def f_counter_plus(label):

    """
    Добавляет к счетчику значение 1
    empty - поле ввода

    cur.execute - Увеличивает счетчик в БД
    """

    cur.execute("""
    UPDATE counter 
    SET count = count + 1""")
    conn.commit()

    new_empty = str(int(label["text"]) + 1)
    label["text"] = new_empty


def f_counter_minus(label):
    
    """
    Убавляет значение 1 со счетчика
    empty - поле ввода

    cur.execute - Уменьшает счетчик в БД
    """

    if label["text"] > "0":

        cur.execute("""
        UPDATE counter 
        SET count = count - 1""")
        conn.commit()

        new_empty = str(int(label["text"]) - 1)
        label["text"] = new_empty


def f_counter_null(label):
    
    """
    Обнуляет счетчик
    empty - поле ввода

    cur.execute - Обнуляет счетчик в БД
    """

    cur.execute("""
    UPDATE counter 
    SET count = 0""")
    conn.commit()

    label["text"] = "0"


def assembling_next_page():
    """
    Переключение страниц скриптов вперед для вкладки сборочных скриптов
    
    Assembling.page - страница скриптов
    Assembling.page_list - Начальный элемент страницы скриптов
    Assembling.center_btn - Кнопка с обозначением страницы скриптов

    val_list - Новый список скриптов

    for i_num, i_val in enumerate(Assembling.label_list) - Переименование текста скриптов
    for i_num, i_val in enumerate(
        Assembling.btn_assembling_list / add_btn_assembling_list
        ) - Переименование закрепленных скриптов на кнопках

    """
        
    if Assembling.page != Assembling.len_assembling_list:
        Assembling.page += 1
        Assembling.page_list += 15
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
    """
    Переключение страниц скриптов назад для вкладки сборочных скриптов
    
    Assembling.page - страница скриптов
    Assembling.page_list - Начальный элемент страницы скриптов
    Assembling.center_btn - Кнопка с обозначением страницы скриптов

    val_list - Новый список скриптов

    for i_num, i_val in enumerate(Assembling.label_list) - Переименование текста скриптов
    for i_num, i_val in enumerate(
        Assembling.btn_assembling_list / add_btn_assembling_list
        ) - Переименование закрепленных скриптов на кнопках

    """
    if Assembling.page != 1:
        Assembling.page -= 1
        Assembling.page_list -= 15
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
    """
    Переключение страниц скриптов на первую для вкладки сборочных скриптов
    
    Assembling.page - страница скриптов
    Assembling.page_list - Начальный элемент страницы скриптов
    Assembling.center_btn - Кнопка с обозначением страницы скриптов

    val_list - Новый список скриптов

    for i_num, i_val in enumerate(Assembling.label_list) - Переименование текста скриптов
    for i_num, i_val in enumerate(
        Assembling.btn_assembling_list / add_btn_assembling_list
        ) - Переименование закрепленных скриптов на кнопках

    """
        
    Assembling.page = 1
    Assembling.page_list = 0
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

def ready_next_page():
    """
    Переключение страниц скриптов вперед для вкладки готовых скриптов
    
    attributes - класс вкладки
    btn_list - список кнопок
    attributes.page - страница скриптов
    attributes.page_list - Начальный элемент страницы скриптов

    val_list - Новый список скриптов

    for i_num, i_val in enumerate(btn_list): - Переименование текста и закрепленных за кнопкой скриптов
    """
        
    attributes = Ready
    btn_list = Ready.btn_ready_list

    if attributes.page != attributes.len_ready_text:
        attributes.page += 1
        attributes.page_list += 10

        len_page = attributes.len_ready_text
        page = attributes.page
        page_list = attributes.page_list

        attributes.center_btn.configure(text = f"{page}/{len_page}")
        
        cur.execute(f"""
                    SELECT ready_text.title, ready_text.text
                    FROM ready_text
                    JOIN ready_category ON ready_category.id = ready_text.id_category
                    WHERE ready_category.title = "{attributes.category}"
                    LIMIT 10 OFFSET {page_list};
                    """)
        val_list = cur.fetchall()
        for i_num, i_val in enumerate(btn_list):
            try:
                val = val_list[i_num][1]
                i_val.configure(text = val_list[i_num][0], command = lambda val=val: copy(val))

            except IndexError:
                i_val.configure(text = "", state='disabled')


def ready_back_page():
    """
    Переключение страниц скриптов назад для вкладки готовых скриптов
    
    attributes - класс вкладки
    btn_list - список кнопок
    attributes.page - страница скриптов
    attributes.page_list - Начальный элемент страницы скриптов

    val_list - Новый список скриптов

    for i_num, i_val in enumerate(btn_list): - Переименование текста и закрепленных за кнопкой скриптов
    """

    attributes = Ready
    btn_list = Ready.btn_ready_list

    if attributes.page != 1:
        attributes.page -= 1
        attributes.page_list -= 10

        len_page = attributes.len_ready_text
        page = attributes.page
        page_list = attributes.page_list

        attributes.center_btn.configure(text = f"{page}/{len_page}")
        
        cur.execute(f"""
                    SELECT ready_text.title, ready_text.text
                    FROM ready_text
                    JOIN ready_category ON ready_category.id = ready_text.id_category
                    WHERE ready_category.title = "{attributes.category}"
                    LIMIT 10 OFFSET {page_list};
                    """)
        val_list = cur.fetchall()
        for i_num, i_val in enumerate(btn_list):
            
            key = val_list[i_num][0]
            val = val_list[i_num][1]

            i_val.configure(text = key, command = lambda val=val: copy(val))


def ready_first_page():
    """
    Переключение страниц скриптов на первую для вкладки готовых скриптов
    
    attributes - класс вкладки
    btn_list - список кнопок
    attributes.page - страница скриптов
    attributes.page_list - Начальный элемент страницы скриптов

    val_list - Новый список скриптов

    for i_num, i_val in enumerate(btn_list): - Переименование текста и закрепленных за кнопкой скриптов
    """

    attributes = Ready
    btn_list = Ready.btn_ready_list
    
    attributes.page = 1
    attributes.page_list = 0

    len_page = attributes.len_ready_text
    page = attributes.page
    page_list = attributes.page_list

    attributes.center_btn.configure(text = f"{page}/{len_page}")
    
    cur.execute(f"""
                SELECT ready_text.title, ready_text.text
                FROM ready_text
                JOIN ready_category ON ready_category.id = ready_text.id_category
                WHERE ready_category.title = "{attributes.category}"
                LIMIT 10 OFFSET {page_list};
                """)
    val_list = cur.fetchall()
    for i_num, i_val in enumerate(btn_list):
        try:
            val = val_list[i_num][1]
            i_val.configure(text = val_list[i_num][0], command = lambda val=val: copy(val))

        except IndexError:
            i_val.configure(text = "", state='disabled')

def ready_swap_category(category):
    """
    Переключение категорий скриптов для вкладки готовых скриптов
    
    Ready.category - Новая категория
    Ready.page - страница скриптов
    Ready.page_list - Начальный элемент страницы скриптов

    ready_text - Новый список скриптов
    len_ready_text - новое максимальное значение для колличества страниц

    for i_val in Ready.category_list - Перекраска кнопок категорий.
    for i_val in range(10) - Переименование кнопок из ready_text 
    """

    Ready.category = category
    Ready.page = 1
    Ready.page_list = 0

    cur.execute(f"""
    SELECT ready_text.title, ready_text.text 
    FROM ready_text
    JOIN ready_category ON 
    ready_category.id = ready_text.id_category
    WHERE ready_category.title = "{Ready.category}"
    ORDER BY ready_text.id;
    """)
    ready_text = cur.fetchall()
    
    len_ready_text = math.ceil(len(ready_text) / 10)
    if len_ready_text == 0:
        len_ready_text = 1
        
    Ready.len_ready_text = len_ready_text

    for i_val in Ready.category_list:
        if i_val["text"] == category:
           i_val.configure(bg = "white", state='disabled') 
        else:
            i_val.configure(bg = "yellow", state='normal')

    for i_val in range(10):
        try:
            key = ready_text[i_val][0]
            val = ready_text[i_val][1]

            Ready.btn_ready_list[i_val].configure(text = key, state='normal', command= lambda val=val: copy(val))

        except IndexError:
            Ready.btn_ready_list[i_val].configure(text = "", state='disabled') 
    
    Ready.center_btn.configure(text = f"1/{len_ready_text}")

def switching_assembling_combobox(event):
    c = Settings_Assembling
    choice = c.choice_val_menu.get()

    if choice == "+ Добавить новый скрипт":
        c.title_empty.delete(0, END)
        c.title_empty.insert(0, "Титульник")

        c.text_empty.delete("1.0", END)
        c.text_empty.insert("1.0", "Текст скрипта")

        c.choice_num_menu.configure(values = c.num_list)

        c.btn_save.configure(bg = "green", text = "Сохранить")
        c.btn_delete.configure(state='disabled')
    else:
        index_title = int(choice[:choice.index('|')])
        
        text = c.val_list[index_title - 1][2]
        c.choice_variable_num.set(index_title) 

        c.title_empty.delete(0, END)
        c.title_empty.insert(0, choice[choice.index(" ") + 1:])

        c.text_empty.delete("1.0", END)
        c.text_empty.insert("1.0", text)
        
        num_list = c.num_list[:len(c.num_list) - 1]
        c.choice_num_menu.configure(values = num_list)

        c.btn_save.configure(bg = "yellow", text = "Изменить", state='normal')
        c.btn_delete.configure(state='normal')

def assembling_delete():

    c = Settings_Assembling
    choice = c.choice_val_menu.get()
    index_title = int(choice[:choice.index('|')])
    
    cur.execute(f"DELETE FROM assembling_list where id = '{index_title}';")
    cur.execute(f"UPDATE assembling_list SET id = id - 1 WHERE id > '{index_title}'")
    conn.commit()

    cur.execute("SELECT id, title, text FROM assembling_list;")
    c.val_list = cur.fetchall()

    num_list = [i_val[0] for i_val in c.val_list]
    num_list.append(len(num_list) + 1)
    c.num_list = num_list

    title_list = [f"{i_val[0]}| " + i_val[1] for i_val in c.val_list]
    c.title_list = ["+ Добавить новый скрипт"] + title_list + ["+ Добавить новый скрипт"]
    
    c.choice_variable_num.set(1) 
    c.choice_variable_val.set(c.title_list[0]) 
    c.choice_num_menu.configure(values = c.num_list)
    c.choice_val_menu.configure(values = c.title_list)
    
    c.title_empty.delete(0, END)
    c.title_empty.insert(0, "Титульник")
    c.text_empty.delete("1.0", END)
    c.text_empty.insert("1.0", "Текст скрипта")
    c.btn_save.configure(bg = "green", text = "Сохранить")

def assembling_save():
    c = Settings_Assembling
    choice = choice = c.choice_val_menu.get()
    index = int(c.choice_variable_num.get())
    title = c.title_empty.get()
    text = c.text_empty.get("1.0", END)

    if choice == "+ Добавить новый скрипт":

        max_index = len(c.val_list) + 1

        for i_index in range(max_index, index - 1, -1):       
            cur.execute(f"UPDATE assembling_list SET id = id + 1 WHERE id = '{i_index}'")
            conn.commit()

        cur.execute("INSERT INTO assembling_list(id, title, text) VALUES (?, ?, ?)", (index, title, text))
        conn.commit()

    else:
        index_title = int(choice[:choice.index('|')])
        if index_title == index:
            cur.execute(f"UPDATE assembling_list SET title = ?, text = ? WHERE id = ?", (title, text, index_title))
            conn.commit()
            
        elif index_title < index:    
            cur.execute(f"DELETE FROM assembling_list where id = '{index_title}';")
            cur.execute(f"UPDATE assembling_list SET id = id - 1 WHERE id > '{index_title}' AND id < '{index + 1}'")
            cur.execute("INSERT INTO assembling_list(id, title, text) VALUES (?, ?, ?)", (index, title, text))
            conn.commit()

        else:
            cur.execute(f"DELETE FROM assembling_list where id = '{index_title}';")
            
            for i_index in range(index_title - 1, index - 1, -1):       
                cur.execute(f"UPDATE assembling_list SET id = id + 1 WHERE id = '{i_index}'")
                conn.commit()

            cur.execute("INSERT INTO assembling_list(id, title, text) VALUES (?, ?, ?)", (index, title, text))
            conn.commit()
        

    cur.execute("SELECT id, title, text FROM assembling_list;")
    c.val_list = cur.fetchall()

    num_list = [i_val[0] for i_val in c.val_list]
    num_list.append(len(num_list) + 1)
    c.num_list = num_list
    
    title_list = [f"{i_val[0]}| " + i_val[1] for i_val in c.val_list]
    c.title_list = ["+ Добавить новый скрипт"] + title_list + ["+ Добавить новый скрипт"]
    
    c.choice_variable_num.set(1) 
    c.choice_variable_val.set(c.title_list[0]) 
    c.choice_num_menu.configure(values = c.num_list)
    c.choice_val_menu.configure(values = c.title_list)
    
    c.title_empty.delete(0, END)
    c.title_empty.insert(0, "Титульник")

    c.text_empty.delete("1.0", END)
    c.text_empty.insert("1.0", "Текст скрипта")

    c.btn_save.configure(bg = "green", text = "Сохранить")

def switching_category_combobox(event):
    c = Settings_Ready
    choice = c.choice_category_val.get()

    if choice == "+ Добавить новую категорию":
        c.title_empty.delete(0, END)
        c.title_empty.insert(0, "Титульник")

        c.choice_script_num_menu.configure(state='disabled')
        c.choice_script_menu.configure(state='disabled')

        c.choice_category_num_menu.configure(values = c.category_num_list)
        
        c.btn_save.configure(bg = "green", text = "Сохранить")
        c.btn_delete.configure(state='disabled')
    else:
        index_title = int(choice[:choice.index('|')])
        cur.execute(f"SELECT id FROM ready_category WHERE num = '{index_title}';")
        id_category = cur.fetchone()[0]

        cur.execute(f"SELECT id, title, text FROM ready_text WHERE id_category = {id_category} ORDER BY id;")
        c.script_list = cur.fetchall()

        c.script_num_list = [i_val[0] for i_val in c.script_list]
        c.script_num_list.append(len(c.script_num_list) + 1)
        c.script_title_list = [f"{i_val[0]}| " + i_val[1] for i_val in c.script_list]
        c.script_title_list = ["+ Добавить новый скрипт", ""] + c.script_title_list + ["", "+ Добавить новый скрипт"]
        
        category_num_list = c.category_num_list[:len(c.category_num_list)-1]
        c.choice_category_num_menu.configure(values = category_num_list)

        c.choice_script_num_menu.configure(values = c.script_num_list)
        c.choice_script_menu.configure(values = c.script_title_list , state='readonly')

        c.choice_category_num.set(index_title) 
 
        c.title_empty.delete(0, END)
        c.title_empty.insert(0, choice[choice.index(" ") + 1:])

        c.btn_save.configure(bg = "yellow", text = "Изменить", state='normal')
        c.btn_delete.configure(state='normal')
    
    c.choice_script_num.set("") 
    c.choice_script_val.set("") 
    c.choice_script_num_menu.configure(state='disabled')
    c.text_empty.delete("1.0", END)
    c.text_empty.configure(state="disabled")

def ready_delete():
    c = Settings_Ready
    choice_category = c.choice_category_val.get()
    choice_script = c.choice_script_val.get()
    index_category = int(choice_category[:choice_category.index('|')])
    
    if choice_script == "":
        conn.execute("PRAGMA foreign_keys = 1")
        cur.execute(f"DELETE FROM ready_category WHERE num = '{index_category}';")
        cur.execute(f"UPDATE ready_category SET num = num - 1 WHERE num > '{index_category}'")
        conn.commit()
    else:    
        index_script = int(choice_script[:choice_script.index('|')])    
        cur.execute(f"SELECT id FROM ready_category WHERE num = '{index_category}'")
        id_category = cur.fetchone()[0]
        
            
        cur.execute(f"DELETE FROM ready_text WHERE id_category = '{id_category}' AND id = '{index_script}';")
        cur.execute(f"UPDATE ready_text SET id = id - 1 WHERE id_category = '{id_category}' AND id > '{index_script}'")
        conn.commit()
    
    cur.execute(f"SELECT num, title FROM ready_category ORDER BY num;")
    val_list = cur.fetchall()

    category_num_list = [i_val[0] for i_val in val_list]
    category_num_list.append(len(category_num_list) + 1)
    c.category_num_list = category_num_list

    category_list = [f"{i_val[0]}| " + i_val[1] for i_val in val_list]
    category_list = ["+ Добавить новую категорию"] + category_list + ["+ Добавить новую категорию"]
    c.category_list = category_list

    c.choice_category_num_menu.configure(values=c.category_num_list)
    c.choice_category_menu.configure(values=c.category_list)
    
    c.choice_script_menu.configure(state='disabled')
    c.choice_script_num_menu.configure(state='disabled')

    c.choice_category_num.set("1") 
    c.choice_category_val.set(category_list[0])
    
    c.title_empty.delete(0, END)
    c.title_empty.insert(0, "Титульник")

    c.text_empty.delete("1.0", END)

    c.btn_save.configure(bg = "green", text = "Сохранить")
    c.btn_delete.configure(state="disabled")


def ready_save():
    c = Settings_Ready
    choice_category = c.choice_category_val.get()
    choice_script = c.choice_script_val.get()
    title = c.title_empty.get()
    text = c.text_empty.get("1.0", END)
    category_num = int(c.choice_category_num.get())
    script_num = c.choice_script_num.get()
    
    cur.execute("SELECT title FROM ready_category WHERE title = ?;", (title,))
    category_choise = cur.fetchall()

    if choice_category == "+ Добавить новую категорию":
        if len(category_choise) == 0:
            cur.execute(f"UPDATE ready_category SET num = num + 1 WHERE num >= '{category_num}'")
            cur.execute("INSERT INTO ready_category(num, title) VALUES (?, ?)", (category_num, title))
        else:
            pass #TODO: Добавить обработку если в базе уже есть категория с данным именем
    
    elif choice_script == "":
        index_category = int(choice_category[:choice_category.index('|')])
        title_val = choice_category[choice_category.index(" ") + 1:]

        if title_val == title or len(category_choise) == 0:
            if index_category == category_num:
                cur.execute(f"UPDATE ready_category SET title = ? WHERE num = ?", (title, category_num))
                
            elif index_category > category_num:
                cur.execute(f"UPDATE ready_category SET num = num + 1 WHERE num >= '{category_num}' AND num < '{index_category}'")
                cur.execute(f"UPDATE ready_category SET num = ?, title = ? WHERE title = ?", (category_num, title, title_val))
                
            elif index_category < category_num:
                cur.execute(f"UPDATE ready_category SET num = num - 1 WHERE num <= '{category_num}' AND num > '{index_category}'")
                cur.execute(f"UPDATE ready_category SET num = ?, title = ? WHERE title = ?", (category_num, title, title_val))  
        else:
            pass #TODO: Добавить обработку если в базе уже есть категория с данным именем

    elif choice_script == "+ Добавить новый скрипт":

        index_category = int(choice_category[:choice_category.index('|')])
        cur.execute(f"SELECT id FROM ready_category WHERE num = '{index_category}'")
        id_category = cur.fetchone()[0]

        cur.execute(f"UPDATE ready_text SET id = id + 1 WHERE id >= '{script_num}' AND id_category = {id_category}")
        cur.execute("INSERT INTO ready_text(id, id_category, title, text) VALUES (?, ?, ?, ?)", (script_num, id_category, title, text))
        conn.commit()
    
    else:
        index_category = int(choice_category[:choice_category.index('|')])
        index_script = int(choice_script[:choice_script.index('|')])
        
        script_num = int(script_num)

        cur.execute(f"SELECT id FROM ready_category WHERE num = '{index_category}'")
        id_category = cur.fetchone()[0]

        if script_num == index_script:
            cur.execute(f"UPDATE ready_text SET title = ?, text = ? WHERE id = ? AND id_category = {id_category}", (title, text, script_num))
            
        elif script_num > index_script:
            cur.execute(f"DELETE FROM ready_text WHERE id = '{index_script}' AND id_category = {id_category};")
            cur.execute(f"UPDATE ready_text SET id = id - 1 WHERE id > '{index_script}' AND id <= '{script_num}' AND id_category = {id_category}")
            cur.execute("INSERT INTO ready_text(id, id_category, title, text) VALUES (?, ?, ?, ?)", (script_num, id_category, title, text))
        
        elif script_num < index_script:
            cur.execute(f"DELETE FROM ready_text WHERE id = '{index_script}' AND id_category = {id_category};")
            cur.execute(f"UPDATE ready_text SET id = id + 1 WHERE id < '{index_script}' AND id >= '{script_num}' AND id_category = {id_category}")
            cur.execute("INSERT INTO ready_text(id, id_category, title, text) VALUES (?, ?, ?, ?)", (script_num, id_category, title, text))
        
        
  
    conn.commit()

    cur.execute(f"SELECT num, title FROM ready_category ORDER BY num;")
    val_list = cur.fetchall()

    category_num_list = [i_val[0] for i_val in val_list]
    category_num_list.append(len(category_num_list) + 1)
    c.category_num_list = category_num_list

    category_list = [f"{i_val[0]}| " + i_val[1] for i_val in val_list]
    category_list = ["+ Добавить новую категорию"] + category_list + ["+ Добавить новую категорию"]
    c.category_list = category_list

    c.choice_category_num_menu.configure(values=c.category_num_list)
    c.choice_category_menu.configure(values=c.category_list)
    
    c.choice_script_menu.configure(state='disabled')
    c.choice_script_num_menu.configure(state='disabled')

    c.choice_category_num.set("1") 
    c.choice_category_val.set(category_list[0])
    
    c.title_empty.delete(0, END)
    c.title_empty.insert(0, "Титульник")

    c.text_empty.delete("1.0", END)

    c.btn_save.configure(bg = "green", text = "Сохранить")
    c.btn_delete.configure(state="disabled")

def switching_script_combobox(event):
    c = Settings_Ready 
    choice_script = c.choice_script_val.get()
    choice_category = c.choice_category_val.get()

    c.title_empty.delete(0, END)
    c.text_empty.delete("1.0", END)

    if choice_script == "":
        c.choice_script_num_menu.configure(state='disabled')
        c.text_empty.configure(state="disabled")
        c.choice_script_num.set("")

        c.title_empty.insert(0, choice_category[choice_category.index(" ") + 1:])
    
        c.btn_delete.configure(state="normal")
        c.btn_save.configure(text="Изменить", bg="yellow")

    elif choice_script == "+ Добавить новый скрипт":
        c.choice_script_num_menu.configure(state="readonly")
        c.choice_script_num_menu.configure(state="readonly", values = c.script_num_list)

        c.text_empty.configure(state="normal")
        if c.choice_script_num.get() == "":
            c.choice_script_num.set(1)

        c.title_empty.insert(0, "Титульник")
        c.text_empty.insert("1.0", "Текст скрипта")


        c.btn_delete.configure(state="disabled")
        c.btn_save.configure(text="Сохранить", bg="green")
    else:
        script_num = int(choice_script[:choice_script.index('|')])

        script_num_list = c.script_num_list[:len(c.script_num_list)-1]
        c.choice_script_num_menu.configure(state="readonly", values = script_num_list)

        c.text_empty.configure(state="normal")
        c.choice_script_num.set(script_num)

        c.title_empty.insert(0, choice_script[choice_script.index(" ") + 1:])
        c.text_empty.insert("1.0", c.script_list[script_num - 1][2])

        c.btn_delete.configure(state="normal")
        c.btn_save.configure(text="Изменить", bg="yellow")
        

root = Tk()
root.title("TCRM+")
root.geometry("218x640")
root.minsize(width=200, height=640)
root.maxsize(width=300, height=700)
root.attributes("-topmost",True)
root.iconbitmap("icon.ico")

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

    frame_Ready, frame_assembling, frame_settings, frame_book - Фреймы для закладок

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

    cur.execute("SELECT count FROM counter")
    count = str(cur.fetchone()[0])
    counter = Label(frame_up_counter, name="counter", text= count)
    counter.grid(column=3, row = 0)

    # создаем набор вкладок
    notebook = ttk.Notebook(frame_bot)
    notebook.pack(expand=True, fill=BOTH)

    # создаем пару фреймвов
    frame_assembling = ttk.Frame(notebook)
    frame_Ready = ttk.Frame(notebook)
    frame_settings = ttk.Frame(notebook)
    frame_book = ttk.Frame(notebook)


    frame_assembling.pack(fill=BOTH, expand=True)
    frame_Ready.pack(fill=BOTH, expand=True)
    frame_settings.pack(fill=BOTH, expand=True)
    frame_book.pack(fill=BOTH, expand=True)

    # добавляем фреймы в качестве вкладок
    notebook.add(frame_assembling, text="СБОРКА")
    notebook.add(frame_Ready, text="ГОТОВЫЕ")
    notebook.add(frame_settings, text="НАСТРОЙКА")
    notebook.add(frame_book, text="Б")

class Ready:
    """
    Вкладка готовых скриптов. Содержит вкладки категорий скриптов и кнопки для копирования скриптов

    select_title - Список всех категорий
    select_text - Список всех значений с выбранной категории

    Canvas_top - фрейм для кнопок категорий и скроллбара
    Сanvas_frame - Фрейм для кнопок категорий
    Canvas_top_scrollbar - Фрейм для скроллбара
    scrollbar - скроллбар для прокрутки 

    Frame_bottom - Нижний фрейм для стрелок и кнопок
    Frame_bottom_arrow - Фрейм для стрелок
    Frame_bottom_text - Фрейм для кнопок

    ready_category - список категорий
    with_list - Размер Canvas_top
    page - Страница скриптов
    page_list - Начальный элемент страницы скриптов
    len_ready_text - Максимальное колличество страниц
    category_list - Лист для категорий скриптов
    btn_ready_list - Кнопка категорий скриптов
    """

    Canvas_top = Canvas(main.frame_Ready, height=25)
    Canvas_top.pack(anchor=NW, fill=X)

    Сanvas_frame = Frame(Canvas_top, height=25)

    Canvas_top_scrollbar = Frame(main.frame_Ready, height=10)
    Canvas_top_scrollbar.pack(anchor=NW, fill=X)

    scrollbar = Scrollbar(Canvas_top_scrollbar, orient=HORIZONTAL, command=Canvas_top.xview)
    scrollbar.pack(expand=True, fill=BOTH)
    

    Frame_bottom = Frame(main.frame_Ready)
    Frame_bottom.pack(expand=True, fill=BOTH)

    Frame_bottom_arrow = Frame(Frame_bottom)
    Frame_bottom_arrow.pack(anchor=NW, fill=X)
    
    Frame_bottom_text = Frame(Frame_bottom)
    Frame_bottom_text.pack(anchor=NW, expand=True, fill=BOTH)
    
    select_title = cur.execute("""
    SELECT title 
    FROM ready_category
    ORDER BY num;""")

    ready_category = cur.fetchall()

    category = ready_category[0][0]
    
    select_text = cur.execute(f"""
    SELECT ready_text.title, ready_text.text 
    FROM ready_text
    JOIN ready_category ON 
    ready_category.id = ready_text.id_category
    WHERE ready_category.id = 1
    ORDER BY ready_text.id;
    """)
    ready_text = cur.fetchall()
    with_list = int()

    page = 1
    page_list = 0
    
    len_ready_text = math.ceil(len(ready_text) / 10)
    if len_ready_text == 0:
        len_ready_text = 1
    
    category_list = list()
    btn_ready_list = list()

    for i_num, i_val in enumerate(ready_category):
        
        val = i_val[0]
        
        width_btn = int(len(str(val)))
        with_list += width_btn

        btn_readys = Button(Сanvas_frame, width = width_btn, text = val, bg = "yellow", command = lambda val=val: ready_swap_category(val)) 
        btn_readys.pack(side=LEFT, expand=True)
        category_list.append(btn_readys)

    category_list[0].configure(bg = "white", state='disabled')
    btn_readys = Button(Сanvas_frame, text = "             ", bg = "yellow", state='disabled') 
    btn_readys.pack(side=LEFT, expand=True)

    left_btn = Button(Frame_bottom_arrow, width = 11, text = "<--", bg = "yellow", command = ready_back_page)
    left_btn.pack(side = LEFT)

    center_btn = Button(Frame_bottom_arrow, width = 4, text = f"{page}/{len_ready_text}", bg = "yellow", command = ready_first_page)
    center_btn.pack(side = LEFT)
    

    right_btn = Button(Frame_bottom_arrow, width = 11, text = "-->", bg = "yellow", command = ready_next_page)
    right_btn.pack(side = LEFT)

    for i_val in range(10):
        
        try:
            key = ready_text[i_val][0]
            val = ready_text[i_val][1]

            btn_readys = Button(Frame_bottom_text, text = key, bg = "yellow", command= lambda val=val: copy(val)) 

        except IndexError:
            btn_readys = Button(Frame_bottom_text, text = "", bg = "yellow", state='disabled') 
        finally:
            btn_readys.pack(fill = X, pady = 10)
            btn_ready_list.append(btn_readys)
    
    Canvas_top.create_window(0, 0, anchor=NW, window=Сanvas_frame, height=25)
    Canvas_top.config(scrollregion=(0, 0, with_list*9, 0))


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

    frame_assembling_bot_arrow = Frame(frame_assembling_bot, width=218, height=25)
    frame_assembling_bot_arrow.grid(column=0, row = 0)

    frame_assembling_bot_text = Frame(frame_assembling_bot, width=218, height=200)
    frame_assembling_bot_text.grid(column=0, row = 1)

    page = 1
    page_list = 0

    cur.execute("SELECT title, text FROM assembling_list;")
    assembling_list = cur.fetchall()
    len_assembling_list = math.ceil(len(assembling_list) / 14)
    if len_assembling_list == 0:
        len_assembling_list = 1
    btn_assembling_list = []
    add_btn_assembling_list = []
    label_list = []

    for i_val in range(14):
        global btn_assembling, add_btn_assembling, buffer_assembling

        try:
            key = assembling_list[i_val][0]
            val = assembling_list[i_val][1]

            btn_assembling = Button(frame_assembling_left, width = 2, text = "С", bg = "yellow", command = lambda val=val: copy(val, buffer_assembling))
            add_btn_assembling = Button(frame_assembling_left, width = 2, text = "+", bg = "yellow", command = lambda val=val: add_copy(val, buffer_assembling))
            frame_lb = Frame(frame_assembling_right)
            lb = Label(frame_lb,  text = key)

        except IndexError:

            btn_assembling = Button(frame_assembling_left, width = 2, text = "С", bg = "yellow", state='disabled')
            add_btn_assembling = Button(frame_assembling_left, width = 2, text = "+", bg = "yellow", state='disabled')
            frame_lb = Frame(frame_assembling_right)
            lb = Label(frame_lb,  text = "")
           
        finally:
            btn_assembling.grid(column=0, row = i_val)
            btn_assembling_list.append(btn_assembling)

            add_btn_assembling.grid(column=1, row = i_val)
            add_btn_assembling_list.append(add_btn_assembling)

            frame_lb.place(rely=0.043 * i_val, relheight=1, relwidth=1)

            lb.grid(column=0, row = i_val)
            label_list.append(lb)

    left_btn = Button(frame_assembling_bot_arrow, width = 11, text = "<--", bg = "yellow", command = assembling_back_page)
    left_btn.pack(side=LEFT)

    center_btn = Button(frame_assembling_bot_arrow, width = 4, text = f"{page}/{len_assembling_list}", bg = "yellow", command = assembling_first_page)
    center_btn.pack(side=LEFT)

    right_btn = Button(frame_assembling_bot_arrow, width = 11, text = "-->", bg = "yellow", command = assembling_next_page)
    right_btn.pack(side=LEFT)

    buffer_assembling = Text(frame_assembling_bot_text, width=25, height=10, wrap=WORD)
    buffer_assembling.pack()
    buffer_assembling.bind("<Key>", lambda e: "break") 

class Settings:
    """
    Вкладка настроек
    
    Имеет подвкладки:
    Настройка сборочных скриптов
    Настройка Готовых скриптов
    Общие настройки


    """
    notebook = ttk.Notebook(main.frame_settings)
    notebook.pack(expand=True, fill=BOTH)

    # создаем пару фреймвов
    frame_assembling = ttk.Frame(notebook)
    frame_Ready = ttk.Frame(notebook)
    frame_general = ttk.Frame(notebook)

    frame_assembling.pack(fill=BOTH, expand=True)
    frame_Ready.pack(fill=BOTH, expand=True)
    frame_general.pack(fill=BOTH, expand=True)


    # добавляем фреймы в качестве вкладок
    notebook.add(frame_assembling, text="Сборка")
    notebook.add(frame_Ready, text="Готовые")
    notebook.add(frame_general, text="Общие")


class Settings_Assembling:
    """
    Вкладка настроек сборочных скриптов
    frame_choice - Фрейм для выбора названия скрипта
    frame_title - Фрейм для имени скрипта
    frame_text - Фрейм для текста скрипта
    frame_btn - Фрейм для кнопок удалить сохранить изменить

    frame_choice_num - Дочерний фрейм frame_choice для нумерации скрипта
    frame_choice_val - Дочерний фрейм frame_choice для названий скриптов

    #TODO: Доделать
    """
    frame_choice = Frame(Settings.frame_assembling, height=25)
    frame_choice.pack(fill=X, pady = 10)

    frame_title = Frame(Settings.frame_assembling, height=30)
    frame_title.pack(fill=X, pady = 10)

    frame_text = Frame(Settings.frame_assembling, height=350)
    frame_text.pack(fill=X, pady = 10)

    frame_btn = Frame(Settings.frame_assembling, height=50)
    frame_btn.pack(fill=BOTH)

    frame_choice_num = Frame(frame_choice, width=40, height=25)
    frame_choice_num.pack(anchor=NW, side=LEFT)

    frame_choice_val = Frame(frame_choice, width=40, height=25)
    frame_choice_val.pack(anchor=NW, side=LEFT)

    cur.execute("SELECT id, title, text FROM assembling_list;")
    val_list = cur.fetchall()

    num_list = [i_val[0] for i_val in val_list]
    num_list.append(len(num_list) + 1)
    title_list = [f"{i_val[0]}| " + i_val[1] for i_val in val_list]
    title_list = ["+ Добавить новый скрипт"] + title_list + ["+ Добавить новый скрипт"]
    title_id = 1
    
    choice_variable_num = StringVar(frame_choice_num)
    choice_variable_num.set(1) 
    choice_num_menu = ttk.Combobox(frame_choice_num, width=3, state = "readonly", textvariable=choice_variable_num, values=num_list)
    choice_num_menu.pack()

    choice_variable_val = StringVar(frame_choice_val)
    choice_variable_val.set(title_list[0]) 
    choice_val_menu = ttk.Combobox(frame_choice_val, width=100, state = "readonly", textvariable=choice_variable_val, values=title_list)
    choice_val_menu.pack()
    choice_val_menu.bind("<<ComboboxSelected>>", switching_assembling_combobox)

    title_empty = Entry(frame_title, width=100)
    title_empty.pack()

    text_empty = Text(frame_text, wrap=WORD, undo=True)
    text_empty.pack(side=LEFT, expand=True, fill = BOTH)

    btn_delete = Button(frame_btn, width = 14, text = "Удалить", state= "disable", bg = "red", command = assembling_delete)
    btn_delete.pack(side=LEFT)
    
    btn_save = Button(frame_btn, width = 14, text = "Сохранить", bg = "green", command = assembling_save)
    btn_save.pack(side=LEFT)


class Settings_Ready:
    frame_choice_category = Frame(Settings.frame_Ready, height=25)
    frame_choice_category.pack(fill=X)
        
    frame_choice_script = Frame(Settings.frame_Ready, height=25)
    frame_choice_script.pack(fill=X, pady = 10)

    frame_title = Frame(Settings.frame_Ready, height=30)
    frame_title.pack(fill=X, pady = 10)

    frame_text = Frame(Settings.frame_Ready, height=300)
    frame_text.pack(fill=X, pady = 10)

    frame_btn = Frame(Settings.frame_Ready, height=50)
    frame_btn.pack(fill=BOTH)

    frame_choice_category_num = Frame(frame_choice_category, width=40, height=25)
    frame_choice_category_num.pack(anchor=NW, side=LEFT)

    frame_choice_category_val = Frame(frame_choice_category, width=40, height=25)
    frame_choice_category_val.pack(anchor=NW, side=LEFT)
    
    frame_choice_script_num = Frame(frame_choice_script, width=40, height=25)
    frame_choice_script_num.pack(anchor=NW, side=LEFT)

    frame_choice_script_val = Frame(frame_choice_script, width=40, height=25)
    frame_choice_script_val.pack(anchor=NW, side=LEFT)

    """--- Раздел с категориями  ---"""

    cur.execute("SELECT num, title FROM ready_category ORDER BY num;")
    category_list = cur.fetchall()

    category_num_list = [i_val[0] for i_val in category_list]
    category_num_list.append(len(category_num_list) + 1)
    category_title_list = [f"{i_val[0]}| " + i_val[1] for i_val in category_list]
    category_title_list = ["+ Добавить новую категорию"] + category_title_list + ["+ Добавить новую категорию"]
    category_id = 1
    
    choice_category_num = StringVar(frame_choice_category_num)
    choice_category_num.set(1) 
    choice_category_num_menu = ttk.Combobox(frame_choice_category_num, width=3, state = "readonly", textvariable=choice_category_num, values=category_num_list)
    choice_category_num_menu.pack()

    choice_category_val = StringVar(frame_choice_category_val)
    choice_category_val.set(category_title_list[0]) 
    choice_category_menu = ttk.Combobox(frame_choice_category_val, width=100, state = "readonly", textvariable=choice_category_val, values=category_title_list)
    choice_category_menu.pack()
    choice_category_menu.bind("<<ComboboxSelected>>", switching_category_combobox)
    
    """--- Раздел с скриптами ---"""
    script_num_list = list()
    script_title_list = list()

    script_list = list()

    choice_script_num = StringVar(frame_choice_script_num)
    choice_script_num.set("") 
    choice_script_num_menu = ttk.Combobox(frame_choice_script_num, width=3, state = "disabled", textvariable=choice_script_num)
    choice_script_num_menu.pack()

    choice_script_val = StringVar(frame_choice_script_val)
    choice_script_val.set("") 
    choice_script_menu = ttk.Combobox(frame_choice_script_val, width=100, state = "disabled", textvariable=choice_script_val)
    choice_script_menu.pack()
    choice_script_menu.bind("<<ComboboxSelected>>", switching_script_combobox)

    """--- Раздел полями ввода  ---"""
    title_empty = Entry(frame_title, width=100)
    title_empty.pack()

    text_empty = Text(frame_text, wrap=WORD, undo=True, state= "disable")
    text_empty.pack(side=LEFT, expand=True, fill = BOTH)

    btn_delete = Button(frame_btn, width = 14, text = "Удалить", state= "disable", bg = "red", command=ready_delete)
    btn_delete.pack(side=LEFT)
    
    btn_save = Button(frame_btn, width = 14, text = "Сохранить", bg = "green", command=ready_save)
    btn_save.pack(side=LEFT)

class Book:
    """
    Вкладка Блокнота
    book_text - Поле для блокнота растянутое на всю ширину вкладки
    """
    book_text = Text(main.frame_book, wrap=WORD, undo=True)
    book_text.pack(side=LEFT, expand=True, fill = BOTH)

    book_text.bind("<Control-KeyPress>", keys)


root.mainloop()
