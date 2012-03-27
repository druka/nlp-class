import math

class LaplaceBigramLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.unigrams = {}
    self.bigrams  = {}
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    for sentence in corpus.corpus: # iterate over sentences in the corpus
      prior_word = None
      for datum in sentence.data: # iterate over datums in the sentence
        word = datum.word
        self.unigrams[word] = self.unigrams.get(word, 0.0) + 1
        if prior_word:
          bigram = (prior_word, word)
          self.bigrams[bigram] = self.bigrams.get(bigram, 0.0) + 1
        prior_word = word

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.0
    prior_word = None
    for token in sentence:
      bigram_count = self.bigrams.get((prior_word, token), 0.0)
      prior_count  = self.unigrams.get(prior_word, 0.0)
      probability  = (bigram_count + 1) / (prior_count + len(self.unigrams))
      score += math.log(probability)
      prior_word = token
    return score
