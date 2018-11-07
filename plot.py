import ujson
import numpy as np
import matplotlib.pyplot as plt

with open('iclr2019.json', 'r') as f:
    dataset = ujson.load(f)
    paper_ratings = {}

    for paper_id in dataset:
        paper = dataset[paper_id]
        s = 0
        for rating in paper:
            if rating[0:2] == '10':
                s += 10
            else:
                s += int(rating[0])
        if len(paper) > 0:
            paper_ratings[paper_id] = 1.0 * s / len(paper)
    print('Got reviews for {} out of {}'.format(len(paper_ratings), len(dataset)))
    ratings = paper_ratings.values()
    ratings = list(map(round, ratings))
    ratings = np.unique(ratings, return_counts=True)
    fig, ax = plt.subplots()

    rects1 = ax.bar(ratings[0], ratings[1])
    for i, v in (list(zip(*ratings))):
        ax.text(i - 0.25, v, str(v), fontweight='bold')

    plt.show()
