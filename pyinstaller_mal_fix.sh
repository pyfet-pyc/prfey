
if [ "$#" -eq  "1" ] 
then
    if [ "$1" -eq "0" ] 
    then
        rm tmp/102168*
        python bin/convert_break_loop.py samples/u6_pyinstaller_3.7/102168.pyc tmp/ pretty_flags
        echo "Output is in tmp with name 102168*"
    fi
    if [ "$1" -eq "1" ] 
    then
        rm tmp/102420*
        python bin/convert_jumps.py samples/u6_pyinstaller_3.7/102420.pyc tmp make_cookies
        echo "Output is in tmp with name 102420*"
    fi
    if [ "$1" -eq "2" ] 
    then
        rm tmp/116051*
        python bin/convert_continue_loop.py samples/u6_pyinstaller_3.7/116051.pyc tmp gammavariate
        echo "Output is in tmp with name 116051*"
    fi
    if [ "$1" -eq "3" ] 
    then
        rm tmp/102150*
        python bin/convert_loop_func_invocation.py samples/u6_pyinstaller_3.7/102150.pyc tmp _format_actions_usage
        echo "Output is in tmp with name 102150*"
    fi
    if [ "$1" -eq "4" ] 
    then
        rm tmp/121042*
        python bin/convert_loop_func_invocation.py samples/u6_pyinstaller_3.7/121042.pyc tmp detwingle
        echo "Output is in tmp with name 121042*"
    fi
    if [ "$1" -eq "5" ] 
    then
        rm tmp/12489*
        python bin/convert_return_tryex.py samples/u6_pyinstaller_3.8/12489.pyc tmp from_param
        echo "Output is in tmp with name 12489*"
    fi
    if [ "$1" -eq "6" ] 
    then
        rm tmp/121817*
        python bin/convert_return_tryex_second.py  samples/u6_pyinstaller_3.8/121817.pyc tmp GetBestInterface
        python bin/convert_return_tryex_second.py  tmp/121817_0loopJump.pyc tmp GetBestInterface
        echo "Output is in tmp with name 121817*"
    fi
    if [ "$1" -eq "7" ] 
    then
        rm tmp/12481*
        python bin/convert_continue_except_block.py samples/u6_pyinstaller_3.8/12481.pyc tmp _check_ctypeslib_typecodes
        echo "Output is in tmp with name 12481*"
    fi
    if [ "$1" -eq "8" ] 
    then
        rm tmp/132693*
        python bin/move_return_outside_with.py samples/u6_pyinstaller_3.8/132693.pyc tmp load_library
        echo "Output is in tmp with name 132693*"
    fi
    if [ "$1" -eq "9" ] 
    then
        rm tmp/132681*
        python bin/convert_return_in_with.py samples/u6_pyinstaller_3.8/132681.pyc tmp typeof
        echo "Output is in tmp with name 132681* and only typeof function fixed"
    fi
    if [ "$1" -eq "10" ] 
    then
        rm tmp/10338*
        python bin/convert_break_except_block.py samples/u6_pyinstaller_3.8/10338.pyc tmp compiler_fixup
        python bin/convert_break_except_block.py tmp/10338_0loopJump.pyc tmp compiler_fixup
        echo "Output is in tmp with name 10338* and only typeof function fixed"
    fi
    if [ "$1" -eq "11" ] 
    then
        rm tmp/121846*
        python bin/convert_break_last_instru.py samples/u6_pyinstaller_3.8/121846.pyc tmp Uninstall
        echo "Output is in tmp with name 121846* and only typeof function fixed"
    fi
    if [ "$1" -eq "12" ] 
    then
        rm tmp/10281*
        python bin/convert_continue_in_with_try.py samples/u6_pyinstaller_3.8/10281.pyc tmp read_windows_registry
        python bin/convert_continue_in_with_try.py tmp/10281_0loopJump.pyc tmp read_windows_registry
        python bin/convert_continue_except_block.py tmp/10281_0loopJump_0loopJump.pyc tmp read_windows_registry
        echo "Output is in tmp with name 10281* and only read_windows_registry function fixed"
    fi
    if [ "$1" -eq "13" ] 
    then
        rm tmp/3600*
        python bin/convert_continue_general.py samples/u6_pyinstaller_3.8/3600.pyc tmp _line_iterator
        echo "Output is in tmp with name 3600* and only typeof function fixed"
    fi
    # DECOMPYLE3 starts here
    if [ "$1" -eq "14" ] 
    then
        rm tmp/2465*
        python bin/convert_not_in_loop_boolean.py samples/d3_parse_errors_py3.7/2465.pyc tmp/ source_synopsis
        echo "Output is in tmp with name 3600* and only typeof function fixed"
    fi
else
    echo "pyinstaller_mal_fix.sh [MWE number]"
    echo  "example: ./pyinstaller_mal_fix.sh 0"
fi

