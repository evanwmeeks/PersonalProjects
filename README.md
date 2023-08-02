
## Personal Projects

 This repository is full of various projects I've coded on my own time for 
 either personal use or to aide in future projects at work. Each project 
 will be detailed below as they are added to this repository. These 
 projects are presented as a portfolio of my work, and not as licensed code 
 for any use. 


### iPoint - Wasabi Uploader

Developed during my time at iPoint Solutions, this Mac App was designed to allow customer support to quickly add images to a Wasabi bucket from their local machine. The app was compiled using pyinstaller onefile. The application was heavily customized for iPoint specifically, and private information has been obfuscated. 

	Files: 

		Shell.sh

			This file ensures the local machine has HomeBrew and pip3 are installed and updated, before installing python packages TKinter and Boto3.

		Wasabi_Uploader.py

			 Using boto3 (since Wasabi is bit-for-bit compatible with AWS S3), 
			 the application first looks for credentials stored on the users computer and tests them. 
			 If they're invalid, the user is prompted to provide credentials. The application then allows 
			 users to multi-select files for upload, uploads the files, then presents a count of the total 
			 number of files uploaded. The user is then given the option to upload more or quit the application.


### banking_project
A new personal project, this is a work in progress. The long term goal of this application is to build a standalone 'bank' using Django and postgreSQL. This applicaiton is a playground of sorts for me to practice OOP, learn best practices, and build a truly full stack application. 

	Files:
		
		postgres.py

			This file acts as the Python - SQL database interpreter. A fully custom built class, I'm developing this as a means of fully controlling the database from within the banking app, never needing to use pgAdmin or a similar GUI. 

		user_module.py

			As of 8/1/23, this module is something of a cross between my original ideation phase and actual development. I had originally wanted this to be a simple OOP project and began scripting as if Python and CSV files would fully encompass my needs. However, since deciding to build a fully-fledged application instead, this file has become a means of testing the postgres module for the time being, and will eventually be fleshed out to be Django friendly. 

