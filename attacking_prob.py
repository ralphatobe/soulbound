import numpy as np
from scipy.special import binom
import matplotlib.pyplot as plt
from collections import Counter


def at_least_m_of_n(num_succ, num_roll, succ_prob, fail_prob):
  output = 0
  for k in range(num_succ, num_roll+1):
    output += binom(num_roll,k) * (succ_prob)**k * (fail_prob)**(num_roll-k)
  return output


def exactly_m_of_n(num_succ, num_roll, succ_prob, fail_prob):
  return binom(num_roll,num_succ) * (succ_prob)**num_succ * (fail_prob)**(num_roll-num_succ)


def recurse(total, current):
  combos = []
  for j in range(current[-1], total+1):
    if total - (sum(current)+j) >= 0:
      combos.append(current+[j])
      new = recurse(total, current+[j])
      combos.extend(new)
  return combos


def attack(body, ballistic_skill, accuracy, defense, talents, dual_wielding, weapon_damage, armour):
  # and you have a ranged weapon in each hand
  if 'Gunslinger' in talents:
    accuracy += 1

  dn = 4 - min([max([accuracy - defense, -2]), 2])
  print('DN:', dn)

  dice_pool_base = body + ballistic_skill[0]
  
  damage_range = dice_pool_base + ballistic_skill[1]

  if dual_wielding:
    weapon_damage = weapon_damage * 2

  if 'Ambidextrous' in talents:
    ambidextrous = 6
    damage_range += 6
  else:
    ambidextrous = 1

  print('base dice:', dice_pool_base)

  if 'Pierce Armour' in talents:
    damage_range += armour

  probabilities = np.zeros((ambidextrous, damage_range+1))
  print(probabilities.shape)
  for i in range(ambidextrous):
    if 'Ambidextrous' in talents:
      dice_pool = dice_pool_base + i + 1
    else:
      dice_pool = dice_pool_base

    for j in range(dice_pool+1):
      # print(j, 'successes')
      base_prob = exactly_m_of_n(j, dice_pool, ((7-dn)/6), ((dn-1)/6))
      

      foci_prob = np.zeros(ballistic_skill[1])

      combos = []
      for k in range(1,ballistic_skill[1]+1):
        combos.append([k])
        sets = recurse(ballistic_skill[1], [k])
        combos.extend(sets)

      print(combos)

      for combo in combos:
        print(j, dice_pool, dn, combo)
        if j + len(combo) <= dice_pool:
          prob = 1
          count = Counter(combo)
          # values below the max are always fixed
          for k in range(1,max(combo)):
            if dn > k:
              prob *= exactly_m_of_n(count[k], dice_pool-j, 1/(dn-k), (dn-(k+1))/(dn-k))

          # remaining foci cannot be used
          for k in range(max(combo), ballistic_skill[1]-sum(combo)+1):
            print(k)
            if dn > k:
              prob *= exactly_m_of_n(0, dice_pool-j-sum(combo), 1/(dn-k), (dn-(k+1))/(dn-k))



          # max value is only fixed if enough foci are available to add another max value
          if dn > max(combo):
            if sum(combo) + max(combo) > ballistic_skill[1]:
              # prob *= base_prob * at_least_m_of_n(count[max(combo)], dice_pool-j, 1/(dn-max(combo)), (dn-(max(combo)+1))/(dn-max(combo)))
              prob *= at_least_m_of_n(count[max(combo)], dice_pool-j, 1/(dn-max(combo)), (dn-(max(combo)+1))/(dn-max(combo)))
            else:
              # prob *= base_prob * exactly_m_of_n(count[max(combo)], dice_pool-j, 1/(dn-max(combo)), (dn-(max(combo)+1))/(dn-max(combo)))
              prob *= exactly_m_of_n(count[max(combo)], dice_pool-j, 1/(dn-max(combo)), (dn-(max(combo)+1))/(dn-max(combo)))

          print('auto prob', len(combo)-1, prob)
          # foci_prob[len(combo)-1] += prob

      # focus calculations
      if j + 1 <= dice_pool:
        if ballistic_skill[1] == 1:
          # focus variants for gaining 1 success
          # at least 1 DN-1
          focus_1_1 = base_prob * at_least_m_of_n(1, dice_pool-j, 1/(dn-1), (dn-2)/(dn-1))
          # redirect to appropriate success bin
          print('foci prob', 0, focus_1_1)
          foci_prob[0] += focus_1_1

        elif ballistic_skill[1] == 2:
          # focus variants for gaining 1 success
          # exactly 1 DN-1
          focus_1_1 = base_prob * exactly_m_of_n(1, dice_pool-j, 1/(dn-1), (dn-2)/(dn-1))
          # redirect to appropriate success bin
          print('foci prob', 0, focus_1_1)
          foci_prob[0] += focus_1_1
          if dn > 2:
            # exactly 0 DN-1 and at least 1 DN-2
            focus_1_2 = base_prob * exactly_m_of_n(0, dice_pool-j, 1/(dn-1), (dn-2)/(dn-1)) * at_least_m_of_n(1, dice_pool-j, 1/(dn-2), (dn-3)/(dn-2))
            # redirect to appropriate success bin
            print('foci prob', 0, focus_1_2)
            foci_prob[0] += focus_1_2

          # focus variants for gaining 2 success
          if j + 2 <= dice_pool:
            # at least 2 DN-1
            focus_2_2 = base_prob * at_least_m_of_n(2, dice_pool-j, 1/(dn-1), (dn-2)/(dn-1))
            # redirect to appropriate success bin
            print('foci prob', 1, focus_2_2)
            foci_prob[1] += focus_2_2

        elif ballistic_skill[1] == 3:
          # focus variants for gaining 1 success
          if dn > 2:
            # exactly 1 DN-1 and exactly 0 DN-2
            focus_1_1 = base_prob * exactly_m_of_n(1, dice_pool-j, 1/(dn-1), (dn-2)/(dn-1)) * exactly_m_of_n(0, dice_pool-j-1, 1/(dn-2), (dn-3)/(dn-2))
            # exactly 0 DN-1 and at least 1 DN-2
            focus_1_2 = base_prob * exactly_m_of_n(0, dice_pool-j, 1/(dn-1), (dn-2)/(dn-1)) * at_least_m_of_n(1, dice_pool-j, 1/(dn-2), (dn-3)/(dn-2))
            # redirect to appropriate success bin
            print('foci prob', 0, focus_1_1)
            print('foci prob', 0, focus_1_2)
            foci_prob[0] += focus_1_1 + focus_1_2
          if dn > 3:
            # exactly 0 DN-1 and exactly 0 DN-2 and at least 1 DN-3
            focus_1_3 = base_prob * exactly_m_of_n(0, dice_pool-j, 1/(dn-1), (dn-2)/(dn-1)) * exactly_m_of_n(0, dice_pool-j, 1/(dn-2), (dn-3)/(dn-2)) * at_least_m_of_n(1, dice_pool-j, 1/(dn-3), (dn-4)/(dn-3))
            # redirect to appropriate success bin
            print('foci prob', 0, focus_1_3)
            foci_prob[0] += focus_1_3

          # focus variants for gaining 2 successes
          if j + 2 <= dice_pool:
            # exactly 2 DN-1
            focus_2_2 = base_prob * exactly_m_of_n(2, dice_pool-j, 1/(dn-1), (dn-2)/(dn-1))
            # redirect to appropriate success bin
            print('foci prob', 1, focus_2_2)
            foci_prob[1] += focus_2_2
            if dn > 2:
              # exactly 1 DN-1 and at least 1 DN-2
              focus_2_3 = base_prob * exactly_m_of_n(1, dice_pool-j, 1/(dn-1), (dn-2)/(dn-1)) * at_least_m_of_n(1, dice_pool-j-1, 1/(dn-2), (dn-3)/(dn-2))
              # redirect to appropriate success bin
              print('foci prob', 1, focus_2_3)
              foci_prob[1] += focus_2_3

          # focus variants for gaining 3 successes
          if j + 3 <= dice_pool:
            # at least 3 DN-1
            focus_3_3 = base_prob * at_least_m_of_n(3, dice_pool-j, 1/(dn-1), (dn-2)/(dn-1))
            # redirect to appropriate success bin
            print('foci prob', 2, focus_3_3)
            foci_prob[2] += focus_3_3


      base_prob -= np.sum(foci_prob)
      succ_prob = np.append(base_prob, foci_prob)

      if 'Pierce Armour' in talents:
        pierce_prob = np.zeros(armour+1)
        for k in range(armour+1):
          if k <= j:
            if k == armour:
              # at least full armour pierce
              pierce_prob[k] = at_least_m_of_n(k, j, 1/(6-dn+1), (6-dn)/(6-dn+1))
            else:
              # exactly k 6s
              pierce_prob[k] = exactly_m_of_n(k, j, 1/(6-dn+1), (6-dn)/(6-dn+1))

        pierce_table = np.matmul(np.expand_dims(pierce_prob, 1), np.expand_dims(succ_prob, 0))

        for pierce, probs in enumerate(pierce_table):
          probabilities[i][j+pierce:j+pierce+ballistic_skill[1]+1] += probs 

      else:
        probabilities[i][j:j+ballistic_skill[1]+1] += succ_prob

  probabilities = np.average(probabilities, axis=0)

  damage = np.array(range(damage_range+1)) + np.array([0] + [weapon_damage]*(damage_range))

  if dual_wielding:
    damage_suffered = np.maximum(damage-(armour*2), np.zeros(damage_range+1))
  else:
    damage_suffered = np.maximum(damage-armour, np.zeros(damage_range+1))

  probabilities = probabilities[:-ballistic_skill[1]]
  damage_suffered = damage_suffered[:-ballistic_skill[1]]

  print('Expected Damage:', np.matmul(probabilities, damage_suffered))

  # plt.bar(damage_suffered, probabilities)
  # plt.show()



body = 4
ballistic_skill = [2, 1]
accuracy = 3
defense = 3
talents = []
# talents = ['Pierce Armour']
talents = ['Ambidextrous']
# talents = ['Gunslinger']
# talents = ['Ambidextrous', 'Pierce Armour']
# talents = ['Pierce Armour', 'Gunslinger']
# talents = ['Ambidextrous', 'Gunslinger']
# talents = ['Ambidextrous', 'Gunslinger', 'Pierce Armour']
dual_wielding = True
# dual_wielding = False
weapon_damage = 1
armour = 1

attack(body, ballistic_skill, accuracy, defense, talents, dual_wielding, weapon_damage, armour)