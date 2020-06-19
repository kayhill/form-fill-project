This is my final project for CS50x Intro to Computer Science from Harvard University. 

"FormFill" allows users to batch fill PDF forms by uploading a template and a data file. The form fields are auto-populated with information from the .csv file and a PDF is generated. A new PDF is generated for each row of data. 

Once the forms are generated, the user can download one or all of the output forms. 

The idea is to make it easy for people to generate lots of files at once (i.e. receipts, invoices, patient forms, etc) without having to open and fill each form by hand. The key to use is to name the .csv columns EXACTLY the same name as the form fields. Using a .csv as the data source allows data queries from a database to easily be prepared for upload.

I built this app in Python using Flask and postgresql. The first version of FormFill uses local addresses for file paths. These are hardcoded right now, but I am in the process of launching the app on Heroku where users will be able to store their files in the cloud.

My biggest challenge so far was learning to work with PDF files. There are a few different ways to manipulate PDFs with Python, but I finally found success with PyPDF2. 

The basic layout of this app was adapted from Week 8's problem set, "Finance".  

Plans for further Development:
- Configure AWS 3 Storage
- Redesign layout and colors 
- Add feedback to improve UX (i.e. timer while loading)

Video Submission: https://www.youtube.com/watch?v=osudVYzcYaY


