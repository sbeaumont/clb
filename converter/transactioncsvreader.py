# Rabobank .csv reader.
# Can handle the pre- and post-2014 (non-SEPA and SEPA compliant) versions.
# Serge Beaumont, 2014

import os
import sys
import itertools
import csv

from transactionfactory import createTransaction

class TransactionCSVReader:
    """Reads CSV files and loads them in memory. You can read multiple files, all records will be collected
    in a cache. The reader deduplicates lines that are exactly the same, so loading a file multiple times
    or having files with copies of transactions will get filtered out.

    The reader defers to the Transaction hierarchy to determine (per transaction line) what type it is,
    meaning that you can have transactions of different types mixed together.
    """
    
    def __init__(self):
        self.transactions = []
        self.uniqueTransactions = []
    
    def _resetCache(self):
        self.uniqueTransactions = []
    
    def __iter__(self):
        """All transactions wrapped in the appropriate Transaction type."""
        for transaction in self.deduplicated():
            yield createTransaction(transaction)
    
    def deduplicated(self):
        """All transactions with exact duplicates filtered out."""
        if not self.uniqueTransactions:
            k = sorted(self.transactions)
            self.uniqueTransactions = [i for i, _ in itertools.groupby(k)]

        return self.uniqueTransactions
    
    def readCSV(self, inputFileName):
        """Load the transactions in inputFileName. Will check if the file exists."""
        assert inputFileName != None, "Can not handle null file name"
        
        if not os.path.isfile(inputFileName):
            raise IOError, "File " + inputFileName + " is not an existing or openable file"
        
        self._resetCache()
        
        with open(inputFileName, 'rb') as f:
            reader = csv.reader(f)
            try:
                for row in reader:
                    self.transactions.append(row)
            except csv.Error as e:
                    sys.exit('file %s, line %d: %s' % (inputFileName, reader.line_num, e))

if __name__ == "__main__":
    ri = TransactionCSVReader()
    ri.readCSV(sys.argv[0])