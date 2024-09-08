# Image-Skeletonisation
Image Skeletonisation (Image Processing) using Breadth-First Search


##### +-----------------------------------+-----------+-----------+-----------+-----------------------+
##### | Skeletonisation (blob)            | Matrix    | BFS       | DFS       | Best First Search     |
##### +-----------------------------------+-----------+-----------+-----------+-----------------------+
##### | Total Pixel Updates               | 1337      | 1339      | 1325      |                       |
##### | Total Zhang-Suen Condition Checks | 249704    | 5375      | 5371      |                       |
##### | Maximum Boundary Stack Size       | -         | 640       | 581       | -                     |
##### | Total Time Taken (s)              | 0.2199    | 0.0314    | 0.0199    |                       |
##### +-----------------------------------+-----------+-----------+-----------+-----------------------+

##### +-----------------------------------+-----------+-----------+-----------+-----------------------+
##### | Skeletonisation (dots)            | Matrix    | BFS       | DFS       | Best First Search     |
##### +-----------------------------------+-----------+-----------+-----------+-----------------------+
##### | Total Pixel Updates               | 1923      | 1884      | 1889      | -                     |
##### | Total Zhang-Suen Condition Checks | 288120    | 7573      | 7586      | -                     |
##### | Maximum Boundary Stack Size       | -         | 1048      | 1139      | -                     |
##### | Total Time Taken (s)              | 0.2519    | 0.0475    | 0.0515    | -                     |
##### +-----------------------------------+-----------+-----------+-----------+-----------------------+

##### +-----------------------------------+-----------+-----------+-----------+-----------------------+
##### | Skeletonisation (hand)            | Matrix    | BFS       | DFS       | Best First Search     |
##### +-----------------------------------+-----------+-----------+-----------+-----------------------+
##### | Total Pixel Updates               | 1880      | 1882      | 1872      | -                     |
##### | Total Zhang-Suen Condition Checks | 230496    | 7981      | 7962      | -                     |
##### | Maximum Boundary Stack Size       | -         | 1163      | 1318      | -                     |
##### | Total Time Taken (s)              | 0.2057    | 0.0362    | 0.0308    | -                     |
##### +-----------------------------------+-----------+-----------+-----------+-----------------------+

##### +-----------------------------------+-----------+-----------+-----------+-----------------------+
##### | Skeletonisation (horse)           | Matrix    | BFS       | DFS       | Best First Search     |
##### +-----------------------------------+-----------+-----------+-----------+-----------------------+
##### | Total Pixel Updates               | 3295      | 3202      | 3222      | -                     |
##### | Total Zhang-Suen Condition Checks | 268912    | 13714     | 13781     | -                     |
##### | Maximum Boundary Stack Size       | -         | 1840      | 2155      | -                     |
##### | Total Time Taken (s)              | 0.2480    | 0.0611    | 0.0562    | -                     |
##### +-----------------------------------+-----------+-----------+-----------+-----------------------+

##### +-----------------------------------+-----------+-----------+-----------+-----------------------+
##### | Skeletonisation (tree)            | Matrix    | BFS       | DFS       | Best First Search     |
##### +-----------------------------------+-----------+-----------+-----------+-----------------------+
##### | Total Pixel Updates               | 1718      | 1642      | 1643      | -                     |
##### | Total Zhang-Suen Condition Checks | 115248    | 8769      | 8777      | -                     |
##### | Maximum Boundary Stack Size       | -         | 3175      | 3640      | -                     |
##### | Total Time Taken (s)              | 0.1143    | 0.0572    | 0.0410    | -                     |
##### +-----------------------------------+-----------+-----------+-----------+-----------------------+

Image: connectfour

BFS
Number of iterations: 10
Total pixel updates: 1667
Total Zhang-Suen condition checks: 7251
Maximum boundary queue size: 1735
Total time taken (seconds): 0.0335848331451416

DFS
Number of iterations: 8
Total pixel updates: 1639
Total Zhang-Suen condition checks: 7231
Maximum boundary stack size: 1951
Total time taken (seconds): 0.034010887145996094

Matrix
Number of iterations: 7
Total pixel updates: 1702
Total Zhang-Suen condition checks: 134456
Total time taken (seconds): 0.1218

Image: fist

BFS
Number of iterations: 18
Total pixel updates: 1191
Total Zhang-Suen condition checks: 4845
Maximum boundary queue size: 458
Total time taken (seconds): 0.02359795570373535

DFS
Number of iterations: 18
Total pixel updates: 1167
Total Zhang-Suen condition checks: 4824
Maximum boundary stack size: 460
Total time taken (seconds): 0.030808210372924805

Matrix
Number of iterations: 12
Total pixel updates: 1185
Total Zhang-Suen condition checks: 230496
Total time taken (seconds): 0.2020

Image: lines

BFS
Number of iterations: 12
Total pixel updates: 1214
Total Zhang-Suen condition checks: 6071
Maximum boundary queue size: 2595
Total time taken (seconds): 0.031323909759521484

DFS
Number of iterations: 12
Total pixel updates: 1217
Total Zhang-Suen condition checks: 6075
Maximum boundary stack size: 2957
Total time taken (seconds): 0.028782129287719727

Matrix
Number of iterations: 8
Total pixel updates: 1321
Total Zhang-Suen condition checks: 153664
Total time taken (seconds): 0.1429

Image: multi_shapes

BFS
Number of iterations: 14
Total pixel updates: 3275
Total Zhang-Suen condition checks: 13491
Maximum boundary queue size: 2311
Total time taken (seconds): 0.06033682823181152

DFS
Number of iterations: 14
Total pixel updates: 3234
Total Zhang-Suen condition checks: 13492
Maximum boundary stack size: 2573
Total time taken (seconds): 0.04505658149719238

Matrix
Number of iterations: 13
Total pixel updates: 3293
Total Zhang-Suen condition checks: 249704
Total time taken (seconds): 0.2232


Image: shape

BFS
Number of iterations: 16
Total pixel updates: 3313
Total Zhang-Suen condition checks: 14052
Maximum boundary queue size: 2081
Total time taken (seconds): 0.08843183517456055

DFS
Number of iterations: 15
Total pixel updates: 3312
Total Zhang-Suen condition checks: 14066
Maximum boundary stack size: 2213
Total time taken (seconds): 0.054579973220825195

Matrix
Number of iterations: 9
Total pixel updates: 3363
Total Zhang-Suen condition checks: 172872
Total time taken (seconds): 0.1591
