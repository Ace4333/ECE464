import re
import sys

def parse_bench(file_path):
    inputs = []
    outputs = []
    gates = []

    # Regex patterns for line matching
    input_pattern  = re.compile(r"^INPUT\s*\(\s*([\w']+)\s*\)", re.IGNORECASE)
    output_pattern = re.compile(r"^OUTPUT\s*\(\s*([\w']+)\s*\)", re.IGNORECASE)
    gate_pattern   = re.compile(r"^([\w']+)\s*=\s*(\w+)\s*\((.*)\)", re.IGNORECASE)

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            # Ignore empty lines and comment lines
            if not line or line.startswith('#'):
                continue

            in_match = input_pattern.match(line)
            if in_match:
                inputs.append(in_match.group(1))
                continue

            out_match = output_pattern.match(line)
            if out_match:
                outputs.append(out_match.group(1))
                continue

            gate_match = gate_pattern.match(line)
            if gate_match:
                out_node = gate_match.group(1)
                gate_type = gate_match.group(2).upper()
                in_nodes = [node.strip() for node in gate_match.group(3).split(',') if node.strip()]
                
                gates.append({
                    'out': out_node,
                    'type': gate_type,
                    'inputs': in_nodes,
                    'count': len(in_nodes)
                })

    # Print nicely formatted results
    print("--- Circuit Benchmark Summary ---")
    print(f"Inputs  ({len(inputs)}): {', '.join(inputs)}")
    print(f"Outputs ({len(outputs)}): {', '.join(outputs)}")
    print("\nGates / Internal Nodes:")
    for g in gates:
        inputs_str = ", ".join(g['inputs'])
        print(f"{g['out']}: {g['count']}-input {g['type']} of {inputs_str}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_bench.py <circuit_file.bench>")
    else:
        parse_bench(sys.argv[1])