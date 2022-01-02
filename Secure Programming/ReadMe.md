# SEED Attack Labs
These labs cover some of the most common vulnerabilities and attacks exploiting these vulnerabilities.
All the labs are presented in the form of PDF files, containing some screenshots.

# Table of Contents
Getting Started
Motivation
List of Attacks
Key Learnings
References

# Getting Started
These instructions will get you to set up the environment on your local machine to perform these attacks.

Step 1: Create a new VM in Virtual Box.
Step 2: Download the image SEEDUbuntu-16.04-32bit.zip from here.
Step 3: Use the Virtual Machine Hard Disk file to setup your VM.
Step 4: Configure the VM.

Refer a document available in the Setup folder.

# Motivation
The labs were completed as a part of the Secure Programming(CSE 5382) course at The University of Texas at Arlington. The course is well structured to understand the concepts of Secure Programming.

# List of Attacks
Shellshock Attack

Description: In this attack we launched the shellshock attack on a remote web server and then gained the reverse shell by exploiting the vulnerability.
# 
Buffer Overflow Vulnerability

Description: Buffer overflow is defined as the condition in which a program attempts to write data beyond the boundaries of pre-allocated fixed-length buffers. This vulnerability can be utilized by a malicious user to alter the flow control of the program, even execute arbitrary pieces of code. The task in this lab is to develop a scheme to exploit the buffer overflow vulnerability and finally gain the root privilege.
# 
Return-to-libc Attack

Description: In this attck, we develop a return-to-libc attack to exploit the vulnerability and finally to gain the root privilege.
#
Format String Vulnerability

Description: The format-string vulnerability is caused by code like printf(user input), where the contents of the variable of user input are provided by users. When this program is running with privileges (e.g., Set-UID program), this printf statement becomes dangerous, because it can lead to one of the following consequences: (1) crash the program, (2) read from an arbitrary memory place, and (3) modify the values of in an arbitrary memory place. The last consequence is very dangerous because it can allow users to modify internal variables of a privileged program, and thus change the behavior of the program. The task is to develop a scheme to exploit the vulnerability.
#
Race Condition Vulnerability

Description: A race condition occurs when multiple processes access and manipulate the same data concurrently, and the outcome of the execution depends on the particular order in which the access takes place. If a privileged program has a race-condition vulnerability, attackers can run a parallel process to “race” against the privileged program, with an intention to change the behaviors of the program. The task is to exploit this vulnerability and gain root privilege.
#
Cross-Site Request Forgery Attack

Description: In this lab, we will be attacking a social networking web application using the CSRF attack. The open-source social networking application called Elgg has countermeasures against CSRF, but we have turned them off for this lab. We also study the most common countermeasures of this attack.
#
SQL injection Attack

Description: In this lab, we have created a web application that is vulnerable to the SQL injection attack. Our web application includes the common mistakes made by many web developers. Our goal is to find ways to exploit the SQL injection vulnerabilities, demonstrate the damage that can be achieved by the attack, and master the techniques that can help defend against such type of attacks.
#
Understanding and Using Static Code Analysis Tools

Description: To familiarize you with using open source static code analysis tools to find bugs and vulnerabilities in source code and to recognize that not all tools are created equal.
#
Input Validation

Description: To produce a program that validates its input using regular expressions.

# Key Learnings
To learn about the major security problems found in software today. Using this knowledge, they will work to find these bugs in software, fix the bugs, and design software so that it has fewer security problems. Topics will include input validation, buffer overflow prevention, error handling, web application issues, static analysis tools and XML. 

# References
https://seedsecuritylabs.org/Labs_20.04/Software/
Lecture slides, extra resources provided by Professor in the project descriptions.

Required Textbooks and Other Course Materials
Computer & Internet Security: A Hands-On Approach, Second Edition
Publisher: Wenliang Du (May 1, 2019)
Language: English
ISBN: 978-1733003926 (hardcover) and 978-1733003933 (paperback)

Optional Textbooks
Secure Programming with Static Analysis
Paperback: 624 pages, (Electronic versions also available)
Publisher: Addison-Wesley Professional (July 9, 2007)
Language: English
ISBN-10: 0321424778
ISBN-13: 978-0321424778
