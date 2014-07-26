from transaction.transaction import CSVParseError
from transactioncsvreader import TransactionCSVReader
from ofxwriter import OFXWriter
import sys
import logging

log = logging.getLogger(__name__)

class CSVToOFXConverter():
    """Converts CSV transaction exports to the OFX format, which is a standard and widely used by banking applications."""
    def __init__(self):
        self.reader = TransactionCSVReader()

    def addFile(self, filename):
        self.reader.readCSV(filename)
    
    def convert(self, outputFile):
        writer = OFXWriter()
        
        for transaction in self.reader:
            try:
                transaction.validate()
                writer.addTransaction(transaction)
            except CSVParseError as e:
                errorText = "Transaction %s did not validate: %s" % (str(transaction.source), str(e))
                print >> sys.stderr, errorText
                log.error(errorText)
        
        f = open(outputFile, 'w')
        try:
            f.write(writer.write())
        finally:
            f.close()