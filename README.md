# Soulbound

This repo is where I'm constructing a set of (mostly damage) calculators for Cubicle 7's Soulbound TTRPG. Currently, the repo is split into three files:
  * attacking_prob.py - This file implements a function that can be used to calculate attack success probability, expected damage, and damage distribution for any basic attack interaction (attack attribute, attack skill, combat ability, weapon damage, opponent defense, and opponent armour) as well as a number of combat-related talents. Please note that the function assume you meet all requirements for talents while performing calculations. This file is the most heavily under development. 
  * utils.py - This file implements shorter functions that are generally utilized by each other or by attacking_prob.py. While these are simpler, they can also be used directly. In particular, the extended_test function returns Test success probability, expected number of succeses, and success distribution. 
  * game_system.py - This functionality is still under development. If finished, this will implement a more object oriented format of attacking_prob and the Soulbound game system as a whole. This new OOP format will perform checks for Talents with requirements. It may not be valuable to finish, so I may not commit as much time to it.

## To Do

I generally implement features as they become useful to me, so these additional tasks may not be implemented in order.

  * Extended tests should be modified to accomodate the Kharadron crafting process (as implemented by my group). Since a new item can be started after the current one is finished, there is nontrivial strategy involved in how the player allocates focus during the extended Test. Codifying this strategy is complex and I no longer play a Kharadron, so it's unlikely I'll work on this soon.
  * Combat-focused Talents:
    * Backstab
    * Barazakdum, the Doom-Oath
    * Battle Rage (this one will have to be a tuple dictating how you change combat abilities)
    * Blood Frenzy (this involves consecutive attacks, and will likely take a bit of work)
    * Bulwark
    * Crushing Blow (this can use Amour Piercing code)
    * Heavy Hitter
    * Immense Strikes
    * Immense Swing
    * Martial Memories (this one will have to be a tuple dictating how you change combat abilities)
    * Mounted Combatant
    * Patient Strike
    * Relentless Assault
    * Rending Blow
    * Sever
    * Shield Mastery
    * Sigmar's Judgement
    * Star-Fated Arrow
    * The Bigger They Are
    * Underdog
  * Weapon traits:
    * Cleave
    * Defensive
    * Ineffective
    * Penetrating
    * Rend
    * Spread (this will be difficult, as it incorporates other creatures making a Body (Reflexes) Test)
  * Errata
    * Pierce Armour may be able to pierce the doubled armour from dual wielding. I'll have to discuss with my DM to get a ruling.

## Too Done

Expansions that have been implemented. If a function is more complicated than you expected, it's because I had to accomodate one of the cases below.

  * Correct calculation for the Armour Piercing Talent. The original version just checked the likelihood of piercing armour given the number of successes. The final version takes into consideration the number of successes that were generated using focus (which we know the exact die value of) and the number of remaining foci (which can be used to pierce armour further). It should be noted that the foci allocation strategy implicit in this calculation is not precisely optimal, but the cases where improvements can be made are narrow. Fail case: this calculator assumes you will always try to get as many successes as possible, even though you could deal more damage by upgrading multiple 5's to 6's instead of gaining a single more success (assuming you aren't already adequately piercing your target's armour).
  * Expanded extended tests to accomodate Witch Brew creation, which swaps attributes and skills partway through the extended Test. Users can still use extended Test the same as before.
  * Implemented extended Test. They return success probability, expected succeses, and success distribution, as usual.
  * Added the Armour Piercing Talent to attacking_prob. This initial version is imperfect and does not account for successes that have been generated by foci and remaining foci.
  * Added the Ambidextrous Talent to attacking_prob. I remain convinced that this interpretation of Ambidextrous is wrong, but it's how we use it with my party. We roll 1d6 and add that many d6's to the dice pool. Additionally, Ambidextrous can be active while the attacker is 'not dual wielding' and targeting a single opponent, meaning the attacker's weapon damage is not doubled, and neither is the opponent's armour.
  * Added the Gunslinger Talent to attacking_prob.
  * Added dual wielding to attacking_prob.