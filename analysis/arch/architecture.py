import subprocess

from capstone import *
from distorm3 import Decode32Bits, Decode64Bits

from analysis.arch.sema_aarch64 import SemaAArch64
from analysis.arch.sema_armv7 import SemaArmV7
from analysis.arch.sema_x86 import SemaX86


class Architecture:
    def __init__(self, name, archvalue, compilerflags):
        self.name = name
        self.archvalue = archvalue
        self.stubs_section_name = "__symbol_stub"
        self.compilerflags = compilerflags
        self.distorm_bits = None
        self.can_open = True

        self.capstone = None

        """:type : Cs"""
        self.otool_swap = 1
        self.bits = 32

        self.sema = None
        """:type : Sema"""

    def is64bit(self):
        return self.bits == 64

    def bytes(self):
        return self.bits // 8

    @staticmethod
    def get_arch_from_archvalue(archvalue):
        for arch in AvailableArchitectures:
            if arch.archvalue == archvalue:
                return arch

        assert False

    def __str__(self):
        return "Architecture %s (%d bit)" % (self.name, self.bits)

    def __repr__(self):
        return str(self)

    def __deepcopy__(self, memo):
        # Return self.
        result = self
        memo[id(self)] = result
        return result

SDKROOT_IPHONEOS = "/"
try:
    SDKROOT_IPHONEOS = subprocess.check_output(["xcrun", "-sdk", "iphoneos", "--show-sdk-path"]).strip()
except:
    pass
SDKROOT_IPHONESIMULATOROS = "/"
try:
    SDKROOT_IPHONESIMULATOROS = subprocess.check_output(["xcrun", "-sdk", "iphonesimulator", "--show-sdk-path"]).strip()
except:
    pass

I386Architecture = Architecture("i386", "i386", ["-arch", "i386", "-isysroot", SDKROOT_IPHONESIMULATOROS, "-mios-simulator-version-min=7.0"])
I386Architecture.distorm_bits = Decode32Bits
I386Architecture.capstone = Cs(CS_ARCH_X86, CS_MODE_32)
I386Architecture.capstone.detail = True
I386Architecture.sema = SemaX86(I386Architecture)

X86_64Architecture = Architecture("x86-64", "x86_64", ["-arch", "x86_64", "-isysroot", SDKROOT_IPHONESIMULATOROS, "-mios-simulator-version-min=7.0"])
X86_64Architecture.distorm_bits = Decode64Bits
X86_64Architecture.capstone = Cs(CS_ARCH_X86, CS_MODE_64)
X86_64Architecture.capstone.detail = True
X86_64Architecture.sema = SemaX86(X86_64Architecture)
X86_64Architecture.bits = 64
X86_64Architecture.stubs_section_name = "__stubs"

ArmV7Architecture = Architecture("armv7", "armv7", ["-arch", "armv7", "-isysroot", SDKROOT_IPHONEOS, "-mios-version-min=7.0"])
ArmV7Architecture.capstone = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
ArmV7Architecture.capstone.detail = True
ArmV7Architecture.otool_swap = 2
ArmV7Architecture.sema = SemaArmV7(ArmV7Architecture)
ArmV7Architecture.can_open = False

ArmV7SArchitecture = Architecture("armv7s", "armv7s", ["-arch", "armv7s", "-isysroot", SDKROOT_IPHONEOS, "-mios-version-min=7.0"])
ArmV7SArchitecture.capstone = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
ArmV7SArchitecture.capstone.detail = True
ArmV7SArchitecture.otool_swap = 2
ArmV7SArchitecture.sema = SemaArmV7(ArmV7SArchitecture)
ArmV7SArchitecture.can_open = False

AArch64Architecture = Architecture("aarch64", "arm64", ["-arch", "arm64", "-isysroot", SDKROOT_IPHONEOS, "-mios-version-min=7.0"])
AArch64Architecture.capstone = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
AArch64Architecture.capstone.detail = True
AArch64Architecture.otool_swap = 4
AArch64Architecture.sema = SemaAArch64(AArch64Architecture)
AArch64Architecture.bits = 64
AArch64Architecture.stubs_section_name = "__stubs"

AvailableArchitectures = [
    I386Architecture,
    X86_64Architecture,
    ArmV7Architecture,
    ArmV7SArchitecture,
    AArch64Architecture
]
