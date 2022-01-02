/*Imported packages to support the functionality implemented.*/
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.mapreduce.lib.input.*;
import org.apache.hadoop.mapreduce.lib.output.*;
import java.util.*;
import org.apache.hadoop.conf.*;
import org.apache.hadoop.util.*;
import java.io.*;
import org.apache.hadoop.fs.FileSystem;
import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import java.util.HashMap;
import java.util.Scanner;
import java.util.Vector;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.mapreduce.lib.input.*;
import org.apache.hadoop.mapreduce.lib.output.*;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

/*MatrixM class to read and write index, matrix value.*/
class MatrixA implements Writable {
	/*variables to read index value i, of Matrix A i*j and the value*/
    public int index;
    public double value;
	/*Constructors*/
    MatrixA () {}
    MatrixA ( int i,double v ) {
        index = i; value = v;
    }
	/*To Write the values*/
    public void write ( DataOutput out ) throws IOException {
        out.writeInt(index);
        out.writeDouble(value);
    }
	/*To read the values*/
    public void readFields ( DataInput in ) throws IOException {
        index = in.readInt();
        value = in.readDouble();
    }
}
/*MatrixB class to read and write index, matrix value.*/
class MatrixB implements Writable {
	/*variables to read index value j, of Matrix B i*j and the value*/
    public int index;
    public double value;
	/*Constructors*/
    MatrixB () {}
    MatrixB ( int j,double v ) {
        index = j; value = v;
    }
	/*To Write the values*/
    public void write ( DataOutput out ) throws IOException {
        out.writeInt(index);
        out.writeDouble(value);
    }
	/*To read the values*/
    public void readFields ( DataInput in ) throws IOException {
        index = in.readInt();
        value = in.readDouble();
    }
}
/*Element class to read and write index, matrix value.*/
class Elem implements Writable {
	/*variables to read index value i of MatrixA i*j, index value j of Matrix B i*j and the values*/
    public short tag;
    public MatrixA mata;
    public MatrixB matb;
	/*constructor*/
    Elem () {}
    Elem ( MatrixA a ) { tag = 0; mata = a; }
    Elem ( MatrixB b ) { tag = 1; matb = b; }
	/*To Write the values*/
    public void write ( DataOutput out ) throws IOException {
        out.writeShort(tag);
        if (tag==0)
            mata.write(out);
        else matb.write(out);
    }
	/*To read the values*/
    public void readFields ( DataInput in ) throws IOException {
        tag = in.readShort();
        if (tag==0) {
            mata = new MatrixA();
            mata.readFields(in);
        } else {
            matb = new MatrixB();
            matb.readFields(in);
        }
    }
}
/*Class to pair the idicies*/
class Pair implements WritableComparable<Pair>{
	/*To pair the index value i of Matrix A i*j , the index value j of Matrix B i*j*/
    public int i;
    public int j;
	/*constructors*/
	Pair(){}
    Pair ( int ival, int jval ) {
        i = ival; j = jval;
		    }
	/*To Write the values*/
    public void write ( DataOutput out ) throws IOException {
		out.writeInt(i);
        out.writeInt(j);
    }
	/*To read the values*/
    public void readFields ( DataInput in ) throws IOException {
		i = in.readInt();
        j = in.readInt();
    }
	/*To compare the values*/
	public int compareTo(Pair o) {
		int ithis = this.i;
		int jthis = this.j;
		if (!(ithis==o.i)) {
			return (ithis < o.i ? -1 : (ithis==o.i ? 0 : 1));
		}
		if (!(jthis==o.j)) {
			return (jthis < o.j ? -1 : (jthis==o.j ? 0 : 1));
		}
		return 0;
    }
	/*To return the pair of indices*/
    public String toString () { return i+"	"+j; }
}

	
/*Defining the Multiply class that defines mappers and reducers for Matrix multiplication.*/
public class Multiply {

	/*
	 * AMatrixMapper produces the key value pair by reading the Matrix A values, provided in the form of the indices numbers seperated by comma and value through the input file.
	 * For each value in the input file, a key value pair is generated with key as j index and value as Elem with tag 0 , i index and v value.
	.*/
	public static class AMatrixMapper extends Mapper<Object,Text,IntWritable,Elem> {
		@Override
		public void map ( Object key, Text value, Context context ) throws IOException, InterruptedException {
			/*Reading each value and extracting the index numbers, value that are seperated by comma.*/
			Scanner s = new Scanner(value.toString()).useDelimiter(",");
			/*Reading the index numbers and value of the Matrix into i, j and v values*/
			int i = s.nextInt();
			int j = s.nextInt();
			double v = s.nextDouble();
			MatrixA a = new MatrixA(i,v);
			/*Writing the context by passing the j and Elem(0,i,v) values by taking the files read from the input file*/
			context.write(new IntWritable(j),new Elem(a));
			/*Closing the scanner method*/
			s.close();
			}
		}
		
	/*
	 * BMatrixMapper produces the key value pair by reading the Matrix B values, provided in the form of the indices numbers seperated by comma and value through the input file.
	 * For each value in the input file, a key value pair is generated with key as j index and value as Elem with tag 0 , i index and v value.
	.*/
	public static class BMatrixMapper extends Mapper<Object,Text,IntWritable,Elem> {
		@Override
		public void map ( Object key, Text value, Context context ) throws IOException, InterruptedException {
			/*Reading each value and extracting the index numbers, value that are seperated by comma.*/
			Scanner s = new Scanner(value.toString()).useDelimiter(",");
			/*Reading the index numbers and value of the Matrix into i, j and v values*/
			int i = s.nextInt();
			int j = s.nextInt();
			double v = s.nextDouble();
			MatrixB b = new MatrixB(j,v);
			/*Writing the context by passing the i and Elem(1,j,v) values by taking the files read from the input file*/
			context.write(new IntWritable(i),new Elem(b));
			/*Closing the scanner method*/
			s.close();
			}
		}
		
	/*
	 * ProductReducer that takes the AMatrixMapper return value and the BMatrixMapper return value as input.Then it will generate the Pair as key and the product as value of output.
	 *  The key value is the Pair with indices values and the value is the product of values at those indices.
	 *  Save these values as output in an intermediate folder provided as command-line arguments while running the program.
	 */
	public static class ProductReducer extends Reducer<IntWritable,Elem,Pair,DoubleWritable> {
        static Vector<MatrixA> avals = new Vector<MatrixA>();
        static Vector<MatrixB> bvals = new Vector<MatrixB>();
		@Override
		public void reduce ( IntWritable key, Iterable<Elem> values, Context context ) throws IOException, InterruptedException {
            avals.clear();
            bvals.clear();
			for (Elem v: values)
                if (v.tag == 0)
                    avals.add(v.mata);
                else bvals.add(v.matb);
            for ( MatrixA a: avals )
                for ( MatrixB b: bvals )
					context.write(new Pair(a.index,b.index),new DoubleWritable(a.value*b.value));
                    
			}
		}
	/*
	 * ProductMapper produces the key value pair by reading the indices pair and product value through the input file.
	 * For each line in the input file, a key value pair is generated with key as pair of indices and value as product value.
	.*/
	public static class ProductMapper extends Mapper<Object,Text,Pair,DoubleWritable> {
		@Override
		public void map ( Object key, Text value, Context context ) throws IOException, InterruptedException {
			/*Reading each line and extracting the indices pair and product value, that are seperated by comma.*/
			Scanner s = new Scanner(value.toString()).useDelimiter("	");
			/*Reading the indices pair and product values*/
			int i = s.nextInt();
			int j = s.nextInt();
			double product = s.nextDouble();
			/*Writing the context by passing the indices pair and product values read from the input file*/
			context.write(new Pair(i,j),new DoubleWritable(product));
			/*Closing the scanner ethod*/
			s.close();
			}
		}
	/*
	 *AdditionReducer takes the emitted key value pair from ProductMapper and will sum the partial products.
	 *It will emit the indices and product of matrix A and B.
	 *The output of this AdditionReducer will be saved in an output folder provided as command-line argument while running the program
	 */	
	public static class AdditionReducer extends Reducer<Pair,DoubleWritable,Pair,DoubleWritable> {
		@Override
			public void reduce ( Pair key, Iterable<DoubleWritable> values, Context context ) throws IOException, InterruptedException {
				/*Initially setting the sum =0*/
				double sum = 0.0;
				/*For each pair, the product values are summed up*/
				for (DoubleWritable v: values) {
					sum += v.get();
					};
				/*Writing the context by passing the indices, product values*/
				context.write(key,new DoubleWritable(sum));
				}
			}
		
	/*Main function of graph class that sets up the jobs*/
    public static void main ( String[] args ) throws Exception 
	{
		/*Job to execute Map Reduce for partial product for each indices pair in the input file.*/
		/*Setting up the properties of job*/
		Job PartialProdjob = Job.getInstance();
		PartialProdjob.setJobName("PartialProductMatrixJob");
		PartialProdjob.setJarByClass(Multiply.class);
		/*Setting up the output key , value classes*/
		PartialProdjob.setOutputKeyClass(Pair.class);
		PartialProdjob.setOutputValueClass(DoubleWritable.class);
		/*Setting up map output key, value classes*/	    		
		PartialProdjob.setMapOutputKeyClass(IntWritable.class);
		PartialProdjob.setMapOutputValueClass(Elem.class);
		/*Setting up the Mapper and Reducer Classes and inputs*/
		MultipleInputs.addInputPath(PartialProdjob,new Path(args[0]),TextInputFormat.class,AMatrixMapper.class);
    	MultipleInputs.addInputPath(PartialProdjob,new Path(args[1]),TextInputFormat.class,BMatrixMapper.class);
		FileOutputFormat.setOutputPath(PartialProdjob,new Path(args[2], "result"));
		PartialProdjob.setReducerClass(ProductReducer.class);		
		PartialProdjob.setOutputFormatClass(TextOutputFormat.class);
		/*Setting the property to wait for the completeion of the job	*/												    		
		PartialProdjob.waitForCompletion(true);
	
		/*Job to execute the Map Reduce for summing the partial products, by taking the file generated by above AMatrixMapper,BMatrixMapper and ProductReducer using PartialProductMatrixJob. */
		Job ProductSumjob = Job.getInstance();
		ProductSumjob.setJobName("ProductSumMatrixJob");
		ProductSumjob.setJarByClass(Multiply.class);
		/*Setting up the output key, value classes*/
		ProductSumjob.setOutputKeyClass(Pair.class);
		ProductSumjob.setOutputValueClass(DoubleWritable.class);
		/*Setting up the map output key, value classes*/
		ProductSumjob.setMapOutputKeyClass(Pair.class);
		ProductSumjob.setMapOutputValueClass(DoubleWritable.class);
		/*Setting up the Mapper and Reducer classes*/
		ProductSumjob.setMapperClass(ProductMapper.class);
		ProductSumjob.setReducerClass(AdditionReducer.class);
		/*Setting up Input and output format classes*/
		ProductSumjob.setInputFormatClass(TextInputFormat.class);
		ProductSumjob.setOutputFormatClass(TextOutputFormat.class);
		FileInputFormat.addInputPath(ProductSumjob, new Path(args[2],"result"));
    	FileOutputFormat.setOutputPath(ProductSumjob, new Path(args[3]));
    	ProductSumjob.waitForCompletion(true);
    }
}