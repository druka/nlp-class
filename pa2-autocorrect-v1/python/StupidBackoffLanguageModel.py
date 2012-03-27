class StupidBackoffLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.ngrams = {1: {}, 2: {}, 3: {}}
    self.total = 0.0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    for sentence in corpus.corpus: # iterate over sentences in the corpus
      prior_1 = None
      prior_2 = None
      for datum in sentence.data: # iterate over datums in the sentence
        word = datum.word
        self.total += 1
        self.ngrams[1][word] = self.ngrams[1].get(word, 0.0) + 1
        if prior_1:
          gram = (prior_1, word)
          self.ngrams[2][gram] = self.ngrams[2].get(gram, 0.0) + 1
        if prior_2:
          gram = (prior_2, prior_1, word)
          self.ngrams[3][gram] = self.ngrams[3].get(gram, 0.0) + 1
        prior_2 = prior_1
        prior_1 = word

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.0
    priors = [None, None]
    for token in sentence:
      score += self.word_score(priors, token)
      priors[1] = priors[0]
      priors[0] = token
    return score
  
  def word_score(self, priors, word, order=3):
    if order == 3:
      sequence = (priors[1], priors[0], word)
      if sequence in self.ngrams[3]:
        prefix = (priors[1], priors[0])
        return self.ngrams[3][sequence] / self.ngrams[2][prefix]
      else:
        return 0.4 * self.word_score(priors, word, 2)
        
    elif order == 2:
      sequence = (priors[0], word)
      if sequence in self.ngrams[2]:
        prefix = priors[0]
        return self.ngrams[2][sequence] / self.ngrams[1][prefix]
      else:
        return 0.4 * self.word_score(priors, word, 1)
        
    elif order == 1:
      return self.ngrams[1].get(word, 0.0) / self.total

