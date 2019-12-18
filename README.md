# SFND 2D Feature Tracking

<img src="images/keypoints.png" width="820" height="248" />

The idea of the camera course is to build a collision detection system - that's the overall goal for the Final Project. As a preparation for this, you will now build the feature tracking part and test various detector / descriptor combinations to see which ones perform best. This mid-term project consists of four parts:

* First, you will focus on loading images, setting up data structures and putting everything into a ring buffer to optimize memory load. 
* Then, you will integrate several keypoint detectors such as HARRIS, FAST, BRISK and SIFT and compare them with regard to number of keypoints and speed. 
* In the next part, you will then focus on descriptor extraction and matching using brute force and also the FLANN approach we discussed in the previous lesson. 
* In the last part, once the code framework is complete, you will test the various algorithms in different combinations and compare them with regard to some performance measures. 

See the classroom instruction and code comments for more details on each of these parts. Once you are finished with this project, the keypoint matching part will be set up and you can proceed to the next lesson, where the focus is on integrating Lidar points and on object detection using deep-learning. 

## Dependencies for Running Locally
* cmake >= 2.8
  * All OSes: [click here for installation instructions](https://cmake.org/install/)
* make >= 4.1 (Linux, Mac), 3.81 (Windows)
  * Linux: make is installed by default on most Linux distros
  * Mac: [install Xcode command line tools to get make](https://developer.apple.com/xcode/features/)
  * Windows: [Click here for installation instructions](http://gnuwin32.sourceforge.net/packages/make.htm)
* OpenCV >= 4.1
  * This must be compiled from source using the `-D OPENCV_ENABLE_NONFREE=ON` cmake flag for testing the SIFT and SURF detectors.
  * The OpenCV 4.1.0 source code can be found [here](https://github.com/opencv/opencv/tree/4.1.0)
* gcc/g++ >= 5.4
  * Linux: gcc / g++ is installed by default on most Linux distros
  * Mac: same deal as make - [install Xcode command line tools](https://developer.apple.com/xcode/features/)
  * Windows: recommend using [MinGW](http://www.mingw.org/)

## Basic Build Instructions

1. Clone this repo.
2. Make a build directory in the top level directory: `mkdir build && cd build`
3. Compile: `cmake .. && make`
4. Run it: `./2D_feature_tracking`.


## REPORT

NOTES:
I have implemented a python3 script that runs various combinations of detectors and descriptors to collect all the necessary data for analysis. Then it analysis the individual detection, extraction times as well as average time spent for each step. Based on the calculations, it sorts the collected data and reports top 3 detectors, descriptors and combinations of both. Invalid combinations will be reported and no data will be collected for them.

The script also analyzes number of detected and extracted keypoints for MP7 and MP8 parts.
To run the script, first all the dependencies need to be installed, such as tabulate:
        pip install tabulate
        pip3 install tabulate

from 'tools' directory, execute 'python3 analyze.py | tee result.txt'. it will dump results to both stdout and save the results in result.txt file as well.


* Data Buffer:
  * MP.1 Data Buffer Optimization:
        vector<template T> STL container allows to remove elements from vector specified with an iterator. Hence, if size of vector is greater than 1, then we should remove the first element and push_back the new element.


* Keypoints:
  * MP.2 Keypoint Detection:
        OpenCV has majority of the detectors/descriptors implemented. Every detector implements "FeatureDetector" interface in their own namespaces. To create a detector, create() function needs to be called which return a shared pointer to "cv::FeatureDetector" (the object gets destructed once it gets out of scope - RAII). The namespace is chosen based on the string parameter that specifies detector type.
        For "Harris" detector, I have used the implementation from Lesson 4 quiz. Hence, it has its own execution path; detKeypointsModern() will call detKeypointsHarris() if type "HARRIS" is specified. As soon as detKeypointsHarris() returns, detKeypointsModern() will return as well.

  * MP.3 Keypoint Removal
        The preceding vehicle is expected to be within rectangle of (535, 180, 180, 150). The class cv::Rect has a member function "bool contains(cv::Point)". For every keypoint we have detected, we have to check whether rectangle contains that point. If yes, we add the point to a new list. Creating a new list and pushing inliers is much cheaper than just removing element from list (easy to read, maintain, and might be faster if erase() is not O(1))

* Descriptors:
  * MP.4 Keypoint Descriptors:
        Similar to detectors, we can use create() function to create a descriptor. Based on the specified type via a string parameter, we can call create() from appropriate namespace.

  * MP.5 FLANN matching:
        FLANN based matching was implemented similarly to the implementation on one of the tutorial codes. Because FLANN expects floating point values, results of binary detectors need to be converted to float type before creating the matcher.
        K nearest neighbouring match requires k == 1 if cross check is enabled, otherwise we can use k == 2.
  * MP.6 Descriptor Distance Ratio:
        Simply, we go through every matched keypoint pair and keep those satisfying inequaltiy D0 lt R * D1 where D0 and D1 are distances between descriptors in images img0 and img1 respectively.

* Performance
  * MP.7 Performance Evaluation 1: Number of nodes detected for each image

        DETECTOR    img1    img2    img3    img4    img5    img6    img7    img8    img9    img10
        ----------  ------  ------  ------  ------  ------  ------  ------  ------  ------  -------
        SHITOMASI   n=1370  n=1301  n=1361  n=1358  n=1333  n=1284  n=1322  n=1366  n=1389  n=1339
        HARRIS      n=118   n=101   n=117   n=121   n=163   n=417   n=85    n=216   n=174   n=303
        BRISK       n=2757  n=2777  n=2741  n=2735  n=2757  n=2695  n=2715  n=2628  n=2639  n=2672
        ORB         n=500   n=500   n=500   n=500   n=500   n=500   n=500   n=500   n=500   n=500
        FAST        n=5063  n=4952  n=4863  n=4840  n=4856  n=4899  n=4870  n=4868  n=4996  n=4997
        AKAZE       n=1351  n=1327  n=1311  n=1351  n=1360  n=1347  n=1363  n=1331  n=1357  n=1331
        SIFT        n=1438  n=1371  n=1380  n=1335  n=1305  n=1370  n=1396  n=1382  n=1463  n=1422 

  * MP.8 Performance Evaluation 2: Number of nodes matched via KNN matching with distance ration 0.8

        DETECTOR    DESCRIPTOR    img1      img2    img3    img4    img5    img6    img7    img8    img9    img10
        ----------  ------------  ------  ------  ------  ------  ------  ------  ------  ------  ------  -------
        SHITOMASI   BRISK         -           95      88      80      90      82      79      85      86       82
        SHITOMASI   BRIEF         -          115     111     104     101     102     102     100     109      100
        SHITOMASI   ORB           -          106     102      99     102     103      97      98     104       97
        SHITOMASI   FREAK         -           36      46      43      37      32      44      38      42       44
        HARRIS      BRISK         -            9      11      12      11      16       9       9      14       15
        HARRIS      BRIEF         -            9      12      14      16      19      12      13      20       22
        HARRIS      ORB           -            5       7       7       7       7      11       3       5        9
        HARRIS      FREAK         -            5       5       7       4       8       8       2      10        7
        HARRIS      SIFT          -            8      10      15      10      16      22      10      20       19
        BRISK       BRISK         -          171     176     157     176     174     188     173     171      184
        BRISK       BRIEF         -          178     205     185     179     183     195     207     189      183
        BRISK       ORB           -          162     175     158     167     160     182     167     171      172
        BRISK       FREAK         -           60      72      72      70      70      78      82      88       84
        ORB         BRISK         -           73      74      79      85      79      92      90      88       91
        ORB         BRIEF         -           49      43      45      59      53      78      68      84       66
        ORB         ORB           -           67      70      72      84      91     101      92      93       93
        ORB         FREAK         -           37      33      26      26      29      46      50      52       52
        FAST        BRISK         -          256     243     241     239     215     251     248     243      247
        FAST        BRIEF         -          320     332     299     331     276     327     324     315      307
        FAST        ORB           -          307     308     298     321     283     315     323     302      311
        FAST        FREAK         -          119     150     136     140     122     144     149     125      149
        AKAZE       BRISK         -          137     125     129     129     131     132     142     146      144
        AKAZE       BRIEF         -          141     134     131     130     134     146     150     148      152
        AKAZE       ORB           -          131     129     127     117     130     131     137     135      145
        AKAZE       FREAK         -           42      50      44      44      53      54      64      67       65
        AKAZE       AKAZE         -          138     138     133     127     129     146     147     151      150
        SIFT        BRISK         -           57      63      58      61      55      52      54      63       73
        SIFT        BRIEF         -           63      72      64      66      52      57      72      67       84
        SIFT        FREAK         -           27      26      33      23      30      30      24      26       26
        SIFT        SIFT          -           82      81      85      93      90      81      82     102      104

  * MP.9 Performance Evaluation 3: Following three sections show average detection, extraction and total time respectively
    * Top 3 detectors based on average time spent to detect keypoints:
        DETECTOR      AVG TIME
        ----------  ----------
        FAST           1.26238
        SHITOMASI      6.37259
        ORB            7.47327

    * Top 3 extractors based on average time spent to extract keypoints
        DESCRIPTOR      AVG TIME
        ------------  ----------
        BRIEF           0.305372
        BRISK           0.465473
        ORB             0.536162

    * Top 3 detector and extractor combinations based on average total time spent to detect and extract keypoints
        DETECTOR    DESCRIPTOR      AVG TIME
        ----------  ------------  ----------
        FAST        BRIEF            1.94783
        FAST        ORB              2.13265
        FAST        BRISK            4.32396
