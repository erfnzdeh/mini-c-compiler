# Yashar Paymai (401100325)
# Pouria Erfanzadeh (401011180)
# Group: G3

from parser.parser import Parser
from parser.syntax_errors import SyntaxErrors
from scanner.buffer import BufferedFileReader
from scanner.init_dfa import init_dfa
from scanner.lexical_errors import LexicalErrors
from scanner.symbol_table import SymbolTable
from scanner.tokens import Tokens
from code_gen.codeGen import CodeGen



def compile(
        code_file_path="input.txt" , 
        lexical_error_file_path="lexical_errors.txt" ,
        tokens_file_path="tokens.txt" ,
        symbol_table_file_path="symbol_table.txt"
    ):
    lexical_errors = LexicalErrors(file_path=lexical_error_file_path)
    buffer = BufferedFileReader(file_path=code_file_path)
    tokens = Tokens(tokens_file_path)
    symbol_table = SymbolTable(file_path=symbol_table_file_path)
    dfa = init_dfa()
    codeGen = CodeGen(symbol_table=symbol_table)

    P = Parser(buffer=buffer , dfa=dfa , lexical_errors=lexical_errors , 
            tokens=tokens , symbol_table=symbol_table , syntax_errors=SyntaxErrors() , codeGen=codeGen , debug=False)
    try : 
        P.start()
    except :
        print(":((((((")

    lexical_errors.update_file()
    tokens.update_file()
    symbol_table.update_file()
    P.codeGen.set_exec_block("main")
    P.codeGen.export(file_path="output.txt")
    P.codeGen.export_semantic_errors(file_path="semantic_errors.txt")


if __name__ == "__main__":
    compile()
