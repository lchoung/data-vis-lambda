# Citius: Interactive data visualizations with AWS Lambda
#### Lillian Choung (lchoung) and Audasia Ho (audasiah)

Citius aims to provide real-time interactive data visualizations by exploiting AWS Lambda's access to a number of highly elastic threads.

## Background

Interactive data visualization applets on the web often suffer from latency issues, especially with larger datasets. As users interact with the visualizations to explore the data input, there may be lags between UI actions such as knob sliding/dropdown selection to adjust parameters and the corresponding update. The members of this team have experienced this with R Shiny interactive plots and D3.

We aim to create a serverless data visualization backend using AWS Lambda. Lambda allows clients to spin up threads running functions quickly, as a response to a trigger event. We can employ thousands of these threads to run parallel data processing jobs, since Lambda threads are able to send messages between them. To demonstrate the concept, we aim to provide live web demos for k-clustering and potentially random forests for non-trivial problem size N. 

## Challenge

### Workload
We must write a parallel algorithm for the k-clustering problem that will be able to accommodate an elastic number of threads that will be running. In each iteration of the algorithm threads will be used to compute the distance between data points and cluster centers. Once data points are reassociated, we must communicate this change to other threads that are computing other clusters in order to recalculate the new means for other clusters. We must be able to efficiently parallelize the computations of the distance and mean, and then pass messages between the threads in order to communicate changes in the clustering of the data. Furthermore, we must figure out how to decide how many threads we want working at a time, depending on how much work needs to be done and what the overhead of having many threads communicating with each other is.

### Constraints
AWS Lambda was created with a few design decisions that reflect its purpose as a on-demand short running thread service, but become limitations that we need to work around in order to perform parallel tasks with it. Each individual function is limited to 1.5 GB of memory and 300 seconds runtime. The time limit is less of a concern because our data sets will not be large enough that analyzing a small subset of the set will take more than 5 minutes. However, we have to make sure each of our algorithms is fine-grained enough so that we can store each working subset in the memory we have. We will also need to write a master program that runs on S3 that will schedule work onto these elastic threads and manage communication between them.

## Resources
We are referencing several sources to gather research on best practices with running parallel jobs on Lambda. Although this is a relatively new idea, we found a few relevant links for background/research:

- [Serverless MapReduce](http://tothestars.io/blog/2016/11/2/serverless-mapreduce)
- [Video Encoding Paper](https://www.usenix.org/conference/nsdi17/technical-sessions/presentation/fouladi)
- [Building Scalable and Responsive Big Data Interfaces with AWS Lambda](https://aws.amazon.com/blogs/big-data/building-scalable-and-responsive-big-data-interfaces-with-aws-lambda/)

The code we write will be mainly from scratch, referencing the AWS Lambda documentation and using the standard parallel algorithms for the data analysis backend:

- [k-Clustering](insertpaperhere.com)
- [Random Forests](somepaperhere.com)

## Goals and Deliverables

The main question we'd like to answer in this project is: "Can interactive data visualization benefit from a serverless highly elastic backend?" 

Our deliverables for this project include running k-clustering on AWS Lambda, with an interactive UI that allows the user to change parameters and see a rapid update of the visualiation. We will test on self-generated datasets ranging from 10 to 50 parameters and various n. We will also benchmark on the [Census-Income Dataset](https://archive.ics.uci.edu/ml/datasets/Census-Income+(KDD)), against the corresponding R Shiny version of the visualization and a serial Python based backend. 

If we are successful in this first part, we will move on to explore other algorithms on AWS Lambda, such as random forests. 

## Platform Choice
We have decided to either use Python or C to implement this project.

## Schedule
#### 04.10.17
Finish project proposal and scope out project.
#### 04.17.17
Go through all resources and sketch out what our worker algorithm will look like. Figure out how to use AWS Lambda. Sketch out our master program that will be running on S3 to allocate work to threads. Benchmark R Shiny version of the visualization in order to compare our project to in the future.
#### 04.24.17
Write, benchmark, and interate on our implementation for worker and master programs. Write Project Checkpoint.
#### 05.01.17
Create interactive visualization of k-clustering problem that will allow users to change parameters. Try to connect our programs to the visualization.
#### 05.08.17
Benchmark our project and make sure everything works. Start putting together final project presentation.
#### 05.12.17
Final project presentation.

