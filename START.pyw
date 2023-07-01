from tkinter import *
from tkinter import ttk
import tkinter as tk
import pyperclip

assembling_list = {
            "Приветствие": "Здравствуйте, {aut_text}. ",
            "Сейчас во всем разберемся.": "Сейчас во всем разберемся. ",
            "Уточните, пожалуйста,": "Уточните, пожалуйста, ",
            "дату и сумму": "дату и сумму ",
            "номер карты": "последние 4 цифры номера карты ",
            "Правильно вас понимаю,": "Правильно вас понимаю, ",
            "Уже занимаюсь встречей": "Уже занимаюсь назначением встречи.", 
            "Уточняем адрес": "Уточните, пожалуйста, по какому адресу будет удобно встретится с представителем?",
            "По адресу, ***": "По адресу, {aut_text}\n",
            "ближайшая дата доставки": "ближайшая дата и время доставки ****. Согласны?",
            "К сожалению,": "К сожалению, ",
            "Ожидание":"Прошу прощение за длительное ожидание. ",
            "Прошу прощение":"Прошу прощение за доставленные неудобства.",
            "Понимаю ваши чувства":"Понимаю ваши чувства, на вашем месте мне так же было не приятно",
            "Я тут чтобы тебе помочь":"Я тут здесь и сейчас чтобы помочь вам решить вопрос.",
}

ready_category = {
            "Прив": {
                "Вопрос":
                    "Здравствуйте, {aut_text}. Уточните, пожалуйста, какой у вас вопрос?",
                "Приведи друга":
                    "Здравствуйте, {aut_text}. Уточните, пожалуйста, ФИО друга.",
                "IOS":
                    "Здравствуйте, {aut_text}. Установить приложение можно только при встрече с представителем. Уточните, пожалуйста, какое приложение требуется установить? 'Тинькофф Банк' или 'Тинькофф Инвестиции' ?",
                "Оспорить":
                    "Здравствуйте, {aut_text}. Уточните, пожалуйста, по какой причине хотите оспорить операцию?",
                "Хз че за клиент":
                    "Здравствуйте. Уточните, пожалуйста, ваше ФИО, дату рождения, номер телефона который оставляли при оформлении банковского продукта.",
                "Справка по операции":
                    "Здравствуйте, {aut_text}. Уточните, пожалуйста, по какой операции вам необходимо получить справку?",
                },
            "Пока": {
                "Позитивно помог":
                    "Рад был вам помочь. Всего вам доброго😄",
                "Подсказал":
                    "Рад был вам подсказать. Всего вам доброго😄",
                "Нейтральное пока":
                    "Спасибо за обращение. Всего вам доброго.",
                "Ничего страшного":
                    "Ничего страшного. Всего вам доброго😄",
                "Понял вас":
                    "Понял вас. Всего вам доброго😄",
                },
            "Описания": {
                "PRO":
                    "С подпиской вы получите бесплатное обслуживание по счету. Бесплатную услугу оповещение об операциях\n\nПроценты на остаток по карте 5%\n\nПроценты по накопительному счету 5% вместо 3%\n\nКэшбэк на кино, театры, концерты 15% вместо 5%\n\nЛимит кэшбэка в месяц 5 000 вместо 3 0000\n\nБонусы в тинькофф инвестиции и мобайл.",
                },
            "Пояснения": {
                "Подписки стороние сервисы":
                    "К сожалению если у вас имеются какие то подписки на сторонних сервисах, проверить и отключить их мне не удастся. Вы сможете это сделать только самостоятельно на сторонних сервисах.",
                "Порядок зачисления по СБП":
                    "Существует определенный приоритет зачисления средств при переводе по номеру телефона:\n1) Счет дебетовой карты. Из двух дебетовых карт с одинаковым приоритетом выбирается та, на которой выше баланс.\n2) Счет дебетовой карты Tinkoff Junior.3) Счет для зачисления бюджетных средств.\n4) Счет дебетовой карты USD.\n5) Счет дебетовой карты EUR.6) Счет дебетовой карты GPB.\n7) Кредитные карты. Из двух кредитных карт выбирается та, у которой позже дата минимального платежа.\n8) Счет Мобайл (мобильная связь).",
                "Почему так долго авторизация?":
                    "Понимаю, как важен вопрос скорости перевода. При этом, не всегда получается быстро зачислить деньги. Для этого понадобиться еще некоторе время пока платежная система запрашивает разрешение у банка. На этот процесс, к сожалению, мы повлилять не сможем.",
                "Когда пройдет авторизация?":
                    "К сожалению, точный срок сказать не смогу. Этим занимается платежная система. Обработка может занимать до нескольких дней. Но не переживайте, обычно все происходит гораздо быстрее. ",
                "Раньше не списывали за обслугу":
                    "Ранее вы не пользовались счетом, поэтому деньги не списывались. Сейчас вы начали им пользоваться, поэтому по мере поступления денег у вас начали списывать за обслуживание и за услугу. Если вы не будете пользоваться счетом, то списаний у вас не будет. Как только начнется движение средств, то у вас спишется за предыдущий месяц, тому месяцу в котором вы начали пользоватся счетом. Долг за все месяца не пользования карты не сохраняется",
                "Не подключал оповещение":
                    "Оповещение об операциях была подключена автоматически при подписании договора, так как не была проставлена галочка о том что она не нужна.",
                "Списали за выкл Оповещений":
                    "Списание произошло поскольку пользовались услугой в течении расчетного периода. Вижу, что услуга окончательно отключена, больше списаний по ней не будет.",
                
                },
            "Другое": {
                "Ожидание звонка":
                    "Ожидайте звонка, пожалуйста,  в течении 5 минут с вами свяжется коллега, если звонок не поступит, свяжитесь с нами самостоятельно: Если находитесь в России, позвоните по номеру 8 800 555-10-10. Звонок бесплатный. Если находитесь за границей, наберите номер +7 495 648-11-11. Плата по тарифу оператора. Если нет мобильной связи, зайдите на tinkoff.ru и нажмите «Онлайн-звонок в банк» !",
                "Слоты":
                    "На **** есть слоты:\nc 09:00 до 11:00\nc 10:00 до 12:00\nc 11:00 до 13:00\nc 12:00 до 14:00\nc 13:00 до 15:00\nc 14:00 до 16:00\nc 15:00 до 17:00\nc 16:00 до 18:00\nc 17:00 до 19:00\nc 18:00 до 20:00\nc 19:00 до 21:00\nc 20:00 до 22:00\nc 21:00 до 23:00",
                },         
}

def validate(new_value):                                                
    return new_value == "" or new_value.isnumeric()

def copy(val, buffer = None):

    pyperclip.copy(val.format(
        aut_text = main.aut_text_entry.get()))

    if buffer != None:
        buffer.delete("1.0", END)
        buffer.insert("2.0", val.format(
        aut_text = main.aut_text_entry.get()))


def add_copy(val, buffer):
    text = pyperclip.paste() + val.format(
        aut_text = main.aut_text_entry.get())

    pyperclip.copy(text)

    buffer.insert(END, val.format(
        aut_text = main.aut_text_entry.get()))


def past(empty):

    empty_str = pyperclip.paste()
    empty_new = str()
    
    if empty_str[-1] == " ":
        empty_new = empty_str[0:len(empty_str)-1]
    else:
        empty_new = empty_str

    empty.delete(0, END)
    empty.insert(0, empty_new)


def f_counter_plus(empty):
    if empty.get() != "":
        new_empty = str(int(empty.get()) + 1)
        empty.delete(0, END)
        empty.insert(0, new_empty)
    else:
        empty.insert(0, "1")

def f_counter_minus(empty):
    if empty.get() != "":
        new_empty = str(int(empty.get()) - 1)
        empty.delete(0, END)
        empty.insert(0, new_empty)
    else:
        pass

def f_counter_null(empty):
    empty.delete(0, END)
    empty.insert(0, "0")

root = Tk()
root.title("TCRM+")
root.geometry("218x640")
root.resizable(width=False, height=False)
root.attributes("-topmost",True)

class VerticalScrolledFrame(ttk.Frame):

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

    aut_text_btn = Button(frame_up_aut_text, text = "Вставить", width=9, command= lambda: past(main.aut_text_entry))
    aut_text_btn.grid(column=0, row = 0)

    aut_text_entry = Entry(frame_up_aut_text, name="name", width=100)
    aut_text_entry.grid(column=1, row = 0)

    counter_plus = Button(frame_up_counter, text = "+", width=4, command= lambda: f_counter_plus(main.counter))
    counter_plus.grid(column=0, row = 0, sticky="nswe")

    counter_minus = Button(frame_up_counter, text = "-", width=4, command= lambda: f_counter_minus(main.counter))
    counter_minus.grid(column=1, row = 0, sticky="nswe")

    counter_null = Button(frame_up_counter, text = "0", width=1, command= lambda: f_counter_null(main.counter))
    counter_null.grid(column=2, row = 0)

    vcmd = (root.register(validate), '%P')  
    counter = Entry(frame_up_counter, name="counter", width= 100, validate="key", validatecommand=vcmd)
    counter.grid(column=3, row = 0)

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
    
    notebook_ready = ttk.Notebook(main.frame_Ready)
    notebook_ready.pack(expand=True, fill=BOTH)

    
    for i_keys in ready_category:
        frame_Ready = ttk.Frame(notebook_ready)
        frame_Ready.pack(fill=BOTH, expand=True)
        notebook_ready.add(frame_Ready, text=i_keys)

        for i_key, i_val in ready_category[i_keys].items():
            btn_readys = Button(frame_Ready, text = i_key, bg = "yellow", command= lambda i_val=i_val: copy(i_val)) 
            btn_readys.pack(fill = X, pady = 10)


class Assembling:
    frame_assembling_left = Frame(main.frame_assembling, width=43.6, height=600)
    frame_assembling_left.pack(side=LEFT, anchor="nw")

    frame_assembling_right = Frame(main.frame_assembling, width=174.8, height=600)
    frame_assembling_right.pack(side=LEFT, anchor="nw")

    frame_assembling_bot = Frame(main.frame_assembling, width=218, height=40)
    frame_assembling_bot.place(y = 450)

    count = 0

    for i_key, i_val in assembling_list.items():
        global btn_assembling, add_btn_assembling, buffer_assembling

        btn_assembling = Button(frame_assembling_left, width = 2, text = "С", bg = "yellow", command = lambda i_val=i_val: copy(i_val, buffer_assembling))
        btn_assembling.grid(column=0, row = count)

        add_btn_assembling = Button(frame_assembling_left, width = 2, text = "+", bg = "yellow", command = lambda i_val=i_val: add_copy(i_val, buffer_assembling))
        add_btn_assembling.grid(column=1, row = count)

        frame_btn_lb = Frame(frame_assembling_right)
        frame_btn_lb.place(rely=0.043 * count, relheight=1, relwidth=1)

        btn_lb = Label(frame_btn_lb,  text = i_key)
        btn_lb.grid(column=0, row = count)

        count += 1

    buffer_assembling = Text(frame_assembling_bot, width=25, height=4, wrap=WORD)
    buffer_assembling.pack(padx=10, pady=10, ipady=30)
    buffer_assembling.bind("<Key>", lambda e: "break") 
    
root.mainloop()