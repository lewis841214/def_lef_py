

class LineTransformer:
    '''
    This is the base class for all the line transformers.

    The structure of each line will be formated as:
    <sign (optional)> <key1> <key2> <value>
    '''
    def clear_line(self, line):
        return line.strip()
    
    def transform(self, line):
        pass

class PropertyLineTransformer(LineTransformer):
    def transform(self, line):
        pass
    

class DefParser:
    def __init__(self, def_file_path, Header_list, NoEndBlockList, WithEndBlockList):
        self.def_file_path = def_file_path
        self.Header_list = Header_list
        self.NoEndBlockList = NoEndBlockList
        self.WithEndBlockList = WithEndBlockList

        self.header_parser = HeaderParser()
        self.block_parser_no_end = BlockParserNoEnd()
        self.block_parser_with_end = BlockParserWithEnd()

        self.collector = {}

    def parse(self):
        # Main parse loop: for each line, find the right parser and delegate
        with open(self.def_file_path, "r", encoding='utf-8', errors='ignore') as f:
            while line := f.readline():
                try:
                    prefix = line.split()[0]
                except:
                    continue
                if prefix in self.Header_list:
                    self.collector[prefix] = self.header_parser.parse(f, line, prefix)
                elif prefix in self.NoEndBlockList:
                    if prefix not in self.collector:
                        self.collector[prefix] = []
                    self.collector[prefix].append(self.block_parser_no_end.parse(f, line, prefix))
                elif prefix in self.WithEndBlockList:
                    self.collector[prefix] = self.block_parser_with_end.parse(f, line, prefix)
                else:
                    print(f"Unknown prefix: {prefix}")
        breakpoint()


Header_list = set([
    "VERSION",
    "NAMESCASESENSITIVE",
    "DIVIDERCHAR",
    "BUSBITCHARS",
    "DESIGN",
    "TECHNOLOGY",
    "UNITS DISTANCE MICRONS"
])

WithEndBlockList = set([
    "PROPERTYDEFINITIONS",
    "VIAS",
    "STYLES",
    "NONDEFAULTRULES",
    "REGIONS",
    "COMPONENTS",
    "PINS",
    "PINPROPERTIES",
    "BLOCKAGES",

    "SPECIALNETS",
    "NETS",
    "SCANCHAINS",
    "GROUPS",
    "SLOTS",
    "FILLS",
    "BEGINEXT"
    
])

NoEndBlockList = set([
    "DIEAREA",
    "ROW",
    "TRACKS",
    "GCELLGRID",
])

if __name__ == "__main__":
    def_parser = DefParser("/home/lewis/1project/def_lef_py/test_data/complete.5.8.def", Header_list, NoEndBlockList, WithEndBlockList)
    def_parser.parse()
        