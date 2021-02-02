import numpy as np
import matplotlib.pyplot as plt

from utils import test_full, at_least_m_of_n, exactly_m_of_n

ABILITY_LEVELS = ['Extraordinary', 'Superb', 'Great', 'Good', 'Average', 'Poor']


def six_prob_calculation(succ_prob, dn, damage_range):
  # create new variable to return
  probabilities = np.zeros((damage_range+1, damage_range+1))
  # iterate over all possible number of successes
  for x in range(succ_prob.shape[0]):
    # iterate over all possible number of remaining foci
    for y in range(succ_prob.shape[1]):
      # iterate over all possible number of foci-generated successes
      for z in range(succ_prob.shape[2]):
        # skip impossible cases
        if succ_prob[x,y,z] > 0:
          six_prob = 0
          for j in range(x-z+1):
            # exactly j pierce of x-z dice
            base_prob = exactly_m_of_n(j, x-z, 1/(7-dn), (6-dn)/(7-dn), known_succ=z*int(6 == dn))
            # track total pierce prob
            six_prob += base_prob
            # focus calculations
            if  j + z + 1 <= x and dn < 6 and y > 0:
              foci_prob = np.zeros(y)
              if y == 1:
                # focus variants for gaining 1 success
                # at least 1 DN-1
                foci_prob[0] += at_least_m_of_n(1, x-j-z, 1/(6-dn), (5-dn)/(6-dn), known_succ=z*int(5 == dn))

              elif y == 2:
                # focus variants for gaining 1 success
                # exactly 1 DN-1
                foci_prob[0] += exactly_m_of_n(1, x-j-z, 1/(6-dn), (5-dn)/(6-dn), known_succ=z*int(5 == dn))
                if dn < 5:
                  # exactly 0 DN-1 and at least 1 DN-2
                  foci_prob[0] += exactly_m_of_n(0, x-j-z, 1/(6-dn), (5-dn)/(6-dn), known_succ=z*int(5 == dn)) * at_least_m_of_n(1, x-j-z, 1/(5-dn), (4-dn)/(5-dn), known_succ=z*int(4 == dn))

                # focus variants for gaining 2 success
                if j + z + 2 <= x:
                  # at least 2 DN-1
                  foci_prob[1] += at_least_m_of_n(2, x-j-z, 1/(6-dn), (5-dn)/(6-dn), known_succ=z*int(5 == dn))

              elif y == 3:
                # focus variants for gaining 1 success
                if dn < 5:
                  # exactly 1 DN-1 and exactly 0 DN-2
                  foci_prob[0] += exactly_m_of_n(1, x-j-z, 1/(6-dn), (5-dn)/(6-dn), known_succ=z*int(5 == dn)) * exactly_m_of_n(0, x-j-z-1, 1/(5-dn), (4-dn)/(5-dn), known_succ=z*int(4 == dn))
                  # exactly 0 DN-1 and at least 1 DN-2
                  foci_prob[0] += exactly_m_of_n(0, x-j-z, 1/(6-dn), (5-dn)/(6-dn), known_succ=z*int(5 == dn)) * at_least_m_of_n(1, x-j-z, 1/(5-dn), (4-dn)/(5-dn), known_succ=z*int(4 == dn))
                if dn < 4:
                  # exactly 0 DN-1 and exactly 0 DN-2 and at least 1 DN-3
                  foci_prob[0] += exactly_m_of_n(0, x-j-z, 1/(6-dn), (5-dn)/(6-dn), known_succ=z*int(5 == dn)) * exactly_m_of_n(0, x-j-z, 1/(5-dn), (4-dn)/(5-dn), known_succ=z*int(4 == dn)) * at_least_m_of_n(1, x-j-z, 1/(4-dn), (3-dn)/(4-dn), known_succ=z*int(3 == dn))

                # focus variants for gaining 2 successes
                if j + z + 2 <= x:
                  # exactly 2 DN-1
                  foci_prob[1] += exactly_m_of_n(2, x-j-z, 1/(6-dn), (5-dn)/(6-dn), known_succ=z*int(5 == dn))
                  if dn < 5:
                    # exactly 1 DN-1 and at least 1 DN-2
                    foci_prob[1] += exactly_m_of_n(1, x-j-z, 1/(6-dn), (5-dn)/(6-dn), known_succ=z*int(5 == dn)) * at_least_m_of_n(1, x-j-z-1, 1/(5-dn), (4-dn)/(5-dn), known_succ=z*int(4 == dn))

                # focus variants for gaining 3 successes
                if j + z + 3 <= x:
                  # at least 3 DN-1
                  foci_prob[2] += at_least_m_of_n(3, x-j-z, 1/(6-dn), (5-dn)/(6-dn), known_succ=z*int(5 == dn))

              # store original probability for double checking
              orig_base = base_prob

              # compound probabilities
              foci_prob = base_prob * foci_prob
              # remove new cases from base probability
              base_prob -= np.sum(foci_prob)
              # combine all success probabilities
              probs = np.concatenate(([base_prob], foci_prob))

              # guarantee calculations aren't completely incorrect
              assert(abs(np.sum(probs) - orig_base) < 0.01)

              # iterate over all computed probabilities
              for k, prob in enumerate(probs):
                # assign probability to correct success slot and compound with success probability
                probabilities[j+k, x] += succ_prob[x,y,z] * prob

            # no focus calculations
            else: 
              # assign probability to correct success slot and compound with success probability
              probabilities[j, x] += succ_prob[x,y,z] * base_prob
          
          # current success probability cannot pierce for different values
          if six_prob == 0:
            # assign probability to correct success slot and compound with success probability                
            probabilities[0, x] += succ_prob[x,y,z]
            # probabilities[x, 0] += succ_prob[x,y,z]

  return probabilities


def attack(attribute, attack_skill, combat_ability, defense, talents, dual_wielding, weapon_damage, weapon_traits, armour, verbose=True):

  # partial backstab implementation
  if 'Backstab' in talents:
    armour = 0

  # full gunslinger implementation
  if 'Gunslinger' in talents:
    # combat ability starts at 0 (Poor)
    combat_ability = min(combat_ability+1, 5)

  # full heavy hitter implementation
  if 'Heavy Hitter' in talents:
    if 'Ineffective' in weapon_traits:
      weapon_traits.remove('Ineffective')
    weapon_damage = 1

  # full immense strikes implementation
  if 'Immense Strikes' in talents:
    weapon_damage += 1

  # full immense swing implementation
  if 'Immense Swing' in talents:
    if 'Cleave' not in weapon_traits:
      weapon_traits.append('Cleave')

  # full martial memories implementation
  if 'Martial Memories' in talents:
    # combat ability starts at 0 (Poor)
    combat_ability = min(combat_ability+1, 5)

  # full mounted combatant implementation
  if 'Mounted Combatant' in talents:
    # combat ability starts at 0 (Poor)
    combat_ability = min(combat_ability+1, 5)

  # full patient strike implementation
  if 'Patient Strike' in talents:
    # combat ability starts at 0 (Poor)
    combat_ability = min(combat_ability+1, 5)

  # full relentless assault implementation
  if 'Relentless Assault' in talents:
    # combat ability starts at 0 (Poor)
    combat_ability = min(combat_ability+1, 5)

  # full sigmar's judgement implementation
  if 'Sigmar\'s Judgement' in talents:
    # combat ability starts at 0 (Poor)
    combat_ability = min(combat_ability+1, 5)

  # full star-fated arrow implementation
  if 'Star-Fated Arrow' in talents:
    armour = 0

  # full the bigger they are implementation
  if 'The Bigger They Are' in talents:
    # combat ability starts at 0 (Poor)
    combat_ability = min(combat_ability+1, 5)

  # full underdog implementation
  if 'Underdog' in talents:
    # combat ability starts at 0 (Poor)
    combat_ability = min(combat_ability+1, 5)

  # full ineffective implementation
  if 'Ineffective' in weapon_traits:
    armour = armour * 2

  # full penetrating implementation
  if 'Penetrating' in weapon_traits:
    armour = max(0, armour-1)

  # calculate the base dice pool size
  dice_pool_base = attribute + attack_skill[0]
  
  # calculate the base damage range
  damage_range = dice_pool_base + attack_skill[1]

  # modify weapon damage for dual wielding
  if dual_wielding:
    weapon_damage = weapon_damage * 2

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
  print('DN:', dn)

  # initialize full attack probabilities
  probabilities = np.zeros((ambidextrous, damage_range+1, damage_range+1))
  # iterate over ambidextrous options
  # this method is overly brute force, but a better method would make my head hurt
  for i in range(ambidextrous):
    # modify dice pool if ambidextrous is active
    if 'Ambidextrous' in talents:
      dice_pool = dice_pool_base + i + 1
    else:
      dice_pool = dice_pool_base

    # compute hit likelihoods
    succ_prob = test_full(dice_pool, attack_skill, [dn], verbose=False)
    succ_prob = six_prob_calculation(succ_prob, dn, damage_range)
    assert(abs(np.sum(succ_prob) - 1.0) < 0.01)

    # integrate armour piercing modifications
    if 'Pierce Armour' in talents:
      for num_six, probs in enumerate(succ_prob):
        if min(num_six,armour) > 0:
          probabilities[i,min(num_six,armour):,num_six] += probs[:-min(num_six,armour)]
          probabilities[i,-1,num_six] += np.sum(probs[-min(num_six,armour):])
        else:
          probabilities[i,:,num_six] = probs
    else:
      probabilities[i,:,:] = np.swapaxes(succ_prob, 0, 1)

    assert(abs((np.sum(probabilities[i,:]) - 1.0)) < 0.01)

  # combine all ambidextrous options
  probs = np.average(probabilities, axis=0)
  probabilities = np.sum(probs, axis=-1)

  # create damage array
  damage = np.array(range(damage_range+1)) + np.array([0] + [weapon_damage]*(damage_range))

  # full barazakdum, the doom-oath implementation
  if 'Barazakdum, the Doom-Oath' in talents:
    damage = damage * 2

  # partial backstab implementation
  if 'Backstab' in talents:
    damage = damage * 2

  # compute damage applied
  if dual_wielding:
    damage_suffered = np.maximum(damage-(armour*2), np.zeros(damage_range+1))
  else:
    damage_suffered = np.maximum(damage-armour, np.zeros(damage_range+1))

  if attack_skill[1] > 0:
    # truncate probabilities and damage suffered to possible ranges
    probabilities = probabilities[:-attack_skill[1]]
    damage_suffered = damage_suffered[:-attack_skill[1]]

  # combine indices that deal zero damage
  probabilities = np.array([np.sum(probabilities[np.where(damage_suffered == 0)]), *probabilities[np.where(damage_suffered > 0)]])
  damage_suffered = np.array([0, *damage_suffered[np.where(damage_suffered > 0)]])

  results = []

  results.append(['Success Likelihood: {:2.2%}'.format(np.sum(probabilities[np.where(damage_suffered > 0)])),
                  'Expected Damage: {:2.3}'.format(np.matmul(probabilities, damage_suffered)),
                  damage_suffered,
                  probabilities,
                  'Damage Distribution',
                  'Damage',
                  'Likelihood'])

  if 'Cleave' in weapon_traits:
    results.append(['Cleave Likelihood: {:2.2%}'.format(np.sum(probs[:,1:])),
                    'Expected Cleave Damage: {:2.3}'.format(np.matmul(np.sum(probs,axis=0), range(probs.shape[-1]))),
                    range(probs.shape[-1]),
                    np.sum(probs,axis=0),
                    'Cleave Distribution',
                    'Cleave Damage',
                    'Likelihood'])

  if 'Crushing Blow' in talents:
    results.append(['Crushing Blow Likelihood: {:2.2%}'.format(np.sum(probs[:,1:])),
                    '',
                    ['Failure', 'Success'],
                    [np.sum(probs[:,0]), np.sum(probs[:,1:])],
                    'Crushing Blow Distribution',
                    '',
                    'Likelihood'])

  if 'Rend' in weapon_traits:
    results.append(['Rend Likelihood: {:2.2%}'.format(np.sum(probs[:,1:])),
                    'Expected Armour Damage: {:2.3}'.format(np.matmul(np.sum(probs,axis=0), range(probs.shape[-1]))),
                    range(probs.shape[-1]),
                    np.sum(probs,axis=0),
                    'Rend Distribution',
                    'Armour Rended',
                    'Likelihood'])

  if 'Sever' in talents:
    results.append(['Sever Likelihood: {:2.2%}'.format(np.sum(probs[:,1:])),
                    '',
                    ['Failure', 'Success'],
                    [np.sum(probs[:,0]), np.sum(probs[:,1:])],
                    'Sever Distribution',
                    '',
                    'Likelihood'])

  if verbose:
    print('Success likelihood: {:2.2%}'.format(np.sum(probabilities[np.where(damage_suffered > 0)])))

    print('Expected Damage: {:2.3}'.format(np.matmul(probabilities, damage_suffered)))

    plt.bar(damage_suffered, probabilities)
    plt.title('Damage Distribution')
    plt.xlabel('Damage')
    plt.ylabel('Likelihood')
    plt.show()

    if 'Cleave' in weapon_traits:
      print('Cleave likelihood: {:2.2%}'.format(np.sum(probs[:,1:])))

      print('Expected Cleave Damage: {:2.3}'.format(np.matmul(np.sum(probs,axis=0), range(probs.shape[-1]))))

      plt.bar(range(probs.shape[-1]), np.sum(probs,axis=0))
      plt.title('Cleave Distribution')
      plt.xlabel('Cleave Damage')
      plt.ylabel('Likelihood')
      plt.show()

    if 'Crushing Blow' in talents:
      print('Crushing Blow likelihood: {:2.2%}'.format(np.sum(probs[:,1:])))

      plt.bar(['Failure', 'Success'], [np.sum(probs[:,0]), np.sum(probs[:,1:])])
      plt.title('Crushing Blow Distribution')
      plt.ylabel('Likelihood')
      plt.show()

    if 'Rend' in weapon_traits:
      print('Rend likelihood: {:2.2%}'.format(np.sum(probs[:,1:])))

      print('Expected Armour Destroyed: {:2.3}'.format(np.matmul(np.sum(probs,axis=0), range(probs.shape[-1]))))

      plt.bar(range(probs.shape[-1]), np.sum(probs,axis=0))
      plt.title('Rend Distribution')
      plt.xlabel('Armour Rended')
      plt.ylabel('Likelihood')
      plt.show()

    if 'Sever' in talents:
      print('Sever likelihood: {:2.2%}'.format(np.sum(probs[:,1:])))

      plt.bar(['Failure', 'Success'], [np.sum(probs[:,0]), np.sum(probs[:,1:])])
      plt.title('Sever Distribution')
      plt.ylabel('Likelihood')
      plt.show()


  return results




if __name__ == "__main__":

  attribute = 2
  attack_skill = [2, 2]
  combat_ability = 4
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
  weapon_damage = 2
  weapon_traits = []
  weapon_traits = ['Penetrating', 'Cleave']
  weapon_traits = ['Cleave']
  # weapon_traits = ['Rend']
  # weapon_traits = ['Cleave', 'Ineffective', 'Penetrating', 'Rend', 'Spread']
  armour = 2


  probabilities = attack(attribute, attack_skill, combat_ability, defense, talents, dual_wielding, weapon_damage, weapon_traits, armour)
