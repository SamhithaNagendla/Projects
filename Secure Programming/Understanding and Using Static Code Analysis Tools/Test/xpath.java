/*
Student Name: Samhitha Nagendla (sxn7208)
File Name: xpath.java
Description: To  evaluates the following XPath queries over the XML data in reed.xml:
				1)Print the titles of all MATH courses that are taught in room LIB 204
				2)Print the instructor name who teaches MATH 412
				3)Print the titles of all courses taught by Wieting
Reference : Referred the Sample programs provided in the Assignment description.
*/
import javax.xml.xpath.*;
import org.xml.sax.InputSource;
import org.w3c.dom.*;
public class xpath {

static void print ( Node e )
{
    if (e instanceof Text)
        System.out.print(((Text) e).getData());
    else
        {
            NodeList c = e.getChildNodes();
            for (int k = 0; k < c.getLength(); k++)
            {
                System.out.print("    ");
                print(c.item(k));
                System.out.print("\n");
            }

        }
}

static void eval ( String query, String document ) throws Exception
{
    XPathFactory xpathFactory = XPathFactory.newInstance();
    XPath xpath = xpathFactory.newXPath();
    InputSource inputSource = new InputSource(document);
    NodeList result = (NodeList) xpath.evaluate(query,inputSource,XPathConstants.NODESET);
    System.out.println("  XPath query:\n    "+query+"\n  Result:");
    for (int i = 0; i < result.getLength(); i++)
        print(result.item(i));
    System.out.println();
}

public static void main ( String[] args ) throws Exception
{
    System.out.println("Titles of all MATH courses that are taught in room LIB 204:");
    eval("root/course[subj='MATH'][place/room='204']/title","http://aiweb.cs.washington.edu/research/projects/xmltk/xmldata/data/courses/reed.xml");
    System.out.println("Instructor name who teaches MATH 412:");
    eval("root/course[subj='MATH'][crse='412']/instructor","http://aiweb.cs.washington.edu/research/projects/xmltk/xmldata/data/courses/reed.xml");
    System.out.println("Titles of all courses taught by Wieting:");
    eval("root/course[instructor='Wieting']/title","http://aiweb.cs.washington.edu/research/projects/xmltk/xmldata/data/courses/reed.xml");
}

}