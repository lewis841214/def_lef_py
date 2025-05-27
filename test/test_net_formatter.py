import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src._def.transformer.specific import NET_Head_formatter

def test_net_formatter():
    # Create formatter instance
    formatter = NET_Head_formatter()
    
    # Test with example data
    # Simulating separated components from a NET line
    test_cases = [
        {
            'description': 'Simple net with two connections',
            'seperate_components': [
                '- net1',  # net name
                '( inst1 pin_A )',  # first connection
                '( inst2 pin_B )'   # second connection
            ]
        },
        {
            'description': 'Net with PIN connection',
            'seperate_components': [
                '- clk_net',
                '( PIN clk_in )',
                '( cpu_inst clk )',
                '( mem_inst clk_port )'
            ]
        },
        {
            'description': 'Single connection net',
            'seperate_components': [
                '- power_net',
                '( power_inst vdd )'
            ]
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{test_case['description']}:")
        print(f"Input: {test_case['seperate_components']}")
        
        result = formatter.formater(test_case['seperate_components'])
        print(f"Parsed result:")
        print(f"  Net name: {result['net_name']}")
        print(f"  Connections:")
        for i, conn in enumerate(result['connections']):
            print(f"    {i+1}: ins_name='{conn['ins_name']}', pin_name='{conn['pin_name']}'")
        print("-" * 50)

def test_individual_parsing():
    """Test the individual parsing logic"""
    print("\nTesting individual ins_pin parsing:")
    
    test_pins = [
        "( inst1 pin_A )",
        "( PIN clk_in )",
        "( cpu_inst clk )",
        "( mem_inst clk_port )"
    ]
    
    for ins_pin in test_pins:
        # Simulate the parsing logic
        cleaned = ins_pin.strip('() ')
        parts = cleaned.split()
        if len(parts) >= 2:
            ins_name = parts[0]
            pin_name = parts[1]
            print(f"'{ins_pin}' -> ins_name: '{ins_name}', pin_name: '{pin_name}'")

if __name__ == "__main__":
    test_individual_parsing()
    test_net_formatter() 