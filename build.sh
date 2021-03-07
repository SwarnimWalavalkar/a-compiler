PYTHON="python3"
COMPILER="a.py"
CC="gcc"

function comp {
    BN=$(basename -s .a $1)
    TTOUTPUT=$(${PYTHON} ${COMPILER} $1 2>&1)
    if [ $? -ne 0 ]; then
        echo "${TTOUTPUT}"
    else
        mkdir -p ./build
        mv out.c ./build/${BN}.c
        cd build
        CCOUTPUT=$(${CC} -o ${BN} ${BN}.c)
        if [ $? -ne 0 ]; then
            echo "${CCOUTPUT}"
        else
            cd ../
            echo "${TTOUTPUT}"
        fi
    fi
}

if [ $# -eq 0 ]; then
    for i in $(ls examples/*.a); do
        comp $i
    done
else
    comp $1
fi