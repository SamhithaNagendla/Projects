/*Imported packages to support the functionality implemented.*/
import org.apache.spark.graphx.{Edge, EdgeRDD, Graph, GraphLoader, VertexId, VertexRDD}
import org.apache.spark.graphx.util.GraphGenerators
import org.apache.spark.SparkContext
import org.apache.spark.SparkConf
import scala.collection.mutable.ListBuffer


object Partition {
	val depth = 6
	def main(args: Array[String] ) {
		val conf = new SparkConf().setAppName("GraphAnalysis")
		val sc = new SparkContext(conf)
		
		/*To keep track of first 5 nodes while reading from the node*/
		var count = 0
		
		/*foreach list of nodes with source node and neighbors, an edgelists of source node,destination node and line number is produced.*/
		def NodeEdges(node:(List[Long],Long)): List[(Long,Long,Long)] ={
			var edge: List[(Long,Long,Long)] = List[(Long,Long,Long)]()
			for(neighbor <- node._1)
			{
				edge = (node._1.head,neighbor,node._2) :: edge
			}
			edge
		}
		
		/* read graph from args(0) and constructed RDD of edges; where arg(0) is the input file name passed through command line argument. */
		var graphInput = sc.textFile(args(0)).map(line => line.split(",")).map(nodeDetails => nodeDetails.map(_.toLong)).map(nodeDetails => nodeDetails.toList).map(nodelist => {count += 1; NodeEdges(nodelist,count)}).flatMap(edgeListDetails =>{edgeListDetails.map(edgeDetails =>{Edge(edgeDetails._1,edgeDetails._2,edgeDetails._3)})})
				
		/*Used the graph builder Graph.fromEdges to construct a graph from the RDD of edges with default value 1L*/
		val graph = Graph.fromEdges(graphInput,1L)
		
		/*To broadcast the initial cluster list to all worker nodes*/
		val initialClustersList = graph.edges.filter(edgeDetails => edgeDetails.attr <= 5).map(edgeDetails=>{edgeDetails.srcId}).distinct().collect()
		val clusterValues =sc.broadcast(initialClustersList)		
		
		/*Accessed the VertexRDD and change the value of each vertex to be the -1 except for the first 5 nodes*/
		val updatedGraph = graph.mapVertices((vertexId,_) => { if(clusterValues.value.contains(vertexId)) { vertexId } else { -1L} })
		
		/*Invoked the Graph.pregel method in the GraphX Pregel API to calculate the new cluster number for each vertex and propagate this number to the neighbors.
		For each vertex, this method changes its cluster number to the max cluster number of its neighbors only if the current cluster number is -1.*/
		val finalGraph = updatedGraph.pregel(-1L,maxIterations = depth)(
        (_,centroid,newCentroid)=> {
          if(centroid == -1L)
            newCentroid
          else
            centroid
        },
        triplet => {
          Iterator((triplet.dstId,triplet.srcAttr))
        },
        (m,n)=> Math.max(m,n)
		)
		
		/*Grouping the graph vertices by their cluster number and print the partition sizes*/
		finalGraph.vertices.map(vertexDetail => (vertexDetail._2,1)).reduceByKey(_+_).collect().foreach(println)
		
		sc.stop()
  }
}

