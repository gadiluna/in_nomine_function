import argparse
from utils.RadareFunctionAnalyzer import RadareFunctionAnalyzer


def get_functions_data(input_executable, symbolic):
    analyzer = RadareFunctionAnalyzer(input_executable, use_symbol=False, depth=1)
    functions = analyzer.analyze()

    instructions = []
    addresses = []
    for function in functions.keys():
        if symbolic or function.startswith("fcn.") or function.startswith("sub."):
            addresses.append(str(functions[function]["address"])+","+str(function))
            instructions.append(functions[function]["filtered_instructions"])
    return instructions, addresses


def dump_data_to_file(data, output_data_file):
    with open(output_data_file, "w") as f:
        for d in data:
            if isinstance(d, list):
                f.write(" ".join(d) + "\n")
            else:
                f.write(d + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, help="Executable file to analyze")
    parser.add_argument("-o", "--output", type=str, help="Suffix for data file. This will dump two files: \
                                                         *suffix*.asm and *suffix*.meta")
    parser.add_argument("-s", "--symbolic", action="store_true", help="Dump data also for functions with a symbol")
    args = parser.parse_args()

    print("Analyzing file: {}".format(args.input))
    instructions, addresses = get_functions_data(args.input, symbolic=args.symbolic)
    assert len(instructions) == len(addresses)
    print("Found {} functions".format(len(instructions)))

    print("Dumping functions asm to: {}".format(args.output+".asm"))
    dump_data_to_file(instructions, args.output+".asm")

    print("Dumping functions metadata to: {}".format(args.output+".meta"))
    dump_data_to_file(addresses, args.output+".meta")


