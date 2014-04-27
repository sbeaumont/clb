from transactioncsvreader import TransactionCSVReader
from ofxwriter import OFXWriter

class RaboConverter():
	
    def convert(self, fileName):
        reader = TransactionCSVReader()
        writer = OFXWriter()
        
        reader.readCSV(fileName)
        
        for transaction in reader:
            writer.addTransaction(transaction)
        
        print writer.write()
            
if __name__ == '__main__':
    converter = RaboConverter()
    converter.convert("test/rabobank-transactions-SEPA.csv")