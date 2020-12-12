from pyspark.sql import SparkSession
import re
import sys


def parseNeighbors(line):
    """Parses a urls pair string into urls pair."""
    parts = re.split(r'\s+', line)
    return int(parts[0]), (int(parts[1]), float(parts[2]))
    #return parts[0], parts[1]


def gettingNeighbors(line):
    parts = re.split(r'\s+', line)
    return int(parts[1]), 0


def probs_compute(l, prob, n, id):
    if len(l)==1:
        for k in range(1, n+1):
            if k!= id:
                yield (k, prob*1/(n-1))
    elif len(l)>1:
        query= list(l)[0]
        sum= 0
        for obj in query:
            if obj!=0:
                sum+= obj[1]

        for obj in query:
            if obj != 0:
                yield (obj[0], prob*obj[1]/sum)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: pagerank <file> <teleport-probability> <max-iterations> <convergence-threshold>", file=sys.stderr)
        sys.exit(-1)

    alpha= float(sys.argv[2])
    iters= int(sys.argv[3])
    beta= float(sys.argv[4])

    spark = SparkSession.builder.appName("SimpleApp").getOrCreate()
    sc= spark.sparkContext

    lines = spark.read.text(sys.argv[1]).rdd.map(lambda r: r[0])
    lines= sc.parallelize(lines.collect(), 4)
    links1 = lines.map(lambda line: parseNeighbors(line)).distinct().groupByKey()
    links2 = lines.map(lambda line: gettingNeighbors(line)).distinct()
    links= links1.union(links2).groupByKey()
    n= links.count()
    links = sc.parallelize(links.collect(), 4).cache()

    probs = links.map(lambda neighbors: (neighbors[0], 1/n))


    for iter in range(iters):
        contribs= links.join(probs).flatMap(lambda neighbors: probs_compute((neighbors[1][0]), neighbors[1][1], n, neighbors[0]))
        probs_new= contribs.reduceByKey(lambda x, y: x+y).mapValues(lambda rank: rank * (1-alpha) + alpha/n)

        probs_new.saveAsTextFile("./Breakpoints/iteration%i.txt" %(iter))

        b= probs.union(probs_new).reduceByKey(lambda x, y: abs(x-y)).map(lambda el: (1, el[1])).reduceByKey(lambda x, y: x+y).collect()[0][1]
        if b < beta:
            probs = probs_new
            break

        probs= probs_new

    probs.saveAsTextFile("./result")

    probs_list= probs.collect()
    print("halted at iteration= "+ str(iter)+ " and beta= "+ str(b)+ " with probabilty vector :")
    print(probs_list)


