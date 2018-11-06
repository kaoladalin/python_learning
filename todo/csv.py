import csv
#import codecs
fileHeader = ["name", "score"]
d1 = ["Wang", "100"]
d2 = ["Li", "80"]
csvFile = open("instance.csv", "w+")
writer = csv.writer(csvFile)
writer.writerows([fileHeader, d1, d2])
csvFile.close()
