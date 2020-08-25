import numpy as np
from scipy.special import binom
import matplotlib.pyplot as plt


COMBAT_LADDER = [None] + ['Poor']*2 + ['Average']*2 + ['Good']*2 + ['Great']*2 + ['Superb']*2 + ['Extraordinary']*2
ATTRIBUTES = ['Body', 'Mind', 'Soul']
SKILLS = ['Arcana', 'Athletics', 'Awareness', 'Ballistic Skill', 'Beast Handling', 'Channelling', 'Crafting', 'Determination', 'Devotion', 'Dexterity', 'Entertain', 'Fortitude', 'Guile', 'Intimidation', 'Intuition', 'Lore', 'Medicine', 'Might', 'Nature', 'Reflexes', 'Stealth', 'Survival', 'Theology', 'Weapon Skill']
TALENTS = ['A Warm Meal', 'Acute Sense', 'Aether-Khemists Guild Member', 'Alley Cat', 'Ambidextrous', 'Ancestral Memories', 'Animal Friend', 'Arcane Discipline', 'Backstab', 'Barazakdum, the Doom-Oath', 'Battle Rage', 'Blessed', 'Blood Frenzy', 'Bulwark', 'Combat Ready', 'Combat Repairs', 'Contortionist', 'Criminal', 'Crushing Blow', 'Demolitions Expert', 'Diplomat', 'Eidetic Memory', 'Endrineers Guild Member', 'Fearless', 'Forbidden Knowledge', 'Graceful Landing', 'Gunslinger', 'Guts', 'Hail of Doom', 'Hard to Kill', 'Heavy Hitter', 'Heroic Challenge', 'Hit and Run', 'Hunter', 'Immense Strikes', 'Immense Swing', 'Intimidating Manner', 'Iron Stomach', 'Iron Will', 'Legendary Saga', 'Loyal Companion', 'Martial Memories', 'Master of Disguise', 'Medic', 'Mounted Combatant', 'Night Vision', 'Observant', 'Opportunist', 'Orientation', 'Patient Strike', 'Pierce Armour', 'Point Blank Range', 'Potent Spells', 'Quick Reload', 'Relentless Assault', 'Rending Blow', 'Savvy', 'Scholar', 'Sense Ur-Gold', 'Sever', 'Shield Mastery', 'Sigmar\'s Judgement', 'Silver Tongue', 'Sleight of Hand', 'Spellcasting', 'Star-Fated Arrow', 'Strong Soul', 'Tactician', 'The Bigger They Are', 'Trader\'s Cache', 'Unbind', 'Unbreakable Spells', 'Underdog', 'Vanish', 'Weapon Weave', 'Witch-Sight', 'Zharrgrim']



class PlayerCharacter:
  def __init__(self, name, player_attributes, player_skills, player_talents):
    self.name = name

    self.attributes = {}
    for attribute in ATTRIBUTES:
      if attribute in player_attributes.keys():
        self.attributes[attribute] = Attribute(attribute, player_attributes[attribute])
      else:
        self.attributes[attribute] = Attribute(attribute, 0)

    self.skills = {}
    for skill in SKILLS:
      if skill in player_skills.keys():
        self.skills[skill] = Skill(skill, player_skills[skill][0], player_skills[skill][1])
      else:
        self.skills[skill] = Skill(skill, 0, 0)

    self.talents = {}
    for talent in TALENTS:
      if talent in player_talents:
        self.talents[talent] = Talent(talent, 'Description')
      # else:
      #   self.talents[talent] = talent(talent, '')

    # self.melee = CombatAbilities('Melee', self.attributes['Body'].rating + self.skills['Weapon Skill'].training)
    # self.accuracy = CombatAbilities('Accuracy', self.attributes['Mind'].rating + self.skills['Ballistic Skill'].training)
    # self.defence = CombatAbilities('Defence', self.attributes['Body'].rating + self.skills['Reflexes'].training)

    self.armour = 0
    self.toughness = self.attributes['Body'].rating + self.attributes['Mind'].rating + self.attributes['Soul'].rating
    self.wounds = np.ceil((self.attributes['Body'].rating + self.attributes['Mind'].rating + self.attributes['Soul'].rating)/2)

    self.initiative = self.attributes['Mind'].rating + self.skills['Awareness'].training + self.skills['Reflexes'].training
    self.natural_awareness = np.ceil((self.attributes['Mind'].rating + self.skills['Awareness'].training)/2)
    self.mettle = np.ceil((self.attributes['Soul'].rating)/2)


    self.inventory = []
    self.equipment = {'Right Hand':None, 'Left Hand':None, 'Armour':None, 'Other':[]}

  def get_body(self):
    body = self.attributes['Body'].rating
    if isinstance(self.equipment['Armour'], AetherRig) and 'Endrinharness' in self.equipment['Armour'].aetheric_devices:
      body += 1
    return body

  def get_melee(self):
    melee = CombatAbilities('Melee', self.get_body() + self.skills['Weapon Skill'].training)
    return melee

  def get_accuracy(self):
    accuracy = CombatAbilities('Accuracy', self.attributes['Mind'].rating + self.skills['Ballistic Skill'].training)
    if 'Gunslinger' in self.talents and \
       isinstance(self.equipment['Left Hand'], RangedWeapon) and 'Two-handed' not in self.equipment['Left Hand'].traits and \
       isinstance(self.equipment['Right Hand'], RangedWeapon) and 'Two-handed' not in self.equipment['Right Hand'].traits:
      accuracy.rating = COMBAT_LADDER[accuracy.value + 2]
      accuracy.explainer += ['Gunslinger active (+1 step)']
    return accuracy

  def get_defence(self):
    defence =  CombatAbilities('Defence', self.get_body() + self.skills['Reflexes'].training)
    if isinstance(self.equipment['Left Hand'], Armour) and self.equipment['Left Hand'].armour_type == 'Shield' or \
       isinstance(self.equipment['Right Hand'], Armour) and self.equipment['Right Hand'].armour_type == 'Shield':
      defence.rating = COMBAT_LADDER[defence.value + 2]
      defence.explainer += ['Shield equipped (+1 step)']
    return defence

  def equip(self, item, slot):
    if self.equipment[slot]:
      self.inventory += [self.equipment[slot]]
    self.equipment[slot] = item
    self.inventory.remove(item)

  def gain(self, item):
    self.inventory += [item]


class CombatAbilities:
  def __init__(self, name, value):
    self.name = name
    self.value = value
    self.rating = COMBAT_LADDER[value]
    self.explainer = ['Base value ' + str(value) + ' (' + str(COMBAT_LADDER[value-1]) + ')']


class Attribute:
  def __init__(self, name, rating):
    self.name = name
    self.rating = rating
    self.explainer = ['Base rating ' + str(rating)]


class Skill:
  def __init__(self, name, training, focus):
    self.name = name
    self.training = training
    self.focus = focus
    self.explainer = ['Base training ' + str(training), 'Base focus ' + str(focus)]


class Talent:
  def __init__(self, name, description, source=None):
    self.name = name
    self.description = description
    if source:
      self.explainer += [source]


class MeleeWeapon:
  def __init__(self, name, cost, availability, damage, traits):
    self.name = name
    self.cost = cost
    self.availability = availability
    self.damage = damage
    self.traits = traits


class RangedWeapon:
  def __init__(self, name, cost, availability, damage, traits):
    self.name = name
    self.cost = cost
    self.availability = availability
    self.damage = damage
    self.traits = traits


class Armour:
  def __init__(self, armour_type, cost, availability, requirements, benefit, traits):
    self.armour_type = armour_type
    self.cost = cost
    self.availability = availability
    self.requirements = requirements
    self.benefit = benefit
    self.traits = traits


class AetherRig(Armour):
  def __init__(self, armour_type, cost, availability, requirements, benefit, traits):
    super().__init__(armour_type, cost, availability, requirements, benefit, traits)

    self.power_capacity = 6
    self.power_level = 6
    self.power_consumed = 0
    self.aetheric_devices = []

  def drain_power(self):
    self.power_level -= 1

  def regular_maintenance(self):
    self.power_level = self.power_capacity

  def equip_aetheric_device(self, aetheric_device):
    if self.power_consumed + aetheric_device.power_consumption <= self.power_level:
      self.power_consumed += aetheric_device.power_consumption
      self.aetheric_devices.append(aetheric_device)

  def unequip_aetheric_device(self, aetheric_device):
    self.power_consumed -= aetheric_device.power_consumption
    self.aetheric_devices.remove(aetheric_device)
    return aetheric_device


class AdventuringGear:
  def __init__(self, name, cost, availability):
    self.name = name
    self.cost = cost
    self.availability = availability


class AethericDevice(AdventuringGear):
  def __init__(self, name, cost, availability, damage, traits, requirements, power_consumption, crafting):
    super().__init__(name, cost, availability)
    self.damage = damage
    self.traits = traits
    self.requirements = requirements
    self.power_consumption = power_consumption
    self.crafting = crafting


class AethericBlueprint:
  def __init__(self, endeavour, dn, cost):
    self.endeavour = endeavour
    self.dn = dn
    self.cost = cost


name = 'Teegansson Bryntok'
player_attributes = {'Body':3, 'Mind':4, 'Soul':1}
player_skills = {'Awareness':[1,1], 'Ballistic Skill':[2,1], 'Crafting':[2,1], 'Reflexes':[1,0]}
player_talents = ['Acute Sense', 'Aether-Khemists Guild Member', 'Iron Stomach', 'Observant', 'Gunslinger']


Teegansson = PlayerCharacter(name, player_attributes, player_skills, player_talents)

shield = Armour('Shield', 180, 'Common', None, 'Defence increases one step', None)
aether_rig = AetherRig('Basic Aether-rig', 350, 'Exotic', None, '1 Armour', None)
pistol_1 = RangedWeapon('Pistol', 65, 'Common', [1, 'S'], ['Close', 'Loud', 'Piercing', 'Range (Medium)'])
pistol_2 = RangedWeapon('Pistol', 65, 'Common', [1, 'S'], ['Close', 'Loud', 'Piercing', 'Range (Medium)'])

Teegansson.gain(shield)
Teegansson.equip(shield, 'Left Hand')
print(Teegansson.get_defence().rating)
print(Teegansson.get_defence().explainer)

Teegansson.gain(aether_rig)
Teegansson.equip(aether_rig, 'Armour')

Teegansson.gain(pistol_1)
Teegansson.gain(pistol_2)
Teegansson.equip(pistol_1, 'Left Hand')
Teegansson.equip(pistol_2, 'Right Hand')
print(Teegansson.get_accuracy().rating)
print(Teegansson.get_accuracy().explainer)
