import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

from utils import test, test_full, at_least_m_of_n, exactly_m_of_n


def attack(attribute, attack_skill, combat_ability, defense, talents, dual_wielding, weapon_damage, armour, verbose=True):

  # calculate the base dice pool size
  dice_pool_base = attribute + attack_skill[0]
  
  # calculate the base damage range
  damage_range = dice_pool_base + attack_skill[1]

  # modify weapon damage for dual wielding
  if dual_wielding:
    weapon_damage = weapon_damage * 2

  # add gunslinger bonus
  if 'Gunslinger' in talents:
    combat_ability += 1

  # add ambidextrous bonus
  if 'Ambidextrous' in talents:
    ambidextrous = 6
    damage_range += 6
  else:
    ambidextrous = 1

  if 'Pierce Armour' in talents:
    damage_range += armour

  # calculate the hit dn
  dn = 4 - min([max([combat_ability - defense, -2]), 2])
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
    succ_prob = test(dice_pool, attack_skill, [dn], verbose=False)

    # integrate armour piercing modifications
    # this calculation is still imperfect
    # it doesn't include spare focus that could be used to pierce armour
    # it also doesn't account for dice upgraded by focus to the dn
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


    # integrate armour piercing modifications
    # this calculation is still imperfect
    # it doesn't include spare focus that could be used to pierce armour
    # a future version will utilize test_full and fully optimal
    if 'Pierce Armour' in talents:
      # iterate over all possible number of successes
      for x in range(dice_pool+1):
        # iterate over all possible number of remaining foci
        for y in range(attack_skill[1]+1):
          # iterate over all possible number of foci-generated successes
          for z in range(attack_skill[1]+1):
            pierce_prob = np.zeros(armour+1)
            for a in range(armour+1):
              if a <= x:
                if a == armour:
                  # at least full armour pierce
                  pierce_prob[a] = at_least_m_of_n(a, x, 1/(6-dn+1), (6-dn)/(6-dn+1))
                else:
                  # exactly a 6s in i successes
                  pierce_prob[a] = exactly_m_of_n(a, x, 1/(6-dn+1), (6-dn)/(6-dn+1))
            probabilities[i,x:x+armour+1] += succ_prob[x] * pierce_prob

    else:
      probabilities[i,:dice_pool+1] += np.sum(probabilities, axis=(1,2))



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
  probabilities = probabilities[:-attack_skill[1]]
  damage_suffered = damage_suffered[:-attack_skill[1]]

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

  attribute = 4
  attack_skill = [2, 1]
  combat_ability = 3
  defense = 4
  talents = []
  # talents = ['Pierce Armour']
  # talents = ['Ambidextrous']
  # talents = ['Gunslinger']
  # talents = ['Ambidextrous', 'Pierce Armour']
  # talents = ['Pierce Armour', 'Gunslinger']
  talents = ['Ambidextrous', 'Gunslinger']
  # talents = ['Ambidextrous', 'Gunslinger', 'Pierce Armour']
  # dual_wielding = True
  dual_wielding = False
  weapon_damage = 1
  armour = 2


  probabilities = attack(attribute, attack_skill, combat_ability, defense, talents, dual_wielding, weapon_damage, armour)
