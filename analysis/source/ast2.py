import ast
import _ast

class Assign(_ast.AST):            _fields = ('targets', 'value', 'decltype',)
class Label(_ast.AST):             _fields = ('body', 'name',)
class Increment(_ast.AST):         _fields = ('target',)
class Statement(_ast.AST):         _fields = ('expr',)
class Declaration(_ast.AST):       _fields = ('typename', 'name',)
class Goto(_ast.AST):              _fields = ('label',)
class Asm(_ast.AST):               _fields = ('instr',)
class Todo(_ast.AST):              _fields = ('text',)
class DoWhile(_ast.AST):           _fields = ('test', 'body', 'orelse',)
class ForEach(_ast.AST):           _fields = ('typename', 'variable', 'source', 'body')
class Dereference(_ast.AST):       _fields = ('pointer',)
class AddressOf(_ast.AST):         _fields = ('variable',)
class Name(_ast.AST):              _fields = ('id',)
class Call(_ast.AST):              _fields = ('func', 'args',)
class ObjCMessageSend(_ast.AST):   _fields = ('receiver', 'selector', 'args',)
class ObjCString(_ast.AST):        _fields = ('value',)
class ObjCSelector(_ast.AST):      _fields = ('value',)
class FieldAccess(_ast.AST):       _fields = ('object', 'field',)
class ObjCFunctionDef(_ast.AST):   _fields = ('classname', 'selector', 'args', 'body', 'static', 'returntype',)
class CFunctionDef(_ast.AST):      _fields = ('name', 'args', 'body', 'returntype',)
class BlockDefinition(_ast.AST):   _fields = ('body',)

class Equals(_ast.AST):            _fields = ('left', 'right')
class Negation(_ast.AST):          _fields = ('value',)

BinOp = ast.BinOp
BoolOp = ast.BoolOp
Expression = ast.Expression
Str = ast.Str
Num = ast.Num
Compare = ast.Compare
Gt = ast.Gt
GtE = ast.GtE
Lt = ast.Lt
LtE = ast.LtE
If = ast.If
While = ast.While
Return = ast.Return

Add = ast.Add
Sub = ast.Sub
Mult = ast.Mult
Div = ast.Div
Mod = ast.Mod

And = ast.And
Or = ast.Or
Xor = ast.BitXor
Shl = ast.LShift
Shr = ast.RShift
