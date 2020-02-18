# Using Python + Google Cloud Vision API to extract text from photos
Python script using Google Cloud Vision API to extract text (line by line) from image(s)

## About Vision API

https://cloud.google.com/vision

## Setup/Requirement

This code requires you to have authentication setup. Refer to the Authentication Getting Started Guide (https://cloud.google.com/docs/authentication/getting-started) for instructions on setting up credentials for applications.

1. Python - v2.7.15 or Python - v3.6.5
2. Enable Google’s Cloud Vision API
3. Install the dependencies needed to run the code using
~~~sh
$ pip install -r requirements.txt   
~~~
## How to run for Single Image
The __detect_final__ script is included .

~~~sh
$  python detect_final.py document ./<folder_name>/<image.png/jpeg>
example
$ python detect_final.py document ./resources/text.jpeg
~~~
## How to run for Mulitple Images

* Note: Get the path of all the images and covert it into a csv file using the code __path.py__
            Set the _rootDir_ inside the path.py to required folder (ex - '/Users/Ayush/Desktop/VisionAPI/ss2text/walmartlaptopDell/') 
~~~sh
$  python path.py
~~~
Open the csv and tranpose the the first row to get the path in a single column

THEN............

The __detect_multiple_ss.py__ script is included .

~~~sh
$  python detect_multiple_ss.py document
~~~

## Results
The code will take one image at a time and get all the text block wise and store the data in a csv format
