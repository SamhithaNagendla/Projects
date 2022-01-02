/*Loading data from input file specified through parameter G, while running the program*/
InputFile = LOAD '$G' USING PigStorage(',') AS (node1:double, node2:double);

/*Grouping InputFile consisting of node1, node2 by node1.*/
Node1Group = GROUP InputFile BY node1;

/*Generating group as node and count of records in each group as nodeCount from Node1Group.*/
CountNodes = FOREACH Node1Group GENERATE group AS node:double, COUNT(InputFile) AS nodeCount:double;

/*Generating nodeCount as neighbor and 1 as neighborcount from CountNodes.*/
SumCountNodes = FOREACH CountNodes GENERATE nodeCount AS neighbor:double, 1 AS  neighborcount:double;

/*Grouping SumCountNodes consisting of neighbor,neighborcount by neighbor.*/
NeighborGroup = GROUP SumCountNodes BY neighbor;

/*Generating group as neigh and sum of neighborcount in SumCountNodes as neighc from NeighborGroup. Type casted the neigh and neighc as integer*/
CountNodes = FOREACH NeighborGroup GENERATE group AS neigh:int, SUM(SumCountNodes.neighborcount) as neighc:int;
STORE CountNodes INTO '$O' USING PigStorage ('	');  
/*Stored the output seperated by tab space in the file specified through parameter O*/