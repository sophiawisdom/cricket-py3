import re
import subprocess

from analysis.arch.architecture import AArch64Architecture


class DyldInfoReader(object):
    def __init__(self, arch, executable):

        bind_info = subprocess.check_output(["xcrun", "dyldinfo", "-arch", arch.archvalue, "-bind", executable])
        bind_lines = bind_info.decode('utf-8').split("\n")[2:]
        lazy_bind_info = subprocess.check_output(["xcrun", "dyldinfo", "-arch", arch.archvalue, "-lazy_bind", executable])
        lazy_bind_lines = lazy_bind_info.decode('utf-8').split("\n")[2:]

        symbol_stub_info = subprocess.check_output(["otool", "-arch", arch.archvalue, "-V", "-s", "__TEXT", arch.stubs_section_name, executable])
        symbol_stub_lines = symbol_stub_info.decode('utf-8').split("\n")[2:]

        self.arch = arch
        self.items = []
        self.stubs = []
        for line in bind_lines:
            if line.strip() == "": continue

            unpack = re.split('[ \n\r]+', line)
            segment = unpack[0]
            section = unpack[1]
            addr = int(unpack[2], 16)
            dylib = unpack[5]
            symbol = unpack[6]
            self.items.append({"segment": segment, "section": section, "addr": addr, "dylib": dylib, "symbol": symbol})

        for line in lazy_bind_lines:
            if line.strip() == "": continue

            unpack = re.split('[ \n\r]+', line)
            segment = unpack[0]
            section = unpack[1]
            addr = int(unpack[2], 16)
            dylib = unpack[4]
            symbol = unpack[5]
            self.items.append({"segment": segment, "section": section, "addr": addr, "dylib": dylib, "symbol": symbol})

        idx = 0
        while idx < len(symbol_stub_lines):
            line = symbol_stub_lines[idx]
            idx += 1

            if line.strip() == "": continue

            if arch != AArch64Architecture:
                unpack = re.split('[ \t]+', line)
                addr = int(unpack[0], 16)
                instr = unpack[1]
                if instr == "jmpl":
                    symbol_addr = int(unpack[2].replace("*", ""), 16)
                elif instr == "jmpq":
                    m = re.match("\*(0x[0-9a-f]+)\\(%rip\\)", unpack[2])
                    assert m
                    rel = int(m.group(1), 16)
                    symbol_addr = addr + rel + 6 # RIP points to the next instruction, "JMPQ" is 6 bytes long
            else:
                unpack = re.split('[\t]+', line)
                addr = int(unpack[0], 16)
                instr = unpack[1]
                assert instr == "nop"

                line = symbol_stub_lines[idx]
                idx += 1
                unpack = re.split('[\t]+', line)
                # addr = int(unpack[0], 16)
                instr = unpack[1]
                assert instr == "ldr"
                m = re.match("x16, #([0-9a-f]+)", unpack[2])
                assert m
                rel = int(m.group(1), 10)
                symbol_addr = addr + rel + 4  # On AArch64, PC points to next instruction.

                line = symbol_stub_lines[idx]
                idx += 1
                unpack = re.split('[\t]+', line)
                # addr = int(unpack[0], 16)
                instr = unpack[1]
                assert instr == "br"

            self.stubs.append({"addr": addr, "symbol_addr": symbol_addr})

    def get_class_refs(self):
        class_refs = {}
        for item in self.items:
            if item["section"] == "__objc_classrefs":
                class_refs[item["addr"]] = item
        return class_refs

    def get_symbols(self):
        syms = {}
        for item in self.items:
            if item["section"] in ["__la_symbol_ptr", "__nl_symbol_ptr"]:
                syms[item["addr"]] = item["symbol"]
        return syms

    def get_imported_data_symbols(self):
        syms = {}
        for item in self.items:
            if item["section"] in ["__const"]:
                syms[item["addr"]] = item["symbol"]
        return syms

    def get_stubs(self):
        symbols = self.get_symbols()
        result = {}
        for item in self.stubs:
            sym_addr = item["symbol_addr"]
            if not sym_addr in list(symbols.keys()): continue
            sym = symbols[sym_addr]
            result[item["addr"]] = sym
        return result

    def get_external_pointers(self):
        syms = {}
        for item in self.items:
            if item["section"] in ["__got"]:
                syms[item["addr"]] = item["symbol"]

        return syms
