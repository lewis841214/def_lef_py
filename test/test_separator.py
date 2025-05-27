import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src._def.transformer.specific import CommonLineSeperator

def test_separator():
    # Create separator instance
    separator = CommonLineSeperator([])
    
    # Test with your example
    test_line = '+ RECT V1 + MASK 1 ( -3600 2200 ) ( -2000 3800 )'
    
    print("Original line:")
    print(f"'{test_line}'")
    print("\nSeparated tokens:")
    
    tokens = separator.seperator(test_line)
    for i, token in enumerate(tokens):
        print(f"{i}: '{token}'")
    
    print("\n" + "="*50)
    
    # Test with more examples
    test_cases = [
        '+ RECT V1 + MASK 1 ( -3600 2200 ) ( -2000 3800 )',
        '+ PROPERTY strprop "aString with spaces"',
        '+ FOREIGN gds2name ( -500 -500 ) N',
        'DESIGN "test_design" VERSION 5.8',
        '+ HALO SOFT 5 6 7 8',
        '+ NESTED ( ( 100 200 ) ( 300 400 ) )'
    ]
    
    for test_case in test_cases:
        print(f"\nInput: '{test_case}'")
        tokens = separator.seperator(test_case)
        print("Tokens:", tokens)

if __name__ == "__main__":
    test_separator() 