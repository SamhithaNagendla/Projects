/*
Student Name: Samhitha Nagendla (sxn7208)
File Name: dom.java
Description: To print the titles of all MATH courses that are taught in room LIB 204
Reference : Referred the Sample programs provided in the Assignment description.
*/

import javax.xml.parsers.*;
import org.w3c.dom.*;
import java.net.URL;

public class dom
{
    public static void main ( String args[] ) throws Exception
    {
		//Indicator to update when Subject equals to MATH
        int subjInd = 0;
		//Indicator to update when Room Number equals to 204
		int	roomInd = 0;
		//To store the Title of the course
        String c = null;
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        DocumentBuilder db = dbf.newDocumentBuilder();
        Document doc = db.parse((new URL("http://aiweb.cs.washington.edu/research/projects/xmltk/xmldata/data/courses/reed.xml")).openStream());
        NodeList course = doc.getElementsByTagName("course");
        System.out.println("\nTitles of all MATH courses that are taught in room LIB 204:");
        for (int k = 0; k < course.getLength(); k++)
        {
            Node coursedet = course.item(k);
            if(coursedet.getNodeName()=="course")
            {
                NodeList childdet = coursedet.getChildNodes();
                for (int i = 0; i < childdet.getLength(); i++)
                {
                    Node childsubdet = childdet.item(i);
                    String a = childsubdet.getTextContent();
                    if (childsubdet.getNodeName() == "subj" && a.equalsIgnoreCase("MATH"))
                    {
                        subjInd=1;
                    }
                    if (childsubdet.getNodeName() == "title")
                    {
                        c = childsubdet.getTextContent();
                    }
                    if (childsubdet.getNodeName() == "place" )
                    {
                        NodeList placedet = childsubdet.getChildNodes();
                        for (int j = 0; j < placedet.getLength(); j++)
                        {
                            Node placesubdet = placedet.item(j);
                            String b = placesubdet.getTextContent();
                            if ((placesubdet.getNodeName() == "room") && (b.equalsIgnoreCase("204")) )
                             {
                                roomInd = 1;
                                if (subjInd == 1 && roomInd == 1  )
                                {
                                    System.out.println(c);
									subjInd = 0;
									roomInd = 0;
                                }
                            }
                        }
                    }
                }
            }
        }

    }
}