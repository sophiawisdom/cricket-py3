import re

from analysis.arch.architecture import Architecture
from analysis.binary import Binary
from analysis.transforms import *


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Decompile an Objective-C function in a binary file.')
    parser.add_argument('--binary', type=str, help='the Mach-O binary (executable or library) to analyze')
    parser.add_argument('--arch', type=str, help='architecture to select from fat binaries')
    parser.add_argument('--select-class', type=str, help='Objective-C class to select')
    parser.add_argument('--select-method', type=str, help='Objective-C method to select (regexp allowed, first match wins)')

    args = parser.parse_args()
    if args.binary is None:
        parser.print_help()
        exit(1)

    print(("Using binary: %s" % args.binary))

    if args.arch is None:
        archs = Binary.list_architectures_from_file(args.binary)
        if len(archs) < 0:
            print("Cannot enumerate architectures from binary!")
            exit(1)

        if len(archs) > 1:
            print("Select an architecture with '--arch'. Available:")
            for a in archs:
                print(("  " + a.archvalue))
            exit(1)

        args.arch = archs[0].archvalue

    print(("Using architecture: %s" % args.arch))
    binary = Binary(args.binary, Architecture.get_arch_from_archvalue(args.arch))
    binary.load()

    if args.select_class is None:
        print("Select class with '--select-class'. Available:")
        for c in binary.classes:
            print(("  " + c.name))
        exit(1)

    cls = None
    for c in binary.classes:
        if c.name == args.select_class:
            cls = c
            break

    if cls is None:
        print("Class not found.")
        exit(1)

    print(("Using class: %s" % cls.name))

    if args.select_method is None:
        print("Select method with '--select-method'. Available:")
        for m in cls.methods:
            print(("  " + m.name))
        exit(1)

    method = None
    regexp = re.compile(args.select_method)
    for m in cls.methods:
        if regexp.match(m.name):
            method = m
            break

    if method is None:
        print("Method not found.")
        exit(1)

    print(("Using method: %s" % method.name))
    print("Decompiling...")
    print("")

    func = method.function
    
    func.load()
    print("Loaded func")
    auto_build_bbs(func)
    print("built bbs")
    auto_transform_bbs(func)
    print("transformed bbs")
    builder = UCodeBuilder(func)
    print("instantiated ucodebuilder")
    builder.build_ucode()
    print("built ucode")
    auto_transform_ucode(func, single_step=False)
    print("transformed ucode")
    func.ufunction.cfg = CFGGraph(func.ufunction)
    print("created cfg")
    auto_match_cfg(func, single_step=False)
    print("matched cfg")
    func.build_ast()
    print("built ast")
    auto_optimize_ast(func)
    print("optimized ast")

    ast_string, _ = func.print_ast()
    print(ast_string)
