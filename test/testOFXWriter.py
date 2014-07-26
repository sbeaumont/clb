import unittest
from ofxwriter import OFXWriter

expectedOutput = """<OFX>
  <BANKMSGSRSV1>
    <STMTTRNRS>
      <STMTRS>
        <CURDEF>EUR</CURDEF>
        <BANKACCTFROM>1234</BANKACCTFROM>
        <BANKTRANLIST>
          <STMTTRN>
            <NAME>name</NAME>
            <DTPOSTED>20140607</DTPOSTED>
            <TRNTYPE>DEBIT</TRNTYPE>
            <TRNAMT>-50.00</TRNAMT>
            <BANKACCTTO>NL20RABO123456890</BANKACCTTO>
            <MEMO>desc</MEMO>
          </STMTTRN>
          <STMTTRN>
            <NAME>name</NAME>
            <DTPOSTED>20140607</DTPOSTED>
            <TRNTYPE>DEBIT</TRNTYPE>
            <TRNAMT>-50.00</TRNAMT>
            <BANKACCTTO>NL20RABO123456890</BANKACCTTO>
            <MEMO>desc</MEMO>
          </STMTTRN>
          <STMTTRN>
            <NAME>name</NAME>
            <DTPOSTED>20140607</DTPOSTED>
            <TRNTYPE>DEBIT</TRNTYPE>
            <TRNAMT>-50.00</TRNAMT>
            <BANKACCTTO>NL20RABO123456890</BANKACCTTO>
            <MEMO>desc</MEMO>
          </STMTTRN>
        </BANKTRANLIST>
      </STMTRS>
    </STMTTRNRS>
  </BANKMSGSRSV1>
</OFX>
"""

class TestTransaction:
    def fromAccount(self):
        return "1234"
    
    def name(self):
        return "name"
    
    def date(self):
        return "20140607"
    
    def type(self):
        return "DEBIT"
    
    def amount(self):
        return "-50.00"
    
    def to(self):
        return "NL20RABO123456890"
        
    def description(self):
        return "desc"

class TestOFXWriter(unittest.TestCase):
    def setUp(self):
        self.writer = OFXWriter()

    def testWrite(self):
        self.writer.addTransaction(TestTransaction())
        self.writer.addTransaction(TestTransaction())
        self.writer.addTransaction(TestTransaction())
        
        self.assertEquals(self.writer.write(), expectedOutput)
