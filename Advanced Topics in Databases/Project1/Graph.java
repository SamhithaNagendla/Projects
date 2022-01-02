/*Imported packages to support the functionality implemented.*/
import java.io.*;
import java.util.Scanner;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.mapreduce.lib.input.*;
import org.apache.hadoop.mapreduce.lib.output.*;


/*Defining the Graph class that defines mappers and reducers for counting the number of neighbors and displaying the number of nodes with same number of neighbors.*/
public class Graph {
	/*
	 * NodeMapper produces the key value pair by reading the directed edges provided in the form of the node numbers seperated by comma, through the input file.
	 * For each directed edge in the input file, a key value pair is generated with key as node1 number and value as node2 number.
	.*/
	public static class NodeMapper extends Mapper<Object,Text,IntWritable,IntWritable> {
		@Override
		public void map ( Object key, Text value, Context context ) throws IOException, InterruptedException {
			/*Reading each directed edge and extracting the node numbers that are seperated by comma.*/
			Scanner s = new Scanner(value.toString()).useDelimiter(",");
			/*Reading the node numbers of the directed edge into node1 and node1 values*/
			int node1 = s.nextInt();
			int node2 = s.nextInt();
			/*Writing the context by passing the node values read from the input file*/
			context.write(new IntWritable(node1),new IntWritable(node2));
			/*Closing the scanner ethod*/
			s.close();
			}
		}

	/*
	 * NodeReducer that takes the NodeMapper return value, as input and will generate the key and value pair as output.
	 *  The key value is the node number and the value is the neighbor counts for that node number.
	 *  Save these values as output in an intermediate folder provided as command-line arguments while running the program.
	 */
	public static class NodeReducer extends Reducer<IntWritable,IntWritable,IntWritable,IntWritable> {
		@Override
		public void reduce ( IntWritable key, Iterable<IntWritable> values, Context context ) throws IOException, InterruptedException {
			/*For each node, initially the neighbor count is set to 0*/
			int NeighborsCount = 0;
			/*for each key that is node number , the neighbors count is generated by counting the number of values with same key value.*/
			for (IntWritable v: values) {
				NeighborsCount++;
				};
			/*Writing the context by passing the node number as key and the neighbor count as value*/
			context.write(key,new IntWritable(NeighborsCount));
			}
		}
	
	/*
	 *GroupMapper takes the file generated by NodeReducer as input and will emit the neighbor count and 1 as key value pair.
	 */
	public static class GroupMapper extends Mapper<Object,Text,IntWritable,IntWritable> {
		@Override
		public void map ( Object key, Text value, Context context ) throws IOException, InterruptedException {
			/*Reading each node number and its neighbor count values from the file that are seperated by tab.*/
			Scanner s = new Scanner(value.toString()).useDelimiter("	");
			/*Reading the node number and the neighbor count numbers into Node and NeighborsCount variables*/
			int Node = s.nextInt();
			int NeighborsCount = s.nextInt();
			/*Writing the context by passing the neighbors count and value 1*/
			context.write(new IntWritable(NeighborsCount),new IntWritable(1));
			/*Closing the scanner method*/
			s.close();
			}
		}
	
	/*
	 *GroupReducer takes the emitted key value pair from GroupMapper and will count the number of nodes with same neighbors count by summation.
	 *It will emit the neighbors count and the number of neighbors with same node count.
	 *The output of this GroupReducer will be saved in an output folder provided as command-line argument while running the program
	 */	
	public static class GroupReducer extends Reducer<IntWritable,IntWritable,IntWritable,IntWritable> {
		@Override
			public void reduce ( IntWritable key, Iterable<IntWritable> values, Context context ) throws IOException, InterruptedException {
				/*Initially setting the number of nodes with same neighbor count as zero by initializing sum =0*/
				int sum = 0;
				/*For each neighbor count, the number of nodes with same neighbor count are summed up*/
				for (IntWritable v: values) {
					sum += v.get();
					};
				/*Writing the context by passing the neighbors count and the number of nodes with the same neighbors count values*/
				context.write(key,new IntWritable(sum));
				}
			}
	/*Main function of graph class that sets up the jobs*/
	public static void main ( String[] args ) throws Exception {
		/*Job to execute Map Reduce for Neighbors count for each node provided in the input file.*/
		/*Setting up the properties of job*/
		Job NeighborCountjob = Job.getInstance();
		NeighborCountjob.setJobName("NeighborCountGraphJob");
		NeighborCountjob.setJarByClass(Graph.class);
		/*Setting up the output key , value classes*/
		NeighborCountjob.setOutputKeyClass(IntWritable.class);
		NeighborCountjob.setOutputValueClass(IntWritable.class);
		/*Setting up map output key, value classes*/	    		
		NeighborCountjob.setMapOutputKeyClass(IntWritable.class);
		NeighborCountjob.setMapOutputValueClass(IntWritable.class);
		/*Setting up the Mapper and Reducer Classes*/					    		
		NeighborCountjob.setMapperClass(NodeMapper.class);
		NeighborCountjob.setReducerClass(NodeReducer.class);
		/*Setting up Input and output format classes*/								    		
		NeighborCountjob.setInputFormatClass(TextInputFormat.class);
		NeighborCountjob.setOutputFormatClass(TextOutputFormat.class);
		/*Setting the input and output paths that will be passed as command line arguments to the program*/		    		
		FileInputFormat.setInputPaths(NeighborCountjob,new Path(args[0]));
		FileOutputFormat.setOutputPath(NeighborCountjob,new Path(args[1]));
		/*Setting the property to wait for the completeion of the job*/													    		
		NeighborCountjob.waitForCompletion(true);
	
		/*Job to execute the Map Reduce for counting nodes with same number of neighbors by taking the file generated by above NodeMapper and NodeReducer using NeighborCountGraphJob. */
		Job CountGroupjob = Job.getInstance();
		CountGroupjob.setJobName("CountGroupGraphJob");
		CountGroupjob.setJarByClass(Graph.class);
		/*Setting up the output key, value classes*/
		CountGroupjob.setOutputKeyClass(IntWritable.class);
		CountGroupjob.setOutputValueClass(IntWritable.class);
		/*Setting up the map output key, value classes*/
		CountGroupjob.setMapOutputKeyClass(IntWritable.class);
		CountGroupjob.setMapOutputValueClass(IntWritable.class);
		/*Setting up the Mapper and Reducer classes*/
		CountGroupjob.setMapperClass(GroupMapper.class);
		CountGroupjob.setReducerClass(GroupReducer.class);
		/*Setting up Input and output format classes*/
		CountGroupjob.setInputFormatClass(TextInputFormat.class);
		CountGroupjob.setOutputFormatClass(TextOutputFormat.class);
		/*Setting the input and output paths that will be passed as command line arguments to the program*/
		FileInputFormat.setInputPaths(CountGroupjob,new Path(args[1]));
		FileOutputFormat.setOutputPath(CountGroupjob,new Path(args[2]));
		/*Setting the property to wait for the completion of the job*/ 
		CountGroupjob.waitForCompletion(true);
		
       	}
}
