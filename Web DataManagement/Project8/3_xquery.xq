(:
Student Name: Samhitha Nagendla (sxn7208)
File Name: 3_xquery.xq
Description: For each different department, display the department code and the number of courses taught by the department.
Reference : Referred the Sample examples provided in the Lecture Notes(slides).
:)

declare boundary-space preserve;
for $department in distinct-values(doc('http://aiweb.cs.washington.edu/research/projects/xmltk/xmldata/data/courses/reed.xml')//course/subj)
return
	{
	$department,
	count(doc('http://aiweb.cs.washington.edu/research/projects/xmltk/xmldata/data/courses/reed.xml')//course[subj =$department]/reg_num)
	}
