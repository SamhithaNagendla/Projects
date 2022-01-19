(:
Student Name: Samhitha Nagendla (sxn7208)
File Name: 5_xquery.xq
Description: For each different instructor, return an element tagged instructor that contains the name of the instructor and the titles of all courses taught by the instructor.
Reference : Referred the Sample examples provided in the Lecture Notes(slides).
:)

declare boundary-space preserve;
for $instructor in distinct-values(doc('http://aiweb.cs.washington.edu/research/projects/xmltk/xmldata/data/courses/reed.xml')//course/instructor)
order by $instructor
return
<instructor>
	<name>{$instructor}</name>
	<courses>{distinct-values(doc('http://aiweb.cs.washington.edu/research/projects/xmltk/xmldata/data/courses/reed.xml')//course[instructor =$instructor]/title)}</courses>
</instructor>
