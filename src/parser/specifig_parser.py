from src.parser.base import BaseParser

class HeaderParser(BaseParser):
    

    def parse(self, f, first_line, keyward):
        return [first_line]

class BlockParserNoEnd(BaseParser):

    def parse(self, f, first_line, keyward):
        self.record = [first_line]
        if ";" in first_line:
            return self.record
        else:
            while (line := f.readline()) and ";" not in line:
                self.record.append(line)
            self.record.append(line)
        return self.record
    
class BlockParserWithEnd(BaseParser):
    def __init__(self):
        self.dash_parser = DashParser()

    def parse(self, f, first_line, keyward):
        self.record = []
        while line := f.readline():
            if line.strip().startswith("- "):
                self.record.append(self.dash_parser.parse(f, line, keyward) )
            if line == '\n':
                continue
            if line.strip() == f"END {keyward}":
                break
        return self.record

class DashParser(BaseParser):

    def parse(self, f, first_line, keyward):
        self.record = {
            'head_section': first_line,
            'property_section': [],
        }
        if ";" in first_line:
            return self.record
        else:
            while line := f.readline():
                self.record['property_section'].append(line)
                if ";" in line:
                    break
        return self.record

class PBlockParserWithEnd(BaseParser):
    def __init__(self):
        self.dash_parser = DashParser()

    def parse(self, f, first_line, keyward):
        # pn = first_line.split()[1]
        self.record = []
        while line := f.readline():
            if line.strip() == f"END {keyward}":
                break
            else:
                self.record.append(line)
        return self.record

class PnBlockParserWithEnd(BaseParser):
    def __init__(self):
        self.dash_parser = DashParser()

    def parse(self, f, first_line, keyward):
        pn = first_line.split()[1]
        
        self.record = []
        while line := f.readline():
            
            if line.startswith(f"END"):# TODO: 这里需要修改
                break
            else:
                self.record.append(line)
        return self.record
