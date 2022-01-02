"""
Title:          apriori.py
Assignment No:  Assignment 3 
Description:    Association Analysis - Simple Python implementation of the Apriori Algorithm.
Purpose:        To implement apriory algorithm and Evaluate Results. 
Reference:      https://github.com/asaini/Apriori/blob/python3/apriori.py

Usage:
    Format:     $python apriori.py datasetname.csv  minimum_support_value minimum_confidence_value
    Example:    $python apriori.py dataset_updated.csv  0.15    0.80
"""



import sys
import csv
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser
#To access the arguments passed during run-time
from sys import argv 

#Arguments passed during run-time.
script, f, s, c = argv


def subsets(arr):
    """ Returns non empty subsets of arr"""
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])


def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):
    """calculates the support for items in the itemSet and returns a subset
    of the itemSet each of whose elements satisfies the minimum support"""
    _itemSet = set()
    localSet = defaultdict(int)
    #To count the occurance of itemset in the transactions.
    for item in itemSet:
        for transaction in transactionList:
            if item.issubset(transaction):
                freqSet[item] += 1
                localSet[item] += 1
    #To calculate the support of item sets.
    for item, count in localSet.items():
        support = float(count) / len(transactionList)
        #Add items to itemset, after checking if the calculated support value is greater than the minimum support value.
        if support >= minSupport:
            _itemSet.add(item)
    #Returns subset of itemsets that satisfies minimum support value.
    return _itemSet


def joinSet(itemSet, length):
    """Join a set with itself and returns the n-element itemsets"""
    #Generates the itemsets of the desired length by combining them with one another, such that new itemset with desired length is obtained.
    return set(
        [i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length]
    )


def getItemSetTransactionList(data_iterator):
    """Returns Transaction List and Item Set"""
    transactionList = list()
    itemSet = set()
    """Each row of the dataset is added to the transaction list and the item names of each row in the dataset, are added to item set"""
    with open(data_iterator,'rt') as readfile:
        data = csv.reader(readfile)
        for record in data:                         #Accessing each row
            transaction = frozenset(record)         #To freeze the transaction and make it unchangeable.
            transactionList.append(transaction)     #Adding to transaction to Transaction list.
            for item in transaction:
                itemSet.add(frozenset([item]))      # Generate 1-itemSets
    return itemSet, transactionList


def runApriori(data_iter, minSupport, minConfidence):
    """
    run the apriori algorithm.
    Returns:
     - items (tuple, support)
     - rules ((pretuple, posttuple), support, confidence)
    """
    
    #Function to construct ItemSet and TransactionList from dataset file.
    itemSet, transactionList = getItemSetTransactionList(data_iter)

    #Set that maintains the frequency of occurance of an itemset. 
    freqSet = defaultdict(int)
    
    #Global dictionary that stores (key=n-itemSets,value=support).
    largeSet = dict()    

    #Dictionary to store Association Rules
    assocRules = dict()
    

    #Initial Pruning Set: Returns only those item sets that satisfies the minimum support, by removing other itemsets. 
    oneCSet = returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet) 
    
    """Below loop helps in generating all combinations of itemsets that satisfies the minimum support value."""
    #Initial candidate set
    currentLSet = oneCSet
    k = 2
    while currentLSet != set([]):
        #Assigning the current candidate set.
        largeSet[k - 1] = currentLSet
        """
        Candidate Generation: Generating candidate set of length k. 
        This step includes candidate pruning too, as we are considering only frequent itemsets.
        Thereby, it will not include candidate sets containing subsets of length k-1 that are infrequent.
        """
        currentLSet = joinSet(currentLSet, k)
        """
        Candidate Elimination: Eliminating the candidates that are in-frequent.
        This step also includes support counting step, as within the called function, we are calculating support of candidates in the candidate itemset
        """
        currentCSet = returnItemsWithMinSupport(
            currentLSet, transactionList, minSupport, freqSet
        )
        #Assigning the candidate set of lenth k.
        currentLSet = currentCSet
        k = k + 1

    def getSupport(item):
        """local function which Returns the support of an item"""
        return float(freqSet[item]) / len(transactionList)
    
    """Generating a itemset list with itemsets and their support values"""
    toRetItems = []
    for key, value in largeSet.items():
        toRetItems.extend([(tuple(item), round(getSupport(item),2)) for item in value])
        
    """Generating a rule list with rules and their support, confidence values"""
    toRetRules = []
    """
    Splitting the generated candiate itemsets into subsets.
    Constructing rules by splitting the subset.
    Calculating the support and confidence values.If confidence satisfies, the minimum confidence value then adding that rule to association rules. 
    """
    for key, value in list(largeSet.items())[1:]:
        for item in value:
            _subsets = map(frozenset, [x for x in subsets(item)])
            for element in _subsets:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = getSupport(item) / getSupport(element)
                    ruleSupport = getSupport(item)
                    if confidence >= minConfidence:
                        toRetRules.append(((tuple(element), tuple(remain)),round(ruleSupport,2), round(confidence,2)))
    
    #returns item sets list and rules list 
    return toRetItems, toRetRules


def printResults(items, rules):
    """prints the generated itemsets sorted by support and the confidence rules sorted by confidence"""
    print("\n------------------------ Item: Itemset, Support Value    ------------------\n")
    for item, support in sorted(items, key=lambda x: x[1]):
        print("item: %s , %.3f" % (str(item), support))
    print("\n------------------------ Rule: Rule (s= support_value , c= confidence_value)----------------------\n")
    for rule, support, confidence in sorted(rules, key=lambda x: x[1]):
        pre, post = rule
        print("Rule: %s ==> %s  (s= %.3f , c =%.3f)" % (str(pre), str(post), support, confidence))




if __name__ == "__main__":
    
    """
    Assigning datasetname, mimimum support, minimum confidence values passed during run-time.
    As the type is unspecified, converting the values to the required format
    """
    inFile = str(f)    
    minSupport = float(s) 
    minConfidence = float(c) 
    
    #Calling runApriori function by passing dataset, minimum support and minimum confidence.
    items, rules = runApriori(inFile, minSupport, minConfidence)
    #To print Items and Rules generated in a specific format.
    printResults(items, rules)
    
    """Plotting the results for evaluation."""
    #Reference:https://seaborn.pydata.org/examples/scatterplot_matrix.html
    df = pd.DataFrame(rules, columns = ["Titles","Support","Confidence"])
    #Specifying the size of the figure
    plt.figure(figsize=(50,25))
    plt.title('Pair Plot of Support and Confidence')
    # plot the data
    sns.pairplot(df)
    # Labelling axes
    plt.savefig(str(minSupport)+"_"+str(minConfidence)+"_plot.png")
