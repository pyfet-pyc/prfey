
if [ "$#" -eq  "1" ] 
then
    if [ "$1" -eq "0" ] 
    then
        rm tmp/103837*
        python bin/convert_into_3_8.py samples/u6_pyinstaller_3.9_modified/103837.pyc tmp/
        echo "Output is in tmp with name 103837*"
    fi
else
    echo "3_9_mal_convert.sh [MWE number]"
    echo  "example: ./3_9_mal_convert.sh 0"
fi

