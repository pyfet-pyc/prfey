
if [ "$#" -eq  "1" ] 
then
    if [ "$1" -eq "0" ] 
    then
        rm tmp/16120c5c704410655c89d5ae64c668414c6434a1*
        python bin/remove_dead_code.py samples/mal_samples/16120c5c704410655c89d5ae64c668414c6434a1.pyc tmp spread
    fi
    if [ "$1" -eq "1" ] 
    then
        rm tmp/3e0b0460fe349343cae4aaacb0ad985b8c8c60fb*
        python bin/remove_dead_code.py samples/mal_samples/3e0b0460fe349343cae4aaacb0ad985b8c8c60fb.pyc tmp set_desktop_background
    fi
    if [ "$1" -eq "2" ] 
    then
        rm tmp/59fff7c9dccbfa15f03afdcbeb7d0a63d6105627*
        python bin/remove_dead_code.py samples/mal_samples/59fff7c9dccbfa15f03afdcbeb7d0a63d6105627.pyc tmp spread
    fi
    if [ "$1" -eq "3" ] 
    then
        rm tmp/b818a4c8d1fb29c71a81a8ffb08708b7aea8044b*
        python bin/remove_dead_code.py samples/mal_samples/b818a4c8d1fb29c71a81a8ffb08708b7aea8044b.pyc tmp spread
    fi
    if [ "$1" -eq "4" ] 
    then
        rm tmp/bb6210796f48c80954a8e214d2ccd2933df442c4*
        python bin/remove_dead_code.py samples/mal_samples/bb6210796f48c80954a8e214d2ccd2933df442c4.pyc tmp spread
    fi
    if [ "$1" -eq "5" ] 
    then
        rm tmp/bf7c8de9e71a6dc68d31078a2166474f62390c66*
        python bin/remove_dead_code.py samples/mal_samples/bf7c8de9e71a6dc68d31078a2166474f62390c66.pyc tmp spread
    fi
    if [ "$1" -eq "6" ] 
    then
        rm tmp/e3beb00b80d7cfd7304e945959ccd7b56a5a95dd*
        python bin/remove_dead_code.py samples/mal_samples/e3beb00b80d7cfd7304e945959ccd7b56a5a95dd.pyc tmp spread
    fi
else
    echo "mal_fix.sh [MWE number]"
    echo  "example: ./mal_fix.sh 0"
fi

