
# Crafting Interpreters

**by Robert Nystrom**  <https://craftinginterpreters.com/contents.html>

- [Crafting Interpreters](#crafting-interpreters)
  - [A Map of the Territory](#a-map-of-the-territory)
    - [Front End](#front-end)
    - [Middle End](#middle-end)
    - [Back End / Code Generation](#back-end--code-generation)
    - [Runtime](#runtime)
  - [Tiny-Interpreter Summary](#tiny-interpreter-summary)
    - [Overview](#overview)
    - [Key Techniques](#key-techniques)
    - [Front-End Components](#front-end-components)
    - [Tree-Walk Interpreter (`interpreter.py`)](#tree-walk-interpreter-interpreterpy)
    - [First-Class \& Higher-Order Functions](#first-class--higher-order-functions)
    - [Testing \& Tooling](#testing--tooling)
    - [Next Steps](#next-steps)


---
## A Map of the Territory

### Front End

- Scanning (Lexing)
  - Turns characters into tokens (e.g. identifiers, literals, symbols).
  - Discards whitespace and comments.

- Parsing
  - Builds an Abstract Syntax Tree (AST) from tokens.
  - Reports syntax errors when grammar rules are violated.

- Static Analysis
  - Name binding/resolution: Links each identifier to its declaration (scope).
  - Type checking (for statically typed languages): Verifies operations on compatible types.
  - Stores semantic info in AST node attributes, symbol tables, or separate tables.

### Middle End

- Intermediate Representation (IR)
  - Transforms AST into one or more IRs (e.g. control-flow graph, SSA, three-address code).
  - Decouples source-specific details from target-specific details.
  - Enables reuse of front ends/back ends (e.g. many front ends → one IR → many back ends).

- Optimization (optional)
  - Semantic-preserving rewrites (e.g. constant folding, dead code elimination, loop unrolling).
  - Often omitted or minimal in dynamic languages (e.g. Lua, CPython).

### Back End / Code Generation


- Machine Code Generation
  - Emits native instructions for a specific CPU (e.g. x86, ARM).
  - Pros: Maximum performance; runs directly on hardware.
  - Cons: Tightly coupled to one architecture; complex instruction sets and pipelines.

- Bytecode Generation
  - Emits compact, architecture-independent “byte” instructions.
  - Bytecode often serves as a second IR:
    - Closer to source semantics (e.g. stack operations, high-level ops).
    - Easier to generate than full machine code.
  - Common in dynamic languages (e.g. Python’s `.pyc`, Java’s `.class`).

- Virtual Machine (VM)
  - Interpreter VM  
    - Executes bytecode by walking a simulated machine model at runtime (tree-walk or stack-machine).
    - Simple, portable; adds interpreter overhead per instruction.
  - Ahead-of-Time (AOT) VM Backend  
    - Translates bytecode to native code ahead of execution (mini-compiler), then runs that.
    - Shares front/middle end across targets; only final lowering is target-specific.
  - Just-In-Time (JIT) VM  
    - Compiles hot bytecode paths to machine code on the fly.
    - May recompile with heavier optimizations based on runtime profiling.

### Runtime

- Provides services needed during execution:
  - Garbage collection, memory management.
  - Type metadata, dynamic dispatch.
  - Standard libraries, I/O, threading, etc.


## Tiny-Interpreter Summary

> Code written in python during 2025 ICLR@Singapore

### Overview
- Interpreter: Walks an AST (or bytecode) at runtime and performs operations directly (tree-walk in `interpreter.py`).  
- Compiler: Translates code into bytecode or machine code up front, then runs that output separately.  
- Transpiler: Converts one high-level language to another (e.g. ES6 → ES5).  
- Common Front End: Lexing → Parsing → Semantic analysis; differences appear in back-end phases.


### Key Techniques

- Recursive-Descent Parsing  
  - A straightforward technique that builds the AST directly while naturally handling operator precedence.  
  - It’s impressive how this elegant algorithm emerged—so simple yet so powerful!

- Precedence Climbing  
  - Organizes parsing into layered methods, each responsible for one level of operator precedence.  

- Visitor Pattern  
  - Decouples the AST node hierarchy from the operations performed on it (e.g., printing, interpreting).  
  - Makes it easy to add new behaviors without modifying existing node classes.

- Environment Chaining  
  - Implements nested scopes via a chain of lookup tables (global → block → function).  
  - Enables straightforward nesting and full support for closures.  


### Front-End Components

1. Scanner / Lexer (`scanner.py`)  
   - Reads raw source, groups characters into tokens.  
   - Handles comments, whitespace, literals, multi-char operators.

2. Token Definitions (`tok.py`)  
   - Enumerates token types & keyword lookup.  
   - Each `Token` holds type, lexeme, literal value, and line number.

3. Parser (`parser.py`)  
   - Recursive-descent grammar (one method per precedence level):  
     `_or()`, `_and()`, `_equality()`, `_comparison()`, `_term()`, `_factor()`, `_unary()`, `_primary()`.  
   - Builds AST nodes for expressions and statements (print, var-decl, control flow, functions).

4. AST & Visitor Pattern  
   - AST node classes (`expr.py`) implement a common interface.  
   - `Visitor` interface (`interface.py`) lets `Interpreter` and `ExprPrinter` dispatch via `accept()`.


### Tree-Walk Interpreter (`interpreter.py`)

- Visitor Methods
  - Evaluate literals, arithmetic/logical ops, grouping, unary ops.  
  - Execute statements: `print`, variable declaration/assignment, blocks, `if`/`while`/`for`, functions, `return`.

- Environment & State (`env.py`)  
  - Manages global, block, and function scopes with nested lookup tables.  
  - Supports user-defined (`Func`) and native functions (`NativeFunc`, e.g. `time()`, `sleep()`).


### First-Class & Higher-Order Functions

- `def` for named functions; `FuncCall` for calls.  
- Pass functions as arguments; recursion via call stack and AST evaluation.


### Testing & Tooling

- Module-specific unit tests (`test_scan`, `test_parser`, `test_interpreter`, `test_ast_printer`).  
- End-to-end smoke tests via `tests.py`.  
- Configured logging and colored output for easier debugging.


### Next Steps

- **Bytecode Compilation**: Build a stack-based VM.  
- **Language Extensions**: Add closures, classes, modules, and robust error recovery.