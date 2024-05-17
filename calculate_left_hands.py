# -*- coding: utf-8 -*-
# @Time : 2024/5/14 19:20
# @Author : CallMeCore
# @File : calculate_left_hands.py
# @Github : https://github.com/CallMeCore/
# libCaculateLeftHands.so from https://github.com/Netease-Games-AI-Lab-Guangzhou/PerfectDou

from ctypes import cdll, c_int
from collections import Counter
import getopt
import sys
import ast

RealCard2EnvCard = {'3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12,
                    'K': 13, 'A': 14, '2': 17, 'X': 20, 'D': 30}
                    
def real_to_env(cards):
    env_card = [RealCard2EnvCard[c] for c in cards]
    env_card.sort()
    return env_card

#XD23456789TJQKA for c_int_array index from 0 to 14   
def env_card_to_c_int_array(list_cards):
    card_array_c = [0 for _ in range(15)]
    
    if len(list_cards) == 0:
        return card_array_c
   
    counter = Counter(list_cards)
    for card, num_times in counter.items():
        if card < 17:
            card_array_c[card] += num_times
        elif card == 17:
            card_array_c[2] += num_times
        elif card == 20 or card == 30:
            card_array_c[0] += num_times
            
    return card_array_c

def calculate_left_hands(input_cards):
    #print(input_cards)
    env_card = input_cards
    if isinstance(input_cards,str):
        env_card = real_to_env(input_cards)
    
    if len(env_card) > 20:
        print('length of input cards should be <= 20')
        return 20
    
    #print(env_card)
    c_int_array = env_card_to_c_int_array(env_card)
    #print(c_int_array)

    lib = cdll.LoadLibrary('./libCaculateLeftHands.so')  
    lib.caculate_left_hands.argtypes = [c_int * 15]
    lib.caculate_left_hands.restype = c_int
    lib.init()
    result = lib.caculate_left_hands((c_int * 15)(*c_int_array))
    #print(result)
    return result

if __name__ == '__main__':
    real_card = 'XD2345678899TJQKA'
    env_card = [3, 4, 5, 6, 6, 7, 7, 7, 8, 9, 10, 11, 12, 13, 14, 17, 20, 30]
     
    args, _ = getopt.getopt(sys.argv[1:], "hr:e:", ["help", "real_card=", "env_card="]) 
     
    for arg, val in args:
        if arg in ("-h", "--help"):
            print('python ' + sys.argv[0] + ' -r <real_card> -e <env_card>')
            print('or python ' + sys.argv[0] + ' --real_card=<real_card> --env_card=<env_card>')
            print('for example: python ' + sys.argv[0] + ' -r \'XD23456789TJQKA\' -e \'[3,4,5,6,7,8,9,10,11,12,13,14,17,20,30]\'')
            print('or for example: python ' + sys.argv[0] + ' --real_card=\'XD\' --env_card=\'[17,20,30]\'')
            sys.exit()
        elif arg in ("-r", "--real_card"):
            real_card = val.replace(' ','')
            #print(real_card)
        elif arg in ("-e", "--env_card"):
            #print(val)
            #print(val.replace(' ',''))
            env_card = ast.literal_eval(val.replace(' ',''))
            #print(env_card)

    if len(real_card) > 0:
        real_card_left_hands = calculate_left_hands(real_card)
        print(real_card)
        print('real_card_left_hands = ',real_card_left_hands)
    
    if len(env_card) > 0:
        env_card_left_hands = calculate_left_hands(env_card)
        print(env_card)
        print('env_card_left_hands = ',env_card_left_hands)
        

