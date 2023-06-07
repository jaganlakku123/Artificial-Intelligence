# Part 1: Part-of-Speech Tagging

### Goal:
To implement part-of-speech tagging in Python, using Bayes networks.

We  were given a large corpus of labeled training and testing data.
Each line consists of a sentence, and each word is followed by one of 12 part-of-speech tags: ADJ (adjective),ADV (adverb), ADP (adposition), CONJ (conjunction), DET (determiner), NOUN, NUM (number), PRON
(pronoun), PRT (particle), VERB, X (foreign word), and . (punctuation mark). Our program outputs the logarithm of the joint probability P(S,W) for each solution it finds under each of the three models using 3 approaches Simple, HMM and Complex

I have to admit that the question was really hard and the code was referenced from https://github.com/surajgupta-git/Artificial-Intelligence-projects/tree/main/POS%20Tagging 

1. Simplified Bayes Net: The emission probabilities(Probability of a word for a given Part of Speech) were calculated and then multiplied with the Prior Probabilitiy. We then estimated the most-probable tag si* for each word Wi,
si*= arg max P(Si = si | W):
             si
The maximum probability value was calculated for each word in every sentence and returned. The simplifies model calculates the log of posterior probability for each word .It basically finds the percentage of the words in the total pos occurrence.  Naive Bayes is kind of cranky and performs in an average way.

2. HMM-Viterbi: We calculated the emission and transition probabilities(Probability of transition from state 1 to state 2) for all the pos. The arg max of the transitions  is considered. The path is then backtracked and the most probable path is returned .It uses the formula  
(s1 *, , , , , , , ,sN)= arg max P(Si = si | W)
                                s1, , , , ,sN


The Viterbi algorithm is much better and outputs a sequence prediction and is faster.

3.MCMC: We used Gibbs Sampling to find the pos for each word in every sentence of the corpus. We first assigned the pos value as ‘noun’ and train the data and store the count of each value  in a dictionary and calculate Gibbs probability. We use Gibbs sampling when the joint probability is difficult to sample from and not known directly.We sample from the posterior distribution  P(S | W)along with the transition probabilities . We store the counts of each word in the sentences and return the pos with the maximum count. The best labeling for each
word is done by by picking the maximum marginal for each word,
 P(Si=si |W) = arg max P(Si = si | W)
                                 si
It can be observed that Gibbs sampling takes more time as the sample size increases
### OUTPUT

So far scored 1403 sentences with 20537 words.

                               Words correct:    Sentences correct:
                               
      0.Ground Truth:            100.00%              100.00%
   
      1.Simple:                 93.88%               47.54%
      
       2.HMM:                   94.94%               53.39%
       
       4.Complex                94.92%               53.17%





## Part 2 ##

* Baye's Net

The Baye's net was pretty simple to carry out, given the edge strength. To get the emission probabilities, I simply normalized the edge strengths to be between one and zero.
First, the airice boundary is found, then the emission probabilities were altered, so that for each column in the emission probabilities, every entry with a row index less than
the boundary at that corresponding column was set to 0. 

* HMM


For the HMM, I had to determine what would be good values for the initial and transition probabilities. For the initial probabilities, I just said that the first one-hundred 
pixels had a uniform probability of .01, and the last 75 had a uniform probability of 0 (So the last 75 pixels could not be the starting point). I picked this, because I did not
see a huge trend between starting points in the different images, except that they were all roughly within the top half of the image. For the transition probabilities, I assumed 
that if pixels in one column were in a similar row as pixels in the next column, then the transition probability would be higher. Pixels in the same row, one row above, or one 
row below, then the transition probability is .2. As we go up or down, the transition probability slightly decreases until 6 rows above or below (.2 -> .2 -> .125 -> .05 -> .025 
.0125 -> .0125). It is assumed that the rest of the transition probabilities are 0, so there is no chance of transitioning more that 6 rows when drawing the boundary. 

* HMM With Human Feedback


The HMM with human feedback was very similar to the regular HMM. However, there were a couple changes, in attempt to increase the accuracy of our boundary. The first is that the 
boundary search was split into two different boundary searches, a search for the boundary before the user provided x position, and a search for the boundary after the user 
provided x position. For the boundary before the user provided x position, the search was conducted from right to left, so that we could start at the user provided point. For the 
initial probabilities, all were 0, except for the one that corresponded to the user provided position, which was 1. The two searches were conducted separately, then combined at 
the user provided position. 

* Performance

Examples:

![alt text](https://github.iu.edu/cs-b551-fa2021/skodeth-slakku-zpetroff-a3/blob/master/part2/test_images/09.png?raw=true)
![alt text](https://github.iu.edu/cs-b551-fa2021/skodeth-slakku-zpetroff-a3/blob/master/part2/air_ice_output_1.png?raw=true)
![alt text](https://github.iu.edu/cs-b551-fa2021/skodeth-slakku-zpetroff-a3/blob/master/part2/ice_rock_output_1.png?raw=true)

![alt text](https://github.iu.edu/cs-b551-fa2021/skodeth-slakku-zpetroff-a3/blob/master/part2/test_images/16.png?raw=true)
![alt text](https://github.iu.edu/cs-b551-fa2021/skodeth-slakku-zpetroff-a3/blob/master/part2/air_ice_output_2.png?raw=true)
![alt text](https://github.iu.edu/cs-b551-fa2021/skodeth-slakku-zpetroff-a3/blob/master/part2/ice_rock_output_2.png?raw=true)


Hardest Example: 

![alt text](https://github.iu.edu/cs-b551-fa2021/skodeth-slakku-zpetroff-a3/blob/master/part2/test_images/23.png?raw=true)
![alt text](https://github.iu.edu/cs-b551-fa2021/skodeth-slakku-zpetroff-a3/blob/master/part2/air_ice_output_3.png?raw=true)
![alt text](https://github.iu.edu/cs-b551-fa2021/skodeth-slakku-zpetroff-a3/blob/master/part2/ice_rock_output_3.png?raw=true)

This example was the most difficult for many reasons, and goes against some of the assumptions made before building the model. The first is that we assumed the boundaries to be 
smooth, and because of this, straight lines were given precedence by the transition probabilities. However, there are many hills in the ice-rock boundary. Moreover, giving 
precedence to straight lines paired with the noise in the image resulted in an error when drawing both boundaries. Also, we assumed that the ice-rock boundary is at least 10 
pixels below the air-ice boundary, and I am not sure that this is true in this example.  


# Part 3 #


Problem : Image processing from text using HMM and MAP interface. We need to extract text from images which is applied in extracting text from scanned documents,captcha etc.

Data Used : For this code we use 2 training files , one is for training images which is used for calculating emission probabilities, One more file is a text file which is used for calculating initial probabilities and transition probabilities.

Assumption:All the text in our images has the same fixed-width font of the same size. 
Each letter fits in a box that’s 16 pixels wide and 25 pixels tall. We’ll also assume that our documents only
have the 26 uppercase latin characters, the 26 lowercase characters, the 10 digits, spaces, and 7 punctuation
symbols, (),.-!?’". 

Naives Bayes assumption that our pixels are conditionally independent on each letter

Approach :

Simple Baysean Net:

In this process we assume letters are independent of its neighbours letters. Based on emission probabilities we predict the maximum probability by P(x)=argmax P(x/o)

Here we have assumed the noise of 42% for all the images and calculated the emission probabilities

HMM Viterbi :

HMM considers the initial, transition and emission probability . Viterbi model starts from initial node using initial and emission probabilities. Next state probability is calculated using maximum viterbi and transition probabilities for each hidden node.

Observation and Conclusion : 

The model predicts inaccurate results for more noisy images. For example, letter 'l' and number '1' almost have the same number of dark pixels and with little noise, the model predicts inaccurate results. However, the HMM model considered transition probabilities and thus could predict correct results.
Sometimes simplified models perform better than HMM. It has been observed that the combination of transition and emission is very important. Even though we have stronger emission probabilities, if transition probabilities are low, then results can be affected. In future work, complex models will be considered.
There may be a better way to calculate emission probabilities
