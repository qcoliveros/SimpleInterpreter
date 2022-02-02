# Mary Ellery Queen Oliveros. 2021 December.

import math
import os

class Constants:
    FILE_EXTENSION = '.ipol'
    
# For reserved keywords and its equivalent tokens.
class Keyword:
    ID = 'IDENTIFIER'
    NUMBER = 'NUMBER'
    INTEGER = 'INTEGER'
    STRING = 'STRING'
    BEGIN = 'BEGIN'
    END = 'END'
    EOS = 'EOS'
    EOF = 'EOF'
    VARINT = 'VARINT'
    VARSTR = 'VARSTR'
    WITH = 'WITH'
    STORE = 'STORE'
    IN = 'IN'
    INPUT = 'INPUT'
    PRINT = 'PRINT'
    PRINTLN = 'PRINTLN'
    ADD = 'ADD'
    SUB = 'SUB'
    MUL = 'MUL'
    DIV = 'DIV'
    MOD = 'MOD'
    RAISE = 'RAISE'
    ROOT = 'ROOT'
    MEAN = 'MEAN'
    DIST = 'DIST'
    AND = 'AND'
    
    keywords = [
        # Basic.
        { 'lexeme': BEGIN, 'token': 'PROGRAM_BEGIN' },
        { 'lexeme': END, 'token': 'PROGRAM_END' },
        { 'lexeme': EOS, 'token': 'END_OF_STATEMENT' },
        { 'lexeme': EOF, 'token': 'END_OF_FILE' },
        # Declaring variable.
        { 'lexeme': VARINT, 'token': 'DECLARATION_INT' },
        { 'lexeme': VARSTR, 'token': 'DECLARATION_STRING' },
        { 'lexeme': WITH, 'token': 'DECLARATION_ASSIGN_WITH_KEY' },
        # Input and output.
        { 'lexeme': INPUT, 'token': 'INPUT' },
        { 'lexeme': PRINT, 'token': 'OUTPUT' },
        { 'lexeme': PRINTLN, 'token': 'OUTPUT_WITH_LINE' },
        # Assignment operation.
        { 'lexeme': STORE, 'token': 'ASSIGN_KEY' },
        { 'lexeme': IN, 'token': 'ASSIGN_VAR_KEY' },
        # Basic arithmetic operation.
        { 'lexeme': ADD, 'token': 'BASIC_OPERATOR_ADD' },
        { 'lexeme': SUB, 'token': 'BASIC_OPERATOR_SUB' },
        { 'lexeme': MUL, 'token': 'BASIC_OPERATOR_MUL' },
        { 'lexeme': DIV, 'token': 'BASIC_OPERATOR_DIV' },
        { 'lexeme': MOD, 'token': 'BASIC_OPERATOR_MOD' },
        # Advanced arithmetic operation.
        { 'lexeme': RAISE, 'token': 'ADVANCED_OPERATOR_EXP' },
        { 'lexeme': ROOT, 'token': 'ADVANCED_OPERATOR_ROOT' },
        { 'lexeme': MEAN, 'token': 'ADVANCED_OPERATOR_AVE' },
        { 'lexeme': DIST, 'token': 'ADVANCED_OPERATOR_DIST' },
        { 'lexeme': AND, 'token': 'DISTANCE_SEPARATOR' },
    ]
    
    @staticmethod
    # Retrieve the keyword dictionary based on reserved keyword.
    def get(lexeme):
        return next((keyword for keyword in Keyword.keywords if keyword['lexeme'] == lexeme), None)

# For generic syntax error.
class Error(Exception):
    INVALID_SYNTAX = 'INVALID_SYNTAX'
    UNDECLARED_VARIABLE = 'UNDECLARED_VARIABLE'
    INVALID_OPERATIONS = 'INVALID_OPERATIONS'
    INVALID_EXPRESSION = 'INVALID_EXPRESSION'
    INVALID_DATA_TYPE = 'INVALID_DATA_TYPE'
    DUPLICATE_VAR = 'DUPLICATE_VAR'
    INCOMPATIBLE_DATA_TYPE = 'INCOMPATIBLE_DATA_TYPE'
    INVALID_DATA_TYPE_INPUT = 'INVALID_DATA_TYPE_INPUT'
    INVALID_EOF = 'INVALID_EOF'
    EMPTY_FILE = 'EMPTY_FILE'
    FILE_NOT_EXISTS = 'FILE_NOT_EXISTS'
    INVALID_FILE = 'INVALID_FILE'
    GENERAL_ERROR = 'GENERAL_ERROR'
    
    errors = [
        { 'code': INVALID_SYNTAX, 'message': 'Invalid syntax at line number [ %d ]\n ----> %s' },
        { 'code': UNDECLARED_VARIABLE, 'message': 'Variable is not declared at line number [ %d ]\n ----> %s' },
        { 'code': INVALID_OPERATIONS, 'message': 'Invalid arithmetic operation at line number [ %d ]\n ----> %s' },
        { 'code': INVALID_EXPRESSION, 'message': 'Invalid expression at line number [ %d ]\n ----> %s' },
        { 'code': INVALID_DATA_TYPE, 'message': 'Invalid data type at line number [ %d ]\n ----> %s' },
        { 'code': DUPLICATE_VAR, 'message': 'Duplicate variable declaration at line number [ %d ]\n ----> %s' },
        { 'code': INCOMPATIBLE_DATA_TYPE, 'message': 'Incompatible data type at line number [ %d ]\n ----> %s' },
        { 'code': INVALID_DATA_TYPE_INPUT, 'message': 'Invalid data type input at line number [ %d ]\n ----> %s' },
        { 'code': INVALID_EOF, 'message': 'Invalid end of file at line number [ %d ]\n ----> %s' },
        { 'code': EMPTY_FILE, 'message': 'File is empty' },
        { 'code': FILE_NOT_EXISTS, 'message': 'File not found' },
        { 'code': INVALID_FILE, 'message': 'Invalid file' },
        { 'code': GENERAL_ERROR, 'message': 'Encountered general error' },
    ]
    
    def __init__(self, code, args = tuple()):
        self.code = code
        error = next((err for err in self.errors if err['code'] == code), None)
        if error is not None:
            # Additional handling for invalid syntax to display the line number and syntax with error.
            if len(args) != 0:
                self.message = error['message'] % args
            else:
                self.message = error['message']
            super().__init__(self.message)
            
    # For string representation of error message.
    def __str__(self):
        return self.message
    
    @staticmethod
    # Retrieve the actual message based on the message code.
    def getMessage(code):
        error = next((err for err in Error.errors if err['code'] == code), None)
        if error is not None:
            return error['message']
    
# To segregate the IO error when reading the file from the actual syntax error.
class IOException(Error):
    pass
    
# For the messages.
class Message:
    messages = {
        'STARTED': '======== INTERPOL INTERPRETER STARTED ========\n',
        'FILE_PROMPT': 'Enter INTERPOL file (%s): ',
        'OUTPUT_TITLE': '\n================ INTERPOL OUTPUT ================\n',
        'OUTPUT_START': '---------------- OUTPUT START ---------------->',
        'OUTPUT_END': '\n<----------------- OUTPUT END -------------------',
        'TOKEN_TITLE': '\n========= INTERPOL LEXEMES/TOKENS TABLE =========\n',
        'TOKEN_HEADER_1': 'LINE NO.',
        'TOKEN_HEADER_2': 'TOKENS',
        'TOKEN_HEADER_3': 'LEXEMES',
        'SYMBOL_TITLE': '\n================= SYMBOLS TABLE =================\n',
        'SYMBOL_HEADER_1': 'VARIABLE NAME',
        'SYMBOL_HEADER_2': 'TYPE',
        'SYMBOL_HEADER_3': 'VALUE',
        'TERMINATED': '\n======== INTERPOL INTERPRETER TERMINATED ========',
    }
    
    @staticmethod
    # Retrieve the actual message based on the message code.
    def get(code):
        return Message.messages[code]
    
# Utility to retrieve the file content.
class File:
    @staticmethod
    def getFileContent():
        file = input(Message.get('FILE_PROMPT') % Constants.FILE_EXTENSION)
        if not file.endswith(Constants.FILE_EXTENSION):
            raise IOException(Error.INVALID_FILE)
        if not os.path.exists(file):
            raise IOException(Error.FILE_NOT_EXISTS)
        if os.path.getsize(file) == 0:
            raise IOException(Error.EMPTY_FILE)
        return open(file, 'r').read()

# Holder for token/lexeme.
class Token:
    def __init__(self, linoNo, _type, token, lexeme):
        self.lineNo = linoNo
        self._type = _type
        self.token = token
        self.lexeme = lexeme
    
    def __repr__(self):
        return repr((self.lineNo, self.token, self.lexeme))
        
# Holder for the token/lexeme table.
class Tokens:
    def __init__(self):
        self.tokens = []
    
    def define(self, token):
        self.tokens.append(token)
        
    # Retrieve all the tokens based on the line number.
    def lookup(self, lineNo):
        return list(filter(lambda item: item.lineNo == lineNo and item.lexeme != Keyword.EOS, self.tokens))
        
    # Display the content of token/lexeme table in the following format:
    #  LINE NO. <padding> TOKENS <padding> LEXEMES
    def display(self):
        col1Padding = 10
        col2Padding = 30
        
        print(Message.get('TOKEN_TITLE'))
        print(Message.get('TOKEN_HEADER_1').ljust(col1Padding), \
              Message.get('TOKEN_HEADER_2').ljust(col2Padding), \
              Message.get('TOKEN_HEADER_3'))
        for item in self.tokens:
            print(str(item.lineNo).ljust(col1Padding), \
                  item.token.ljust(col2Padding), \
                  item.lexeme)

# Holder for the symbols.        
class Variable:
    def __init__(self, name, _type, value):
        self.name = name
        self._type = _type
        self.displayType = _type
        if _type == Keyword.NUMBER:
            self.displayType = Keyword.INTEGER
        self.value = value
    
    def __repr__(self):
        return repr((self.name, self._type, self.value))

# Holder for the symbols table.   
class Variables:
    def __init__(self):
        self.variables = []
    
    # Use to define a variable i.e., for VARINT and VARSTR.
    def define(self, variable):
        self.variables.append(variable)
        
    # Use to update the variable value i.e., for STORE.
    def update(self, name, value):
        for item in self.variables:
            if getattr(item, 'name', None) == name:
                setattr(item, 'value', value)
        
    # Retrieve the variable based on variable name.
    def lookup(self, name):
        return next((item for item in self.variables if item.name == name), None)
        
    # Display the content of symbol table in the following format:
    #  VARIABLE NAME <padding> TYPE <padding> VALUE
    def display(self):
        col1Padding = 20
        col2Padding = 15
        
        print(Message.get('SYMBOL_TITLE'))
        print(Message.get('SYMBOL_HEADER_1').ljust(col1Padding), \
              Message.get('SYMBOL_HEADER_2').ljust(col2Padding), \
              Message.get('SYMBOL_HEADER_3'))
        for item in self.variables:
            print(item.name.ljust(col1Padding), \
                  item.displayType.ljust(col2Padding), \
                  item.value)

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.lineNo = 1
        self.currentChar = self.text[self.pos]
        self.previousChar = self.text[self.pos - 1]
    
    # Raise an error and stop the execution.
    def raiseError(self, code):
        raise Error(code, (self.lineNo, self.peekUptoStatementEnd()))

    # Use to retrieve the line syntax with error.
    def peekUptoStatementEnd(self):
        text = ''
        peekPos = self.pos
        if self.text[peekPos] == '\n':
            peekPos = peekPos - 1
        while self.text[peekPos] != '\n':
            text = text + self.text[peekPos]
            peekPos = peekPos - 1
        return text[::-1]
    
    # Process the next character.
    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.currentChar = None
        else:
            if self.previousChar == '\n':
                self.lineNo += 1
            self.previousChar = self.currentChar
            self.currentChar = self.text[self.pos]
            
    # Look at the next character but do not process it yet.
    def peek(self):
        peekPos = self.pos + 1
        if peekPos > len(self.text) - 1:
            return None
        else:
            return self.text[peekPos]
    
    # Ignore all white spaces.
    def skipWhitespace(self):
        while self.currentChar is not None and self.currentChar.isspace() and self.currentChar != '\n':
            self.advance()

    # Ignore all comments.
    def skipComment(self):
        while self.currentChar is not None and self.currentChar != '\n':
            self.advance()
    
    # Check if valid printable characters (ASCII 32 to 126).
    def isPrintableCharacter(self, value):
        return all(ord(c) >= 32 and ord(c) <= 126 for c in value)
    
    # Check if valid integer.
    # +/- sign is accepted.
    def isInteger(self, currentChar, nextChar):
        return currentChar.isdigit() \
                or ((currentChar == '+' or currentChar == '-') and nextChar.isdigit())

    # Retrieve the integer token.
    def getInteger(self):
        result = ''
        while self.currentChar is not None and not self.currentChar.isspace():
            result += self.currentChar
            self.advance()
            
        try:
            return Token(self.lineNo, Keyword.NUMBER, Keyword.NUMBER, int(result))
        except ValueError:
            self.raiseError(Error.INVALID_DATA_TYPE)

    # Retrieve the string token.
    def getString(self):
        result = ''
        while self.currentChar is not None and self.currentChar != '"':
            if self.isPrintableCharacter(self.currentChar):
                result += self.currentChar
                self.advance()
            else:
                self.raiseError(Error.INVALID_SYNTAX)

        self.advance()
        return Token(self.lineNo, Keyword.STRING, Keyword.STRING, result)
    
    # Retrieve the identifier token.
    def getIdentifier(self):
        result = ''
        while self.currentChar is not None and self.currentChar.isalnum():
            result += self.currentChar
            self.advance()
            
        keyword = Keyword.get(result)
        if keyword is not None:
            # For keyword.
            token = Token(self.lineNo, keyword['lexeme'], keyword['token'], keyword['lexeme'])
        elif len(result) < 50 and result[0].isalpha():
            # For identifier.
            # 1. Should be less than 50 characters.
            # 2. Should start with a character in the alphabet.
            token = Token(self.lineNo, Keyword.ID, Keyword.ID, result)
        else:
            self.raiseError(Error.INVALID_SYNTAX)
                
        return token
    
    # Retrieve the next token.
    def getNextToken(self):
        while self.currentChar is not None:
            # For end of statement.
            if self.currentChar == '\n':
                self.advance()
                keyword = Keyword.get(Keyword.EOS)
                return Token(self.lineNo, keyword['lexeme'], keyword['token'], keyword['lexeme'])
            
            # For spaces.
            if self.currentChar.isspace():
                self.skipWhitespace()
                continue
            
            # For comments.
            if self.currentChar == '#':
                self.skipComment()
                continue
            
            # For string.
            if self.currentChar == '"':
                self.advance()
                return self.getString()
            
            # For integer.
            if self.isInteger(self.currentChar, self.peek()):
                return self.getInteger()
            
            # For variable and reserved keyword.
            if self.currentChar.isalnum():
                return self.getIdentifier()
            
            # If reached here means syntax error.
            self.raiseError(Error.INVALID_SYNTAX)
            
        # For end of file.
        keyword = Keyword.get(Keyword.EOF)
        return Token(self.lineNo, keyword['lexeme'], keyword['token'], keyword['lexeme'])

class Interpreter:
    def __init__(self, lexer, tokens, variables):
        self.lexer = lexer
        self.tokens = tokens
        self.variables = variables
        self.currentToken = self.lexer.getNextToken()
        
    def raiseError(self, code):
        tokens = self.tokens.lookup(self.lexer.lineNo)
        if self.currentToken._type is not Keyword.EOS:
            tokens.append(self.currentToken)
        lexemes = ''
        for item in tokens:
            if item._type == Keyword.STRING:
                lexemes += '"' + item.lexeme + '" '
            else:
                lexemes += str(item.lexeme) + ' '
        raise Error(code, (self.lexer.lineNo, lexemes))
    
    # Consume the token and retrieve the next token.
    def consume(self, _type):
        if self.currentToken._type == _type:
            if self.currentToken._type == Keyword.EOF:
                self.tokens.define(Token(self.lexer.lineNo + 1, _type, self.currentToken.token, self.currentToken.lexeme))
            else:
                self.tokens.define(Token(self.lexer.lineNo, _type, self.currentToken.token, self.currentToken.lexeme))
                
            if self.currentToken._type != Keyword.EOF:
                self.currentToken = self.lexer.getNextToken()
        else:
            self.raiseError(Error.INVALID_SYNTAX)
            
    def isInteger(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False
        
    # Create stack for expression.
    def createStack(self):
        stack = []
        while self.currentToken._type != Keyword.EOS and self.currentToken._type != Keyword.IN:
            stackItem = ''
            if self.currentToken._type in (Keyword.ADD, Keyword.SUB, Keyword.MUL, Keyword.DIV, Keyword.MOD, \
                                           Keyword.RAISE, Keyword.ROOT, Keyword.MEAN, Keyword.DIST, \
                                           Keyword.AND, Keyword.NUMBER, Keyword.ID):
                if self.currentToken._type == Keyword.ID:
                    variable = self.variables.lookup(self.currentToken.lexeme)
                    if variable is not None:
                        stackItem = variable.value
                        if variable._type == Keyword.NUMBER and self.isInteger(stackItem):
                            self.consume(Keyword.ID)
                            stack.append(stackItem)
                        else:
                            self.raiseError(Error.INCOMPATIBLE_DATA_TYPE)

                    else:
                        self.raiseError(Error.UNDECLARED_VARIABLE)
                # if not identifier or the rest of the valid tokens.
                else:
                    stackItem = self.currentToken.lexeme
                    self.consume(self.currentToken._type)
                    stack.append(stackItem)
            else:
                self.raiseError(Error.INVALID_SYNTAX)

        return stack
    
    # Process expression:
    #  <number> | 
    #  ADD <expression> <expression> | 
    #  SUB <expression> <expression> | 
    #  MUL <expression> <expression> | 
    #  DIV <expression> <expression> | 
    #  MOD <expression> <expression> | 
    #  RAISE <expression> <expression> | 
    #  ROOT <expression> <expression> | 
    #  MEAN ( <expression> )* | 
    #  DIST <expression> <expression> AND <expression> <expression>
    def parseExpression(self):
        try:
            if self.currentToken._type in (Keyword.ADD, Keyword.SUB, Keyword.MUL, Keyword.DIV, Keyword.MOD, \
                                           Keyword.RAISE, Keyword.ROOT, Keyword.MEAN, Keyword.DIST, \
                                           Keyword.AND, Keyword.NUMBER, Keyword.ID):
                stack = self.createStack()
            else:
                self.raiseError(Error.INVALID_SYNTAX)
    
            # Scan the stack from right to left.
            result = 0
            workingStack = []
    
            for i in range((len(stack) - 1), -1, -1):
    
                currentStack = stack[i]
    
                # Get the AND for DIST.
                if currentStack == Keyword.AND:
                    workingStack.append(currentStack)
                    continue
    
                if currentStack in (Keyword.ADD, Keyword.SUB, Keyword.MUL, Keyword.DIV, Keyword.MOD, Keyword.RAISE, Keyword.ROOT):
                    if len(workingStack) >= 2:
                        operand1 = workingStack.pop()
                        operand2 = workingStack.pop()
                    else:
                        self.raiseError(Error.INVALID_EXPRESSION)
    
                    if self.isInteger(operand1) and self.isInteger(operand2):
                        operand1 = int(operand1)
                        operand2 = int(operand2)
                        
                        if currentStack == Keyword.ADD:
                            result = operand1 + operand2
                        elif currentStack == Keyword.SUB:
                            result = operand1 - operand2
                        elif currentStack == Keyword.MUL:
                            result = operand1 * operand2
                        elif currentStack == Keyword.DIV:
                            result = operand1 // operand2
                        elif currentStack == Keyword.MOD:
                            result = operand1 % operand2
                        elif currentStack == Keyword.RAISE:
                            result = operand1 ** operand2
                        elif currentStack == Keyword.ROOT:
                            result = int(operand2 ** (1 / operand1))
    
                        workingStack.append(int(result))
                        continue
                    else:
                        self.raiseError(Error.INVALID_EXPRESSION)
    
                elif currentStack == Keyword.DIST:
                    # Check if DIST has 4 parameters.
                    if len(workingStack) >= 4:
                        operand1 = workingStack.pop()
                        operand2 = workingStack.pop()
                        operatorAnd = workingStack.pop()
                        operand3 = workingStack.pop()
                        operand4 = workingStack.pop()
                    else:
                        self.raiseError(Error.INVALID_EXPRESSION)
    
                    if self.isInteger(operand1) and self.isInteger(operand2) and self.isInteger(operand3) \
                        and self.isInteger(operand4) and operatorAnd == Keyword.AND:
                        operand1 = int(operand1)
                        operand2 = int(operand2)
                        operand3 = int(operand3)
                        operand4 = int(operand4)
                        result = int(math.sqrt(((operand1 - operand3) ** 2) + ((operand2 - operand4) ** 2)))
                        workingStack.append(int(result))
                        continue
    
                elif currentStack == Keyword.MEAN:
                    if len(workingStack) > 0:
    
                        meanStack = []
                        while len(workingStack) > 0:
                            operand1 = workingStack.pop()
                            if self.isInteger(operand1):
                                meanStack.append(int(operand1))
                            else:
                                workingStack.append(operand1)
                                break
    
                        result = sum(meanStack) // len(meanStack)
                        workingStack.append(int(result))
                        continue
    
                if self.isInteger(currentStack):
                    workingStack.append(int(currentStack))
                    continue
    
            # Expression must provide only one final result.
            if len(workingStack) == 1:
                result = workingStack.pop()
                return result
            else:
                self.raiseError(Error.INVALID_EXPRESSION)
        except ArithmeticError:
            self.raiseError(Error.INVALID_OPERATIONS)
            
    # Process assign statement:
    #  VARINT <variable> ( WITH <expression> ) | 
    #  VARSTR <variable> ( WITH "<string>" | <expression> ) | 
    #  STORE "<string>" | <expression> IN <variable>
    def assignStatement(self):
        if self.currentToken._type == Keyword.VARINT:
            self.consume(Keyword.VARINT)
        
            varName = self.currentToken.lexeme
            if self.variables.lookup(varName) is not None:
                self.raiseError(Error.DUPLICATE_VAR)
            self.consume(Keyword.ID)
        
            result = 0
            if self.currentToken._type == Keyword.WITH:
                self.consume(Keyword.WITH)
                
                # For strong-typing; must not accept string.
                if self.currentToken._type == Keyword.STRING:
                    self.raiseError(Error.INVALID_DATA_TYPE)
                    
                result = self.parseExpression()
                
            self.variables.define(Variable(varName, Keyword.NUMBER, result))
        elif self.currentToken._type == Keyword.VARSTR:
            self.consume(Keyword.VARSTR)
            
            varName = self.currentToken.lexeme
            if self.variables.lookup(varName) is not None:
                self.raiseError(Error.DUPLICATE_VAR)
            self.consume(Keyword.ID)
            
            result = ''
            if self.currentToken._type == Keyword.WITH:
                self.consume(Keyword.WITH)
                
                # For strong-typing; must only accept string.
                if self.currentToken._type != Keyword.STRING:
                    result = self.parseExpression()
                    self.raiseError(Error.INVALID_DATA_TYPE)
                    
                result = self.currentToken.lexeme
                self.consume(Keyword.STRING)
                
            self.variables.define(Variable(varName, Keyword.STRING, result))
        elif self.currentToken._type == Keyword.STORE: 
            self.consume(Keyword.STORE)
            
            result = ''
            varType = self.currentToken._type
            if self.currentToken._type == Keyword.STRING:
                result = self.currentToken.lexeme
                self.consume(Keyword.STRING)
            else:
                varType = Keyword.NUMBER
                result = self.parseExpression()
            
            if self.currentToken._type != Keyword.IN:
                self.raiseError(Error.INVALID_SYNTAX)
            self.consume(Keyword.IN)
            
            varName = self.currentToken.lexeme
            variable = self.variables.lookup(varName)
            if variable is None:
                self.raiseError(Error.UNDECLARED_VARIABLE)
            # For strong-typing; must only accept the declared type.
            if variable._type != varType:
                self.raiseError(Error.INVALID_DATA_TYPE)
            self.consume(Keyword.ID)
            
            self.variables.update(varName, result)
    
    # Process the input statement:
    #  INPUT <variable>
    def getInputStatement(self):
        self.consume(Keyword.INPUT)
        
        varName = self.currentToken.lexeme
        variable = self.variables.lookup(varName)
        if variable is None:
            self.raiseError(Error.UNDECLARED_VARIABLE)
        self.consume(Keyword.ID)
        
        _input = input()
        if variable._type == Keyword.NUMBER and not self.isInteger(_input):
            self.raiseError(Error.INVALID_DATA_TYPE_INPUT)
        
        self.variables.update(varName, _input)
        
    # Process the output statement:
    #  PRINT <variable> | PRINT "<string>" | PRINT <expression> | 
    #  PRINTLN <variable> | PRINTLN "<string>" | PRINTLN <expression>
    def printOutputStatement(self):
        appendNextLine = False
        if self.currentToken._type == Keyword.PRINT:
            self.consume(Keyword.PRINT)
        elif self.currentToken._type == Keyword.PRINTLN: 
            appendNextLine = True
            self.consume(Keyword.PRINTLN)
            
        if self.currentToken._type == Keyword.ID:
            variable = self.variables.lookup(self.currentToken.lexeme)
            if variable is None:
                self.raiseError(Error.UNDECLARED_VARIABLE)
            result = str(variable.value)
            self.consume(Keyword.ID)
        elif self.currentToken._type == Keyword.STRING:
            result = self.currentToken.lexeme
            self.consume(Keyword.STRING)
        else:
            result = str(self.parseExpression())
            
        if appendNextLine:
            result += '\n'
        
        print(result, end = '', flush = True)
     
    # Parse a line.       
    def parseStatement(self):
        if self.currentToken._type == Keyword.VARINT \
            or self.currentToken._type == Keyword.VARSTR \
            or self.currentToken._type == Keyword.STORE:
            # Process assign statement.
            self.assignStatement()
        elif self.currentToken._type == Keyword.INPUT:
            # Process the input statement.
            self.getInputStatement()
        elif self.currentToken._type == Keyword.PRINT \
            or self.currentToken._type == Keyword.PRINTLN:
            # Process the output statement.
            self.printOutputStatement()
        elif self.currentToken._type in (Keyword.ADD, Keyword.SUB, Keyword.MUL, Keyword.DIV, Keyword.MOD, \
                                         Keyword.RAISE, Keyword.ROOT, Keyword.MEAN, Keyword.DIST):
            self.parseExpression()
    
    # Parse all the lines.
    def parseStatementList(self):
        while self.currentToken._type == Keyword.EOS:
            # Consume any line break.
            self.consume(Keyword.EOS)
            
            # Ignore any BEGIN syntax.
            if self.currentToken._type != Keyword.BEGIN:   
                self.parseStatement()
                
    def parseProgram(self):
        # Everything must begin and it should be with BEGIN.
        if self.currentToken._type == Keyword.BEGIN:
            self.consume(Keyword.BEGIN)
        else:
            self.raiseError(Error.INVALID_SYNTAX)
            
        self.parseStatementList()
        
        # Display error if reached EOF before END.
        if self.currentToken._type == Keyword.EOF:
            self.raiseError(Error.INVALID_EOF)
        
        # Everything must end and it should be with END.
        if self.currentToken._type == Keyword.END:
            self.consume(Keyword.END)
        else:
            self.raiseError(Error.INVALID_SYNTAX)
            
    def parse(self):
        # Consume any line break before BEGIN.
        while self.currentToken._type == Keyword.EOS:
            self.consume(Keyword.EOS)
        
        self.parseProgram()
        
        # Consume any line break before the end-of-file.
        while self.currentToken._type == Keyword.EOS:
            self.consume(Keyword.EOS)
            
        # Actual end-of-file.
        if self.currentToken._type == Keyword.EOF:
            self.consume(Keyword.EOF)
        else:
            self.raiseError(Error.INVALID_SYNTAX)

if __name__ == '__main__':
    try:
        print(Message.get('STARTED'))
    
        text = File.getFileContent()
        
        lexer = Lexer(text)
        variables = Variables()
        tokens = Tokens()
        interpreter = Interpreter(lexer, tokens, variables)
        
        print(Message.get('OUTPUT_TITLE'))
        print(Message.get('OUTPUT_START'))
        interpreter.parse()
        print(Message.get('OUTPUT_END'))

        tokens.display()
        variables.display()
        
        print(Message.get('TERMINATED'))
    except IOException as ioe:
        print(Message.get('OUTPUT_TITLE'))
        print(Message.get('OUTPUT_START'))
        print(ioe)
    except Error as err:
        print(err)
    except:
        print(Error.getMessage('GENERAL_ERROR'))
    
