from converter.rabocsvtoofxconverter import RaboConverter
import sys

converter = RaboConverter()
converter.convert(sys.argv[1])