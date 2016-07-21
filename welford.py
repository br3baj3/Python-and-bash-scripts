# Numerical method to compute variance, avoiding "catastrophic cancellation" and making the algorithm more numerically stable
# + info: http://jonisalonen.com/2013/deriving-welfords-method-for-computing-variance/

import math
import sys

router=sys.argv[1]
file=open('/var/tmp/values_aux','r')
list=file.readlines()

try:
        list_flotantes=map(float,list)

except ValueError as e:
        print router
        print 'There is no latency data file'

def online_variance(data):
    n = 0
    mean = 0.0
    M2 = 0.0
    for x in data:
        n += 1
        delta = x - mean
        mean += delta/n
        M2 += delta*(x - mean)


    if n < 2:
        return float('nan')
    else:
        a= M2 / (n - 1)
        return a, mean


try:
        variance=online_variance(list_flotantes)
        average=variance[1]
        deviation=math.sqrt(variance[0])
        deviation=round(deviation,4)
        average=round(average,4)

        if int(deviation) > 50:
                print router
                print "Average:  %f" % average
                print "Deviation: %f\n" % deviation

except  NameError as e:
        print 'Not possible to compute deviation\n'
