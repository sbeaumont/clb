import sys
import os
import config
import logging

from converter.csvtoofxconverter import CSVToOFXConverter

rootlog = logging.getLogger('')
rootlog.setLevel(logging.DEBUG)
fh = logging.FileHandler('spam.log')
rootlog.addHandler(fh)

if len(sys.argv) != 3:
    # No parameters passed: show help text
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