import numpy as np
from scipy.special import binom
import matplotlib.pyplot as plt


def at_least_m_of_n(num_succ, num_roll, succ_prob, fail_prob):
  output = 0
  for k in range(num_succ, num_roll+1):
    output += binom(num_roll,k) * (succ_prob)**k * (fail_prob)**(num_roll-k)
  return output


def exactly_m_of_n(num_succ, num_roll, succ_prob, fail_prob):
  return binom(num_roll,num_succ) * (succ_prob)**num_succ * (fail_prob)**(num_roll-num_succ)


def craft(body, crafting, dn):

  dice_pool = body + crafting[0]

  probabilities = np.zeros(int(dice_pool+crafting[1]+1))
  for i in range(int(dice_pool+1)):
    base_prob = exactly_m_of_n(i, dice_pool, ((7-dn[0])/6), ((dn[0]-1)/6))
    foci_prob = np.zeros(crafting[1])
    # focus calculations
    if i + 1 <= int(dice_pool):
      if crafting[1] == 1:
        # focus variants for gaining 1 success
        # at least 1 DN-1
        focus_1_1 = base_prob * at_least_m_of_n(1, dice_pool-i, 1/(dn[0]-1), (dn[0]-2)/(dn[0]-1))
        # redirect to appropriate success bin
        foci_prob[0] += focus_1_1

      elif crafting[1] == 2:
        # focus variants for gaining 1 success
        # exactly 1 DN-1
        focus_1_1 = base_prob * exactly_m_of_n(1, dice_pool-i, 1/(dn[0]-1), (dn[0]-2)/(dn[0]-1))
        # redirect to appropriate success bin
        foci_prob[0] += focus_1_1
        if dn[0] > 2:
          # exactly 0 DN-1 and at least 1 DN-2
          focus_1_2 = base_prob * exactly_m_of_n(0, dice_pool-i, 1/(dn[0]-1), (dn[0]-2)/(dn[0]-1)) * at_least_m_of_n(1, dice_pool-i, 1/(dn[0]-2), (dn[0]-3)/(dn[0]-2))
          # redirect to appropriate success bin
          foci_prob[0] += focus_1_2

        # focus variants for gaining 2 success
        if i + 2 <= int(dice_pool):
          # at least 2 DN-1
          focus_2_2 = base_prob * at_least_m_of_n(2, dice_pool-i, 1/(dn[0]-1), (dn[0]-2)/(dn[0]-1))
          # redirect to appropriate success bin
          foci_prob[1] += focus_2_2

      elif crafting[1] == 3:
        # focus variants for gaining 1 success
        if dn[0] > 2:
          # exactly 1 DN-1 and exactly 0 DN-2
          focus_1_1 = base_prob * exactly_m_of_n(1, dice_pool-i, 1/(dn[0]-1), (dn[0]-2)/(dn[0]-1)) * exactly_m_of_n(0, dice_pool-i-1, 1/(dn[0]-2), (dn[0]-3)/(dn[0]-2))
          # exactly 0 DN-1 and at least 1 DN-2
          focus_1_2 = base_prob * exactly_m_of_n(0, dice_pool-i, 1/(dn[0]-1), (dn[0]-2)/(dn[0]-1)) * at_least_m_of_n(1, dice_pool-i, 1/(dn[0]-2), (dn[0]-3)/(dn[0]-2))
          # redirect to appropriate success bin
          foci_prob[0] += focus_1_1 + focus_1_2
        if dn[0] > 3:
          # exactly 0 DN-1 and exactly 0 DN-2 and at least 1 DN-3
          focus_1_3 = base_prob * exactly_m_of_n(0, dice_pool-i, 1/(dn[0]-1), (dn[0]-2)/(dn[0]-1)) * exactly_m_of_n(0, dice_pool-i, 1/(dn[0]-2), (dn[0]-3)/(dn[0]-2)) * at_least_m_of_n(1, dice_pool-i, 1/(dn[0]-3), (dn[0]-4)/(dn[0]-3))
          # redirect to appropriate success bin
          foci_prob[0] += focus_1_3

        # focus variants for gaining 2 successes
        if i + 2 <= int(dice_pool):
          # exactly 2 DN-1
          focus_2_2 = base_prob * exactly_m_of_n(2, dice_pool-i, 1/(dn[0]-1), (dn[0]-2)/(dn[0]-1))
          # redirect to appropriate success bin
          foci_prob[1] += focus_2_2
          if dn[0] > 2:
            # exactly 1 DN-1 and at least 1 DN-2
            focus_2_3 = base_prob * exactly_m_of_n(1, dice_pool-i, 1/(dn[0]-1), (dn[0]-2)/(dn[0]-1)) * at_least_m_of_n(1, dice_pool-i-1, 1/(dn[0]-2), (dn[0]-3)/(dn[0]-2))
            # redirect to appropriate success bin
            foci_prob[1] += focus_2_3

        # focus variants for gaining 3 successes
        if i + 3 <= int(dice_pool):
          # at least 3 DN-1
          focus_3_3 = base_prob * at_least_m_of_n(3, dice_pool-i, 1/(dn[0]-1), (dn[0]-2)/(dn[0]-1))
          # redirect to appropriate success bin
          foci_prob[2] += focus_3_3

    # properly assign probabilities
    base_prob -= np.sum(foci_prob)
    # print(base_prob)
    succ_prob = np.append(base_prob, foci_prob)
    # print(succ_prob)
    probabilities[i:i+crafting[1]+1] += succ_prob

  if dn[1] <= dice_pool:
    print('Completion likelihood:', np.sum(probabilities[dn[1]:]))

  print('Expected successes:', np.matmul(range(dice_pool+1), probabilities[:-crafting[-1]]))
  
  # plt.bar(range(dice_pool+1), probabilities[:-crafting[1]])
  # plt.show()

  return probabilities[:-crafting[1]]





body = 4
crafting = [2, 1]
dn = [5, 3]

probs = craft(body, crafting, dn)