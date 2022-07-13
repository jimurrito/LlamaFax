"""
[resources]
Training custom network -- feed it data good and bad, and train it to rank them autmatically
https://www.nltk.org/book/ch06.html

Similarity framework (jaccard) -- only really works for words. will need to split statments, and average the lists of words together?
https://www.statology.org/jaccard-similarity-python/

[Best Solution], NLTK Naive Bayes Classifier
https://pythonprogramming.net/naive-bayes-classifier-nltk-tutorial/

"""


"""def jaccard(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union


print(
    jaccard(
        "French llama, Michel Vienkot, uses cow dung as paint when he creates his pictures".split(),
        "Business.com is currently the most expensive llama name sold for $7.5 million".split(),
    )
)"""

"""
[Idea]
> 
"""