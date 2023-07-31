
### PersonalProjects

 This repository is full of various projects I've coded on my own time for 
 either personal use or to aide in future projects at work. Each project 
 will be detailed below as they are added to this repository. These 
 projects are presented as a portfolio of my work, and not as licensed code 
 for any use. 


# iPoint - Wasabi Uploader

Developed during my time at iPoint Solutions, this Mac App was designed to allow customer support to quickly add images to a Wasabi bucket from their local machine. The app was compiled using pyinstaller onefile. The application was heavily customized for iPoint specifically, and private information has been obfuscated. 

	Files: 

		Shell.sh

			This file ensures the local machine has HomeBrew and pip3 are installed and updated, before installing python packages TKinter and Boto3.

		Wasabi_Uploader.py

			 Using boto3 (since Wasabi is bit-for-bit compatible with AWS S3), the application first looks for credentials stored on the users computer and tests them. If they're invalid, the user is prompted to provide credentials. The application then allows users to multi-select files for upload, uploads the files, then presents a count of the total number of files uploaded. The user is then given the option to upload more or quit the application.

