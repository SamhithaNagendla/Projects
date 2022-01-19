(:
Student Name: Samhitha Nagendla (sxn7208)
File Name: 2_xquery.xq
Description: For each different course, return an element tagged course with the course title and all the instructor names that teach this course.
Reference : Referred the Sample examples provided in the Lecture Notes(slides).
:)

declare boundary-space preserve;
for $title2 in distinct-values(doc('http://aiweb.cs.washington.edu/research/projects/xmltk/xmldata/data/courses/reed.xml')//course/title)
return
<course>
	<title>{$title2}</title>
	<instructors>{distinct-values(doc('http://aiweb.cs.washington.edu/research/projects/xmltk/xmldata/data/courses/reed.xml')//course[title =$title2]/instructor)}</instructors>
</course>