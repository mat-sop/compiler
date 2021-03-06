# jfft_compiler
Compiler of a simple imperative language, created as final project for 'Formal Languages and Translation Techniques' course.


## Language`s grammar
    program       -> DECLARE declarations BEGIN commands END
                | BEGIN commands END

    declarations  -> declarations, pidentifier
                | declarations, pidentifier(num:num)
                | pidentifier
                | pidentifier(num:num)

    commands      -> commands command
                | command

    command       -> identifier ASSIGN expression;
                | IF condition THEN commands ELSE commands ENDIF
                | IF condition THEN commands ENDIF
                | WHILE condition DO commands ENDWHILE
                | DO commands WHILE condition ENDDO
                | FOR pidentifier FROM value TO value DO commands ENDFOR
                | FOR pidentifier FROM value DOWNTO value DO commands ENDFOR
                | READ identifier;
                | WRITE value;

    expression    -> value
                | value PLUS value
                | value MINUS value
                | value TIMES value
                | value DIV value
                | value MOD value

    condition     -> value EQ value
                | value NEQ value
                | value LE value
                | value GE value
                | value LEQ value
                | value GEQ value

    value         -> num
                | identifier

    identifier    -> pidentifier
                | pidentifier(pidentifier)
                | pidentifier(num)


## Virtual machine & examples
Virtual machine and examples can be found in [this](assigment/virtual_machine.zip) zip file. More tests are available [here](assigment/tests.zip).


## Dependencies
Python version: `3.7`

    pip install pipenv
    pipenv install


## Usage
`python compiler/main.py input_file output_file`

