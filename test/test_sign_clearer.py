from src._def.transformer.specific import SignLineClearer

# Test the SignLineClearer with DEF file format signs
def test_sign_clearer():
    # Common signs in DEF files
    sign_list = ['+', '-']
    clearer = SignLineClearer(sign_list)
    
    # Test cases based on the DEF file format
    test_lines = [
        "- I1 B",
        "  + EEQMASTER A",
        "  + GENERATE generator ",
        "  + SOURCE NETLIST",
        "  + FOREIGN gds2name ( -500 -500 ) N",
        "  + PLACED ( 100 100 ) N",
        "  + WEIGHT 100",
        "  + REGION region1 ",
        "  + MASKSHIFT 1102",
        "  + HALO 5 6 7 8",
        "  + HALO SOFT 5 6 7 8",
        "  + ROUTEHALO 100 METAL1 M3",
        "  + PROPERTY strprop \"aString\" ",
        "  + PROPERTY intprop 1 ",
        "  + PROPERTY realprop 1.1 ",
        "  + PROPERTY intrangeprop 25",
        "  + PROPERTY realrangeprop 25.25 ;",
        "DESIGN test_design ;",
        "VERSION 5.8 ;"
    ]
    
    print("Original Line -> Cleaned Line")
    print("-" * 50)
    
    for line in test_lines:
        cleaned = clearer.clear_line(line)
        print(f"'{line}' -> '{cleaned}'")

if __name__ == "__main__":
    test_sign_clearer() 