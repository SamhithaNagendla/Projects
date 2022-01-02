/*Imported packages to support the functionality implemented.*/
import java.io.*;
import java.util.Scanner;
import java.util.Vector;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.lib.input.*;
import org.apache.hadoop.mapreduce.lib.output.*;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

/*Vertex class Defination*/
class Vertex implements Writable {
        public long id;
        public int adjsize;
        public Vector<Long> adjacent= new Vector<Long>();
        public long centroid;
        public short depth;
        Vertex(){}
        Vertex(long t,int s, Vector<Long> g, long v, short a)
        {
                id = t;
                adjsize = s;
                adjacent = (Vector)g.clone();
                centroid = v;
                depth = a;
        }
        public void write(DataOutput out) throws IOException{
                out.writeLong(id);
                out.writeInt(adjsize);
                for(int i=0;i<adjsize;i++)
                {
                        out.writeLong(adjacent.get(i));
                }
                out.writeLong(centroid);
                out.writeShort(depth);
        }
        public void readFields(DataInput in) throws IOException,EOFException{
                id = in.readLong();
                adjsize = in.readInt();
                adjacent.clear();
                for(int i=0;i<adjsize;i++)
                {
                        adjacent.add(in.readLong());
                }
                centroid =in.readLong();
                depth =in.readShort();
        }
        public String toString(){

                        String tmp ="";
                        tmp = tmp+ id+"	";
                        tmp = tmp+adjsize+"	";
                        for (int i =0; i<adjsize;i++)
                        {
                                tmp = tmp + adjacent.get(i)+"	";
                        }
                        tmp = tmp+ centroid+"	";
                        tmp = tmp+ depth;
                        return tmp;

                }
}
public class GraphPartition {
        static Vector<Long> centroids = new Vector<Long>();
        final static short max_depth = 8;
        static short BFS_depth = 0;
        public static class InitialMapper extends Mapper<Object,Text,LongWritable,Vertex> {
                public int countid = 0;
                public int adjsize =0;
                @Override
                public void map ( Object key, Text value, Context context ) throws IOException, InterruptedException {
                        Scanner s = new Scanner(value.toString()).useDelimiter(",");
                        long centroid = -1;
                        long nextid;
                        int temp;
                        long id = s.nextLong();
                        short depth =0 ;
                        Vector<Long> adj=new Vector<Long>();
                        while(s.hasNext()){
                                nextid = s.nextLong();
                                adj.add(nextid);

                        }
                        if(adj.isEmpty())
                        {
                                 adjsize=0;
                         }
                         else
                         {
                                adjsize=adj.size();
                         }
                        if(countid < 10)
                        {
                                centroid = id;
                        }
                        countid ++;
                        context.write(new LongWritable(id),new Vertex(id,adjsize,adj,centroid,depth));
                        s.close();
                }
        }
        public static class InitialReducer extends Reducer<LongWritable,Vertex,LongWritable,Vertex> {
                static Vector<Long> neig = new Vector<Long>();
                public long tid ;
                public int tadjsize;
                public long tcentroid;
                public short tdepth;
                @Override
                public void reduce ( LongWritable key, Iterable<Vertex> values, Context context ) throws IOException, InterruptedException {
                        neig.clear();
                        for (Vertex v: values)
                        {
                                tid =v.id;
                                tadjsize =v.adjsize;
                                neig = (Vector)v.adjacent.clone();
                                tcentroid =v.centroid;
                                tdepth =v.depth;
                                context.write(key, new Vertex(tid,tadjsize,neig,tcentroid,tdepth));
                        }
                }
        }
        public static class IterativeMapper extends Mapper<Object,Text,LongWritable,Vertex> {
                                        public  long iid;
                                        public int iadjsize;
                                        public int temp;
                                        public long nextid;
                                        public static Vector<Long> iadj=new Vector<Long>();
                                        public long icentroid;
                                        public short idepth;
                @Override
                public void map ( Object key, Text value, Context context ) throws IOException, InterruptedException {
                                Scanner s = new Scanner(value.toString()).useDelimiter("	");
                                long tmp = s.nextLong();
                                iid = s.nextLong();
                                iadjsize = s.nextInt();
                                iadj.clear();
                                for(int i=0; i<iadjsize;i++)
                                {
                                         nextid = s.nextLong();
                                         iadj.add(nextid);
                                 }
                                icentroid = s.nextLong();
                                idepth = s.nextShort();
                                s.close();
                                context.write(new LongWritable(iid), new Vertex(iid,iadjsize,iadj,icentroid,idepth));
                                if (icentroid >0 )
                                {
                                        Vector<Long> b = new Vector<Long>();
                                        for (long n : iadj)
                                        {
                                                b.clear();
                                                context.write(new LongWritable(n), new Vertex(n,0,b,icentroid,BFS_depth) );
                                        }
                                }


                }
        }
        public static class IterativeReducer extends Reducer<LongWritable,Vertex,LongWritable,Vertex> {
                @Override
                public void reduce ( LongWritable key, Iterable<Vertex> values, Context context ) throws IOException, InterruptedException {
                        long min_depth = 1000;
                        Vector<Long> c = new Vector<Long>();
                        long d=-1;
                        int x;
                        short e =0;
                        c.clear();
                        Vertex m = new Vertex(key.get(),0,c,d,e);
                        for (Vertex v : values)
                        {
                                if (!(v.adjacent.isEmpty()))
                                {
                                        m.adjacent = (Vector) v.adjacent.clone();
                                }
                                if (v.centroid > 0 && v.depth < min_depth)
                                {
                                        min_depth = v.depth;
                                        m.centroid = v.centroid;
                                }
                        }
                        m.depth = (short) min_depth;
                        if(m.adjacent.isEmpty())
                        {
                                x=0;
                        }
                        else
                        {
                                x= m.adjacent.size();
                        }
                        context.write(new LongWritable(m.id), new Vertex(m.id,x,m.adjacent,m.centroid,m.depth));
                }
        }
        public static class FinalMapper extends Mapper<Object,Text,LongWritable,IntWritable> {

                public long fiid;
                public int fiadjsize;
                public int ftemp;
                public long fnextid;
                public static Vector<Long> fiadj=new Vector<Long>();
                public long ficentroid;
                public short fidepth;
                @Override
                public void map ( Object key, Text value, Context context ) throws IOException, InterruptedException {
                        String a = value.toString();
                        Scanner s = new Scanner(a).useDelimiter("	");
                        long ftmp = s.nextLong();
                        int count =1;
                        fiid = s.nextLong();
                        fiadjsize = s.nextInt();
                        fiadj.clear();
                        for(int i=0; i<fiadjsize;i++)
                        {
                                fnextid = s.nextLong();
                                fiadj.add(fnextid);
                         }
                        ficentroid = s.nextLong();
                        fidepth =  s.nextShort();
                        s.close();
                        context.write(new LongWritable(ficentroid), new IntWritable(count));
                }
        }
        public static class FinalReducer extends Reducer<LongWritable,IntWritable,LongWritable,IntWritable> {
                @Override
                public void reduce ( LongWritable key, Iterable<IntWritable> values, Context context ) throws IOException, InterruptedException {
                        int count = 0;
                        for (IntWritable v: values)
                        {
                                count = count+v.get() ;
                        }
                        context.write(key, new IntWritable(count));
                }
        }
        public static void main ( String[] args ) throws Exception {
                int max_depth =8;
                int x = 0;
                Configuration conf = new Configuration();
                Job job = Job.getInstance(conf, "Project3");
                job.setJarByClass(GraphPartition.class);
                job.setJobName("MyJob");
                job.setOutputKeyClass(LongWritable.class);
                job.setOutputValueClass(Text.class);
                job.setMapOutputKeyClass(LongWritable.class);
                job.setMapOutputValueClass(Vertex.class);
                job.setMapperClass(InitialMapper.class);
                job.setReducerClass(InitialReducer.class);
                job.setInputFormatClass(TextInputFormat.class);
                job.setOutputFormatClass(TextOutputFormat.class);
                FileInputFormat.setInputPaths(job,new Path(args[0]));
                FileOutputFormat.setOutputPath(job,new Path(args[1]+"/i0"));
                job.waitForCompletion(true);
                /**/
                for ( short i = 0; i < max_depth; i++ ) {
                        BFS_depth++;
                        Configuration conf_iterate = new Configuration();
                        Job job1 = Job.getInstance(conf_iterate, "Project3");
                        job1.setJobName("iterative Job");
                        job1.setJarByClass(GraphPartition.class);
                        job1.setOutputKeyClass(LongWritable.class);
                        job1.setOutputValueClass(Vertex.class);
                        job1.setMapOutputKeyClass(LongWritable.class);
                        job1.setMapOutputValueClass(Vertex.class);
                        job1.setMapperClass(IterativeMapper.class);
                        job1.setReducerClass(IterativeReducer.class);
                        job1.setInputFormatClass(TextInputFormat.class);
                        job1.setOutputFormatClass(TextOutputFormat.class);
                        FileInputFormat.setInputPaths(job1,new Path(args[1]+"/i"+i));
                        x =i+1;
                        FileOutputFormat.setOutputPath(job1,new Path(args[1]+"/i"+x));
                        job1.waitForCompletion(true);

                }
                /**/
                Configuration conf_f = new Configuration();
                Job job2 = Job.getInstance(conf_f, "Project3");
                job2.setJobName("Final Job");
                job2.setJarByClass(GraphPartition.class);
                job2.setOutputKeyClass(LongWritable.class);
                job2.setOutputValueClass(IntWritable.class);
                job2.setMapOutputKeyClass(LongWritable.class);
                job2.setMapOutputValueClass(IntWritable.class);
                job2.setMapperClass(FinalMapper.class);
                job2.setReducerClass(FinalReducer.class);
                job2.setInputFormatClass(TextInputFormat.class);
                job2.setOutputFormatClass(TextOutputFormat.class);
                FileInputFormat.setInputPaths(job2,new Path(args[1]+"/i"+x));
                FileOutputFormat.setOutputPath(job2,new Path(args[2]));
                job2.waitForCompletion(true);
        }
}
