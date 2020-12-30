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


def test(attribute, skill, dn, verbose=True):

  dice_pool = attribute + skill[0]

  probabilities = np.zeros(dice_pool+skill[1]+1)
  for i in range(int(dice_pool+1)):
    # baseline probability
    base_prob = exactly_m_of_n(i, dice_pool, ((7-dn[0])/6), ((dn[0]-1)/6))
    # focus calculations
    foci_prob = np.zeros(skill[1])
    if i + 1 <= int(dice_pool):
      # 1 focus in skill
      if skill[1] == 1:
        # focus variants for gaining 1 success
        # at least 1 DN-1
        focus_1_1 = base_prob * at_least_m_of_n(1, dice_pool-i, 1/(dn[0]-1), (dn[0]-2)/(dn[0]-1))
        # redirect to appropriate success bin
        foci_prob[0] += focus_1_1

      # 2 foci in skill
      elif skill[1] == 2:
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

      # 3 foci in skill
      elif skill[1] == 3:
        # focus variants for gaining 1 success
        if dn[0] > 2:
          # exactly 1 DN-1 and exactly 0 DN-2
          focus_1_1 = base_prob * exactly_m_of_n(1, dice_pool-i, 1/(dn[0]-1), (dn[0]-2)/(dn[0]-1)) * exactly_m_of_n(0, dice_pool-i-1, 1/(dn[0]-2), (dn[0]-3)/(dn[0]-2))
          # redirect to appropriate success bin
          foci_prob[0] += focus_1_1
          # exactly 0 DN-1 and at least 1 DN-2
          focus_1_2 = base_prob * exactly_m_of_n(0, dice_pool-i, 1/(dn[0]-1), (dn[0]-2)/(dn[0]-1)) * at_least_m_of_n(1, dice_pool-i, 1/(dn[0]-2), (dn[0]-3)/(dn[0]-2))
          # redirect to appropriate success bin
          foci_prob[0] += focus_1_2
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
    succ_prob = np.append(base_prob, foci_prob)
    probabilities[i:i+skill[1]+1] += succ_prob

  if verbose:
    print('Success likelihood: {:2.2%}'.format(np.sum(probabilities[dn[1]:])))

    print('Expected successes: {:2.3}'.format(np.matmul(range(dice_pool+1), probabilities[:dice_pool+1])))
    
    plt.bar(range(dice_pool+1), probabilities[:dice_pool+1])
    plt.xlabel('Number of Successes')
    plt.ylabel('Likelihood')
    plt.show()

    # for prob in probabilities[:dice_pool+1]:
    #   print('{:2.2%}'.format(prob))

  return probabilities[:dice_pool+1]



def extended_test(attribute, skill, dn, verbose=True):
  # find success probabilities for given dn difficulty
  probs = test(attribute, skill, dn, verbose=False)

  # set dice pool size
  dice_pool = attribute + skill[0]

  probabilities = np.ones(1)

  for _ in range(3):
    probabilities = np.convolve(probabilities, probs)

  if verbose:
    print('Success likelihood: {:2.2%}'.format(np.sum(probabilities[dn[1]:])))

    print('Expected successes: {:2.3}'.format(np.matmul(range(dice_pool*3+1), probabilities)))
    
    plt.bar(range(dice_pool*3+1), probabilities)
    plt.xlabel('Number of Successes')
    plt.ylabel('Likelihood')
    plt.show()

    # for prob in probabilities:
    #   print('{:2.2%}'.format(prob))

  return probabilities[:dice_pool*3+1]



# mind = 4
# channelling = [1,2]
# dn = [5,1]

# test(mind, channelling, dn)

# channelling = [2,1]

# test(mind, channelling, dn)

# mind = 4
# medicine = [1,2]
# dn = [4,3]

# test(mind, medicine, dn)

# medicine = [2,1]

# test(mind, medicine, dn)

soul = 2
crafting = [1,1]
dn = [4,6]

extended_test(soul, crafting, dn)

crafting = [2,1]

extended_test(soul, crafting, dn)

crafting = [1,2]

extended_test(soul, crafting, dn)

crafting = [2,2]

extended_test(soul, crafting, dn)


# soul = 2
# crafting = [1,1]
# dn = [5,1]

# test(soul, crafting, dn)