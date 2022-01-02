/*Imported packages to support the functionality implemented.*/

import org.apache.spark.SparkContext
import org.apache.spark.SparkConf
import org.apache.spark.rdd.RDD._
import scala.collection.mutable.ListBuffer
import scala.math

object Partition {

  val depth = 6

  def main ( args: Array[ String ] ) {
	val conf = new SparkConf().setAppName("GraphAnalysis")
	val sc = new SparkContext(conf)
	
	/*To keep track of first 5 nodes while reading from the node*/
	var count = 0
	
    /* read graph from args(0); the graph cluster ID is set to -1 except for the first 5 nodes */
    var graph = sc.textFile(args(0)).map(line => line.split(",")).map(nodeDetails => nodeDetails.map(_.toLong)).map(nodeDetails => nodeDetails.toList).map(nodelist => if (count < 5) {count += 1;(nodelist.head, nodelist.head, nodelist.tail)} else {count += 1;(nodelist.head, -1.toLong, nodelist.tail)})
	
	/*This function takes a node ( id, cluster, adjacent) in the graph and returns (id,cluster) along with all (x,cluster) for all x in adjacent if cluster!=-1.*/
    def nodeSplit(node: (Long, Long, List[Long])) = {
      var nodes = new ListBuffer[(Long, Long)]
      var id = (node._1, node._2)
      nodes += id 
      if (node._2 > 0) {
        for (adjacentList <- node._3) {
          id = (adjacentList, node._2)
          nodes += id
        }
      }
      nodes
    }
	
    for (i <- 1 to depth)
       graph = graph.flatMap{ nodeSplit(_) }
                    .reduceByKey(_ max _)
                    .join( graph.map{ case (id,cluster,adjacentList) => (id,(cluster,adjacentList)) })
                    .map{ case (id,(newclusterid,(oldclusterid,adjacentList))) => if (oldclusterid == -1.toLong) {(id,newclusterid,adjacentList)} else {(id,oldclusterid,adjacentList)} }

    /* finally, print the partition sizes */
	graph.map(finalnode => (finalnode._2, 1)).reduceByKey(_ + _).collect().foreach(println)
  }
}
