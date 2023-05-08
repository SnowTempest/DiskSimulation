#** ***********************************************************
#    @file disksimulation.py
#    @author Snow Tempest
#    @date Oct 21, 2022
#    @brief  Disk simulation program which simulates the C-Scan, SSTF, and FIFO algorithms used by disk schedulers.

# This program will take in 3 arguments, the algorithm type, queue size, and the name of the input file.
# It will then go through the program depending on the inputs given. It will track the amount of time seeking and the rotational latency 
# to calculate the average time that a request sits in a queue with disks. 

#Compiler: 
#Company: Me

# How to run: python prog3.py ALGORITHM QUEUESIZE INPUTFILE

#*************************************************************** **/

import sys

global LATENCY
global QSIZE
global FILE

class Request:
    def __init__(self, cylinderNum, accumTime):
        self.cylinderNum = cylinderNum
        self.accumTime = accumTime

    def __str__(self): 
        return "Cylinder No: %s, Accum Time: %d" % (self.cylinderNum, self.accumTime)

class Queue:
    def __init__(self, rNum, REQUESTS):
        self.rNum = rNum
        self.REQUESTS = REQUESTS

def main():
    global FILE
    global QSIZE
    global LATENCY
    if (len(sys.argv) < 4):
        print( "Not enough arguments given.")
        print ("USAGE: ALGORITHM QUEUESIZE INPUTFILE\n")
    elif (len(sys.argv) > 4):
        print("Too many arguments entered.")
        print ("USAGE: ALGORITHM QUEUESIZE INPUTFILE")

    if sys.argv[1] == "C-SCAN" or sys.argv[1] == "FIFO" or sys.argv[1] == "SSTF":
        algorithm = sys.argv[1]
    else:
        print ("Incorrect algorithm entered.")
        print ("Valid Algorithms case sensitive: C-SCAN | FIFO | SSTF\n")
        quit()

    QSIZE = int(sys.argv[2])
    FILE = sys.argv[3]
    LATENCY = 4.2
    REQUESTS = []
    start = 0


    q = Queue(0, REQUESTS)

    if algorithm == "C-SCAN":
        cscan(start, q)
    elif algorithm == "FIFO":
        fifo(start, q)
    elif algorithm == "SSTF":
        sstf(start, q)
    

def cscan (start, q):
    i, j, totTime = 0,0,0 #Grand total time spent is set to zero

    f = open(FILE, 'r')

    q = fillUpQueue(f, q) #Fill up the queue with requests. Each request has the cylinder number and an accumulated  time. 

    f.close()

    i = len(q.REQUESTS)

    with open (FILE, 'r') as f:
        for j in range(j, i):
            next(f)
        for line in f:
            line = int(line)
            requestIndex = cscanOrdering(q, start)
            request = q.REQUESTS[requestIndex]
            q.REQUESTS.pop(requestIndex)

            distance = abs(start - request.cylinderNum)

            if distance == 0:
                time = LATENCY
            else:
                time = ((1) * 2) + (distance * 0.15) + LATENCY

            totTime = totTime + (request.accumTime + time)

            q = addTimeToAll(q, time)
            q.REQUESTS.append(Request(line, 0))
            start = request.cylinderNum
            q.rNum = q.rNum + 1
    
    while (len(q.REQUESTS) != 0):
            requestIndex = cscanOrdering(q, start) #Pick next appropiate cylinder based on the algorithm
            request = q.REQUESTS[requestIndex]
            q.REQUESTS.pop(requestIndex)

            distance = abs(start - request.cylinderNum) #abs( starting cylinder – ending cylinder ) 

            if distance == 0:
                time = LATENCY
            else:
                time = ((1) * 2) + (distance * 0.15) + LATENCY

            totTime = totTime + (request.accumTime + time) #Add that request's accumalated time to the grand total.

            q = addTimeToAll(q, time) #Add this time to all requests in the queue
            start = request.cylinderNum
            q.rNum = q.rNum + 1

    print ("CSCAN Q%s %.2f" % (QSIZE, totTime / q.rNum))

def fifo (start, q):
    i, j, totTime = 0,0,0 #Grand total time spent is set to zero

    f = open(FILE, 'r')

    q = fillUpQueue(f, q) #Fill up the queue with requests. Each request has the cylinder number and an accumulated  time. 

    f.close()

    i = len(q.REQUESTS)

    with open (FILE, 'r') as f:
        for j in range(j, i):
            next(f)
        for line in f:
            line = int(line)
            request = q.REQUESTS[0] #Pick next appropiate cylinder based on the algorithm
            q.REQUESTS.pop(0)

            distance = abs(start - request.cylinderNum) #abs( starting cylinder – ending cylinder ) 

            if distance == 0:
                time = LATENCY
            else:
                time = ((1) * 2) + (distance * 0.15) + LATENCY

            totTime = totTime + (request.accumTime + time) #Add that request's accumalated time to the grand total.

            q = addTimeToAll(q, time) #Add this time to all requests in the queue
            q.REQUESTS.append(Request(line, 0)) #Read in next request and initialize its accumalated time to zero
            start = request.cylinderNum #re-order based on the algorithm
            q.rNum = q.rNum + 1

    while (len(q.REQUESTS) != 0):
            request = q.REQUESTS[0] #Pick next appropiate cylinder based on the algorithm
            q.REQUESTS.pop(0)

            distance = abs(start - request.cylinderNum) #abs( starting cylinder – ending cylinder ) 

            if distance == 0:
                time = LATENCY
            else:
                time = ((1) * 2) + (distance * 0.15) + LATENCY

            totTime = totTime + (request.accumTime + time) #Add that request's accumalated time to the grand total.

            q = addTimeToAll(q, time) #Add this time to all requests in the queue
            start = request.cylinderNum
            q.rNum = q.rNum + 1

    print ("FIFO Q%s %.2f" % (QSIZE, totTime / q.rNum))

def sstf (start, q):
    i, j, totTime = 0,0,0 #Grand total time spent is set to zero
    
    f = open(FILE, 'r')

    q = fillUpQueue(f, q) #Fill up the queue with requests. Each request has the cylinder number and an accumulated  time. 

    f.close()

    i = len(q.REQUESTS)

    with open (FILE, 'r') as f:
        for j in range(j, i):
            next(f)
        for line in f:
            line = int(line)
            requestIndex = sstfOrdering(q, start)
            request = q.REQUESTS[requestIndex]
            q.REQUESTS.pop(requestIndex)

            distance = abs(start - request.cylinderNum) #abs( starting cylinder – ending cylinder ) 

            if distance == 0:
                time = LATENCY
            else:
                time = ((1) * 2) + (distance * 0.15) + LATENCY

            totTime = totTime + (request.accumTime + time) #Add that request's accumalated time to the grand total.

            q = addTimeToAll(q, time) #Add this time to all requests in the queue
            q.REQUESTS.append(Request(line, 0)) #Read in next request and initialize its accumalated time to zero
            start = request.cylinderNum #re-order based on the algorithm
            q.rNum = q.rNum + 1

    while (len(q.REQUESTS) != 0):
            requestIndex = sstfOrdering(q, start) #Pick next appropiate cylinder based on the algorithm
            request = q.REQUESTS[requestIndex]
            q.REQUESTS.pop(requestIndex)

            distance = abs(start - request.cylinderNum) #abs( starting cylinder – ending cylinder ) 

            if distance == 0:
                time = LATENCY
            else:
                time = ((1) * 2) + (distance * 0.15) + LATENCY

            totTime = totTime + (request.accumTime + time) #Add that request's accumalated time to the grand total.

            q = addTimeToAll(q, time) #Add this time to all requests in the queue
            start = request.cylinderNum
            q.rNum = q.rNum + 1

    print ("SSTF Q%s %.2f" % (QSIZE, totTime / q.rNum))

# SSTF ordering algorithm which chooses the next request to process based on the algorithm.
def sstfOrdering (q, start):
    i = 0
    small_distance = abs(start - q.REQUESTS[0].cylinderNum)
    smallestDistancerequest = 0

    while i < len(q.REQUESTS):
        distance = abs(start - q.REQUESTS[i].cylinderNum)

        if (distance < small_distance):
            small_distance = distance
            smallestDistancerequest = i
        i = i + 1

    return smallestDistancerequest

# CSCAN ordering algorithm which chooses the next request to process based on the algorithm.
def cscanOrdering(q, start):
    nextStartIndex = -1
    i = 0
    while i < len(q.REQUESTS):
        cylinder = q.REQUESTS[i].cylinderNum
        nextCylinder = q.REQUESTS[nextStartIndex].cylinderNum

        if (start <= cylinder and (nextStartIndex == -1 or cylinder <= nextCylinder)):
            nextStartIndex = i
        i = i + 1
    
    # When the highest numbered cylinder with a pending request has been serviced, the arm goes to 
    # the lowest-numbered cylinder with a pending request and then continues moving an an upward direction.
    # So, if the start is the highest cylinder avaliable in the queue then it goes to the smallest cylinder avaliable and go from there.
    if (nextStartIndex == -1):
        return sstfOrdering(q, 0)
    else:
        return nextStartIndex

# Fills up the queue until its filled until the given size of QSIZE
def fillUpQueue(f, q):
    i = 0

    while i < QSIZE:
        line = int(f.readline())
        q.REQUESTS.append(Request(line, 0))
        i = i + 1

    return q

# Adds the accumalated time to every request currently in the queue.
def addTimeToAll(q, time):

    for request in q.REQUESTS:
        request.accumTime += time
    
    return q

# Prints the array.
def printArray (array):
    for item in array:
        print (item)

main()