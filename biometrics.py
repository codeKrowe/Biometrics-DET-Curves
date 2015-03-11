#!/usr/bin/python
from numpy.random import beta
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import random

def gen_thersholds(n):
    thersholds = []
    for x in xrange(1,n+1):
        thersholds.append(float("{:.9f}".format(random.uniform(0.0,1))))

    return sorted(thersholds)

with open('i.dat', 'r') as i, open('g.dat', 'r') as g:
    imposter = i.read()
    genuine = g.read()

imposter = imposter.split()
imposter = [float(i) for i in imposter]

genuine = genuine.split()
genuine = [float(g) for g in genuine]

genuine.sort()
imposter.sort()

plt.hist(imposter, facecolor='g', alpha=0.50, label='Imposter')
plt.hist(genuine, facecolor='y', alpha=0.50, label='Genuine')

legend = plt.legend(loc='upper right', shadow=True, fontsize='x-large')

# Put a nicer background color on the legend.
legend.get_frame().set_facecolor('#ffffff')

plt.xlabel('Score')
plt.ylabel('Frequency')
plt.title('Score Distribution')
plt.grid(True)
plt.show()

thersholds = gen_thersholds(100)
results = []

far = []
frr = []
cost = []

for t in thersholds:

    FP = 0
    FN = 0
    TP = 0
    TN = 0

    # go through imposters
    for score in imposter:

        if score >= t:
            # imposter passes as a genuine user
            FP += 1
        else:
            # imposter correctly rejected
            # true_negative.append(score)
            TN += 1

    for score in genuine:
        if score >= t:
            # genuine user correctly identified
            # true_positive.append(score)
            TP += 1
        else:
            # genuine user incorrectly rejected
            # false_negative.append(score)
            FN += 1


    far.append(float(FP) / float(len(imposter)))
    frr.append(float(FN) / float(len(genuine)))

    CFA=25
    CFR=15
    equal_apriori = 0.5
    far_current = float(FP) / float(len(imposter))
    frr_current = float(FN) / float(len(genuine))


    cost.append((CFA * equal_apriori * far_current) + (CFR * 0.5 * float(FN) / float(len(genuine))))
print
print "cost", sorted(cost)
print


l2 = sorted(cost)
smallest_cost = l2[0]

for i in xrange(100):
    if smallest_cost == cost[i]:
        print
        print "cost index", i
        print "far", far[i]
        print "frr", frr[i]
        print
        break

plt.plot(far,frr,linestyle="--", linewidth=5, label="DET Curve")

t = []
for i in xrange(100):
    t.append(far[i] + frr[i])


t2 = sorted(t)
smallest = t2[0]

far_optimum = 0
frr_optimum = 0
for i in xrange(100):
    if smallest == far[i] + frr[i]:
        # EER = (far[i], frr[i])
        print "EER:", far[i],  frr[i]
        far_optimum = far[i]
        frr_optimum = frr[i]
        print "index", i
        break

plt.plot(far_optimum,frr_optimum, "ro", label="Suitable Operating Point")
legend = plt.legend(loc='upper right', shadow=True, fontsize='x-large')

# Put a nicer background color on the legend.
legend.get_frame().set_facecolor('#ffffff')
plt.plot([1.0,0.0], [0.0,1.0],"k--")
plt.show()
