drop table Graph;

create table Graph (
  node1 int,
  node2 int)
row format delimited fields terminated by ',' stored as textfile;

load data local inpath '${hiveconf:G}' overwrite into table Graph;

SELECT A.neighbors, count(A.node1) AS countNeighbor FROM (
SELECT node1, count(node2) AS neighbors FROM Graph GROUP BY node1) A GROUP BY A.neighbors; 
