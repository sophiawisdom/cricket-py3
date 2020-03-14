#    
#    sym.py ... Symbols.
#    Copyright (C) 2010  KennyTM~ <kennytm@gmail.com>
#    
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

SYMTYPE_UNDEFINED = -1
SYMTYPE_GENERIC = 0
SYMTYPE_CSTRING = 3
SYMTYPE_CFSTRING = 4
SYMTYPE_OBJC_SEL = 5

_symtypeNames = dict((v, k) for k, v in list(globals().items()) if k.startswith('SYMTYPE_'))

class Symbol(object):
    """A symbol consists minimally of a VM address and a name. It represents a 
    mapping from one to the other. It is useful to get human-recognizable info
    from an address.
    
    .. attribute:: name
    
        The name of the symbol.
    
    .. attribute:: addr
    
        The address of the symbol
    
    .. attribute:: ordinal
    
        Index of this symbol in the local symbol table. If it does not live in
        the symbol table, the ordinal is -1.
    
    .. attribute:: libord
    
        The "library ordinal" of this symbol. If this symbol is not undefined,
        this value should be 0.
        
        For Mach-O objects, the library can be recovered with the method
        :meth:`~macho.loadcommands.dylib.MachO_FromLibord.dylibFromLibord` 
        patched in :mod:`macho.loadcommands.dylib`.
        
    .. attribute:: extern
    
        A boolean indicating whether this is an exported symbol.
    
    .. attribute:: symtype
    
        The type of symbol. Can be one of:
        
        +----------------------------+-----------------------------------+
        | Value                      | Meaning                           |
        +============================+===================================+
        | :const:`SYMTYPE_UNDEFINED` | Undefined (i.e. external) symbol. |
        +----------------------------+-----------------------------------+
        | :const:`SYMTYPE_GENERIC`   | Generic local symbol.             |
        +----------------------------+-----------------------------------+
        | :const:`SYMTYPE_CSTRING`   | C strings.                        |
        +----------------------------+-----------------------------------+
        | :const:`SYMTYPE_CFSTRING`  | CoreFoundation strings.           |
        +----------------------------+-----------------------------------+
        | :const:`SYMTYPE_OBJC_SEL`  | Objective-C selector.             |
        +----------------------------+-----------------------------------+
    
    .. attribute:: isThumb
    
        Whether this symbol is in Thumb. This is meaningful for ARM architecture
        only.
    
    """
    
    def __init__(self, name, addr, symtype, ordinal=-1, libord=0, extern=False, isThumb=False):
        self.name = name
        self.addr = addr
        self.symtype = symtype
        self.ordinal = ordinal
        self.libord = libord
        self.extern = extern
        self.isThumb = isThumb
    
    def __copy__(self):
        '''Create a copy of this symbol.'''
        return type(self)(*self._toTuple())
    copy = __copy__
    
    def _toTuple(self):
        return (self.name, self.addr, self.symtype, self.ordinal, self.libord, self.extern, self.isThumb)

    def __eq__(self, other):
        "Check whether two symbols are equivalent."
        return self._toTuple() == other._toTuple()
    
    def __hash__(self):
        "Compute the hash of the symbol."
        return hash(self._toTuple())
        
    
    def __str__(self):
        return "<Symbol({}) '{}':0x{:x}>".format(_symtypeNames[self.symtype], self.name, self.addr)
        
    def __repr__(self):
        args = [repr(self.name), '0x{:x}'.format(self.addr), _symtypeNames[self.symtype]]
        args_app = args.append
        if self.ordinal >= 0:
            args_app('ordinal={!r}'.format(self.ordinal))
        if self.libord:
            args_app('libord={!r}'.format(self.libord))
        if self.extern:
            args_app('extern=True')
        if self.isThumb:
            args_app('isThumb=True')
        return 'Symbol({})'.format(', '.join(args))

