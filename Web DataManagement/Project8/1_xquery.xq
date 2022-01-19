(:
Student Name: Samhitha Nagendla (sxn7208)
File Name: 1_xquery.xq
Description: For each MATH course taught in room LIB 204, return an element tagged course with the title, the instructor, the start, and the end times of the course.
Reference : Referred the Sample examples provided in the Lecture Notes(slides).
:)

declare boundary-space preserve;
for $course1 in (doc('http://aiweb.cs.washington.edu/research/projects/xmltk/xmldata/data/courses/reed.xml')//course[subj="MATH" and place/room="204" ] )
return
<course>
	{$course1/title}
	{$course1/instructor}
	{$course1/time/start_time}
	{$course1/time/end_time}
</course>
