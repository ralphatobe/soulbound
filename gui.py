import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from PIL import Image, ImageTk

from attacking_prob import attack_tkinter


TRAITS_ALL = ['Cleave', 'Ineffective', 'Penetrating', 'Rend', 'Spread']
TALENTS_ALL = ['Ambidextrous', 'Backstab', 'Barazakdum, the Doom-Oath', 'Battle Rage', 'Blood Frenzy', 'Bulwark', 'Crushing Blow', 'Gunslinger', 'Heavy Hitter', 'Immense Strikes', 'Immense Swing', 'Martial Memories', 'Mounted Combatant', 'Patient Strike', 'Pierce Armour', 'Relentless Assault', 'Rending Blow', 'Sever', 'Shield Mastery', 'Sigmar\'s Judgement', 'Star-Fated Arrow', 'The Bigger They Are', 'Underdog']
ABILITY_LEVELS = ['Extraordinary', 'Superb', 'Great', 'Good', 'Average', 'Poor']



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
    for F in (StartPage, PageOne, PageTwo, DamageCalculator):
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
                        command=lambda: controller.show_frame("DamageCalculator"),
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

    # # Combobox creation 
    # n = tk.StringVar() 
    # monthchoosen = ttk.Combobox(self, width = 27, textvariable = n) 
      
    # # Adding combobox drop down list 
    # monthchoosen['values'] = ATTRIBUTE_RANGE
      
    # # monthchoosen.grid(column = 1, row = 5) 
    # monthchoosen.current() 
    # monthchoosen.pack()

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
      ca.grid(row=i+1, column=0)
      ca_1 = ttk.Radiobutton(combat_abilities, variable=self.combat, value=level)
      ca_1.grid(row=i+1, column=1)
      ca_2 = ttk.Radiobutton(combat_abilities, variable=self.defence, value=level)
      ca_2.grid(row=i+1, column=2)
    
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

    self.attribute = tk.StringVar()
    lbl = tk.Label(miscellaneous, text='Attack Attribute: ')
    lbl.grid(row=0, column=0)
    cbx = ttk.Combobox(miscellaneous, textvariable=self.attribute)
    cbx['values'] = ('0','1','2','3','4','5','6','7','8')
    cbx.current(0)
    cbx.grid(row=0, column=1)

    self.sk_train = tk.StringVar()
    lbl = tk.Label(miscellaneous, text='Attack Skill Training: ')
    lbl.grid(row=1, column=0)
    cbx = ttk.Combobox(miscellaneous, textvariable=self.sk_train)
    cbx['values'] = ('0','1','2','3')
    cbx.current(0)
    cbx.grid(row=1, column=1)

    self.sk_focus = tk.StringVar()
    lbl = tk.Label(miscellaneous, text='Attack Skill Focus: ')
    lbl.grid(row=2, column=0)
    cbx = ttk.Combobox(miscellaneous, textvariable=self.sk_focus)
    cbx['values'] = ('0','1','2','3')
    cbx.current(0)
    cbx.grid(row=2, column=1)

    self.wpn_damage = tk.StringVar()
    lbl = tk.Label(miscellaneous, text='Weapon Damage: ')
    lbl.grid(row=3, column=0)
    cbx = ttk.Combobox(miscellaneous, textvariable=self.wpn_damage)
    cbx['values'] = ('0+S','1+S','2+S','3+S','4+S')
    cbx.current(0)
    cbx.grid(row=3, column=1)

    self.tgt_armour = tk.StringVar()
    lbl = tk.Label(miscellaneous, text='Target Armour: ')
    lbl.grid(row=3, column=0)
    cbx = ttk.Combobox(miscellaneous, textvariable=self.tgt_armour)
    cbx['values'] = ('0','1','2','3','4','5')
    cbx.current(0)
    cbx.grid(row=3, column=1)

    self.dual_wield = tk.BooleanVar()
    lbl = tk.Label(miscellaneous, text='Dual Wielding: ')
    lbl.grid(row=4, column=0)
    cbn = ttk.Checkbutton(miscellaneous, variable=self.dual_wield, onvalue=True, offvalue=False)
    cbn.grid(row=4, column=1)

    miscellaneous.grid(row=2, column=1)


    button = tk.Button(self, text="Go to the start page",
                       command=lambda: controller.show_frame("StartPage"))
    button.grid(row=3, column=0)

    button = tk.Button(self, text="Calculate!",
                       command=lambda attribute=self.attribute, attack_skill=(self.sk_train, self.sk_focus), combat_ability=self.combat, defense=self.defence, talents=self.talents, dual_wielding=self.dual_wield, weapon_damage=self.wpn_damage, weapon_traits=self.traits, armour=self.tgt_armour: attack_tkinter(attribute, attack_skill, combat_ability, defense, talents, dual_wielding, weapon_damage, weapon_traits, armour))
    button.grid(row=3, column=1)



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