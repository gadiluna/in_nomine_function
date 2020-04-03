# SAFE TEAM
#
#
# distributed under license: CC BY-NC-SA 4.0 (https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.txt) #
#
import json
import r2pipe


class RadareFunctionAnalyzer:

    def __init__(self, filename, use_symbol, depth):
        self.r2 = r2pipe.open(filename, flags=['-2'])
        self.filename = filename
        self.arch, self.bits = self.get_arch()
        self.top_depth = depth
        self.use_symbol = use_symbol

    def __enter__(self):
        return self

    @staticmethod
    def filter_reg(op):
        return op["value"]

    @staticmethod
    def filter_imm(op):
        imm = int(op["value"])
        if -int(5000) <= imm <= int(5000):
            ret = str(hex(op["value"]))
        else:
            ret = str('HIMM')
        return ret

    @staticmethod
    def filter_mem(op):
        if "base" not in op:
            op["base"] = 0

        if op["base"] == 0:
            r = "[" + "MEM" + "]"
        else:
            reg_base = str(op["base"])
            disp = str(op["disp"])
            scale = str(op["scale"])
            r = '[' + reg_base + "*" + scale + "+" + disp + ']'
        return r

    @staticmethod
    def filter_memory_references(i):
        inst = "" + i["mnemonic"]

        for op in i["operands"]:
            if op["type"] == 'reg':
                inst += " " + RadareFunctionAnalyzer.filter_reg(op)
            elif op["type"] == 'imm':
                inst += " " + RadareFunctionAnalyzer.filter_imm(op)
            elif op["type"] == 'mem':
                inst += " " + RadareFunctionAnalyzer.filter_mem(op)
            if len(i["operands"]) > 1:
                inst = inst + ","

        if "," in inst:
            inst = inst[:-1]
        inst = inst.replace(" ", "_")

        return str(inst)

    @staticmethod
    def get_callref(my_function, depth):
        calls = {}
        if 'callrefs' in my_function and depth > 0:
            for cc in my_function['callrefs']:
                if cc["type"] == "C":
                    calls[cc['at']] = cc['addr']
        return calls

    def get_instruction(self):
        instruction = json.loads(self.r2.cmd("aoj 1"))
        if len(instruction) > 0:
            instruction = instruction[0]
        else:
            return None

        operands = []
        if 'opex' not in instruction:
            return None

        for op in instruction['opex']['operands']:
            operands.append(op)
        instruction['operands'] = operands
        return instruction

    def function_to_inst(self, my_function):
        instructions = []
        s = my_function['vaddr'] if self.use_symbol else my_function['offset']
        self.r2.cmd('s ' + str(s))

        end_address = s + my_function["size"] if self.use_symbol else s + my_function["realsz"]

        while s < end_address:
            instruction = self.get_instruction()
            filtered_instruction = "X_" + RadareFunctionAnalyzer.filter_memory_references(instruction)
            instructions.append(filtered_instruction)
            self.r2.cmd("so 1")
            s = int(self.r2.cmd("s"), 16)

        return instructions

    def get_arch(self):
        try:
            info = json.loads(self.r2.cmd('ij'))
            if 'bin' in info:
                arch = info['bin']['arch']
                bits = info['bin']['bits']
        except:
            print("Error loading file")
            arch = None
            bits = None
        return arch, bits

    def find_functions(self):
        self.r2.cmd('aaa')
        try:
            function_list = json.loads(self.r2.cmd('aflj'))
        except:
            function_list = []
        return function_list

    def find_functions_by_symbols(self):
        self.r2.cmd('aa')
        try:
            symbols = json.loads(self.r2.cmd('isj'))
            fcn_symb = [s for s in symbols if s['type'] == 'FUNC']
        except:
            fcn_symb = []
        return fcn_symb

    def analyze(self):
        function_list = self.find_functions_by_symbols() if self.use_symbol else self.find_functions()
        result = {}
        for my_function in function_list:
            address = my_function['vaddr'] if self.use_symbol else  my_function['offset']
            try:
                instructions = self.function_to_inst(my_function)
                result[my_function['name']] = {'filtered_instructions': instructions, "address": address}
            except:
                print("Error in functions: {} from {}".format(my_function['name'], self.filename))
        return result

    def close(self):
        self.r2.quit()

    def __exit__(self, exc_type, exc_value, traceback):
        self.r2.quit()



