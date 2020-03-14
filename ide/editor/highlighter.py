# Based on
# http://ftp.ics.uci.edu/pub/centos0/ics-custom-build/BUILD/PyQt-x11-gpl-4.7.2/examples/richtext/syntaxhighlighter.py

from PyQt5 import QtCore, QtGui


class Highlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)

    def load_syntax_c(self):
        keywordFormat = QtGui.QTextCharFormat()
        keywordFormat.setForeground(QtCore.Qt.darkBlue)
        keywordFormat.setFontWeight(QtGui.QFont.Bold)

        keywords = "assign,strong,retain,atomic,nonatomic,BOOL,copy,readonly,readwrite," + \
            "char,class,const,double,enum,explicit,for,friend,id,if,inline,int,long,namespace,operator,private,protected," + \
            "public,return,short,signals,signed,slots,static,struct,template,typedef,typename,union,unsigned,virtual,void,volatile,while"
        keywords = keywords.split(",")

        keywordPatterns = ["\\b" + k + "\\b" for k in keywords]

        self.highlightingRules = [(QtCore.QRegExp(pattern), keywordFormat)
                for pattern in keywordPatterns]

        objc_keywords = "@interface,@end,@implementation,@class,@public,@package,@protected,@private,@property,@synthesize,@dynamic,@protocol,@required,@optional,@try,@catch,@finally,@throw,@selector,@protocol,@encode,@defs,@autoreleasepool,@synchronized,@compatibility_alias"
        objc_keywords = objc_keywords.split(",")
        keywordPatterns = [k for k in objc_keywords]
        for k in keywordPatterns:
            self.highlightingRules.append((QtCore.QRegExp(k), keywordFormat))

        classFormat = QtGui.QTextCharFormat()
        classFormat.setFontWeight(QtGui.QFont.Bold)
        classFormat.setForeground(QtCore.Qt.darkMagenta)
        self.highlightingRules.append((QtCore.QRegExp("\\bQ[A-Za-z]+\\b"),
                classFormat))

        singleLineCommentFormat = QtGui.QTextCharFormat()
        singleLineCommentFormat.setForeground(QtCore.Qt.darkGreen)
        self.highlightingRules.append((QtCore.QRegExp("//[^\n]*"),
                singleLineCommentFormat))

        self.multiLineCommentFormat = QtGui.QTextCharFormat()
        self.multiLineCommentFormat.setForeground(QtCore.Qt.darkGreen)

        quotationFormat = QtGui.QTextCharFormat()
        quotationFormat.setForeground(QtCore.Qt.darkGreen)
        self.highlightingRules.append((QtCore.QRegExp("\".*\""),
                quotationFormat))

        # functionFormat = QtGui.QTextCharFormat()
        # functionFormat.setFontItalic(True)
        # functionFormat.setForeground(QtCore.Qt.blue)
        # self.highlightingRules.append((QtCore.QRegExp("\\b[A-Za-z0-9_]+(?=\\()"),
        #         functionFormat))

        self.commentStartExpression = QtCore.QRegExp("/\\*")
        self.commentEndExpression = QtCore.QRegExp("\\*/")

    def load_syntax_asm(self):
        self.highlightingRules = []

        mnemPattern = QtCore.QRegExp("        [a-zA-Z.]+(\\.[0-9])? ")
        mnemPattern2 = QtCore.QRegExp("        [a-zA-Z.]+(\\.[0-9])?$")
        mnemFormat = QtGui.QTextCharFormat()
        mnemFormat.setFontWeight(QtGui.QFont.Bold)
        self.highlightingRules.append((mnemPattern, mnemFormat))
        self.highlightingRules.append((mnemPattern2, mnemFormat))



        keywordFormat = QtGui.QTextCharFormat()
        keywordFormat.setForeground(QtGui.QColor("#388CD6"))
        keywordFormat.setFontWeight(QtGui.QFont.Bold)

        control_flow_keywords = "call,ret,jmp,jg,jng,jge,jnge,jb,jnb,jbe,jnbe,jz,jnz,je,jne,bl(\\.[a-z][a-z])?,b(\\.[a-z][a-z])?,cbnz,cbz,tbz,tbnz" + \
            ",uCALL,uRET,uJUMPIF"
        control_flow_keywords = control_flow_keywords.split(",")
        keywordPatterns = ["\\b" + k + "\\b" for k in control_flow_keywords]
        for k in keywordPatterns:
            self.highlightingRules.append((QtCore.QRegExp(k), keywordFormat))

        addressesPattern = QtCore.QRegExp("^0x[0-9a-f]+")
        addressesFormat = QtGui.QTextCharFormat()
        addressesFormat.setForeground(QtCore.Qt.darkGray)
        self.highlightingRules.append((addressesPattern, addressesFormat))

        constantPattern = QtCore.QRegExp(" (\\-)?0x[0-9a-f]+| [0-9]+")
        constantFormat = QtGui.QTextCharFormat()
        constantFormat.setFontWeight(QtGui.QFont.Bold)
        constantFormat.setForeground(QtCore.Qt.darkRed)
        self.highlightingRules.append((constantPattern, constantFormat))

        ptrPattern = QtCore.QRegExp(" (dword|qword|byte|word) ptr ")
        ptrFormat = QtGui.QTextCharFormat()
        ptrFormat.setForeground(QtCore.Qt.darkGray)
        self.highlightingRules.append((ptrPattern, ptrFormat))


        classFormat = QtGui.QTextCharFormat()
        classFormat.setFontWeight(QtGui.QFont.Bold)
        classFormat.setForeground(QtCore.Qt.darkMagenta)
        self.highlightingRules.append((QtCore.QRegExp("\\bQ[A-Za-z]+\\b"),
                classFormat))

        singleLineCommentFormat = QtGui.QTextCharFormat()
        singleLineCommentFormat.setForeground(QtCore.Qt.darkGreen)
        self.highlightingRules.append((QtCore.QRegExp(";[^\n]*"),
                singleLineCommentFormat))

        quotationFormat = QtGui.QTextCharFormat()
        quotationFormat.setForeground(QtCore.Qt.darkGreen)
        self.highlightingRules.append((QtCore.QRegExp("\".*\""),
                quotationFormat))

        # functionFormat = QtGui.QTextCharFormat()
        # functionFormat.setFontItalic(True)
        # functionFormat.setForeground(QtCore.Qt.blue)
        # self.highlightingRules.append((QtCore.QRegExp("\\b[A-Za-z0-9_]+(?=\\()"),
        #         functionFormat))

        self.commentStartExpression = QtCore.QRegExp("/\\*")
        self.commentEndExpression = QtCore.QRegExp("\\*/")

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QtCore.QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.commentStartExpression.indexIn(text)

        while startIndex >= 0:
            endIndex = self.commentEndExpression.indexIn(text, startIndex)

            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()

            self.setFormat(startIndex, commentLength,
                    self.multiLineCommentFormat)
            startIndex = self.commentStartExpression.indexIn(text,
                    startIndex + commentLength)
