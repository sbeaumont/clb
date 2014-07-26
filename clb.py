import sys
import os

# This will trigger configuration
import config

from converter.csvtoofxconverter import CSVToOFXConverter

if len(sys.argv) != 3:
    # Did not pass two parameters (sys.argv[0] is file name): show help text
    print "Usage: clb.py <directory with .csv files> <output file>"
    print "Example: python clb.py ../data output.xml"
    sys.exit()

directoryWithCSVs = sys.argv[1]
outputFile = sys.argv[2]

if not os.path.isdir(directoryWithCSVs):
    print directoryWithCSVs, "is not a directory"
    sys.exit(1)

converter = CSVToOFXConverter()

for filename in os.listdir(directoryWithCSVs):
    if filename.endswith(".csv"):
        converter.addFile(os.path.join(directoryWithCSVs, filename))

converter.convert(outputFile)    