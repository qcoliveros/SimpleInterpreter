# Simple Interpreter

### Syntactic Elements
1. **Character Set:** set of symbols used in the programming language.
   <br/>The interpreter is able to process all ASCII printable characters.

2. **Identifiers:** strings used to name variables, data objects, procedures/functions, etc.
   * Less than 50 characters.
   * Start with a character in the alphabet.
   * Can be uppercase/lowercase.

3. **Operator Symbols:** symbols used to represent the primitive operations in the language.
   <br/>The interpreter does not use operator symbols.
   
4. **Keyword:** an identifier used as a fixed part of the syntax.
   <br/>**Reserved words:** keywords that may not be used as a programmer-chosen identifier.
   <br/>All keywords are reserved words.
   
5. **Comments:** words ignored during translation
   <br/>All lines starting with # are considered comments.
   
6. **Delimiters:** used to mark the beginning or end of some syntactic constructs
   <br/>A new line is a delimiter.
   
7. **Field Format**
   <br/>The interpreter uses a free-field format where program statements can be written anywhere on an input line without regard for positioning.
   
8. **Expressions**
   <br/>An expression can be a literal/value, a variable, or it can be composed of several adjacent operators. Hence, nested expressions is accepted.
   
9. **Statement**
   <br/>Using the correct syntax, each keyword can be considered a statement.
   
10. **Overall Structure**
   <br/>Programs should begin with the BEGIN keyword and end with the END keyword.
   
   
### Variables and Data Types
   * There are only 2 main data types: integer and string.
   * The interpreter follows the principles of strong typing. Therefore, intermixing of integers and strings in arithmetic operations is not allowed.
   * All variables are declared and are global in scope.
   * Any attempts to use floating-point values should result in an error.
   * A string is enclosed by double quotes.

| <!-- --> | <!-- --> |
| --- | --- |
| Declaring an integer variable without an initial value | VARINT <_variable> |
| Declaring an integer variable with an initial value | VARINT <_variable> WITH <_expression> |
| Declaring a string variable without an initial value | VARSTR <_variable> |
| Declaring a string variable with an initial value | VARSTR <_variable> WITH <_expression> |

### User Input and Output

| <!-- --> | <!-- --> |
| --- | --- |
| Asking input from the user | INPUT <_variable> |
| Printing values, variables, and expressions | PRINT <_expression> |
| Printing values, variables, and expressions with a new line affixed at the end | PRINTLN <_expression> |

### Operations

| <!-- --> | <!-- --> | <!-- --> |
| --- | --- | --- |
| Assignment Statement | Assignment | STORE <_expression> IN <_variable> |
| Basic Arithmetic Operations | Addition | ADD <_expression1> <_expression2> |
|| Subtraction | SUB <_expression1> <_expression2> |
|| Multiplication | MUL <_expression1> <_expression2> |
|| Division | DIV <_expression1> <_expression2> |
|| Modulo | MOD <_expression1> <_expression2> |
| Advanced Arithmetic Operations | Exponentiation | RAISE <_expression> <_exponent> |
|| Nth Root of a No. | ROOT <_expression> <_expression> |
|| Average | MEAN <_expression1> <_expression2> <_expression3> … <_expressionN><br/>● This is the only operation that accepts an unlimited number of parameters. |
|| Distance between two points | DIST <_expression1> <_expression2> AND <_expression3> <_expression4><br/>● The 2 points are separated by ‘AND’ <br/>● The coordinates of the first point are <_expression1> and <_expression2> <br/>● The coordinates of the second point are <_expression3> and <_expression4>


**Important Note:** An expression can be a literal/value, a variable, or it can be composed of several adjacent operators. Hence, nested expressions is acceptable.
