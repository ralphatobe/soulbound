import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

from utils import test, at_least_m_of_n, exactly_m_of_n


def attack(body, ballistic_skill, accuracy, defense, talents, dual_wielding, weapon_damage, armour, verbose=True):

  # calculate the base dice pool size
  dice_pool_base = body + ballistic_skill[0]
  # print('base dice:', dice_pool_base)
  
  # calculate the base damage range
  damage_range = dice_pool_base + ballistic_skill[1]

  # modify weapon damage for dual wielding
  if dual_wielding:
    weapon_damage = weapon_damage * 2

  # add gunslinger bonus
  if 'Gunslinger' in talents:
    accuracy += 1

  # add ambidextrous bonus
  if 'Ambidextrous' in talents:
    ambidextrous = 6
    damage_range += 6
  else:
    ambidextrous = 1

  if 'Pierce Armour' in talents:
    damage_range += armour

  # calculate the hit dn
  dn = 4 - min([max([accuracy - defense, -2]), 2])
  # print('DN:', dn)

  # initialize full attack probabilities
  probabilities = np.zeros((ambidextrous, damage_range+1))
  # iterate over ambidextrous options
  # this method is overly brute force, but a better method would make my head hurt
  for i in range(ambidextrous):
    # modify dice pool if ambidextrous is active
    if 'Ambidextrous' in talents:
      dice_pool = dice_pool_base + i + 1
    else:
      dice_pool = dice_pool_base

    # compute hit likelihoods
    succ_prob = test(dice_pool, ballistic_skill, [dn], verbose=False)

    # integrate armour piercing modifications
    # this calculation is still imperfect
    # it doesn't include spare focus that could be used to pierce armour
    # a future version will utilize test_full and fully optimal
    if 'Pierce Armour' in talents:
      for j in range(dice_pool+1):
        pierce_prob = np.zeros(armour+1)
        for k in range(armour+1):
          if k <= j:
            if k == armour:
              # at least full armour pierce
              pierce_prob[k] = at_least_m_of_n(k, j, 1/(6-dn+1), (6-dn)/(6-dn+1))
            else:
              # exactly k 6s in i successes
              pierce_prob[k] = exactly_m_of_n(k, j, 1/(6-dn+1), (6-dn)/(6-dn+1))
        probabilities[i,j:j+armour+1] += succ_prob[j] * pierce_prob

    else:
      probabilities[i,:dice_pool+1] += succ_prob

  # combine all ambidextrous options
  probabilities = np.average(probabilities, axis=0)

  # create damage array
  damage = np.array(range(damage_range+1)) + np.array([0] + [weapon_damage]*(damage_range))

  # compute damage applied 
  if dual_wielding:
    damage_suffered = np.maximum(damage-(armour*2), np.zeros(damage_range+1))
  else:
    damage_suffered = np.maximum(damage-armour, np.zeros(damage_range+1))

  # truncate probabilities and damage suffered to possible ranges
  probabilities = probabilities[:-ballistic_skill[1]]
  damage_suffered = damage_suffered[:-ballistic_skill[1]]

  # combine indices that deal zero damage
  probabilities = np.array([np.sum(probabilities[np.where(damage_suffered == 0)]), *probabilities[np.where(damage_suffered > 0)]])
  damage_suffered = np.array(range(probabilities.size))

  if verbose:
    print('Success likelihood: {:2.2%}'.format(np.sum(probabilities[np.where(damage_suffered > 0)])))

    print('Expected Damage: {:2.3}'.format(np.matmul(probabilities, damage_suffered)))

    plt.bar(damage_suffered, probabilities)
    plt.show()

  return probabilities



if __name__ == "__main__":

  body = 4
  ballistic_skill = [2, 1]
  accuracy = 3
  defense = 3
  talents = []
  talents = ['Pierce Armour']
  # talents = ['Ambidextrous']
  # talents = ['Gunslinger']
  # talents = ['Ambidextrous', 'Pierce Armour']
  # talents = ['Pierce Armour', 'Gunslinger']
  # talents = ['Ambidextrous', 'Gunslinger']
  # talents = ['Ambidextrous', 'Gunslinger', 'Pierce Armour']
  # dual_wielding = True
  dual_wielding = False
  weapon_damage = 1
  armour = 2


  probabilities = attack(body, ballistic_skill, accuracy, defense, talents, dual_wielding, weapon_damage, armour)
