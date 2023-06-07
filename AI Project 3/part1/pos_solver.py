
  
###################################
# CS B551 Spring 2021, Assignment #3
#
# Kodetham Sai Nikitha, skodeth
# Petroff Zach James, zpetroff
# Lakku Sai Jagan L, slakku :
#
# (Based on skeleton code by D. Crandall)
#
#The following code has been referenced from https://github.com/surajgupta-git/Artificial-Intelligence-projects/tree/main/POS%20Tagging

import random
import math


# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:
    #Creating an empty dictionary to store the transition probabilities
    transition_probability={}
    #Creating an empty dictionary to store the emission probabilities
    emission_probability={}
    #Creating an empty dictionary to store the
    cross={}
    #Creating an empty dictionary to store the gibbs probability
    gibbs_probability={}
    #Initialize a minimum value to be assigned to the 12 parts of speech to avoid errors during computation
    minimum=0.0000001
    #Initializing the probabilities of the 12 part of speech tags to the minimum value
    initial_probability={'adj':minimum,'adv':minimum,'adp':minimum,'conj':minimum,'det':minimum,'noun':minimum,'num':minimum,'pron':minimum,'prt':minimum,'verb':minimum,'x':minimum,'.':minimum}
    pos = ['adj', 'adv', 'adp', 'conj', 'det', 'noun', 'num', 'pron', 'prt', 'verb', 'x', '.']

    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!
    def posterior(self, model, sentence, label):
        length = len(sentence)
        
        if model == "Simple":
            simple_model_result = 0
            for i in range(length):
                simple_model_result += math.log(self.emission_prob(sentence[i])[label[i]])
            return simple_model_result
        
        elif model == "HMM":
            hmm_result = 0
            for i in range(length):
                if i == 0:
                    hmm_result += math.log(self.emission_prob(sentence[i])[label[i]])
                else:
                    hmm_result += math.log(self.emission_prob(sentence[i])[label[i]]) \
                              + math.log(self.transition_prob(label[i])[label[i - 1]])

            return hmm_result

        elif model == "Complex":
            complex_model_result = 0

            for i in range(length):
                if length == 1:
                    complex_model_result += math.log(self.emission_prob(sentence[i])[label[i]]
                                       * (self.initial_probability[label[i]] / sum(self.initial_probability.values())))

                elif i == 0:
                    complex_model_result += math.log(self.emission_prob(sentence[i])[label[i]]
                                       * (self.initial_probability[label[i]] / sum(self.initial_probability.values()))
                                       * self.transition_prob(label[i])[label[i + 1]]
                                       * self.gibbs_prob(sentence[i + 1],(label[i], label[i + 1])))
                elif i == length - 1:
                    complex_model_result += math.log(self.gibbs_prob(sentence[i], (label[i - 1], label[i]))
                                       * self.transition_prob(label[i - 1])[label[i]])
                else:
                    complex_model_result += math.log(self.gibbs_prob(sentence[i], (label[i - 1], label[i]))
                                       * self.transition_prob(label[i - 1])[label[i]]
                                       * self.transition_prob(label[i])[label[i + 1]]
                                       * self.gibbs_prob(sentence[i + 1],(label[i], label[i + 1])))

            return complex_model_result
        else:
            print("Unknown algo!")

    # Do the training!

    #Creating a dictionary to store transition probability values
    trans_prob={}

    
    #Create a dictionary to store the emission probability values
    emi_prob = {}


    def transition_prob(self, t):
        if t not in self.trans_prob.keys():
            new_dict = {}
            for i in self.pos:
                new_dict[i] = self.transition_probability[t][i] / (
                        sum(self.transition_probability[t].values()) - self.transition_probability[t]['pos appearance'])
            self.trans_prob[t] = new_dict
        return self.trans_prob[t]


    def emission_prob(self, word):

        if word not in self.emi_prob.keys():
            new_dict1 = {}
            for i in self.pos:
                if word in self.emission_probability.keys():
                    new_dict1[i] = self.emission_probability[word][i] / self.transition_probability[i]['pos appearance']
                elif i == 'noun':
                    new_dict1[i] = 1 - (11 * self.minimum)
                else:
                    new_dict1[i] = self.minimum
            self.emi_prob[word] = new_dict1
        return self.emi_prob[word]


    def gibbs_prob(self, word, speeches):
        if word in self.gibbs_probability.keys():
            if speeches in self.gibbs_probability[word].keys():
                return self.gibbs_probability[word][speeches] / sum([self.gibbs_probability[word][k] for k in self.gibbs_probability[word].keys() if k[0] == speeches[0]])

        return self.emission_prob(word)[speeches[1]]



    def train(self, data):
        pos_new = {'adj': self.minimum, 'adv': self.minimum, 'adp': self.minimum, 'conj': self.minimum, 'det': self.minimum,
                     'noun': self.minimum, 'num': self.minimum, 'pron': self.minimum, 'prt': self.minimum, 'verb': self.minimum,
                     'x': self.minimum, '.': self.minimum, 'word appearance': 0}

        pos_trans = {'adj': self.minimum, 'adv': self.minimum, 'adp': self.minimum, 'conj': self.minimum, 'det': self.minimum,
                          'noun': self.minimum, 'num': self.minimum, 'pron': self.minimum, 'prt': self.minimum, 'verb': self.minimum,
                          'x': self.minimum, '.': self.minimum, 'pos appearance': 0}

        self.wordcount=0

        for line in data:
            for i in range(0, len(line[1]) - 1):
                if i == 0:
                    self.initial_probability[line[1][i]] += 1
                if line[1][i] not in self.transition_probability.keys():
                    self.transition_probability[line[1][i]] = pos_trans.copy()
                    self.transition_probability[line[1][i]][line[1][i + 1]] += 1
                    self.transition_probability[line[1][i]]['pos appearance'] += 1
                else:
                    self.transition_probability[line[1][i]][line[1][i + 1]] += 1
                    self.transition_probability[line[1][i]]['pos appearance'] += 1
                
            self.transition_probability[line[1][-1]]['pos appearance'] += 1
            
            for i, j in zip(line[0], line[1]):
                self.wordcount+=1
                if i in self.emission_probability.keys():
                    self.emission_probability[i][j] += 1
                    self.emission_probability[i]['word appearance'] += 1

                else:
                    self.emission_probability[i] = pos_new.copy()
                    self.emission_probability[i][j] += 1
                    self.emission_probability[i]['word appearance'] += 1

            for i, j, k in zip(line[0][1:-1], line[1][0:-2], line[1][1:-1]):
                if i in self.gibbs_probability.keys():
                    if (j, k) in self.gibbs_probability[i].keys():
                        self.gibbs_probability[i][(j, k)] += 1
                    else:
                        self.gibbs_probability[i][(j, k)] = 1
                else:
                    self.gibbs_probability[i] = {}
                    self.gibbs_probability[i][(j, k)] = 1

        self.prior_prob={}
        
        for p in self.pos:
            self.prior_prob[p]=self.transition_probability[p]['pos appearance']
        for p in self.pos:
            self.prior_prob[p]/=self.wordcount

    # Functions for each algorithm. Right now this just returns nouns -- fix this!
    #

    def simplified(self, sentence):
        simplified_result = []
        for word in sentence:
            s = self.emission_prob(word).copy()
            for p in self.pos:
                s[p]*=self.prior_prob[p]
            simplified_result.append(max(s, key=s.get))

        return simplified_result

    def hmm_viterbi(self, sentence):
        length = len(sentence)

        viterbi_table = [[0 for i in range(12)] for t in range(length)]

        best = [[0 for t in range(length)] for j in range(12)]
        viterbi_result = []
        for i in range(0, length):
            count = 0
            for p in self.pos:
                if i == 0:
                    viterbi_table[i][count] = -math.log(self.emission_prob(sentence[i])[p]) \
                                      - math.log((self.initial_probability[p] /
                                            sum(self.initial_probability.values())))
                    count = count + 1
                else:
                    q = list(range(0, 12))
                    tablevalues = [viterbi_table[i - 1][l]
                                   - math.log(self.transition_prob(p2)[p])
                                   - math.log(self.emission_prob(sentence[i])[p])
                                   for l, p2 in zip(q, self.pos)]
                    cost = min(tablevalues)
                    viterbi_table[i][count] = cost
                    best[count][i] = tablevalues.index(cost)
                    count = count + 1

        last = viterbi_table[length - 1].index(min(viterbi_table[length - 1]))
        viterbi_result.append(self.pos[last])
        k = length - 1
        while k > 0:
            last = best[last][k]
            viterbi_result.append(self.pos[last])
            k = k - 1
        return viterbi_result[::-1]

    def joint_prob(self, sample, sentence, j):
        prob = {}
        length = len(sample)
        for p in self.pos:
            if length == 1:
                prob[p] = self.emission_prob(sentence[j])[p] * \
                          (self.initial_probability[p] / sum(self.initial_probability.values()))
            

            elif j == 0:
                prob[p] = self.emission_prob(sentence[j])[p] * \
                          (self.initial_probability[p] / sum(self.initial_probability.values())) * \
                          self.transition_prob(p)[sample[j + 1]] * \
                          self.gibbs_prob(sentence[j + 1],(p, sample[j + 1]))
            elif j == length - 1:
                prob[p] = self.gibbs_prob(sentence[j], (sample[j - 1], p)) * \
                          self.transition_prob(sample[j - 1])[p]
            else:
                prob[p] = self.gibbs_prob(sentence[j], (sample[j - 1], p)) * \
                          self.transition_prob(sample[j - 1])[p] * \
                          self.transition_prob(p)[sample[j + 1]] * \
                          self.gibbs_prob(sentence[j + 1],(p, sample[j + 1]))
        return {v: float(prob[v]) / sum(prob.values()) for v in self.pos}

    def complex_mcmc(self, sentence):
        length = len(sentence)
        sample_sentence = ["noun" for i in range(length)]
        sample_length = len(sample_sentence)
        count = [{p: 0 for p in self.pos} for i in range(length)]
        iteration = 1000
        for i in range(iteration):
            for j in range(len(sample_sentence)):
                prob = self.joint_prob(sample_sentence, sentence, j)

               
                rand = random.random()
                num = 0
                for p in self.pos:
                    num += prob[p]
                    if rand < num:
                        sample_sentence[j] = p
                        break

               
                if i > iteration / 2:
                    for k in range(sample_length):
                        count[k][sample_sentence[k]] += 1

        final_result = []
        for i in range(sample_length):
            pos = "noun"
            max_val = 0
            for p in self.pos:
                if count[i][p] >= max_val:
                    max_val = count[i][p]
                    pos = p
            final_result.append(pos)

        return final_result

    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself.
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        else:
            print("Unknown algo!")
