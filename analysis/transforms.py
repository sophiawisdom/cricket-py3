from analysis.ucode.ucode_builder import UCodeBuilder
from analysis.ucode.ucode_cfg import CFGGraph
from analysis.ucode.ucode_transformsbb import *
from analysis.ucode.ucode_transformsfunction import *
from analysis.ucode.ucode_transformsinstruction import *


def auto_build_bbs(func):
    func.detect_basic_blocks()

def auto_transform_bbs(func):
    for i in range(0, 10):
        pattern = func.arch.sema.detect_pattern(func)
        if not pattern: break
        func.arch.sema.remove_pattern(func, pattern)
    # Strip BBs.
    # RemoveUnreachableBasicBlocks(func).run()
    # JoinLinearBasicBlocks(func).run()

def auto_build_ucode(func):
    builder = UCodeBuilder(func)
    builder.build_ucode()

def de_spill(func):
    UCodeApplyBasicBlockTransformToAll(func.ufunction, UCodeConvertStackVariablesToRegisters).perform()
    func.ufunction.compute_def_use_chains()
    t = UCodeApplyInstructionTransformToAll(func.ufunction, UCodeStackArgumentsToRegisters)
    t.binary = func.binary
    t.perform()

def propagate(func):
    func.ufunction.compute_def_use_chains()
    UCodeApplyInstructionTransformToAll(func.ufunction, UCodeCopyPropagateInstruction).perform()

def simplify(func):
    UCodeApplyInstructionTransformToAll(func.ufunction, UCodeRemovePCReferences).perform()
    UCodeApplyInstructionTransformToAll(func.ufunction, UCodeConstantFoldInstruction).perform()
    UCodeApplyInstructionTransformToAll(func.ufunction, UCodeRemoveUselessMoves).perform()
    func.ufunction.compute_def_use_chains()
    UCodeApplyInstructionTransformToAll(func.ufunction, UCodeFoldArithmeticChains).perform()
    func.ufunction.compute_def_use_chains()
    UCodeApplyInstructionTransformToAll(func.ufunction, UCodeRemoveUnusedCallResults).perform()

    UCodeApplyInstructionTransformToAll(func.ufunction, UCodeNormalizeArithmetics).perform()

def eliminate_ucode(func):
    func.ufunction.compute_def_use_chains()
    UCodeApplyInstructionTransformToAll(func.ufunction, UCodeDeadCodeEliminateInstruction).perform()

def ucode_patterns(func):
    func.ufunction.compute_def_use_chains()
    UCodeApplyBasicBlockTransformToAll(func.ufunction, UCodeDetectPattern1).perform()
    func.ufunction.compute_def_use_chains()
    UCodeApplyBasicBlockTransformToAll(func.ufunction, UCodeDetectPattern2).perform()
    func.ufunction.compute_def_use_chains()
    UCodeApplyBasicBlockTransformToAll(func.ufunction, UCodeDetectPattern3).perform()
    func.ufunction.compute_def_use_chains()
    UCodeApplyBasicBlockTransformToAll(func.ufunction, UCodeDetectPattern4).perform()

def arc(func):
    UCodeApplyInstructionTransformToAll(func.ufunction, UCodeRemoveRetainRelease).perform()

def resolve(func):
    t = UCodeApplyInstructionTransformToAll(func.ufunction, UCodeResolveIVars)
    t.binary = func.binary
    t.perform()

    func.ufunction.compute_def_use_chains()
    t = UCodeApplyInstructionTransformToAll(func.ufunction, UCodeResolveCalls)
    t.binary = func.binary
    t.perform()

    func.ufunction.compute_def_use_chains()
    t = UCodeApplyInstructionTransformToAll(func.ufunction, UCodeResolveUnknownCalls)
    t.binary = func.binary
    t.perform()

    t = UCodeApplyInstructionTransformToAll(func.ufunction, UCodeResolveSelectors)
    t.binary = func.binary
    t.perform()
    t = UCodeApplyInstructionTransformToAll(func.ufunction, UCodeResolveClassRefs)
    t.binary = func.binary
    t.perform()
    t = UCodeApplyInstructionTransformToAll(func.ufunction, UCodeResolveCFStrings)
    t.binary = func.binary
    t.perform()

    t = UCodeApplyInstructionTransformToAll(func.ufunction, UCodeResolveOffsetCalls)
    t.binary = func.binary
    t.perform()

    t = UCodeApplyInstructionTransformToAll(func.ufunction, UCodeResolveCCalls)
    t.binary = func.binary
    t.perform()


def strip_nops(func):
    UCodeApplyBasicBlockTransformToAll(func.ufunction, UCodeRemoveNopsFromBasicBlock).perform()


def auto_transform_ucode(func, single_step=False):
    changing = True
    while changing:
        changing = False
        ucode_pre, _ = func.ufunction.print_to_text(False, func)

        resolve(func)
        simplify(func)
        propagate(func)
        resolve(func)
        simplify(func)
        propagate(func)
        resolve(func)
        eliminate_ucode(func)
        de_spill(func)
        resolve(func)
        ucode_patterns(func)
        simplify(func)
        eliminate_ucode(func)
        strip_nops(func)
        arc(func)

        ucode_post, _ = func.ufunction.print_to_text(False, func)
        if ucode_post != ucode_pre: changing = True

        if single_step and changing: return

def auto_build_cfg(func):
    func.ufunction.cfg = CFGGraph(func.ufunction)


def auto_match_cfg(func, single_step=False):
    transforms = [
        func.ufunction.cfg.convert_if,
        func.ufunction.cfg.convert_if_else,
        func.ufunction.cfg.convert_sequence,
        func.ufunction.cfg.convert_while,
        func.ufunction.cfg.convert_single_bb_while,
        func.ufunction.cfg.convert_do_while,
        func.ufunction.cfg.convert_multi_if,
        func.ufunction.cfg.convert_infinite_loop,
        func.ufunction.cfg.convert_switch,

        # Damn, we can't find anything simple. Let's be more aggressive.
        func.ufunction.cfg.convert_early_return,
        func.ufunction.cfg.convert_duplicate_exit_node,
    ]

    changing = True
    while changing:
        changing = False

        num_root_nodes = len(func.ufunction.cfg.unassigned_bbs_with_cfg_roots)
        if num_root_nodes == 1: return

        for t in transforms:
            for cfg_node in func.ufunction.cfg.unassigned_bbs_with_cfg_roots:
                changing |= t(cfg_node)
                if single_step and changing: return

            if changing: break

        if single_step and changing: return

def auto_build_ast(func):
    func.build_ast()

def auto_optimize_ast(func):
    func.transform_ast()
