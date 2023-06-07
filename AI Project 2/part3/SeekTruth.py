# SeekTruth.py : Classify text objects into two categories
#
# PLEASE PUT YOUR NAMES AND USER IDs HERE
#
# Based on skeleton code by D. Crandall, October 2021
#

import sys
import math

def load_file(filename):
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(parsed[1] if len(parsed)>1 else "")
    return {"objects": objects, "labels": labels, "classes": list(set(labels))}


# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to reviews
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each review
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
#

def classifier(train_data, test_data):
    
    probabilities = {}

    maps = {"truthful": 0,"deceptive": 1}
    tokens_in_class = {"truthful": 0,"deceptive": 0}
    prior_probability = {"truthful": 0,"deceptive": 0}
    numberoflinescount = 0
    line_token_count = 0
    count=0
    for i in train_data["objects"]:
        j=i.split(" ")
        #print("valuse for count {} is {}".format(count,train_data["labels"][count]))
        prior_probability[train_data["labels"][count]] += 1
        for k in j:
        
            k=k.lower()
            
                

            if k not in probabilities:
                probabilities[k] = [0, 0]

            probabilities[k][maps[train_data["labels"][count]]] += 1
            tokens_in_class[train_data["labels"][count]] += 1

        line_token_count += 1
        numberoflinescount += 1
        count=count+1
        #print(tokens)
        #print(train_data["classes"])
    #print("probabilities are",probabilities)
   

    # delete top 2 high frequency and low frequency tokens
    high_freq_token = ""
    low_freq_token = ""
    for i in range(2):
        maxp = -1
        minp = 99999999999
        p = 0
        #print("probabilities are",probabilities)
        for token in probabilities:
            p = probabilities[token][0] + probabilities[token][1]
            if p > maxp:
                maxp = p
                high_freq_token = token
            if p < minp:
                minp = p
                low_freq_token = token
        del probabilities[high_freq_token]
        #print("high frequency is",high_freq_token)
        #print("low frequency is ",low_freq_token)
        del probabilities[low_freq_token]

        #print("prior_probability is ",prior_probability)
        #print("numberoflinescount is ",numberoflinescount)

    #print("line count is ",numberoflinescount)
    #print("class_prior_probability is ",prior_probability)
    #print("class_map is ",maps)
    # convert to probabilities and do add one smoothing
    for token in probabilities:
        for c in tokens_in_class:
            i = maps[c]
            probabilities[token][i] = math.log2((probabilities[token][i] + 1) / (tokens_in_class[c] + len(probabilities)))

    for c in prior_probability:
        prior_probability[c] = math.log2(prior_probability[c] / numberoflinescount)

    prior_probabilities = prior_probability
    output = []
    numberoflinescount = 0
    for line in test_data["objects"]:
            
            tokens = line.split(" ")

            line_token_count = 0
            observation_probability = [0, 0]
            i = 0

            for c in maps:
                i = maps[c]
                observation_probability[i] = prior_probabilities[c]

                for token in tokens:
                    if line_token_count >0:
                        token = token.lower()

                        if token in probabilities:
                            observation_probability[i] += probabilities[token][i]

                    line_token_count += 1

            if observation_probability[0] > observation_probability[1]:
                output.append("truthful")
            else:
                output.append("deceptive")
            numberoflinescount += 1
        
    return output
if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")
    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if(sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")
    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}
    results= classifier(train_data, test_data_sanitized)
    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))


   






