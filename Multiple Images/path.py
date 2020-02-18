import os
import csv
rootDir = '/Users/Ayush/Desktop/VisionAPI/ss2text/walmartlaptopDell/'
fileSet = set()

for dir_, _, files in os.walk(rootDir):
    for fileName in files:
        relDir = os.path.relpath(dir_, rootDir)
        relFile = os.path.join(relDir, fileName)
        fileSet.add(relFile)
        #print(fileSet)
        #print('\n')
    
    with open('/Users/Ayush/Desktop/VisionAPI/ss2text/dell_path_104.csv', 'a') as csv_file:
        writeCSV = csv.writer(csv_file, delimiter=',')
        writeCSV.writerow(fileSet)