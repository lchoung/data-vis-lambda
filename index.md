# Serverless Map + Reduce with AWS Lambda
#### Lillian Choung (lchoung) and Audasia Ho (audasiah)

We aim to demonstrate the power of AWS Lambda's microservice platform for serverless computing. Our focus is upon massively parallel map and map/reduce problems, and we benchmark against typical personal computers (4-core MacBook Pro) and more powerful academic computers (CMU linux.andrew.cmu.edu with 40 cores).

**The main challenge of this project is to work around the memory, communication, and concurrent execution limits (1000 parallel jobs) to identify use cases where using Amazon Lambda would be preferable over running your own multi-core servers.** The ideal algorithm can be uploaded to Lambda via a zipped deployment package of under 50 MB including scientific packages. Each lambda call itself cannot use more than 512 MB of space. Most importantly, each driver to Lambda and Lambda to S3 (AWS storage filesystem) communication unit happens across a HTTP network, which means our system is quite bandwidth limited. (Implementation wise, deployment was tricky with scientific libraries, since Lambda's original purpose is to process in short 100-500ms bursts, event-triggered requests, not do scientific computation)

## Intermediate Results

### Random Forest
We identified Random Forest as a good algorithm to run on Amazon Lambda. This algorithm trains a random forest by computing n independent trees, basically a map. An individual tree during sequential evaluation took about 8 seconds to train,on our 4-core and 40-core machine, and 16 seconds on Amazon Lambda. The extra 8 seconds Lambda requires is due to communicating the driver's requests over HTTP, and the short but non-trivial time it takes for the lambda function to boot and open all the included scientific libraries.

The tree creating process is computationally intensive, since at each step it searches for local optimum for all data points across the feature space. But crucially, all trees are independent. This means that the 4-core implementation on our personal machinse is consistently faster than the Lambda process implementation for up to 8 trees. However, past n = 8 trees, **the amount of time the Lambda uses levels off to 16-20 seconds per random forest**, while the personal machine implementation doubles in time with each double in size of tree. With a limited number of cores, the personal machine can only run tree computations for as many contexts are available on the machine. But Lambda can compute all of them simultaneously and is bottlenecked by the speed by which it can communicate with the local driver. However, we also observed high variance in the runtime of each n number of trees on AWS Lambda, since we have no control of how AWS Lambda chooses to schedule, run, and pause the function calls. 

![RF Graph](http://i.imgur.com/dHw3Bbi.png)

### Mandelbrot Set (TO WRITE) 
### Map-Reduce with S3 temp files (TO DO) 

## Details of Implementation (TO WRITE) 


# Checkpoint

After submitting our project proposal, we went to meet with Kayvon in order to discuss the feasibility of our project and to ask for advice. We decided to slightly modify our project after our discussion with Kayvon. 

First, we will be implementing the random forest algorithm. We want to see if it is worth it to run this algorithm on Amazon Lambda, and if we would get more speedup running the algorithm on Lambda than we would running it on a Macbook Pro. We have updated our proposal and schedule in the proposal section below accordingly.

We decided to choose the random forest algorithm, as it handles a lot of data but it is straightforward to parallelize, with not that much communication necessary between the different parts. We wanted to implement an algorithm that was arithmetically intense, which would benefit the most from parallelism. 

So far, we have implemented a sequential and parallel version of the random forests tree generation to be run on the Macbook Pro. We have seen a 4x speedup from the parallel version running on a 4-core machine, which means that we have parallelized it for the Macbook (as seen below).

![Speedup](https://scontent.fagc1-2.fna.fbcdn.net/v/t35.0-12/18120508_1504818782861963_830733573_o.png?oh=9f9f5792d484688a5ae3fc562ec58aed&oe=59150AB3 "4x speedup")

In order to do the above, we had to gather the data from the Lending Club Loan Data, and then first clean the data in order to make it usable for our purposes. Then, we implemented the sequential version of the tree generation algorithm, as seen in [this youtube video](https://www.youtube.com/watch?v=loNcrMjYh64). We then used multiprocessing in python in order to parallelize the data for the 4-core machine (Macbook).

We believe that we will be able to finish implementing the random forests algorithm in Lambda and be able to see if running this algorithm on Lambda is beneficial and worth it. We would like to be able to also implement another algorithm, possibly Mandelbrot, as another comparison for the usage of Lambda. 

For the final presentation we would like to have a graph that illustrates the benefit of using Lambda for these algorithms, while also taking into account the monetary cost that it will take to run them on Lambda. 

Currently we are having issues with figuring out how exactly to use Lambda to run our parallel code, as we realized we have to include some Python libraries. However, we have found resources showing us how to package in Python libraries that are dependencies, so we should be able to finish this part quite soon.


# Proposal

## Background

**UPDATE:**
We aim to find a use case that will run faster and better on AWS Lambda when compared to a typical 4-core machine (Macbook Pro).

-------

Interactive data visualization applets on the web often suffer from latency issues, especially with larger datasets. As users interact with the visualizations to explore the data input, there may be lags between UI actions such as knob sliding/dropdown selection to adjust parameters and the corresponding update. The members of this team have experienced this with R Shiny interactive plots and D3.

We aim to create a serverless data visualization backend using AWS Lambda. Lambda allows clients to spin up threads running functions quickly, as a response to a trigger event. We can employ thousands of these threads to run parallel data processing jobs, since Lambda threads are able to send messages between them. To demonstrate the concept, we aim to provide live web demos for k-clustering and potentially random forests for non-trivial problem size N. 

## Challenge

**UPDATE:**
We will be writing a parallel algorithm for the random forest problem that we will first run on a Macbook Pro. Using a sequential algorithm for benchmarking, we will then see if running the same algorithm with optimizations on AWS Lambda will be faster and more optimal. We will be using the dataset from [Lending Club Loan Data](https://www.kaggle.com/wendykan/lending-club-loan-data) in order to generate decision trees for the random forest problem. 

-------

### Workload
We must write a parallel algorithm for the k-clustering problem that will be able to accommodate an elastic number of threads that will be running. In each iteration of the algorithm threads will be used to compute the distance between data points and cluster centers. Once data points are reassociated, we must communicate this change to other threads that are computing other clusters in order to recalculate the new means for other clusters. We must be able to efficiently parallelize the computations of the distance and mean, and then pass messages between the threads in order to communicate changes in the clustering of the data. Furthermore, we must figure out how to decide how many threads we want working at a time, depending on how much work needs to be done and what the overhead of having many threads communicating with each other is.

### Constraints
AWS Lambda was created with a few design decisions that reflect its purpose as a on-demand short running thread service, but become limitations that we need to work around in order to perform parallel tasks with it. Each individual function is limited to 1.5 GB of memory and 300 seconds runtime. The time limit is less of a concern because our data sets will not be large enough that analyzing a small subset of the set will take more than 5 minutes. However, we have to make sure each of our algorithms is fine-grained enough so that we can store each working subset in the memory we have. We will also need to write a master program that runs on a server + S3 that will schedule work onto these elastic threads and manage communication between them.

## Resources
We are referencing several sources to gather research on best practices with running parallel jobs on Lambda. Although this is a relatively new idea, we found a few relevant links for background/research:

- [Serverless MapReduce](http://tothestars.io/blog/2016/11/2/serverless-mapreduce)
- [Video Encoding Paper](https://www.usenix.org/conference/nsdi17/technical-sessions/presentation/fouladi)
- [Building Scalable and Responsive Big Data Interfaces with AWS Lambda](https://aws.amazon.com/blogs/big-data/building-scalable-and-responsive-big-data-interfaces-with-aws-lambda/)

The code we write will be mainly from scratch, referencing the AWS Lambda documentation and using the standard parallel algorithms for the data analysis backend:

- [k-Clustering](insertpaperhere.com)
- [Random Forests](somepaperhere.com)

## Goals and Deliverables

**UPDATE:**
The main question we'd like th answer in this project is: "Is there a use case for AWS Lambda such that it runs better on Lambda than on a typical 4-core machine?"

Our deliverables for this project include a sequential and parallel version of random forest, running on a Macbook Pro, and then the code that we run on AWS Lambda. We will then compare and see if we can get much better speedup on Lambda than from running the same problem on a Macbook Pro.

If we are successful with the random forest problem. we will move on to attempt to implement another algorithm for AWS Lambda, possibly Mandelbrot. 

-------

The main question we'd like to answer in this project is: "Can interactive data visualization benefit from a serverless highly elastic backend?" 

Our deliverables for this project include running k-clustering on AWS Lambda, with an interactive UI that allows the user to change parameters and see a rapid update of the visualiation. We will test on self-generated datasets ranging from 10 to 50 parameters and various n. We will also benchmark on the [Census-Income Dataset](https://archive.ics.uci.edu/ml/datasets/Census-Income+(KDD)), against the corresponding R Shiny version of the visualization and a serial Python based backend. 

If we are successful in this first part, we will move on to explore other algorithms on AWS Lambda, such as random forests. 

## Platform Choice
We have decided to use Python to implement this project, to run on Lambda.

## Schedule
#### 04.10.17
Finish project proposal and scope out project.
#### 04.17.17
Find an algorithm that we feel is arithmetically intensive but parallelizable for Lambda. Implement the sequential version and parallel version for the Macbook and benchmark it.
#### 04.24.17
Implement the parallel version of the algorithm for Lambda and see if it is faster. Write Project Checkpoint.

-----

#### 04.27.17
Implement sequential and parallel version of another algorithm for testing. [Audasia] 
Finish implementing parallel version of random forest for Lambda. [Lilli]
#### 05.01.17
Implement parallel Lambda version of second algorithm and run on Lambda, benchmark [Audasia, Lilli]
#### 05.04.17
Create graphs and visuals for comparing the differences in runtime of different algorithms [Audasia, Lilli]
#### 05.08.17
Benchmark our project and make sure everything works. Start putting together final project presentation. [Team]
#### 05.12.17
Final project presentation.

