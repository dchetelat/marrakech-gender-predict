############################################################
# Naive Bayes classifier prediction code
#
# 10/05/2015
# By Didier

import csv
import re
import math

class Classifier:
    # -------------------------------
    # __init__
    #
    def __init__(self):
        self.isModelLoaded = False

    # -------------------------------
    # load
    # 
    # Arguments
    # ---
    # modelFile  : Path on server to model file generated
    #              by the training code.
    #
    def load(self, modelFile):
        # Load the model file from the provided path
        modelCsv = open(modelFile,'rb')
        modelReader = csv.reader(modelCsv)
        
        # First line are the prior probabilities Male/Female
        p = modelReader.next()
        self.priorM = float(p[0])
        self.priorF = float(p[1])
        
        # Second line are the ranges of the histograms Male/Female
        m = modelReader.next()
        self.maxHistM = int(m[0])
        self.maxHistF = int(m[1])
        
        # Third line are the corpus words
        self.wordNames = modelReader.next()
        
        # The next maxHistM+1 lines are the univariate word male
        # histograms from 0 to maxHistM+1
        self.histM = [0]*(self.maxHistM+1)
        for i in range(0,self.maxHistM+1):
                self.histM[i] = [float(x) for x in modelReader.next()]

        # Then one line of the normalization constants
        self.histNormM = [float(x) for x in modelReader.next()]

        # The next maxHistF+1 lines are the univariate word female
        # histograms from 0 to maxHistF+1
        self.histF = [0]*(self.maxHistF+1)
        for i in range(0,self.maxHistF+1):
                self.histF[i] = [float(x) for x in modelReader.next()]

        # Then one line of the normalization constants
        self.histNormF = [float(x) for x in modelReader.next()]

        self.isModelLoaded = True
        modelCsv.close()
    
    # -------------------------------
    # predict
    # 
    # Arguments
    # ---
    # text  : String containing the raw, ASCII text to be
    #         classified according to the Naive Bayes model.
    #
    # Returns
    # ---
    # [label,prob] where
    #
    # label   : Either "Male" or "Female" based on the algorithm's
    #           best guess, or 'No model loaded' if no model
    #           had been loaded.

    # prob    : Probability, in percentage, of confidence in the
    #           prediction. (As a float.)
    def predict(self,text):
        # Doublechecks that a model has been loaded
        if self.isModelLoaded==False:
            return ['No model loaded',0]

        # 1) Preprocess the text
        # Turn to lower case
        text = text.lower()
        # Replace non-alphabetic characters by spaces
        text = re.sub('[^a-z]',' ',text)
        # Cut words at whitespace
        text = re.split(' {1,}',text)
      
        
        # 2) Compute word frequencies
        textFreq = dict.fromkeys(self.wordNames,0)
        for word in text:
            if word in textFreq:
                textFreq[word] += 1
        
        # 3) Compute the probability
        # For each gender, find the probability associated with 
        # each word count, multiply them and multiply the total 
        # by the prior gender probability. Then normalize to get the
        # posterior probability.
        
        # Male unnormalized log-posterior
        probUnM = math.log(self.priorM)
        for i in range(0,len(self.wordNames)):
            if textFreq[self.wordNames[i]]>self.maxHistM:
                probUnM += math.log(1/(1+self.histNormM[i]))
            else:
                probUnM += math.log(
                    (1+self.histM[textFreq[self.wordNames[i]]][i]) /
                    (1+self.histNormM[i]))
        
        # Female unnormalized log-posterior
        probUnF = math.log(self.priorF)
        for i in range(0,len(self.wordNames)):
            if textFreq[self.wordNames[i]]>self.maxHistF:
                probUnF += math.log(1/(1+self.histNormF[i]))
            else:
                probUnF += math.log(
                    (1+self.histF[textFreq[self.wordNames[i]]][i]) /
                    (1+self.histNormF[i]))

        # Normalize the probabilities
        m = max(probUnM, probUnF)
        probM = math.exp(probUnM-m)/(math.exp(probUnM-m)+math.exp(probUnF-m))
        probF = math.exp(probUnF-m)/(math.exp(probUnM-m)+math.exp(probUnF-m))
        
        # Conclude the prediction based on the probability
        # The prediction probability is rounded to three significant digits
        if probM>probF:
            return ['Male', 100*round(probM,3)]
        else:
            return ['Female', 100*round(probF,3)]

