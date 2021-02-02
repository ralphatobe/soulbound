import os
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np

from attacking_prob import attack
from utils import test, extended_test


TRAITS_ALL = ['Cleave', 'Ineffective', 'Penetrating', 'Rend']
TALENTS_ALL = ['Ambidextrous', 'Backstab', 'Barazakdum, the Doom-Oath', 'Battle Rage', 'Blood Frenzy', 'Crushing Blow', 'Gunslinger', 'Heavy Hitter', 'Immense Strikes', 'Immense Swing', 'Martial Memories', 'Mounted Combatant', 'Patient Strike', 'Pierce Armour', 'Relentless Assault', 'Sever', 'Sigmar\'s Judgement', 'Star-Fated Arrow', 'The Bigger They Are', 'Underdog']
ABILITY_LEVELS = ['Poor', 'Average', 'Good', 'Great', 'Superb', 'Extraordinary']


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



class SampleApp(tk.Tk):

  def __init__(self, *args, **kwargs):
    tk.Tk.__init__(self, *args, **kwargs)

    self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

    self.winfo_toplevel().title("Soulbound Calculator")

    # the container is where we'll stack a bunch of frames
    # on top of each other, then the one we want visible
    # will be raised above the others
    container = tk.Frame(self)
    container.pack(side="top", fill="both", expand=True)
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    self.frames = {}
    for F in (StartPage, TestRegular, TestExtended, TestExtendedCustom, DamageCalculator):
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

    self.title_font = tkfont.Font(family='Helvetica', size=16, weight="bold", slant="italic")
    # frame = tk.Frame()


    path = resource_path("soulbound_logo.png")
    load = Image.open(path)
    render = ImageTk.PhotoImage(load)
    img = tk.Label(self, image=render)
    img.image = render
    img.pack()

    frm = tk.Frame(self, borderwidth=5)
    btn = tk.Button(master=frm, text='Attack Probability Calculator', 
                        command=lambda: controller.show_frame("DamageCalculator"),
                        font=self.title_font)
    btn.pack(fill=tk.BOTH, expand=True)
    frm.pack(side=tk.LEFT, expand=True)

    frm = tk.Frame(self, borderwidth=5)
    btn = tk.Button(master=frm, text='Regular Test Calculator', 
                        command=lambda: controller.show_frame("TestRegular"),
                        font=self.title_font)
    btn.pack(fill=tk.BOTH, expand=True)
    frm.pack(side=tk.LEFT, expand=True)

    frm = tk.Frame(self, borderwidth=5)
    btn = tk.Button(master=frm, text='Extended Test Calculator', 
                        command=lambda: controller.show_frame("TestExtended"),
                        font=self.title_font)
    btn.pack(fill=tk.BOTH, expand=True)
    frm.pack(side=tk.LEFT, expand=True)


class TestRegular(tk.Frame):

  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller

    # title
    lbl = tk.Label(self, text="Test Calculator", font=controller.title_font)
    lbl.grid(row=0, columnspan=2)

    # attribute
    self.attri = tk.IntVar()

    frm = tk.Frame(self)

    lbl = tk.Label(frm, text='Attribute:')
    lbl.grid(row=0, column=0)

    cbx = ttk.Combobox(frm, textvariable=self.attri, width=3)
    cbx['values'] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    cbx.grid(row=0, column=1)

    frm.grid(row=1, column=0)


    # skill values
    self.train = tk.IntVar()
    self.focus = tk.IntVar()

    frm = tk.Frame(self)

    for i in range(4):
      lbl = tk.Label(frm, text=str(i))
      lbl.grid(row=0, column=i+1)

    lbl = tk.Label(frm, text='Training')
    lbl.grid(row=1, column=0)

    for i in range(4):
      rad = ttk.Radiobutton(frm, variable=self.train, value=i)
      rad.grid(row=1, column=i+1)

    lbl = tk.Label(frm, text='Focus')
    lbl.grid(row=2, column=0)

    for i in range(4):
      rad = ttk.Radiobutton(frm, variable=self.focus, value=i)
      rad.grid(row=2, column=i+1)
    
    frm.grid(row=2, column=0)


    # difficulty number
    self.dn = [tk.IntVar(), tk.IntVar()]

    frm = tk.Frame(self)

    lbl = tk.Label(frm, text='Difficulty Number -')
    lbl.grid(row=0, column=0)

    cbx = ttk.Combobox(frm, textvariable=self.dn[0], width=3)
    cbx['values'] = (2, 3, 4, 5, 6)
    cbx.grid(row=0, column=1)

    lbl = tk.Label(frm, text=':')
    lbl.grid(row=0, column=2)

    cbx = ttk.Combobox(frm, textvariable=self.dn[1], width=3)
    cbx['values'] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
    cbx.grid(row=0, column=3)

    frm.grid(row=3, column=0)


    # skill values
    self.succ_lik = tk.StringVar()
    self.succ_exp = tk.StringVar()

    frm = tk.Frame(self)

    lbl = tk.Label(frm, text='Success Likelihood:')
    lbl.grid(row=0, column=0)

    lbl = tk.Label(frm, textvariable=self.succ_lik)
    lbl.grid(row=0, column=1)

    lbl = tk.Label(frm, text='Expected Successes:')
    lbl.grid(row=1, column=0)

    lbl = tk.Label(frm, textvariable=self.succ_exp)
    lbl.grid(row=1, column=1)
    
    frm.grid(row=4, column=0)


    # figure
    frm = tk.Frame(self)

    fig = Figure(figsize=(5, 4), dpi=100)
    self.canvas = FigureCanvasTkAgg(fig, master=frm)
    self.plot = fig.add_subplot(111)
    self.canvas.draw()
    self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    frm.grid(row=1, rowspan=4, column=1, padx=3, pady=3)


    # navigation buttons
    frm = tk.Frame(self)

    btn = tk.Button(frm, text="Go to the start page",
                       command=lambda: controller.show_frame("StartPage"))
    btn.grid(row=0, column=0, padx=30)

    btn = tk.Button(frm, text="Reset",
                       command=lambda: self.reset())
    btn.grid(row=0, column=1, padx=30)

    btn = tk.Button(frm, text="Calculate!",
                       command=lambda attribute=self.attri, training=self.train, focus=self.focus, dn=self.dn : self.calculate(attribute, training, focus, dn))
    btn.grid(row=0, column=2, padx=30)

    frm.grid(row=5, column=0, columnspan=2)


    # clear all fields
    self.reset()


  def reset(self):

    self.attri.set('')
    self.train.set('')
    self.focus.set('')

    self.dn[0].set('')
    self.dn[1].set('')

    self.succ_lik.set('')
    self.succ_exp.set('')

    self.canvas.draw()
    self.plot.clear()
    self.plot.cla()


  def calculate(self, attribute, training, focus, dn):

    probabilities = test(attribute.get()+training.get(), [training.get(), focus.get()], [dn[0].get(), dn[1].get()], verbose=False)

    self.plot.set_title('Success Distribution')
    self.plot.set_xlabel('Number of Successes')
    self.plot.set_ylabel('Likelihood')
    self.plot.bar(range(probabilities.shape[0]), probabilities)
    self.canvas.draw()
    self.plot.clear()
    self.plot.cla()

    self.succ_lik.set('{:2.2%}'.format(np.sum(probabilities[dn_1.get():])))
    self.succ_exp.set('{:2.3}'.format(np.matmul(range(probabilities.shape[0]), probabilities)))



class TestExtended(tk.Frame):

  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller

    # title
    title = tk.Label(self, text="Extended Test Calculator", font=controller.title_font)
    title.grid(row=0, columnspan=3)

    # attribute
    self.attri = tk.IntVar()

    frm = tk.Frame(self)

    lbl = tk.Label(frm, text='Attribute:')
    lbl.grid(row=0, column=0)

    cbx = ttk.Combobox(frm, textvariable=self.attri, width=3)
    cbx['values'] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    cbx.current(0)
    cbx.grid(row=0, column=1)

    frm.grid(row=1, column=0)


    # skill values
    self.train = tk.IntVar()
    self.focus = tk.IntVar()

    frm = tk.Frame(self)

    for i in range(4):
      lbl = tk.Label(frm, text=str(i))
      lbl.grid(row=0, column=i+1)

    lbl = tk.Label(frm, text='Training')
    lbl.grid(row=1, column=0)

    for i in range(4):
      rad = ttk.Radiobutton(frm, variable=self.train, value=i)
      rad.grid(row=1, column=i+1)

    lbl = tk.Label(frm, text='Focus')
    lbl.grid(row=2, column=0)

    for i in range(4):
      rad = ttk.Radiobutton(frm, variable=self.focus, value=i)
      rad.grid(row=2, column=i+1)
    
    frm.grid(row=2, column=0)


    # difficulty number
    self.dn = [tk.IntVar(), tk.IntVar()]

    frm = tk.Frame(self)

    lbl = tk.Label(frm, text='Difficulty Number -')
    lbl.grid(row=0, column=0)

    cbx = ttk.Combobox(frm, textvariable=self.dn[0], width=3)
    cbx['values'] = (2, 3, 4, 5, 6)
    cbx.grid(row=0, column=1)

    lbl = tk.Label(frm, text=':')
    lbl.grid(row=0, column=2)

    cbx = ttk.Combobox(frm, textvariable=self.dn[1], width=3)
    cbx['values'] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
    cbx.grid(row=0, column=3)

    frm.grid(row=3, column=0)


    # Results
    self.succ_lik = tk.StringVar()
    self.succ_exp = tk.StringVar()

    frm = tk.Frame(self)

    lbl = tk.Label(frm, text='Success Likelihood:')
    lbl.grid(row=0, column=0)

    lbl = tk.Label(frm, textvariable=self.succ_lik)
    lbl.grid(row=0, column=1)

    lbl = tk.Label(frm, text='Expected Successes:')
    lbl.grid(row=1, column=0)

    lbl = tk.Label(frm, textvariable=self.succ_exp)
    lbl.grid(row=1, column=1)
    
    frm.grid(row=4, column=0)


    # figure
    frm = tk.Frame(self)

    fig = Figure(figsize=(5, 4), dpi=100)

    self.canvas = FigureCanvasTkAgg(fig, master=frm)
    self.plot = fig.add_subplot(111)
    self.canvas.draw()
    self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    frm.grid(row=1, rowspan=4, column=1, padx=3, pady=3)


    # navigation buttons
    frm = tk.Frame(self)

    btn = tk.Button(frm, text="Go to the start page",
                       command=lambda: controller.show_frame("StartPage"))
    btn.grid(row=0, column=0, padx=30)

    btn = tk.Button(frm, text="Reset",
                       command=lambda: self.reset())
    btn.grid(row=0, column=1, padx=30)

    btn = tk.Button(frm, text="Calculate!",
                       command=lambda attribute=self.attri, training=self.train, focus=self.focus, dn=self.dn : self.calculate(attribute, training, focus, dn))
    btn.grid(row=0, column=2, padx=30)

    btn = tk.Button(frm, text='Custom Extended Test', 
                        command=lambda: controller.show_frame("TestExtendedCustom"))
    btn.grid(row=0, column=3, padx=30)

    frm.grid(row=5, column=0, columnspan=2)


    # clear all fields
    self.reset()


  def reset(self):

    self.attri.set('')
    self.train.set('')
    self.focus.set('')

    self.dn[0].set('')
    self.dn[1].set('')

    self.succ_lik.set('')
    self.succ_exp.set('')

    self.canvas.draw()
    self.plot.clear()
    self.plot.cla()


  def calculate(self, attribute, training, focus, dn):

    probabilities = extended_test(attribute.get()+training.get(), [training.get(), focus.get()], [dn[0].get(), dn[1].get()], verbose=False)

    self.plot.set_title('Success Distribution')
    self.plot.set_xlabel('Number of Successes')
    self.plot.set_ylabel('Likelihood')
    self.plot.bar(range(probabilities.shape[0]), probabilities)
    self.canvas.draw()
    self.plot.clear()
    self.plot.cla()

    self.succ_lik.set('{:2.2%}'.format(np.sum(probabilities[dn_1.get():])))
    self.succ_exp.set('{:2.3}'.format(np.matmul(range(probabilities.shape[0]), probabilities)))




class TestExtendedCustom(tk.Frame):

  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller


    # title
    title = tk.Label(self, text="Custom Extended Test Calculator", font=controller.title_font)
    title.grid(row=0, columnspan=3)


    # attributes
    self.attri = [tk.IntVar(), tk.IntVar(), tk.IntVar()]

    frm = tk.Frame(self)

    for i in range(3):
        lbl = tk.Label(frm, text='Attribute ' + str(i+1) + ':')
        lbl.grid(row=i, column=0)

        cbx = ttk.Combobox(frm, textvariable=self.attri[i], width=3)
        cbx['values'] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        cbx.grid(row=i, column=1)

    frm.grid(row=1, column=0)


    # skill values
    self.train = [tk.IntVar(), tk.IntVar(), tk.IntVar()]
    self.focus = [tk.IntVar(), tk.IntVar(), tk.IntVar()]

    frm = tk.Frame(self)

    for i in range(4):
      lbl = tk.Label(frm, text=str(i))
      lbl.grid(row=0, column=i+1)

    for i in range(3):
        lbl = tk.Label(frm, text='Training ' + str(i+1))
        lbl.grid(row=(2*i)+1, column=0)

        for j in range(4):
          rad = ttk.Radiobutton(frm, variable=self.train[i], value=j)
          rad.grid(row=(2*i)+1, column=j+1)

        lbl = tk.Label(frm, text='Focus ' + str(i+1))
        lbl.grid(row=2*(i+1), column=0)

        for j in range(4):
          rad = ttk.Radiobutton(frm, variable=self.focus[i], value=j)
          rad.grid(row=2*(i+1), column=j+1)
    
    frm.grid(row=2, column=0)


    # difficulty number
    self.dn = [tk.IntVar(), tk.IntVar()]

    frm = tk.Frame(self)

    lbl = tk.Label(frm, text='Difficulty Number -')
    lbl.grid(row=0, column=0)

    cbx = ttk.Combobox(frm, textvariable=self.dn[0], width=3)
    cbx['values'] = (2, 3, 4, 5, 6)
    cbx.grid(row=0, column=1)

    lbl = tk.Label(frm, text=':')
    lbl.grid(row=0, column=2)

    cbx = ttk.Combobox(frm, textvariable=self.dn[1], width=3)
    cbx['values'] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
    cbx.grid(row=0, column=3)

    frm.grid(row=3, column=0)


    # results
    self.succ_lik = tk.StringVar()
    self.succ_exp = tk.StringVar()

    frm = tk.Frame(self)

    lbl = tk.Label(frm, text='Success Likelihood:')
    lbl.grid(row=0, column=0)

    lbl = tk.Label(frm, textvariable=self.succ_lik)
    lbl.grid(row=0, column=1)

    lbl = tk.Label(frm, text='Expected Successes:')
    lbl.grid(row=1, column=0)

    lbl = tk.Label(frm, textvariable=self.succ_exp)
    lbl.grid(row=1, column=1)
    
    frm.grid(row=4, column=0)


    # figure
    frm = tk.Frame(self)

    fig = Figure(figsize=(5, 4), dpi=100)

    self.canvas = FigureCanvasTkAgg(fig, master=frm)
    self.plot = fig.add_subplot(111)
    self.canvas.draw()
    self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    frm.grid(row=1, rowspan=4, column=1, padx=3, pady=3)


    # navigation
    frm = tk.Frame(self)

    btn = tk.Button(frm, text="Go to the start page",
                       command=lambda: controller.show_frame("StartPage"))
    btn.grid(row=0, column=0, padx=30)

    btn = tk.Button(frm, text="Reset",
                       command=lambda: self.reset())
    btn.grid(row=0, column=1, padx=30)

    btn = tk.Button(frm, text="Calculate!",
                       command=lambda attribute=self.attri, training=self.train, focus=self.focus, dn=self.dn : self.calculate(attribute, training, focus, dn))
    btn.grid(row=0, column=2, padx=30)

    btn = tk.Button(frm, text='Standard Extended Test', 
                        command=lambda: controller.show_frame("TestExtended"))
    btn.grid(row=0, column=3, padx=30)

    frm.grid(row=5, column=0, columnspan=2)

    # clear all fields
    self.reset()


  def reset(self):

    self.attri[0].set('')
    self.attri[1].set('')
    self.attri[2].set('')

    self.train[0].set('')
    self.train[1].set('')
    self.train[2].set('')

    self.focus[0].set('')
    self.focus[1].set('')
    self.focus[2].set('')

    self.dn[0].set('')
    self.dn[1].set('')

    self.succ_lik.set('')
    self.succ_exp.set('')

    self.canvas.draw()
    self.plot.clear()
    self.plot.cla()



  def calculate(self, attribute, training, focus, dn):

    dice_pool = [attribute[0].get()+training[0].get(), attribute[1].get()+training[1].get(), attribute[2].get()+training[2].get()]
    skill = [[training[0].get(), focus[0].get()], [training[1].get(), focus[1].get()], [training[2].get(), focus[2].get()]]

    probabilities = extended_test(dice_pool, skill, [dn[0].get(), dn[1].get()], verbose=False)

    self.plot.set_title('Success Distribution')
    self.plot.set_xlabel('Number of Successes')
    self.plot.set_ylabel('Likelihood')
    self.plot.bar(range(probabilities.shape[0]), probabilities)
    self.canvas.draw()
    self.plot.clear()
    self.plot.cla()

    self.succ_lik.set('{:2.2%}'.format(np.sum(probabilities[dn_1.get():])))
    self.succ_exp.set('{:2.3}'.format(np.matmul(range(probabilities.shape[0]), probabilities)))




class DamageCalculator(tk.Frame):

  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller

    title = tk.Label(self, text="Damage Calculator", font=controller.title_font)
    title.grid(row=0, columnspan=4)

    # combat abilities
    self.combat = tk.StringVar()
    self.defence = tk.StringVar()

    frm = tk.Frame(self)

    lbl = tk.Label(frm, text='Your Combat\nAbility')
    lbl.grid(row=0, column=1)
    
    lbl = tk.Label(frm, text='Target\nDefence')
    lbl.grid(row=0, column=2)

    for i, level in enumerate(ABILITY_LEVELS):
      lbl = tk.Label(frm, text=level)
      lbl.grid(row=6-i, column=0)
      
      rad = ttk.Radiobutton(frm, variable=self.combat, value=level)
      rad.grid(row=6-i, column=1)
      
      rad = ttk.Radiobutton(frm, variable=self.defence, value=level)
      rad.grid(row=6-i, column=2)

    self.combat.set('')
    self.defence.set('')
    
    frm.grid(row=3, column=0)


    # talents
    self.talents = []
    self.talent_buttons = {}

    frm = tk.Frame(self)

    lbl = tk.Label(frm, text='Combat Talents')
    lbl.grid(row=0, columnspan=4)

    for i, talent in enumerate(TALENTS_ALL):
      self.talent_buttons[talent] = tk.Button(frm, text=talent, command=lambda tal=talent: self.press_talent(tal))
      self.talent_buttons[talent].grid(row=int(i/4) + 1, column=int(i%4), sticky='NSEW')

    frm.grid(row=1, column=0, columnspan=2, padx=3)


    # weapon traits
    self.traits = []
    self.trait_buttons = {}

    frm = tk.Frame(self)

    lbl = tk.Label(frm, text='Weapon Traits')
    lbl.grid(row=0, column=0, columnspan=4)

    for i, trait in enumerate(TRAITS_ALL):
      self.trait_buttons[trait] = tk.Button(frm, text=trait, command=lambda tra=trait: self.press_trait(tra))
      self.trait_buttons[trait].grid(row=1, column=i, sticky='NSEW')

    frm.grid(row=2, column=0, columnspan=2, padx=3)


    # other necessary values
    self.attri = tk.IntVar()
    self.sk_train = tk.IntVar()
    self.sk_focus = tk.IntVar()
    self.wpn_damage = tk.StringVar()
    self.tgt_armour = tk.IntVar()
    self.dual_wield = tk.BooleanVar()

    frm = tk.Frame(self)

    lbl = tk.Label(frm, text='Attack Attribute: ')
    lbl.grid(row=0, column=0)
    cbx = ttk.Combobox(frm, textvariable=self.attri)
    cbx['values'] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    cbx.current(0)
    cbx.grid(row=0, column=1)

    lbl = tk.Label(frm, text='Attack Skill Training: ')
    lbl.grid(row=1, column=0)
    cbx = ttk.Combobox(frm, textvariable=self.sk_train)
    cbx['values'] = (0, 1, 2, 3)
    cbx.current(0)
    cbx.grid(row=1, column=1)

    lbl = tk.Label(frm, text='Attack Skill Focus: ')
    lbl.grid(row=2, column=0)
    cbx = ttk.Combobox(frm, textvariable=self.sk_focus)
    cbx['values'] = (0, 1, 2, 3)
    cbx.current(0)
    cbx.grid(row=2, column=1)

    lbl = tk.Label(frm, text='Weapon Damage: ')
    lbl.grid(row=3, column=0)
    cbx = ttk.Combobox(frm, textvariable=self.wpn_damage)
    cbx['values'] = ('0+S','1+S','2+S','3+S','4+S')
    cbx.current(0)
    cbx.grid(row=3, column=1)

    lbl = tk.Label(frm, text='Target Armour: ')
    lbl.grid(row=4, column=0)
    cbx = ttk.Combobox(frm, textvariable=self.tgt_armour)
    cbx['values'] = (0, 1, 2, 3, 4, 5)
    cbx.current(0)
    cbx.grid(row=4, column=1)

    lbl = tk.Label(frm, text='Dual Wielding: ')
    lbl.grid(row=5, column=0)
    cbn = ttk.Checkbutton(frm, variable=self.dual_wield, onvalue=True, offvalue=False)
    cbn.grid(row=5, column=1)

    self.attri.set('')
    self.sk_train.set('')
    self.sk_focus.set('')
    self.wpn_damage.set('')
    self.tgt_armour.set('')
    self.dual_wield.set(False)

    frm.grid(row=3, column=1)


    # figure 
    frm = tk.Frame(self)

    fig = Figure(figsize=(5, 4), dpi=100)

    self.canvas = FigureCanvasTkAgg(fig, master=frm)
    self.plot = fig.add_subplot(111)
    self.canvas.draw()
    self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    frm.grid(row=1, rowspan=3, column=2, padx=3, pady=3)


    # results and figure navigation
    self.results = []
    self.succ_lik = tk.StringVar()
    self.succ_exp = tk.StringVar()
    self.results_desc = tk.StringVar()

    frm = tk.Frame(self)

    lbl = tk.Label(frm, textvariable=self.succ_lik)
    lbl.grid(row=0, column=0)

    lbl = tk.Label(frm, textvariable=self.succ_exp)
    lbl.grid(row=1, column=0)

    btn = tk.Button(frm, text='<',
                    command=lambda: self.press_left())
    btn.grid(row=0, rowspan=2, column=1, padx=3)

    lbl = tk.Label(frm, textvariable=self.results_desc)
    lbl.grid(row=0, rowspan=2, column=2, padx=3)

    btn = tk.Button(frm, text='>',
                    command=lambda: self.press_right())
    btn.grid(row=0, rowspan=2, column=3, padx=3)
    
    self.succ_lik.set('')
    self.succ_exp.set('')
    self.results_desc.set('0 of 0')
    
    frm.grid(row=4, column=2)


    # navigation
    frm = tk.Frame(self)

    btn = tk.Button(frm, text="Go to the start page",
                    command=lambda: controller.show_frame("StartPage"))
    btn.grid(row=0, column=0, padx=30)

    btn = tk.Button(frm, text="Reset",
                    command=lambda: self.reset())
    btn.grid(row=0, column=1, padx=30)

    btn = tk.Button(frm, text="Calculate!",
                    command=lambda attribute=self.attri, 
                                   attack_skill=(self.sk_train, self.sk_focus), 
                                   combat_ability=self.combat, 
                                   defense=self.defence, 
                                   talents=self.talents, 
                                   dual_wielding=self.dual_wield, 
                                   weapon_damage=self.wpn_damage, 
                                   weapon_traits=self.traits, 
                                   armour=self.tgt_armour: self.calculate(attribute, attack_skill, combat_ability, defense, talents, dual_wielding, weapon_damage, weapon_traits, armour))
    btn.grid(row=0, column=2, padx=30)

    frm.grid(row=5, column=0, columnspan=4)


  def reset(self):
    for talent in self.talents:
      self.talent_buttons[talent].configure(background='SystemButtonFace')
    self.talents = []

    for trait in self.traits:
      self.trait_buttons[trait].configure(background='SystemButtonFace')
    self.traits = []

    self.combat.set('')
    self.defence.set('')

    self.attri.set('')
    self.sk_train.set('')
    self.sk_focus.set('')
    self.wpn_damage.set('')
    self.tgt_armour.set('')
    self.dual_wield.set(False)

    self.results = []
    self.succ_lik.set('')
    self.succ_exp.set('')
    self.results_desc.set('0 of 0')

    self.canvas.draw()
    self.plot.clear()
    self.plot.cla()

  def press_talent(self, talent):
    if self.talent_buttons[talent].cget('bg') == 'SystemButtonFace':
      self.talent_buttons[talent].configure(background='LightBlue2')
      self.talents.append(talent)
    else:
      self.talent_buttons[talent].configure(background='SystemButtonFace')
      self.talents.remove(talent)

    print(self.talents)

  def press_trait(self, trait):
    if self.trait_buttons[trait].cget('bg') == 'SystemButtonFace':
      self.trait_buttons[trait].configure(background='LightBlue2')
      self.traits.append(trait)
    else:
      self.trait_buttons[trait].configure(background='SystemButtonFace')
      self.traits.remove(trait)

    print(self.traits)

  def press_left(self):
    if len(self.results) > 1:
      num_res = len(self.results)
      self.idx = (self.idx-1) % num_res
      self.results_desc.set(str(self.idx+1) + ' of ' + str(num_res))

      self.plot.set_title(self.results[self.idx][4])
      self.plot.set_xlabel(self.results[self.idx][5])
      self.plot.set_ylabel(self.results[self.idx][6])
      self.plot.bar(self.results[self.idx][2], self.results[self.idx][3])
      self.canvas.draw()
      self.plot.clear()
      self.plot.cla()

      self.succ_lik.set(self.results[self.idx][0])
      self.succ_exp.set(self.results[self.idx][1])

  def press_right(self):
    if len(self.results) > 1:
      num_res = len(self.results)
      self.idx = (self.idx+1) % num_res
      self.results_desc.set(str(self.idx+1) + ' of ' + str(num_res))

      self.plot.set_title(self.results[self.idx][4])
      self.plot.set_xlabel(self.results[self.idx][5])
      self.plot.set_ylabel(self.results[self.idx][6])
      self.plot.bar(self.results[self.idx][2], self.results[self.idx][3])
      self.canvas.draw()
      self.plot.clear()
      self.plot.cla()

      self.succ_lik.set(self.results[self.idx][0])
      self.succ_exp.set(self.results[self.idx][1])

  def calculate(self, attribute, attack_skill, combat_ability, defense, talents, dual_wielding, weapon_damage, weapon_traits, armour, verbose=True):

    print(talents, weapon_traits)

    self.results = attack(attribute.get(), (attack_skill[0].get(), attack_skill[1].get()), ABILITY_LEVELS.index(combat_ability.get()), ABILITY_LEVELS.index(defense.get()), talents, dual_wielding.get(), int(weapon_damage.get()[0]), weapon_traits, armour.get(), verbose=False)

    print(self.results)

    if len(self.results) > 0:
      self.idx = 0
      num_res = len(self.results)
      self.results_desc.set('1 of ' + str(num_res))

      self.plot.set_title(self.results[0][4])
      self.plot.set_xlabel(self.results[0][5])
      self.plot.set_ylabel(self.results[0][6])
      self.plot.bar(self.results[0][2], self.results[0][3])
      self.canvas.draw()
      self.plot.clear()
      self.plot.cla()

      self.succ_lik.set(self.results[0][0])
      self.succ_exp.set(self.results[0][1])




if __name__ == "__main__":
  app = SampleApp()
  app.mainloop()