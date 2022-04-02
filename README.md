# pyc-cfg

Run:
```
python run_uncompyle6.py test/main.pyc
```

Will decompile and parse the errors and create CFG for error inducing functions.

Scripts:

`compile.sh`: Compiles `main.py` and `solution.py` in `target_py` directory to create `main.pyc` in `test` directory for python 3+ and `main.dis` for bytecode in `dis_output` directory.

`2compile.sh`: Compiles `main.py` and `solution.py` in `target_py` directory to create `main.pyc` in `test` directory for python 2 and `main.dis` for bytecode in `dis_output` directory.

`clean.sh`: Removes all `.png` for CFG

Run for python version of `.pyc` file in `test` directory:
```
python scripts/header_recover.py test
```


To manipulat bytecode use this:
```
python manipulate_pyc.py [source pyc file path] [output pyc name]
```

```
instrument.sh [source-pyc-file-path]
```
will generate `source-pyc-file-path.instr.pyc`
python bin/batch_diff_funcs.py samples/d3_parse_errors_py3.7/ samples/u6_pyinstaller_3.7/
