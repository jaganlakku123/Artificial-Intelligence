#!/usr/bin/python
#
# Perform optical character recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png
# 
# Authors: Lakku Jagan,Petroff Zach James,Kodetham Sai Nikitha
# (based on skeleton code by D. Crandall, Oct 2020)
#



from __future__ import division
from PIL import Image, ImageDraw, ImageFont
import sys
import math
import numpy as np


CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25
TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "

def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    print (im.size)
    print (int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }


def calculate_initial_transition(filename):
  
    # We have written this function to calculate the initial and trasition probabilities by reading training text file
    ft = []
    wt=[]
    initialt = [0]*len(TRAIN_LETTERS)
    text = open(filename,'r')
    linesinfile = text.readlines()
    
    for l in linesinfile:
        for word in l.split():
            wt.append(word)
        for a in l:
            ft.append(a)
    #print("length of file before",len(ft))
    #print("ft is ",ft) #It is list of letters
    #print("wt is ",wt)# It is list of words
    
    for a in range(len(TRAIN_LETTERS)):
        for l in ft :
            if TRAIN_LETTERS[a] == l:
                initialt[a] +=1
    
    initial=[]
    for i in initialt:
        initial.append((i+1)/len(wt))
    transition = np.zeros(shape=(len(TRAIN_LETTERS), len(TRAIN_LETTERS)))
    for i in range(0,len(ft)-1):
        if ft[i] in TRAIN_LETTERS and ft[i+1] in TRAIN_LETTERS:
            t = TRAIN_LETTERS.index(ft[i])
            t1 = TRAIN_LETTERS.index(ft[i+1])
            transition[t,t1] += 1

    for i in range(0,len(ft)-1):
        if ft[i].upper() in TRAIN_LETTERS and ft[i+1].upper() in TRAIN_LETTERS:
            t = TRAIN_LETTERS.index(ft[i].upper())
            t1 = TRAIN_LETTERS.index(ft[i+1].upper())
            transition[t,t1] += 1    
    #print("transition matrix is ",trans)
    for i in range(0,len(TRAIN_LETTERS)):
        for j in range(0,len(TRAIN_LETTERS)):
            if transition[i,j] == 0:
                transition[i,j] = 1e-10
    #Transition probabilities can be calculated as  P(t = j |t-1 = i) i.e the probability of transitioning from state i to state j
    for i in range(len(transition)):
        transition[i] /= sum(transition[i])
    #print("transition matrix after updating",trans)
    return initial,transition           
def simple(test_letters,emission):
    
    emission = emission
    obs = test_letters
    
    rows = len(TRAIN_LETTERS)
    cols = len(obs)
    
    y,temp_results = np.zeros(cols),np.zeros(shape=(rows,cols))
    
    for i in range(0,cols):
        for j in range(0,rows):
            temp_results[j,i] = emission[j,i]
    y = np.argmax(temp_results, axis=0)
    
    return y
def viterbi(test_letters,initial,transition,emission):
    
    # Here we calculate the most likely alphabet using viterbi algorithm
    test_letters = test_letters
    arr = np.zeros(shape=(len(TRAIN_LETTERS),len(test_letters)))
    prob_way =  np.empty(shape=(len(TRAIN_LETTERS),len(test_letters)),dtype=int)
    for i in range(len(TRAIN_LETTERS)):
        arr[i,0] = math.log(initial[i]) + math.log(emission[i,0])
    for j in range(1,len(test_letters)):
        for i in range(len(TRAIN_LETTERS)):
            temp_val = [] 
            for k in range(len(TRAIN_LETTERS)):
                temp_val.append(arr[k,j-1] + (math.log(transition[k,i])) + math.log(emission[i,j]))   
            max_state = max(temp_val)
            arr[i,j] = max_state 
            prob_way[i,j] = temp_val.index(max_state)
    maxprobable = np.zeros(len(test_letters),dtype=int)
    maxprobable[-1] = np.argmax(arr[:,-1])
    
    for i in range(1,len(test_letters))[::-1]: 
        maxprobable[i-1] = prob_way[maxprobable[i],i]
    return maxprobable
(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]

#train_img_fname = courier-train.png
#test_img_fname=test-3-0.png
#train_txt_fname= 12345.txt
train_letters = load_training_letters(train_img_fname)
#print("\n".join([ r for r in train_letters['a'] ]))
test_letters = load_letters(test_img_fname)
#print("\n".join([ r for r in test_letters[4] ]))
init, trans = calculate_initial_transition(train_txt_fname)
#print(init)
#print(trans)
'''
Below we are calculating the emission probabilities by 
Emission probability = P(all observed pixels | letter) = P(p1|a) P(p2|a)...P(pn|a)
    and the pixel is either black or white i.e 1 or 0 
P(all observed pixels | letter) = (1)^(number of black pixels) *(0)^(no. of white pixels)
The above formulae is refered from : https://github.com/snehalvartak/Optical-Character-Recognition-using-HMM/blob/master/ocr.py
'''
x = len(train_letters)
y = len(test_letters)
emissions = np.zeros(shape=(x,y))
noise = 0.42
for letter in train_letters:
    for j in range(y):
        val = train_letters.get(letter)
        #print(val)
        observed = test_letters[j]
        #print("observed is",observed)
        numberofmissed=0
        numberofmatched = 0
        for m in range(25):
            for n in range(14):
                if val[m][n] != observed[m][n]:
                    numberofmissed += 1 
                else:
                    numberofmatched += 1 
        emissions[TRAIN_LETTERS.index(letter)][j] = (math.pow(1-noise,numberofmatched)) * (math.pow(noise,numberofmissed))



simple = simple(test_letters,emissions)
print ("Simple: "+"".join([TRAIN_LETTERS[i] for i in simple]))
output = viterbi(test_letters,init,trans,emissions)
print ("   HMM: " + "".join([TRAIN_LETTERS[i] for i in output]))