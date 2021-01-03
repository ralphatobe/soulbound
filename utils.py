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


def test_full(dice_pool, skill, dn, verbose=True):

  probabilities = np.zeros((int(dice_pool+skill[1]+1), skill[1]+1))
  for i in range(int(dice_pool+1)):
    base_prob = exactly_m_of_n(i, dice_pool, ((7-dn[0])/6), ((dn[0]-1)/6))
    foci_prob = np.zeros((skill[1], skill[1]))
    # focus calculations
    if i + 1 <= int(dice_pool):
      if skill[1] == 1:
        # focus variants for gaining 1 success
        # at least 1 DN-1
        focus_1_1 = base_prob * at_least_m_of_n(1, dice_pool-i, 1/(dn[0]-1), (dn[0]-2)/(dn[0]-1))
        # redirect to appropriate success bin
        foci_prob[0,0] += focus_1_1

      elif skill[1] == 2:
        # focus variants for gaining 1 success
        # exactly 1 DN-1
        focus_1_1 = base_prob * exactly_m_of_n(1, dice_pool-i, 1/(dn[0]-1), (dn[0]-2)/(dn[0]-1))
        # redirect to appropriate success bin
        foci_prob[0,0] += focus_1_1
        if dn[0] > 2:
          # exactly 0 DN-1 and at least 1 DN-2
          focus_1_2 = base_prob * exactly_m_of_n(0, dice_pool-i, 1/(dn[0]-1), (dn[0]-2)/(dn[0]-1)) * at_least_m_of_n(1, dice_pool-i, 1/(dn[0]-2), (dn[0]-3)/(dn[0]-2))
          # redirect to appropriate success bin
          foci_prob[0,1] += focus_1_2

        # focus variants for gaining 2 success
        if i + 2 <= int(dice_pool):
          # at least 2 DN-1
          focus_2_2 = base_prob * at_least_m_of_n(2, dice_pool-i, 1/(dn[0]-1), (dn[0]-2)/(dn[0]-1))
          # redirect to appropriate success bin
          foci_prob[1,1] += focus_2_2

      elif skill[1] == 3:
        # focus variants for gaining 1 success
        if dn[0] > 2:
          # exactly 1 DN-1 and exactly 0 DN-2
          focus_1_1 = base_prob * exactly_m_of_n(1, dice_pool-i, 1/(dn[0]-1), (dn[0]-2)/(dn[0]-1)) * exactly_m_of_n(0, dice_pool-i-1, 1/(dn[0]-2), (dn[0]-3)/(dn[0]-2))
          # redirect to appropriate success bin
          foci_prob[0,0] += focus_1_1
          # exactly 0 DN-1 and at least 1 DN-2
          focus_1_2 = base_prob * exactly_m_of_n(0, dice_pool-i, 1/(dn[0]-1), (dn[0]-2)/(dn[0]-1)) * at_least_m_of_n(1, dice_pool-i, 1/(dn[0]-2), (dn[0]-3)/(dn[0]-2))
          # redirect to appropriate success bin
          foci_prob[0,1] += focus_1_2
        if dn[0] > 3:
          # exactly 0 DN-1 and exactly 0 DN-2 and at least 1 DN-3
          focus_1_3 = base_prob * exactly_m_of_n(0, dice_pool-i, 1/(dn[0]-1), (dn[0]-2)/(dn[0]-1)) * exactly_m_of_n(0, dice_pool-i, 1/(dn[0]-2), (dn[0]-3)/(dn[0]-2)) * at_least_m_of_n(1, dice_pool-i, 1/(dn[0]-3), (dn[0]-4)/(dn[0]-3))
          # redirect to appropriate success bin
          foci_prob[0,2] += focus_1_3

        # focus variants for gaining 2 successes
        if i + 2 <= int(dice_pool):
          # exactly 2 DN-1
          focus_2_2 = base_prob * exactly_m_of_n(2, dice_pool-i, 1/(dn[0]-1), (dn[0]-2)/(dn[0]-1))
          # redirect to appropriate success bin
          foci_prob[1,1] += focus_2_2
          if dn[0] > 2:
            # exactly 1 DN-1 and at least 1 DN-2
            focus_2_3 = base_prob * exactly_m_of_n(1, dice_pool-i, 1/(dn[0]-1), (dn[0]-2)/(dn[0]-1)) * at_least_m_of_n(1, dice_pool-i-1, 1/(dn[0]-2), (dn[0]-3)/(dn[0]-2))
            # redirect to appropriate success bin
            foci_prob[1,2] += focus_2_3

        # focus variants for gaining 3 successes
        if i + 3 <= int(dice_pool):
          # at least 3 DN-1
          focus_3_3 = base_prob * at_least_m_of_n(3, dice_pool-i, 1/(dn[0]-1), (dn[0]-2)/(dn[0]-1))
          # redirect to appropriate success bin
          foci_prob[2,2] += focus_3_3

    # properly assign probabilities
    base_prob -= np.sum(foci_prob)
    # track probabilities and foci count
    probabilities[i,0] += base_prob
    probabilities[i+1:i+skill[1]+1,1:] += foci_prob
    
  if verbose:
    print('Success likelihood: {:2.2%}'.format(np.sum(probabilities[dn[1]:,:])))

    print('Expected successes: {:2.3}'.format(np.matmul(range(dice_pool+1), np.sum(probabilities[:dice_pool+1], axis=1))))
    
    plt.bar(range(dice_pool+1), np.sum(probabilities[:dice_pool+1], axis=1))
    plt.xlabel('Number of Successes')
    plt.ylabel('Likelihood')
    plt.show()

    # for prob in probabilities[:dice_pool+1]:
    #   print('{:2.2%}'.format(prob))

  return probabilities[:-skill[1],:]


def test(dice_pool, skill, dn, verbose=True):

  probabilities = test_full(dice_pool, skill, dn, verbose=verbose)

  probabilities = np.sum(probabilities, axis=1)

  return probabilities


def extended_test(dice_pool, skill, dn, verbose=True):
  # find success probabilities for given dn difficulty
  probs = test(dice_pool, skill, dn, verbose=False)

  # compute probabilities across three tests
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



if __name__ == "__main__":

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

  # soul = 2
  # dn = [4,6]

  # skill = [1,1]
  # extended_test(soul, skill, dn)

  # skill = [2,1]
  # extended_test(soul, skill, dn)

  # skill = [1,2]
  # extended_test(soul, skill, dn)

  # skill = [2,2]
  # extended_test(soul, skill, dn)

  # skill = [3,2]
  # extended_test(soul, skill, dn)


  soul = 2
  skill = [2,2]
  dn = [5,1]

  test(soul+skill[0], skill, dn)