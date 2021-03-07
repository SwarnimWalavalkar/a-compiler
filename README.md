# A Compiler

An extraordinarily simple implementation of a BSAIC-like-dialect language to C compiler to learn the fundamentals of Compiler Design.

It supports:

-   Numerical variables
-   Basic arithmetic
-   If statements
-   While loops
-   Print text and numbers
-   Input numbers
-   Labels and goto
-   Comments

## Dependencies

-   Python >= 3
-   GCC >= 9

## Build an example program with build.sh

Compile:

```bash
bash build.sh ./examples/hello.a
```

Run:

```bash
./build/hello.exe
```

Expected Output:

```bash
Hello, World!
```

## Manually compile an example program

Compile into C:

```bash
 python3 a.py ./examples/hello.a
```

Compile C code with your preffered C compiler:

```bash
gcc out.c
```

Run the outputted binary:

```bash
./a.exe
```

Expected Output:

```bash
Hello, World!
```
