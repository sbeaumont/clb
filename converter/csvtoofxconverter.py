from transaction import CSVParseError
from transactioncsvreader import TransactionCSVReader
from ofxwriter import OFXWriter
import sys

class CSVToOFXConverter():
    
    def __init__(self):
        self.reader = TransactionCSVReader()

    def addFile(self, filename):
        self.reader.readCSV(filename)
    
    def convert(self):
        writer = OFXWriter()
        
        for transaction in self.reader:
            try:
                transaction.validate()
                writer.addTransaction(transaction)
            except CSVParseError as e:
                print >> sys.stderr, "Transaction " + str(transaction.source) + " did not validate: " + str(e)
        
        print writer.write()
            
if __name__ == '__main__':
    converter = CSVToOFXConverter()
    converter.addFile("test/rabobank-transactions-SEPA.csv")
    converter.convert()