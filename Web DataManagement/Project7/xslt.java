/*
Student Name: Samhitha Nagendla (sxn7208)
File Name: xslt.java
Description: To display all MATH courses in Reed College by transforming the XML file reed.xml to XHTML using XSLT.
Reference : Referred the Sample programs provided in the Assignment description.
*/
import javax.xml.parsers.*;
import org.w3c.dom.*;
import javax.xml.transform.*;
import javax.xml.transform.dom.*;
import javax.xml.transform.stream.*;
import java.io.*;
import java.net.URL;
import java.awt.Desktop;
import java.net.URI;
import java.net.URISyntaxException;

public class xslt
{
    public static void main (String[] argv) throws Exception
    {

        File currdir = new File(new File(".").getCanonicalPath());
        String c = currdir.getCanonicalPath();
        String loc = c.replace('\\','/');
        File stylesheet = new File(c+"/math.xsl");
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        DocumentBuilder db = dbf.newDocumentBuilder();
        Document document = db.parse((new URL("http://aiweb.cs.washington.edu/research/projects/xmltk/xmldata/data/courses/reed.xml")).openStream());
        StreamSource stylesource = new StreamSource(stylesheet);
        TransformerFactory tf = TransformerFactory.newInstance();
        Transformer transformer = tf.newTransformer(stylesource);
        DOMSource source = new DOMSource(document);
        StreamResult result = new StreamResult(new FileWriter(c+"/math.xhtml"));
        transformer.transform(source,result);
		System.out.println("Transforming the XML file reed.xml to display all MATH courses in Reed College to XHTML using XSLT is completed successfully!!\n math.xhtml file is created in "+loc+" file location.");
		//To open the file in the default folder
		File xhtmlFile = new File(c+"/math.xhtml");
		Desktop.getDesktop().browse(xhtmlFile.toURI());
    }
}