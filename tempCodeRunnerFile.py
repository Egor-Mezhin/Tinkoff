    style = ttk.Style()
    style.theme_use('default')
    style.configure('rtr', troughcolor='#ffffff', bordercolor='#ffffff', darkcolor='#ffffff', lightcolor='#ffffff')

    scrollbar = Scrollbar(Canvas_top_scrollbar, orient=HORIZONTAL, style = "rtr", command=Canvas_top.xview)
    scrollbar.pack(expand=True, fill=BOTH)