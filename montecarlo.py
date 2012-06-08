#    montecarlo.py - Using the MonteCarlo method in problem solving.
#    Copyright (C) 2011 Sakis Kasampalis <faif at dtek period gr> 

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import random, math, datetime

# pi problem parameters
N_POINTS = 1000                 # increase it to get a better pi approximation

# factory problem parameters
P_LEN = 28                      # total items/production
F_LEN = 9                       # maximum number of faulty chips/production
P_FAULTS = 5                    # faulty orders indicating a bad production
N_PRODUCTIONS = 200             # increase it to see how the probability of getting
                                # bad productions increases as the number of total 
                                # productions increases

# Approximates the mathematical pi number, by approximating
# the area of a circle with center (1/2, 1/2) and radius
# 1/2, using n points.
#
# @param n the total number of random points to use
# @return the pi approximation as a floating point number
def calc_pi(n):
    assert(n > 0)
    good = 0                    # indicates a good case
    for _ in range(n):
        x = random.random()     # [0.0 - 1.0)
        y = random.random()
        num1 = math.pow(x - 0.5, 2) # (x - 1/2) ^ 2
        num2 = math.pow(y - 0.5, 2)
        # compare the sum with 1/2 ^ 2
        if num1 + num2 <= math.pow(0.5, 2):
            good += 1
    # pi = 4 * area of circle
    return 4 * (good / float(n))


# Calculates the probability of finding f orders of faulty
# chips produced in a factory. There are t chips produced
# in each production.
#
# @param f the number of faulty orders to search for
# @param t the number of total chips per order
# @param c the number of faulty chips per production
# @param n how many productions to generate
# @return the probability of getting f faulty orders as
# a floating point number
def elect_chips(f, t, c, n):
    assert(f > 0 and t > 0 and c > 0 and n > 0)
    bad = 0                    # indicates a bad case
    for _ in range(n):
        r = list()
        # generate a random production with c faulty chips
        while not count_production_faults(r, c):
            r = gen_rnd_production(t)
        # check if the production is faulty
        if f == faulty_orders(r):
            bad += 1
    return bad / float(n)


# Generates a random production.
#
# @param n the number of total chips/production
# @return the random production as a list
def gen_rnd_production(n):
    return rnd_bool_list(n)


# Counts the faulty chips found in a production.
#
# @param r the production (list) to use while searching for faulty chips
# @return True if the faulty chips are equal to c; False otherwise
def count_production_faults(r, c):
    return count_true_vals(r) == c


# Counts the number of True items found in a boolean 
# container
#
# @param c the container (list/tuple, etc.)
# @return the number of True items as an integer
def count_true_vals(c):
    i = 0
    for it in c:
        if it:
            i += 1
    return i


# Organizes the given container as pairs.
#
# @param c the container (list/tuple, etc.)
# @return the two items forming a pair in the container
def pairs(c):
    for i in range(1, len(c)):
        yield c[i-1], c[i]
    yield c[-1], c[0]


# Counts the faulty orders in a
#
# @param c the container (list/tuple, etc.)
# @return the number of unmatched pairs as an integer
def faulty_orders(c):
    i = 0
    for x1, x2 in pairs(c):
        # faulty order when the first item is True
        # and the second False
        if x1 and not x2:
            i += 1
    return i


# Generates a random boolean list.
#
# @param list_len the length of the list
# @return a list with random True/False values
def rnd_bool_list(list_len):
    c = list()
    [c.append(random.choice([True, False])) for _ in range(list_len)]
    return c

# pi approximation
pi = calc_pi(N_POINTS)
print('pi approximation using', N_POINTS, 'points:', pi)

# factory production problem
fe = elect_chips(P_FAULTS, P_LEN, F_LEN, N_PRODUCTIONS)
print('probability of getting', P_FAULTS, 'faulty orders in', N_PRODUCTIONS, 'productions:', fe)
