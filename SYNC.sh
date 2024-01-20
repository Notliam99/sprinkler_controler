mut_prams=$@

ampy_put () {
    echo -e "${2}\033[38:5:27;1mStarting Transfer: ${1}\033[0m"
    {
        ampy -p /dev/ttyACM0 put $1 $1
    }&> /dev/null
    ampy_exit=$?
    if [ "${ampy_exit}" != "0" ]; then
        if [ "${ampy_exit}" == "1" ]; then
            echo -e "\n\033[38:5:9;1;4mERROR: ^C Exiting\033[0m\n"
            exit 1
        fi
        echo -e "\n\033[38:5:9;1;4mERROR: ${1} is not a valid input directory or file\033[0m\n"
        help_func
        exit $ampy_exit
    fi
    echo -e "\033[38:5:29;1mDone Transfer Of: ${1}\033[0m"
}

help_func () {
    echo -e "\033[38:5:141;1;4mSYNC Shell Script\033[0m\n\n\033[38:5:39m./SYNC.sh <files/directory> <options>\033[0m\n\n\033[38:5:141;1;4mOPTIONS:\033[0m\n\n\033[38:5:29;1m--init-repo # populates the git submodules\n\033[38:5:27;1m--update # updates the git submodules\033[0m\n\033[38:5:11m--help # This Page The Help Docs\033[0m"
}

get_item_pos_array () {
    my_array="${1}"
    value="${2}"
    out=()

    for i in "${!my_array[@]}"; do
        if [[ "${my_array[$i]}" != "${value}" ]]; then
            out+=$i
        fi
    done

    echo $out
}

if [ "${*}" != "" ]; then
    for i in "${@}"
    do
        if [ "${i}" == "--init-repo" ]; then
            git submodule init
            git submodule update
            mut_prams=$(get_item_pos_array --init-repo "${mut_prams}")
        elif [ "${i}" == "--update" ]; then
            git submodule update --remote
            mut_prams=$(get_item_pos_array --update "${mut_prams}")
        elif [ "${i}" == "--sync-all" ]; then
            echo -e "\033[38:5:27;1mCopying All The Code Onto The Device\033[0m"
            ampy_put ./piApi "\n(1 Of 3)"
            ampy_put ./spricklerUI "\n(2 Of 3)"
            ampy_put ./main.py "\n(3 Of 3)"
            mut_prams=$(get_item_pos_array --sync-all "${mut_prams}")
        elif [ "${i}" == "--help" ]; then
            help_func
            exit 0
        fi
    done
    if [ "${mut_prams}" != "" ]; then
        for x in "${mut_prams}"; do
            ampy_put "${x}"
        done
    fi
else
    help_func
fi
