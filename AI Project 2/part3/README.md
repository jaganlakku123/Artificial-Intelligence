# a2


**# Part3**:


Problem statement :

We are given  a dataset of user-generated reviews which has both training data set and test dataset. Task is to find the accuracy of classified datasets.


Analysis:

We have a set of data for training and testing which contains the classification of reviews to truthful and deceptive.

Using the training data set we find the accuracy of given test data test.

For finding the  accuracy we calculate the probability  of Truthful/deceptive in the given test dataset and comparing it with the Truthful/deceptive given in training dataset.

For calculating the probability of data in test data set we use naive bayes classifier

**Posterior Probability= Likelihood*Class Prior Probability/Predictor Prior Probability**

We have applied laplace smoothing to the data for more accuracy of the data.

Laplace smoothing:

It is entirely possible for a word in our vocabulary to be present in one class but not another — the probability of finding this word in that class will be 0! We can use Laplace smoothing to fix this problem. We’ll simply add 1 to the numerator but also add the size of our vocabulary to the denominator:

**probabilities[token][i] = math.log2((probabilities[token][i] + 1) / (tokens_in_class[c] + len(probabilities)))**

Referencee : https://levelup.gitconnected.com/movie-review-sentiment-analysis-with-naive-bayes-machine-learning-from-scratch-part-v-7bb869391bab
