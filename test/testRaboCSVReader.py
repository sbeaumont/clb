import unittest

import converter
from converter.transactioncsvreader import TransactionCSVReader
from converter.transaction.rabobanknonsepatransaction import RabobankNonSEPATransaction
from converter.transaction.rabobanksepatransaction import RabobankSEPATransaction
from converter.transaction.nulltransaction import NullTransaction
from converter.transaction.transaction import CSVParseError

TEST_FILE_DIR = "test/data/"

RABOBANK_TRANSACTIONS_SEPA = TEST_FILE_DIR + "rabobank-transactions-SEPA.csv"
RABOBANK_TRANSACTIONS_SEPA_NUM_RECORDS = 4

RABOBANK_TRANSACTIONS_NON_SEPA = TEST_FILE_DIR + "rabobank-transactions-non-SEPA.csv"
RABOBANK_TRANSACTIONS_NON_SEPA_NUM_RECORDS = 6

UNKNOWN_TRANSACTIONS = TEST_FILE_DIR + "unknown-transactions.csv"
UNKNOWN_TRANSACTIONS_NUM_RECORDS = 4

MALFORMED_SEPA = TEST_FILE_DIR + "malformed-SEPA.csv"
MALFORMED_SEPA_NUM_RECORDS = 4

MALFORMED_NON_SEPA = TEST_FILE_DIR + "rabobank-transactions-malformed-non-SEPA.csv"
MALFORMED_NON_SEPA_NUM_RECORDS = 6

RABOBANK_5_DUPLICATE_TRANSACTIONS_MIXED = TEST_FILE_DIR + "rabobank-5-duplicate-transactions-mixed.csv"
RABOBANK_5_DUPLICATE_TRANSACTIONS_MIXED_NUM_RECORDS = 5

IBAN_RABOBANK_PREFIX = converter.transaction.transaction.IBAN_RABOBANK_PREFIX
NUM_FIELDS_SEPA = converter.transaction.rabobanksepatransaction.NUM_FIELDS_SEPA
NUM_FIELDS_NON_SEPA = converter.transaction.rabobanknonsepatransaction.NUM_FIELDS_NON_SEPA

class TestRaboCSVReader(unittest.TestCase):

    def setUp(self):
        self.reader = TransactionCSVReader()

    def readCSVFile(self, filename):
        self.reader.readCSV(filename)
        self.transactions = self.reader.transactions
        self.firstTransaction = self.transactions[0]

    def testBorkedFileName(self):
        self.assertRaises(IOError, self.readCSVFile, "Bork! Bork! Bork!")
        
    def testReadingSEPACSVFile(self):
        self.readCSVFile(RABOBANK_TRANSACTIONS_SEPA)
        
        self.assertEqual(RABOBANK_TRANSACTIONS_SEPA_NUM_RECORDS, len(self.transactions))
        self.assertEqual(NUM_FIELDS_SEPA, len(self.firstTransaction))
        self.assertTrue(self.firstTransaction[0].startswith(IBAN_RABOBANK_PREFIX))

    def testReadingTwoCSVFiles(self):
        self.readCSVFile(RABOBANK_TRANSACTIONS_SEPA)
        self.readCSVFile(RABOBANK_TRANSACTIONS_NON_SEPA)
        
        self.assertEqual(RABOBANK_TRANSACTIONS_NON_SEPA_NUM_RECORDS + RABOBANK_TRANSACTIONS_SEPA_NUM_RECORDS, len(self.transactions))

    def testReadingNonSEPACSVFile(self):
        self.readCSVFile(RABOBANK_TRANSACTIONS_NON_SEPA)
        self.assertEqual(RABOBANK_TRANSACTIONS_NON_SEPA_NUM_RECORDS, len(self.transactions))
        self.assertEqual(NUM_FIELDS_NON_SEPA, len(self.firstTransaction))
        self.assertFalse(self.firstTransaction[0].startswith(IBAN_RABOBANK_PREFIX))

    def testReadingUnknownTransactionsCSVFile(self):
        self.readCSVFile(UNKNOWN_TRANSACTIONS)

        for transaction in self.reader:
            self.assertTrue(isinstance(transaction, NullTransaction))
        
    def testAllNonSEPATransactionsIdentified(self):
        self.readCSVFile(RABOBANK_TRANSACTIONS_NON_SEPA)
        
        for transaction in self.reader:
            self.assertTrue(isinstance(transaction, RabobankNonSEPATransaction), "Transaction: '" + str(transaction) + "' is not the " + str(RabobankNonSEPATransaction) + " as expected.")
        
    def testAllSEPATransactionsIdentified(self):
        self.readCSVFile(RABOBANK_TRANSACTIONS_SEPA)
        
        for transaction in self.reader:
            self.assertTrue(isinstance(transaction, RabobankSEPATransaction), "Transaction: '" + str(transaction) + "' is not the " + str(RabobankSEPATransaction) + " as expected.")
        
    def testMixedTransactionsIdentified(self):
        self.readCSVFile(RABOBANK_TRANSACTIONS_SEPA)
        self.readCSVFile(RABOBANK_TRANSACTIONS_NON_SEPA)
        self.readCSVFile(UNKNOWN_TRANSACTIONS)
        
        self.assertEquals(RABOBANK_TRANSACTIONS_SEPA_NUM_RECORDS + RABOBANK_TRANSACTIONS_NON_SEPA_NUM_RECORDS + UNKNOWN_TRANSACTIONS_NUM_RECORDS, len(self.transactions))
        
        num_SEPA_records = 0
        num_non_SEPA_records = 0
        num_unknown_records = 0
        
        for transaction in self.reader:
            if isinstance(transaction, RabobankSEPATransaction):
                num_SEPA_records += 1
            elif isinstance(transaction, RabobankNonSEPATransaction):
                num_non_SEPA_records +=1
            elif isinstance(transaction, NullTransaction):
                num_unknown_records +=1
            else:
                self.fail("transaction type " + str(transaction.__class__) + " unknown to this test.")

        self.assertEquals(RABOBANK_TRANSACTIONS_NON_SEPA_NUM_RECORDS, num_non_SEPA_records)
        self.assertEquals(RABOBANK_TRANSACTIONS_SEPA_NUM_RECORDS, num_SEPA_records)
        self.assertEquals(UNKNOWN_TRANSACTIONS_NUM_RECORDS, num_unknown_records)
            
    def testDuplicates(self):
        self.readCSVFile(RABOBANK_TRANSACTIONS_SEPA)
        self.readCSVFile(RABOBANK_TRANSACTIONS_NON_SEPA)
        self.readCSVFile(MALFORMED_SEPA)
        self.readCSVFile(RABOBANK_5_DUPLICATE_TRANSACTIONS_MIXED)
        
        self.assertEqual(RABOBANK_TRANSACTIONS_SEPA_NUM_RECORDS + RABOBANK_TRANSACTIONS_NON_SEPA_NUM_RECORDS + MALFORMED_SEPA_NUM_RECORDS + RABOBANK_5_DUPLICATE_TRANSACTIONS_MIXED_NUM_RECORDS, len(self.transactions))
        self.assertEqual(RABOBANK_TRANSACTIONS_SEPA_NUM_RECORDS + RABOBANK_TRANSACTIONS_NON_SEPA_NUM_RECORDS + MALFORMED_SEPA_NUM_RECORDS, len(self.reader.deduplicated()))

    def testMassiveDuplicates(self):
        num_duplicate_runs = 10
        # Tested this with 100000 times, ran in 4.5s. Good enough.
        for i in range(0, num_duplicate_runs):
            self.readCSVFile(RABOBANK_TRANSACTIONS_SEPA)
        
        self.assertEqual(RABOBANK_TRANSACTIONS_SEPA_NUM_RECORDS * num_duplicate_runs, len(self.transactions))
        self.assertEqual(RABOBANK_TRANSACTIONS_SEPA_NUM_RECORDS, len(self.reader.deduplicated()))
        # Check that multiple calls don't screw up in light of the caching of deduplicated transactions
        self.assertEqual(RABOBANK_TRANSACTIONS_SEPA_NUM_RECORDS, len(self.reader.deduplicated()))
        
    def testValidationOfMalformedTransaction(self):
        self.readCSVFile(MALFORMED_SEPA)
        self.readCSVFile(MALFORMED_NON_SEPA)
        
        for transaction in self.reader:
            self.assertRaises(CSVParseError, transaction.validate)
            
            # For testing what is going wrong: comment out above line, uncomment below lines.
            #try:
            #    print transaction
            #    self.reader.validate(transaction)
            #except CSVParseError, e:
            #    print e

if __name__ == '__main__':
    unittest.main()