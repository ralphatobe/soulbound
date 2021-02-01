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

    load = Image.open("soulbound_logo.png")
    render = ImageTk.PhotoImage(load)
    img = tk.Label(self, image=render)
    img.image = render
    img.pack()

    frm_atk = tk.Frame(self, borderwidth=5)
    btn_atk = tk.Button(master=frm_atk, text='Attack Probability Calculator', 
                        command=lambda: controller.show_frame("DamageCalculator"),
                        font=self.title_font)
    # btn_atk.bind("<Button-1>", atk_prob_calc)
    btn_atk.pack(fill=tk.BOTH, expand=True)
    frm_atk.pack(side=tk.LEFT, expand=True)

    frm_tst = tk.Frame(self, borderwidth=5)
    btn_tst = tk.Button(master=frm_tst, text='Regular Test Calculator', 
                        command=lambda: controller.show_frame("TestRegular"),
                        font=self.title_font)
    # btn_tst.bind("<Button-1>", reg_test_calc)
    btn_tst.pack(fill=tk.BOTH, expand=True)
    frm_tst.pack(side=tk.LEFT, expand=True)

    frm_ext = tk.Frame(self, borderwidth=5)
    btn_ext = tk.Button(master=frm_ext, text='Extended Test Calculator', 
                        command=lambda: controller.show_frame("TestExtended"),
                        font=self.title_font)
    # btn_ext.bind("<Button-1>", ext_test_calc)
    btn_ext.pack(fill=tk.BOTH, expand=True)
    frm_ext.pack(side=tk.LEFT, expand=True)

    frm_ext = tk.Frame(self, borderwidth=5)
    btn_ext = tk.Button(master=frm_ext, text='Custom Extended Test Calculator', 
                        command=lambda: controller.show_frame("TestExtendedCustom"),
                        font=self.title_font)
    # btn_ext.bind("<Button-1>", ext_test_calc)
    btn_ext.pack(fill=tk.BOTH, expand=True)
    frm_ext.pack(side=tk.LEFT, expand=True)


class TestRegular(tk.Frame):

  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller

    # title
    title = tk.Label(self, text="Test Calculator", font=controller.title_font)
    title.grid(row=0, columnspan=2)


    frm_attri = tk.Frame(self)

    lbl_attri = tk.Label(frm_attri, text='Target Attribute:')
    lbl_attri.grid(row=0, column=0)

    self.attri = tk.IntVar()
    cbx_attri = ttk.Combobox(frm_attri, textvariable=self.attri, width=3)
    cbx_attri['values'] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    cbx_attri.current(0)
    cbx_attri.grid(row=0, column=1)

    frm_attri.grid(row=1, column=0)


    # skill values
    frm_skill = tk.Frame(self)

    lbl_skill = tk.Label(frm_skill, text='Target Skill')
    lbl_skill.grid(row=0, columnspan=5)

    for i in range(4):
      lbl_num = tk.Label(frm_skill, text=str(i))
      lbl_num.grid(row=1, column=i+1)

    lbl_train = tk.Label(frm_skill, text='Training')
    lbl_train.grid(row=2, column=0)

    self.train = tk.IntVar()
    for i in range(4):
      rad_train = ttk.Radiobutton(frm_skill, variable=self.train, value=i)
      rad_train.grid(row=2, column=i+1)

    lbl_train = tk.Label(frm_skill, text='Focus')
    lbl_train.grid(row=3, column=0)

    self.focus = tk.IntVar()
    for i in range(4):
      rad_focus = ttk.Radiobutton(frm_skill, variable=self.focus, value=i)
      rad_focus.grid(row=3, column=i+1)
    
    frm_skill.grid(row=2, column=0)


    frm_dn = tk.Frame(self)

    lbl_dn = tk.Label(frm_dn, text='Difficulty Number -')
    lbl_dn.grid(row=0, column=0)

    self.dn_0 = tk.IntVar()
    cbx_dn_0 = ttk.Combobox(frm_dn, textvariable=self.dn_0, width=3)
    cbx_dn_0['values'] = (2, 3, 4, 5, 6)
    cbx_dn_0.grid(row=0, column=1)

    lbl_dn = tk.Label(frm_dn, text=':')
    lbl_dn.grid(row=0, column=2)

    self.dn_1 = tk.IntVar()
    cbx_dn_1 = ttk.Combobox(frm_dn, textvariable=self.dn_1, width=3)
    cbx_dn_1['values'] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
    cbx_dn_1.grid(row=0, column=3)

    frm_dn.grid(row=3, column=0)




    # skill values
    frm_results = tk.Frame(self)

    lbl_results = tk.Label(frm_results, text='Success Likelihood:')
    lbl_results.grid(row=0, column=0)

    self.succ_lik = tk.StringVar()
    self.succ_lik.set('')
    lbl_results = tk.Label(frm_results, textvariable=self.succ_lik)
    lbl_results.grid(row=0, column=1)

    lbl_results = tk.Label(frm_results, text='Expected Successes:')
    lbl_results.grid(row=1, column=0)

    self.succ_exp = tk.StringVar()
    self.succ_exp.set('')
    lbl_results = tk.Label(frm_results, textvariable=self.succ_exp)
    lbl_results.grid(row=1, column=1)
    
    frm_results.grid(row=4, column=0)



    frm_fig = tk.Frame(self)

    self.fig = Figure(figsize=(5, 4), dpi=100)
    # t = np.arange(0, 3, .01)
    # fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

    self.canvas = FigureCanvasTkAgg(self.fig, master=frm_fig)
    self.canvas.draw()
    self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    frm_fig.grid(row=1, rowspan=4, column=1, padx=3, pady=3)

    button = tk.Button(self, text="Go to the start page",
                       command=lambda: controller.show_frame("StartPage"))
    button.grid(row=5, column=0)


    button = tk.Button(self, text="Calculate!",
                       command=lambda attribute=self.attri, training=self.train, focus=self.focus, dn_0=self.dn_0, dn_1=self.dn_1 : self.calculate(attribute, training, focus, dn_0, dn_1))
    button.grid(row=5, column=1)


  def calculate(self, attribute, training, focus, dn_0, dn_1):

    probabilities = test(attribute.get()+training.get(), [training.get(), focus.get()], [dn_0.get(), dn_1.get()], verbose=False)

    plot = self.fig.add_subplot(111, xlabel='Number of Successes', ylabel='Likelihood')
    plot.bar(range(probabilities.shape[0]), probabilities)
    self.canvas.draw()
    plot.clear()

    print('{:2.2%}'.format(np.sum(probabilities[dn_1.get():])))
    print('{:2.3}'.format(np.matmul(range(probabilities.shape[0]), probabilities)))

    self.succ_lik.set('{:2.2%}'.format(np.sum(probabilities[dn_1.get():])))
    self.succ_exp.set('{:2.3}'.format(np.matmul(range(probabilities.shape[0]), probabilities)))



class TestExtended(tk.Frame):

  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller

    # title
    title = tk.Label(self, text="Extended Test Calculator", font=controller.title_font)
    title.grid(row=0, columnspan=2)


    frm_attri = tk.Frame(self)

    lbl_attri = tk.Label(frm_attri, text='Target Attribute:')
    lbl_attri.grid(row=0, column=0)

    self.attri = tk.IntVar()
    cbx_attri = ttk.Combobox(frm_attri, textvariable=self.attri, width=3)
    cbx_attri['values'] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    cbx_attri.current(0)
    cbx_attri.grid(row=0, column=1)

    frm_attri.grid(row=1, column=0)


    # skill values
    frm_skill = tk.Frame(self)

    lbl_skill = tk.Label(frm_skill, text='Target Skill')
    lbl_skill.grid(row=0, columnspan=5)

    for i in range(4):
      lbl_num = tk.Label(frm_skill, text=str(i))
      lbl_num.grid(row=1, column=i+1)

    lbl_train = tk.Label(frm_skill, text='Training')
    lbl_train.grid(row=2, column=0)

    self.train = tk.IntVar()
    for i in range(4):
      rad_train = ttk.Radiobutton(frm_skill, variable=self.train, value=i)
      rad_train.grid(row=2, column=i+1)

    lbl_train = tk.Label(frm_skill, text='Focus')
    lbl_train.grid(row=3, column=0)

    self.focus = tk.IntVar()
    for i in range(4):
      rad_focus = ttk.Radiobutton(frm_skill, variable=self.focus, value=i)
      rad_focus.grid(row=3, column=i+1)
    
    frm_skill.grid(row=2, column=0)


    frm_dn = tk.Frame(self)

    lbl_dn = tk.Label(frm_dn, text='Difficulty Number -')
    lbl_dn.grid(row=0, column=0)

    self.dn_0 = tk.IntVar()
    cbx_dn_0 = ttk.Combobox(frm_dn, textvariable=self.dn_0, width=3)
    cbx_dn_0['values'] = (2, 3, 4, 5, 6)
    cbx_dn_0.grid(row=0, column=1)

    lbl_dn = tk.Label(frm_dn, text=':')
    lbl_dn.grid(row=0, column=2)

    self.dn_1 = tk.IntVar()
    cbx_dn_1 = ttk.Combobox(frm_dn, textvariable=self.dn_1, width=3)
    cbx_dn_1['values'] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
    cbx_dn_1.grid(row=0, column=3)

    frm_dn.grid(row=3, column=0)




    # skill values
    frm_results = tk.Frame(self)

    lbl_results = tk.Label(frm_results, text='Success Likelihood:')
    lbl_results.grid(row=0, column=0)

    self.succ_lik = tk.StringVar()
    self.succ_lik.set('')
    lbl_results = tk.Label(frm_results, textvariable=self.succ_lik)
    lbl_results.grid(row=0, column=1)

    lbl_results = tk.Label(frm_results, text='Expected Successes:')
    lbl_results.grid(row=1, column=0)

    self.succ_exp = tk.StringVar()
    self.succ_exp.set('')
    lbl_results = tk.Label(frm_results, textvariable=self.succ_exp)
    lbl_results.grid(row=1, column=1)
    
    frm_results.grid(row=4, column=0)


    frm_fig = tk.Frame(self)

    self.fig = Figure(figsize=(5, 4), dpi=100)

    self.canvas = FigureCanvasTkAgg(self.fig, master=frm_fig)
    self.canvas.draw()
    self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    frm_fig.grid(row=1, rowspan=4, column=1, padx=3, pady=3)


    button = tk.Button(self, text="Go to the start page",
                       command=lambda: controller.show_frame("StartPage"))
    button.grid(row=5, column=0)


    button = tk.Button(self, text="Calculate!",
                       command=lambda attribute=self.attri, training=self.train, focus=self.focus, dn_0=self.dn_0, dn_1=self.dn_1 : self.calculate(attribute, training, focus, dn_0, dn_1))
    button.grid(row=5, column=1)


  def calculate(self, attribute, training, focus, dn_0, dn_1):

    probabilities = extended_test(attribute.get()+training.get(), [training.get(), focus.get()], [dn_0.get(), dn_1.get()], verbose=False)

    plot = self.fig.add_subplot(111, xlabel='Number of Successes', ylabel='Likelihood')
    plot.bar(range(probabilities.shape[0]), probabilities)
    self.canvas.draw()
    plot.clear()

    print('{:2.2%}'.format(np.sum(probabilities[dn_1.get():])))
    print('{:2.3}'.format(np.matmul(range(probabilities.shape[0]), probabilities)))

    self.succ_lik.set('{:2.2%}'.format(np.sum(probabilities[dn_1.get():])))
    self.succ_exp.set('{:2.3}'.format(np.matmul(range(probabilities.shape[0]), probabilities)))




class TestExtendedCustom(tk.Frame):

  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller

    # title
    title = tk.Label(self, text="Custom Extended Test Calculator", font=controller.title_font)
    title.grid(row=0, columnspan=2)


    frm_attri = tk.Frame(self)

    lbl_attri = tk.Label(frm_attri, text='Target Attribute 1:')
    lbl_attri.grid(row=0, column=0)

    self.attri = [tk.IntVar(), tk.IntVar(), tk.IntVar()]

    cbx_attri = ttk.Combobox(frm_attri, textvariable=self.attri[0], width=3)
    cbx_attri['values'] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    cbx_attri.current(0)
    cbx_attri.grid(row=0, column=1)

    lbl_attri = tk.Label(frm_attri, text='Target Attribute 2:')
    lbl_attri.grid(row=1, column=0)

    cbx_attri = ttk.Combobox(frm_attri, textvariable=self.attri[1], width=3)
    cbx_attri['values'] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    cbx_attri.current(0)
    cbx_attri.grid(row=1, column=1)

    lbl_attri = tk.Label(frm_attri, text='Target Attribute 3:')
    lbl_attri.grid(row=2, column=0)

    cbx_attri = ttk.Combobox(frm_attri, textvariable=self.attri[2], width=3)
    cbx_attri['values'] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    cbx_attri.current(0)
    cbx_attri.grid(row=2, column=1)

    frm_attri.grid(row=1, column=0)


    # skill values
    frm_skill = tk.Frame(self)

    lbl_skill = tk.Label(frm_skill, text='Target Skill')
    lbl_skill.grid(row=0, columnspan=5)

    self.train = [tk.IntVar(), tk.IntVar(), tk.IntVar()]
    self.focus = [tk.IntVar(), tk.IntVar(), tk.IntVar()]

    for i in range(4):
      lbl_num = tk.Label(frm_skill, text=str(i))
      lbl_num.grid(row=1, column=i+1)

    lbl_train = tk.Label(frm_skill, text='Training 1')
    lbl_train.grid(row=2, column=0)

    for i in range(4):
      rad_train = ttk.Radiobutton(frm_skill, variable=self.train[0], value=i)
      rad_train.grid(row=2, column=i+1)

    lbl_train = tk.Label(frm_skill, text='Focus 1')
    lbl_train.grid(row=3, column=0)

    for i in range(4):
      rad_focus = ttk.Radiobutton(frm_skill, variable=self.focus[0], value=i)
      rad_focus.grid(row=3, column=i+1)

    lbl_train = tk.Label(frm_skill, text='Training 2')
    lbl_train.grid(row=4, column=0)

    for i in range(4):
      rad_train = ttk.Radiobutton(frm_skill, variable=self.train[1], value=i)
      rad_train.grid(row=4, column=i+1)

    lbl_train = tk.Label(frm_skill, text='Focus 2')
    lbl_train.grid(row=5, column=0)

    for i in range(4):
      rad_focus = ttk.Radiobutton(frm_skill, variable=self.focus[1], value=i)
      rad_focus.grid(row=5, column=i+1)

    lbl_train = tk.Label(frm_skill, text='Training 3')
    lbl_train.grid(row=6, column=0)

    for i in range(4):
      rad_train = ttk.Radiobutton(frm_skill, variable=self.train[2], value=i)
      rad_train.grid(row=6, column=i+1)

    lbl_train = tk.Label(frm_skill, text='Focus 3')
    lbl_train.grid(row=7, column=0)

    for i in range(4):
      rad_focus = ttk.Radiobutton(frm_skill, variable=self.focus[2], value=i)
      rad_focus.grid(row=7, column=i+1)
    
    frm_skill.grid(row=2, column=0)


    frm_dn = tk.Frame(self)

    lbl_dn = tk.Label(frm_dn, text='Difficulty Number -')
    lbl_dn.grid(row=0, column=0)

    self.dn_0 = tk.IntVar()
    cbx_dn_0 = ttk.Combobox(frm_dn, textvariable=self.dn_0, width=3)
    cbx_dn_0['values'] = (2, 3, 4, 5, 6)
    cbx_dn_0.grid(row=0, column=1)

    lbl_dn = tk.Label(frm_dn, text=':')
    lbl_dn.grid(row=0, column=2)

    self.dn_1 = tk.IntVar()
    cbx_dn_1 = ttk.Combobox(frm_dn, textvariable=self.dn_1, width=3)
    cbx_dn_1['values'] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
    cbx_dn_1.grid(row=0, column=3)

    frm_dn.grid(row=3, column=0)




    # skill values
    frm_results = tk.Frame(self)

    lbl_results = tk.Label(frm_results, text='Success Likelihood:')
    lbl_results.grid(row=0, column=0)

    self.succ_lik = tk.StringVar()
    self.succ_lik.set('')
    lbl_results = tk.Label(frm_results, textvariable=self.succ_lik)
    lbl_results.grid(row=0, column=1)

    lbl_results = tk.Label(frm_results, text='Expected Successes:')
    lbl_results.grid(row=1, column=0)

    self.succ_exp = tk.StringVar()
    self.succ_exp.set('')
    lbl_results = tk.Label(frm_results, textvariable=self.succ_exp)
    lbl_results.grid(row=1, column=1)
    
    frm_results.grid(row=4, column=0)


    frm_fig = tk.Frame(self)

    self.fig = Figure(figsize=(5, 4), dpi=100)

    self.canvas = FigureCanvasTkAgg(self.fig, master=frm_fig)
    self.canvas.draw()
    self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    frm_fig.grid(row=1, rowspan=4, column=1, padx=3, pady=3)


    button = tk.Button(self, text="Go to the start page",
                       command=lambda: controller.show_frame("StartPage"))
    button.grid(row=5, column=0)


    button = tk.Button(self, text="Calculate!",
                       command=lambda attribute=self.attri, training=self.train, focus=self.focus, dn_0=self.dn_0, dn_1=self.dn_1 : self.calculate(attribute, training, focus, dn_0, dn_1))
    button.grid(row=5, column=1)


  def calculate(self, attribute, training, focus, dn_0, dn_1):

    dice_pool = [attribute[0].get()+training[0].get(), attribute[1].get()+training[1].get(), attribute[2].get()+training[2].get()]
    skill = [[training[0].get(), focus[0].get()], [training[1].get(), focus[1].get()], [training[2].get(), focus[2].get()]]

    probabilities = extended_test(dice_pool, skill, [dn_0.get(), dn_1.get()], verbose=False)

    plot = self.fig.add_subplot(111, xlabel='Number of Successes', ylabel='Likelihood')
    plot.bar(range(probabilities.shape[0]), probabilities)
    self.canvas.draw()
    plot.clear()

    print('{:2.2%}'.format(np.sum(probabilities[dn_1.get():])))
    print('{:2.3}'.format(np.matmul(range(probabilities.shape[0]), probabilities)))

    self.succ_lik.set('{:2.2%}'.format(np.sum(probabilities[dn_1.get():])))
    self.succ_exp.set('{:2.3}'.format(np.matmul(range(probabilities.shape[0]), probabilities)))




class DamageCalculator(tk.Frame):

  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller

    title = tk.Label(self, text="Damage Calculator", font=controller.title_font)
    title.grid(row=0, columnspan=4)

    combat_abilities = tk.Frame(self)

    yca = tk.Label(combat_abilities, text='Your Combat\nAbility')
    yca.grid(row=0, column=1)
    td = tk.Label(combat_abilities, text='Target\nDefence')
    td.grid(row=0, column=2)

    self.combat = tk.StringVar()
    self.defence = tk.StringVar()
    for i, level in enumerate(ABILITY_LEVELS):
      ca = tk.Label(combat_abilities, text=level)
      ca.grid(row=6-i, column=0)
      ca_1 = ttk.Radiobutton(combat_abilities, variable=self.combat, value=level)
      ca_1.grid(row=6-i, column=1)
      ca_2 = ttk.Radiobutton(combat_abilities, variable=self.defence, value=level)
      ca_2.grid(row=6-i, column=2)
    
    combat_abilities.grid(row=2, column=0)


    talents = tk.Frame(self)

    t_title = tk.Label(talents, text='Combat Talents')
    t_title.grid(row=0, columnspan=4)

    self.talent_buttons = {}

    for i, talent in enumerate(TALENTS_ALL):
      row = int(i/4) + 1
      col = int(i%4)
      self.talent_buttons[talent] = tk.Button(talents, text=talent, command=lambda tal=talent: self.press_talent(tal))
      self.talent_buttons[talent].grid(row=row, column=col, sticky='NSEW')

    self.talents = []

    talents.grid(row=1, column=0)

    traits = tk.Frame(self)


    t_title = tk.Label(traits, text='Weapon Traits')
    t_title.grid(row=0, columnspan=1)

    self.trait_buttons = {}

    for i, trait in enumerate(TRAITS_ALL):
      row = i+1
      self.trait_buttons[trait] = tk.Button(traits, text=trait, command=lambda tra=trait: self.press_trait(tra))
      self.trait_buttons[trait].grid(row=row, sticky='NSEW')

    self.traits = []

    traits.grid(row=1, column=1)

    miscellaneous = tk.Frame(self)

    self.attri = tk.IntVar()
    lbl = tk.Label(miscellaneous, text='Attack Attribute: ')
    lbl.grid(row=0, column=0)
    cbx = ttk.Combobox(miscellaneous, textvariable=self.attri)
    cbx['values'] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    cbx.current(0)
    cbx.grid(row=0, column=1)

    self.sk_train = tk.IntVar()
    lbl = tk.Label(miscellaneous, text='Attack Skill Training: ')
    lbl.grid(row=1, column=0)
    cbx = ttk.Combobox(miscellaneous, textvariable=self.sk_train)
    cbx['values'] = (0, 1, 2, 3)
    cbx.current(0)
    cbx.grid(row=1, column=1)

    self.sk_focus = tk.IntVar()
    lbl = tk.Label(miscellaneous, text='Attack Skill Focus: ')
    lbl.grid(row=2, column=0)
    cbx = ttk.Combobox(miscellaneous, textvariable=self.sk_focus)
    cbx['values'] = (0, 1, 2, 3)
    cbx.current(0)
    cbx.grid(row=2, column=1)

    self.wpn_damage = tk.StringVar()
    lbl = tk.Label(miscellaneous, text='Weapon Damage: ')
    lbl.grid(row=3, column=0)
    cbx = ttk.Combobox(miscellaneous, textvariable=self.wpn_damage)
    cbx['values'] = ('0+S','1+S','2+S','3+S','4+S')
    cbx.current(0)
    cbx.grid(row=3, column=1)

    self.tgt_armour = tk.IntVar()
    lbl = tk.Label(miscellaneous, text='Target Armour: ')
    lbl.grid(row=4, column=0)
    cbx = ttk.Combobox(miscellaneous, textvariable=self.tgt_armour)
    cbx['values'] = (0, 1, 2, 3, 4, 5)
    cbx.current(0)
    cbx.grid(row=4, column=1)

    self.dual_wield = tk.BooleanVar()
    lbl = tk.Label(miscellaneous, text='Dual Wielding: ')
    lbl.grid(row=5, column=0)
    cbn = ttk.Checkbutton(miscellaneous, variable=self.dual_wield, onvalue=True, offvalue=False)
    cbn.grid(row=5, column=1)

    miscellaneous.grid(row=2, column=1)




    # skill values
    frm_results = tk.Frame(self)

    lbl_results = tk.Label(frm_results, text='Success Likelihood:')
    lbl_results.grid(row=0, column=0)

    self.succ_lik = tk.StringVar()
    self.succ_lik.set('')
    lbl_results = tk.Label(frm_results, textvariable=self.succ_lik)
    lbl_results.grid(row=0, column=1)

    lbl_results = tk.Label(frm_results, text='Expected Successes:')
    lbl_results.grid(row=1, column=0)

    self.succ_exp = tk.StringVar()
    self.succ_exp.set('')
    lbl_results = tk.Label(frm_results, textvariable=self.succ_exp)
    lbl_results.grid(row=1, column=1)
    
    frm_results.grid(row=3, column=2)


    frm_fig = tk.Frame(self)

    self.fig = Figure(figsize=(5, 4), dpi=100)

    self.canvas = FigureCanvasTkAgg(self.fig, master=frm_fig)
    self.canvas.draw()
    self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    frm_fig.grid(row=1, rowspan=2, column=2, padx=3, pady=3)


    button = tk.Button(self, text="Go to the start page",
                       command=lambda: controller.show_frame("StartPage"))
    button.grid(row=4, column=0)

    button = tk.Button(self, text="Calculate!",
                       command=lambda attribute=self.attri, 
                                      attack_skill=(self.sk_train, self.sk_focus), 
                                      combat_ability=self.combat, 
                                      defense=self.defence, 
                                      talents=self.talents, 
                                      dual_wielding=self.dual_wield, 
                                      weapon_damage=self.wpn_damage, 
                                      weapon_traits=self.traits, 
                                      armour=self.tgt_armour: self.calculate(attribute, attack_skill, combat_ability, defense, talents, dual_wielding, weapon_damage, weapon_traits, armour))
    button.grid(row=4, column=1)



  def press_talent(self, talent):
    if self.talent_buttons[talent].cget('bg') == 'SystemButtonFace':
      self.talent_buttons[talent].configure(background='LightBlue2')
      self.talents.append(talent)
    else:
      self.talent_buttons[talent].configure(background='SystemButtonFace')
      self.talents.remove(talent)


  def press_trait(self, trait):
    if self.trait_buttons[trait].cget('bg') == 'SystemButtonFace':
      self.trait_buttons[trait].configure(background='LightBlue2')
      self.traits.append(trait)
    else:
      self.trait_buttons[trait].configure(background='SystemButtonFace')
      self.traits.remove(trait)


  def calculate(self, attribute, attack_skill, combat_ability, defense, talents, dual_wielding, weapon_damage, weapon_traits, armour, verbose=True):

    probabilities, damage = attack(attribute.get(), (attack_skill[0].get(), attack_skill[1].get()), ABILITY_LEVELS.index(combat_ability.get()), ABILITY_LEVELS.index(defense.get()), talents, dual_wielding.get(), int(weapon_damage.get()[0]), weapon_traits, armour.get(), verbose=False)

    print(damage)
    print(probabilities)

    plot = self.fig.add_subplot(111, xlabel='Number of Successes', ylabel='Likelihood')
    plot.bar(damage, probabilities)
    self.canvas.draw()
    plot.clear()

    self.succ_lik.set('{:2.2%}'.format(np.sum(probabilities[1:])))
    self.succ_exp.set('{:2.3}'.format(np.matmul(damage, probabilities)))





if __name__ == "__main__":
  app = SampleApp()
  app.mainloop()