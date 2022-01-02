/*Imported packages to support the functionality implemented.*/

import org.apache.spark.SparkContext
import org.apache.spark.SparkConf
import org.apache.spark.rdd.PairRDDFunctions

object KMeans {

	/*Defining the Point type*/
	type Point = (Double,Double)
	
	/*For Centroids values*/
	var centroids: Array[Point] = Array[Point]()
	
	/*For Points values*/
	var points: Array[Point] = Array[Point]()
	
	/*For Partition values*/
	var partition:Array[(KMeans.Point, KMeans.Point)] = Array[(KMeans.Point, KMeans.Point)]()
	
	/*To convert it into Point type*/
	def toPoint(x:Double,y:Double):Point ={(x,y)}
	
	/*To calculate the distance between two points*/
	def distance (c:Point,p:Point):Double = {
		var dist:Double =0.0
		dist = ((c._1 - p._1)* (c._1 - p._1)) + ((c._2 - p._2)* (c._2 - p._2))
		return dist
	}
	
	/*To calculate new average value for new set of centroid values*/
	def average(x:Iterable[KMeans.Point]):Point = {
		var y:Iterable[KMeans.Point] =x
		var sumx:Double =0.0
		var sumy:Double =0.0
		var count:Double =0.0
		for (elem <- y)
		{
			sumx =sumx +elem._1
			sumy =sumy +elem._2
			count +=1
		}
		return toPoint(sumx/count, sumy/count)
	}
	
	def main(args: Array[ String ]) {

		val conf = new SparkConf().setAppName("KMeans")
		val sc = new SparkContext(conf)
	
		/*Read initial centroids from centroids.txt */
		centroids =  sc.textFile(args(1)).map( line => { val a = line.split(",")
                                                     val b = toPoint(a(0).toDouble,a(1).toDouble)
                                                     b } ).collect();
	
		/*Read points */
		points =  sc.textFile(args(0)).map( line => { val a = line.split(",")
                                                  val b = toPoint(a(0).toDouble,a(1).toDouble)
                                                  b } ).collect();
	
		/*Lloyd K-Means Clustering*/
	        for(i <- 1 to 5)	
                {
              
    
			/*Broadcast the centroids to worker nodes*/
			val cs =sc.broadcast(centroids)
	  
			/*Assignment Step: Partitioning the points*/
			partition = points.map { p => (cs.value.minBy(distance(p,_)),p)}
			var y = sc.parallelize(partition,1)
		
			/*Calculating the new centroid in the partitioned group of points*/
			var x  = y.groupByKey().mapValues{ p => average(p)}
			var z = x.values
                        
	
			/*Assigning newly calculated centroids*/
		        centroids = z.collect()
          
                }
	
		/*Displaying the final set of centroids*/
               centroids.foreach(println)
	}
}
