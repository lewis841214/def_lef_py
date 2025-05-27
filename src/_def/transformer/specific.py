from .base import LineClearer, LineSeperator, LineFormatter, BlockTransformer, SectionTransformer

#############################################
# Common Line cleaner
#############################################
class CommonLineClearer(LineClearer):
    def __init__(self):
        self.end_sign = ';'

    def clear_line(self, line):
        # Strip whitespace from the line
        cleaned_line = line.strip()
        
        # Remove the end sign if present
        if cleaned_line.endswith(self.end_sign):
            cleaned_line = cleaned_line[:-1].strip()
        
        return cleaned_line

class CommonLineSeperator(LineSeperator):

    def seperate(self, line):
        """
        Separate line into tokens following these rules:
        1. + word should be put together as "+ word"
        2. ( ) content should be put together
        3. " " content should be put together
        """
        tokens = []
        i = 0
        line = line.strip()
        
        while i < len(line):
            # Skip whitespace
            while i < len(line) and line[i].isspace():
                i += 1
            
            if i >= len(line):
                break
            
            # Rule 1: Handle + followed by word
            if line[i] == '+' and i + 1 < len(line):
                # Find the end of the word after +
                j = i + 1
                # Skip whitespace after +
                while j < len(line) and line[j].isspace():
                    j += 1
                # Find end of word
                word_start = j
                while j < len(line) and not line[j].isspace() and line[j] not in '()':
                    j += 1
                if word_start < j:
                    tokens.append(f"+ {line[word_start:j]}")
                    i = j
                else:
                    tokens.append('+')
                    i += 1
                continue
            
            # Rule 2: Handle parentheses content
            if line[i] == '(':
                j = i + 1
                paren_count = 1
                while j < len(line) and paren_count > 0:
                    if line[j] == '(':
                        paren_count += 1
                    elif line[j] == ')':
                        paren_count -= 1
                    j += 1
                tokens.append(line[i:j])
                i = j
                continue
            
            # Rule 3: Handle quoted content
            if line[i] == '"':
                j = i + 1
                while j < len(line) and line[j] != '"':
                    if line[j] == '\\':  # Handle escaped quotes
                        j += 2
                    else:
                        j += 1
                if j < len(line):  # Include closing quote
                    j += 1
                tokens.append(line[i:j])
                i = j
                continue
            
            # Handle regular words
            j = i
            while j < len(line) and not line[j].isspace() and line[j] not in '()"':
                j += 1
            tokens.append(line[i:j])
            i = j
        
        return tokens

#############################################
# Specific Line formatter
#############################################
class ComponentHeadFormatter(LineFormatter):
    '''
    - compName modelName[netName | *]
    '''
    
    def format(self, seperate_components):
        # breakpoint()
        ins_name = seperate_components[1]
        cell_name = seperate_components[2]
        return {
            'ins_name': ins_name,
            'cell_name': cell_name
        }

class NetHeadFormatter(LineFormatter):
    '''
    - { netName [( {compName | PIN} pinName 
#           [+ SYNTHESIZED])]
    '''
    
    def format(self, seperate_components):
        net_name = seperate_components[1]

        connections = []
        for ins_pin in seperate_components[2:]:
            # ins_pin = "( ins_name pin_name )"
            # Remove parentheses and split by whitespace
            cleaned = ins_pin.strip('() ')
            parts = cleaned.split()
            if len(parts) >= 2:
                ins_name = parts[0]
                pin_name = parts[1]
                connections.append({
                    'ins_name': ins_name,
                    'pin_name': pin_name
                })
            else:
                breakpoint()
        return {
            'net_name': net_name,
            'connections': connections
        }

#############################################
# Specific Section transformer
#############################################

class NoPerpertySectionTransformer(SectionTransformer):
    '''
    Currently, we don't need to parse the properties of the section, so we only need to parse the head line.
    '''
    def __init__(self, line_cleaner, line_seperator, line_formatter):
        self.line_cleaner = line_cleaner
        self.line_seperator = line_seperator
        self.line_formatter = line_formatter

    def transform(self, raw_section : dict):
        '''
        input: {'head_section': , 'property_section':[]}
        '''
        head_line = raw_section['head_section']
        cleaned_head_line = self.line_cleaner.clear_line(head_line)
        seperated_head_line = self.line_seperator.seperate(cleaned_head_line)
        formatted_head_line = self.line_formatter.format(seperated_head_line)
        return formatted_head_line


#############################################
# Specific Block transformer
#############################################

class NoPropertyBlockTransformer(BlockTransformer):
    '''
    '''
    def __init__(self, line_cleaner, line_seperator, line_formatter):
        self.section_transformer = NoPerpertySectionTransformer(
            line_cleaner,
            line_seperator,
            line_formatter
        )

    def transform(self, list_of_raw_sections : list[dict]):
        '''
        input: [{'head_section': , 'property_section':[]}]
        '''
        component_list = []
        
        for raw_section in list_of_raw_sections:
            component_section = self.section_transformer.transform(raw_section)
            
            component_list.append(component_section)

        return component_list

component_block_transformer = NoPropertyBlockTransformer(
    CommonLineClearer(),
    CommonLineSeperator(),
    ComponentHeadFormatter()
)

net_block_transformer = NoPropertyBlockTransformer(
    CommonLineClearer(),
    CommonLineSeperator(),
    NetHeadFormatter()
)