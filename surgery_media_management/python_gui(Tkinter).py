from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter.ttk import Progressbar
from tkinter import ttk
from tkinter import Menu

window = Tk()  ## creating a window

window.title("Welcome to LikeGeeks app") ## adding title for window

window.geometry('350x200')  ## setting window size

## inserting 'Hello' text in windows (0 row 0 column), changing font to Arial Bold, and font size 40
lbl = Label(window, text = 'Hello', font = ("Arial Bold", 20))

lbl.grid(column=0, row=0)

txt = Entry(window, width = 10)  ## getting input using Entry

txt.grid(column = 1, row = 0)

##
def clicked():
    res = "Welcome to " + txt.get()
    lbl.configure(text = res)

## adding button to window with text = 'Click me', background colour = green and foreground colour = red
btn = Button(window, text = 'Click me', command = clicked, bg = "green", fg = "red")

btn.grid(column=2, row=0)

window.mainloop()
##

window = Tk()

window.title("Welcome to LikeGeeks app")

window.geometry('350x200')

combo = Combobox(window)

combo['values']= (1, 2, 3, 4, 5, "Text")

combo.current(1) #set the selected item

combo.grid(column=0, row=0)

window.mainloop()

##
window = Tk()

window.title("Welcome to LikeGeeks app")

window.geometry('350x200')

chk_state = BooleanVar()

chk_state.set(True)      ##set check state

## chk_state = IntVar()

## chk_state.set(0) #uncheck

## chk_state.set(1) #check

chk = Checkbutton(window, text='Choose', var=chk_state)

chk.grid(column=0, row=0)

window.mainloop()

## radio button

window = Tk()

window.title("Welcome to LikeGeeks app")

window.geometry('350x200')

rad1 = Radiobutton(window,text='First', value=1)

rad2 = Radiobutton(window,text='Second', value=2)

rad3 = Radiobutton(window,text='Third', value=3)

rad1.grid(column=0, row=0)

rad2.grid(column=1, row=0)

rad3.grid(column=2, row=0)

window.mainloop()

##
window = Tk()

window.title("Welcome to LikeGeeks app")

selected = IntVar()

rad1 = Radiobutton(window,text='First', value=1, variable=selected)

rad2 = Radiobutton(window,text='Second', value=2, variable=selected)

rad3 = Radiobutton(window,text='Third', value=3, variable=selected)

def clicked():

   print(selected.get())

btn = Button(window, text="Click Me", command=clicked)

rad1.grid(column=0, row=0)

rad2.grid(column=1, row=0)

rad3.grid(column=2, row=0)

btn.grid(column=3, row=0)

window.mainloop()

##
window = Tk()

window.title("Welcome to LikeGeeks app")

window.geometry('350x200')

txt = scrolledtext.ScrolledText(window,width=40,height=10)

txt.grid(column=0,row=0)

window.mainloop()
##
window = Tk()

window.title("Welcome to LikeGeeks app")

window.geometry('350x200')

def clicked():

    messagebox.showinfo('Message title', 'Message content')

btn = Button(window,text='Click here', command=clicked)

btn.grid(column=0,row=0)

window.mainloop()
##

window = Tk()

window.title("Welcome to LikeGeeks app")

window.geometry('350x200')

spin = Spinbox(window, from_=0, to=100, width=5)

spin.grid(column=0,row=0)

window.mainloop()
##
window = Tk()

window.title("Welcome to LikeGeeks app")

window.geometry('350x200')

style = ttk.Style()

style.theme_use('default')

style.configure("black.Horizontal.TProgressbar", background='black')

bar = Progressbar(window, length=200, style='black.Horizontal.TProgressbar')

bar['value'] = 70

bar.grid(column=0, row=0)

window.mainloop()
##

window = Tk()

window.title("Welcome to LikeGeeks app")

menu = Menu(window)

new_item = Menu(menu)

new_item.add_command(label='New')

menu.add_cascade(label='File', menu=new_item)

window.config(menu=menu)

window.mainloop()
##
window = Tk()

window.title("Welcome to LikeGeeks app")

tab_control = ttk.Notebook(window)

tab1 = ttk.Frame(tab_control)

tab_control.add(tab1, text='First')

tab_control.pack(expand=1, fill='both')

window.mainloop()
##
window = Tk()

window.title("Welcome to LikeGeeks app")

tab_control = ttk.Notebook(window)

tab1 = ttk.Frame(tab_control)

tab2 = ttk.Frame(tab_control)

tab_control.add(tab1, text='First')

tab_control.add(tab2, text='Second')

lbl1 = Label(tab1, text= 'label1')

lbl1.grid(column=0, row=0)

lbl2 = Label(tab2, text= 'label2')

lbl2.grid(column=0, row=0)

tab_control.pack(expand=1, fill='both')

window.mainloop()
##
