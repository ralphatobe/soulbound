import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from PIL import Image, ImageTk

ATTRIBUTE_RANGE = (1,2,3,4,5,6,7,8,9,10)
SKILL_RANGE = (0,1,2,3)
DN_RANGES = [(2,3,4,5,6), (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)]


class SampleApp(tk.Tk):

  def __init__(self, *args, **kwargs):
    tk.Tk.__init__(self, *args, **kwargs)

    self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

    # the container is where we'll stack a bunch of frames
    # on top of each other, then the one we want visible
    # will be raised above the others
    container = tk.Frame(self)
    container.pack(side="top", fill="both", expand=True)
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    self.frames = {}
    for F in (StartPage, PageOne, PageTwo):
      page_name = F.__name__
      frame = F(parent=container, controller=self)
      self.frames[page_name] = frame

      # put all of the pages in the same location;
      # the one on the top of the stacking order
      # will be the one that is visible.
      frame.grid(row=0, column=0, sticky="nsew")

    self.show_frame("StartPage")

  def show_frame(self, page_name):
    '''Show a frame for the given page name'''
    frame = self.frames[page_name]
    frame.tkraise()


class StartPage(tk.Frame):

  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller

    self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
    # frame = tk.Frame()

    load = Image.open("soulbound_logo.png")
    render = ImageTk.PhotoImage(load)
    img = tk.Label(self, image=render)
    img.image = render
    img.pack()

    frm_atk = tk.Frame(self, borderwidth=5)
    btn_atk = tk.Button(master=frm_atk, text='Attack Probability Calculator', 
                        command=lambda: controller.show_frame("PageOne"),
                        font=self.title_font)
    # btn_atk.bind("<Button-1>", atk_prob_calc)
    btn_atk.pack(fill=tk.BOTH, expand=True)
    frm_atk.pack(side=tk.LEFT, expand=True)

    frm_tst = tk.Frame(self, borderwidth=5)
    btn_tst = tk.Button(master=frm_tst, text='Regular Test Calculator', 
                        command=lambda: controller.show_frame("PageTwo"),
                        font=self.title_font)
    # btn_tst.bind("<Button-1>", reg_test_calc)
    btn_tst.pack(fill=tk.BOTH, expand=True)
    frm_tst.pack(side=tk.LEFT, expand=True)

    frm_ext = tk.Frame(self, borderwidth=5)
    btn_ext = tk.Button(master=frm_ext, text='Extended Test Calculator', 
                        command=lambda: controller.show_frame("PageOne"),
                        font=self.title_font)
    # btn_ext.bind("<Button-1>", ext_test_calc)
    btn_ext.pack(fill=tk.BOTH, expand=True)
    frm_ext.pack(side=tk.LEFT, expand=True)

    # frame.pack()

class PageOne(tk.Frame):

  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller

    # frame = tk.Frame()

    # load = Image.open("soulbound_logo.png")
    # render = ImageTk.PhotoImage(load)
    # img = tk.Label(self, image=render)
    # img.image = render
    # img.pack()

    label = tk.Label(self, text="This is page 1", font=controller.title_font)
    label.pack(side="top", fill="x", pady=10)
    button = tk.Button(self, text="Go to the start page",
                       command=lambda: controller.show_frame("StartPage"))
    button.pack()

    # Combobox creation 
    n = tk.StringVar() 
    monthchoosen = ttk.Combobox(self, width = 27, textvariable = n) 
      
    # Adding combobox drop down list 
    monthchoosen['values'] = ATTRIBUTE_RANGE
      
    # monthchoosen.grid(column = 1, row = 5) 
    monthchoosen.current() 
    monthchoosen.pack()

    # frame.pack()


class PageTwo(tk.Frame):

  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller

    # frame = tk.Frame(height=200, width=200, bg='blue')

    # load = Image.open("soulbound_logo.png")
    # render = ImageTk.PhotoImage(load)
    # img = tk.Label(self, image=render)
    # img.image = render
    # img.pack()

    label = tk.Label(self, text="This is page 2", font=controller.title_font)
    label.pack(side="top", fill="x", pady=10)
    button = tk.Button(self, text="Go to the start page",
                       command=lambda: controller.show_frame("StartPage"))
    button.pack()

    # frame.pack()


# def atk_prob_calc():
#   print('opened attack probability calculator')


# def reg_test_calc():
#   print('opened regular test calculator')


# def ext_test_calc():
#   print('opened extended test calculator')


# def main():
#   window = tk.Tk()

#   frm_title = tk.Frame(master=window, height=100, relief=tk.GROOVE, borderwidth=5)

#   lbl_title = tk.Label(master=frm_title, text='Soulbound Calculator')
#   lbl_title.pack(fill=tk.BOTH, expand=True)

#   frm_title.pack(fill=tk.BOTH, expand=True)

#   frm_body = tk.Frame(master=window, borderwidth=25)

#   frm_atk = tk.Frame(master=frm_body, borderwidth=5)
#   btn_atk = tk.Button(master=frm_atk, text='Attack Probability Calculator', command=atk_prob_calc)
#   # btn_atk.bind("<Button-1>", atk_prob_calc)
#   btn_atk.pack(fill=tk.BOTH, expand=True)
#   frm_atk.pack(fill=tk.BOTH, expand=True)

#   frm_tst = tk.Frame(master=frm_body, borderwidth=5)
#   btn_tst = tk.Button(master=frm_tst, text='Regular Test Calculator', command=reg_test_calc)
#   # btn_tst.bind("<Button-1>", reg_test_calc)
#   btn_tst.pack(fill=tk.BOTH, expand=True)
#   frm_tst.pack(fill=tk.BOTH, expand=True)

#   frm_ext = tk.Frame(master=frm_body, borderwidth=5)
#   btn_ext = tk.Button(master=frm_ext, text='Extended Test Calculator', command=ext_test_calc)
#   # btn_ext.bind("<Button-1>", ext_test_calc)
#   btn_ext.pack(fill=tk.BOTH, expand=True)
#   frm_ext.pack(fill=tk.BOTH, expand=True)

#   frm_body.pack(fill=tk.BOTH, expand=True)

#   window.mainloop()


if __name__ == "__main__":
  app = SampleApp()
  app.mainloop()