# ComputorV2
A calculator interpreter than can operate on real, complex numbers, and 2D matrix data types, store variables, define and evaluate functions, and solve [quadratic equations](https://en.wikipedia.org/wiki/Quadratic_equation) in Python using [lark-parser](https://github.com/lark-parser/lark). (42 Silicon Valley)

<p float="left">
  <img src="https://github.com/ashih42/ComputorV2/blob/master/Screenshots/screenshot1.png" width="600" />
</p>

## Prerequisites

You have `python3` installed.

## Installing

```
./setup/setup.sh
```

* **Note:** If you get the error `ImportError: cannot import name 'Lark' from 'lark'`, it's because you had also installed `lark` besides `lark-parser`.  To fix the problem, uninstall both and reinstall `lark-parser`.
```
pip3 uninstall lark lark-parser
pip3 install lark-parser
```

## Running

### Interactive Mode
```
python3 main.py
```

### Single Statement Mode
```
python3 main.py "<statement>"
```

### File-Processing Mode
```
python3 main.py -f file
```

### Preset Constants
* `i` Imaginary number.
* `pi` Constant pi.

### Preset Functions
* `a ** b` Matrix-multiply matrices `a` and `b`.
* `inv(x)` Multiplicative inverse of `x`.
* `transp(x)` Matrix transpose of matrix `x`.
* `sqrt(x)` Square root of `x`.
* `sin(x)` Sine of `x` in radians.
* `cos(x)` Cosine of `x` in radians.
* `tan(x)` Tangent of `x` in radians.
* `deg(x)` Convert `x` from radians to degrees.
* `rad(x)` Convert `x` from degrees to radians.

### Useful Commands
* `@VARS` List all variables.
* `@FUNCS` List all functions.
* `@SOLVE <equation>` Solve quadratic equation with unknown `X`.
* `EXIT` Terminate interactive session.
