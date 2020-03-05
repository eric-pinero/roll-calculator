import random
#1
#1,1
#1,2,1
#1,3,3,1
#1,4,6,4,1

def coefficient_list(row_num):
    true_row = row_num + 1
    final_row = [1]
    C = 1 # used to represent C(line, i) 
    for i in range(1, true_row): 
        C = int(C * (true_row - i) / i) 
        final_row.append(C)
    final_row.pop()
    return final_row

# Driver code 
n = 5
print(coefficient_list(n))

# This code is contributed by mits 



def d6():
    result = random.randint(1,6)
    # print(result)
    return result

def success_roll(goal, roll):
    return roll >= goal

def wound_threshold(strength, toughness):
    if strength <= toughness / 2:
        return 6
    elif strength < toughness:
        return 5
    elif strength == toughness:
        return 4
    elif strength < toughness * 2:
        return 3
    else:
        return 2

def to_hit_wound(rolls, threshold):
    count = 0
    for roll in rolls:
        if roll >= threshold:
            count += 1
    
    return count

def armor_save(rolls, save):
    count = 0
    for roll in rolls:
        if roll < save:
            count += 1
    return count

skitarii_vanguard = {
    "to_hit": 3,
    "shooting_strength": 3,
    "attacks": 3,
    "toughness": 3,
    "armor_save": 4
}

wych = {
    "toughness": 3,
    "armor_save": 6
}

neophyte_hybrid = {
    "to_hit": 4,
    "shooting_strength": 3,
    "attacks": 2,
    "toughness": 3,
    "armor_save": 5
}

def prob_algo(size, s_rate, f_rate):
    coefficients = coefficient_list(size)
    final_prob = 0
    s_rate_exp = size
    f_rate_exp = 0
    
    for coefficient in coefficients:
        success_space = s_rate ** s_rate_exp
        failure_space = f_rate ** f_rate_exp
        # print(coefficients)
        # print(str(coefficient) + " * " + str(s_rate) + " ^ " + str(s_rate_exp) + " * " + str(f_rate) + " ^ " + str(f_rate_exp))
        final_prob += coefficient * (success_space * failure_space)

        s_rate_exp -= 1
        f_rate_exp += 1
        # print(final_prob)

    return str(round(final_prob * 100 , 2) ) + "%"


def probability(attacker, defender):
    rolls = [1,2,3,4,5,6]
    attacks = attacker["attacks"]
    hit_prob = to_hit_wound(rolls, attacker["to_hit"]) / len(rolls)
    wound_prob = to_hit_wound(rolls, wound_threshold(attacker["shooting_strength"], defender["toughness"])) / len(rolls)
    save_fail_prob = armor_save(rolls, defender["armor_save"]) / len(rolls)

    success_prob = hit_prob * wound_prob * save_fail_prob
    fail_prob = 1 - success_prob

    # print(success_prob)
    # print(fail_prob)

    return "derived: " + prob_algo(attacks, success_prob, fail_prob)

print(probability(skitarii_vanguard, wych))

def simulate(attacker, defender):
    to_wound = wound_threshold(attacker["shooting_strength"], defender["toughness"])
    attacks = attacker["attacks"]

    results = {
        "hits": 0,
        "wounds": 0,
        "successes": 0,
        "percent_success": 0
    }
    for shot in range(attacks):
        if success_roll(attacker["to_hit"], d6()):
            results["hits"] += 1

    for hit in range(results["hits"]):
        if success_roll(to_wound, d6()):
            results["wounds"] += 1

    for wound in range(results["wounds"]):
        if not success_roll(defender["armor_save"], d6()):
            results["successes"] += 1

    results["percent_success"] = round(results["successes"] / attacks * 100, 2)

    return results

def sample(size, attacker, defender, simulation):
    i = 0
    successes = 0
    total = 0
    while i < size:
        sim_results = simulation(attacker, defender)

        if sim_results["successes"] > 0:
            successes += 1

        total += 1
        i += 1

    return "simulated: " + str(round(successes / total * 100, 2)) + "%"

print((sample(10000, skitarii_vanguard, wych, simulate)))



# print(simulate(skitarii_vanguard, wych))
    