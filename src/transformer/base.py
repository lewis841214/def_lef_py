
class LineClearer:
    '''
    This is the base class for all the line cleaners.
    The input line will be "raw" line.
    return the "cleaned" line.
    '''
    def clear_line(self, line):
        pass

class LineSeperator:
    '''
    This is the base class for all the line seperators.
    The input line will be "cleaned" line.
    return the "seperated" line.
    '''
    def seperator(self, line):
        pass

class ComponentFormatter:
    '''
    Given separated line with n components, 
    return a dict which assign each component as key or values.
    '''
    def formater(self, line):
        pass

class LineTransformer:
    '''
    This is the base class for all the line transformers.

    The structure of each line will be formated as:
    <sign (optional)> <key1> <key2> <value>
    '''
    def __init__(self, clean_type):
        self.clean_type = clean_type
        self.cleaner = LineClearer()
        
    def clear_line(self, line):
        return line.strip()
    
    def transform(self, line):
        pass
