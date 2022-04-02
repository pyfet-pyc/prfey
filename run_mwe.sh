 #!/bin/bash
if [ "$#" -eq  "1" ] 
then
    if [ "$1" -eq "0" ] 
    then
        rm output/test_output_pyc/0_*
        python bin/convert_jumps.py samples/org-pyc/0.pyc output/test_output_pyc is_at_turn
        # python bin/convert_jumps.py [input file name] [output dir name] [target function]
    fi
    if [ "$1" -eq "1" ] 
    then
        rm output/test_output_pyc/10_*
        python bin/convert_jumps.py samples/org-pyc/10.pyc output/test_output_pyc is_message
        # python bin/convert_jumps.py [input file name] [output dir name] [target function]
    fi
    if [ "$1" -eq "2" ] 
    then
        rm output/test_output_pyc/16_*
        python bin/convert_jumps.py samples/org-pyc/16.pyc output/test_output_pyc _resolve_relative_to
        # python bin/convert_jumps.py [input file name] [output dir name] [target function]
    fi
    if [ "$1" -eq "3" ] 
    then
        rm output/test_output_pyc/19_*
        python bin/convert_jmpforward.py samples/org-pyc/19.pyc output/test_output_pyc/ unit_operation
        python bin/instr_at_offset.py samples/org-pyc/19.pyc output/test_output_pyc/19_instr_48.pyc unit_operation 48
        # python bin/convert_jumps.py [input file name] [output dir name] [target function]
    fi
    if [ "$1" -eq "4" ] 
    then
        echo "This is only instrumentation on mannually annotated offset which is received by uncompyle6"
        rm output/test_output_pyc/23_*
        python bin/instr_at_offset.py samples/org-pyc/23.pyc output/test_output_pyc/23_instr_128.pyc infer_type 128
        # python bin/convert_jumps.py [input file name] [output dir name] [target function]
    fi
    if [ "$1" -eq "5" ] 
    then
        rm output/test_output_pyc/24_*
        rm tmp/24*
        python bin/convert_jumps.py samples/org-pyc/24.pyc tmp _is_punctuation
        python bin/convert_jumps.py tmp/24_0jump.pyc tmp _is_whitespace
        python bin/convert_jumps.py tmp/24_0jump_0jump.pyc output/test_output_pyc _is_chinese_char

        # python bin/convert_jumps.py [input file name] [output dir name] [target function]
    fi
    if [ "$1" -eq "6" ] 
    then
        echo "user_exception function is not correct - Fix this"
        rm output/test_output_pyc/46_*
        rm tmp/46*
        python bin/convert_jumps.py samples/org-pyc/46.pyc tmp checkline
        python bin/convert_jumps.py tmp/46_0jump.pyc output/test_output_pyc user_exception
        # python bin/convert_jumps.py tmp/24_0jump_0jump.pyc output/test_output_pyc _is_chinese_char

        # python bin/convert_jumps.py [input file name] [output dir name] [target function]
    fi
    if [ "$1" -eq "7" ] 
    then
        echo "POC for mwe 158"
        rm output/test_output_pyc/loops_*
        python bin/convert_loopBoolean.py samples/mwe/loops.pyc output/test_output_pyc/ scan_directive_name
        # python bin/convert_jumps.py tmp/24_0jump_0jump.pyc output/test_output_pyc _is_chinese_char

        # python bin/convert_jumps.py [input file name] [output dir name] [target function]
    fi
else
    echo "run_mwe.sh [MWE number]"
    echo  "example: ./run_mwe.sh 1"
fi

