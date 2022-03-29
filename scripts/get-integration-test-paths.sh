#!/usr/bin/env bash

set -ex
if [[ $1 == "windows" ]]; then

    declare -a array2=( $(ls -d tests/{unit,system}/*/ | grep -v '__pycache__'| grep -v 'unit/serve' | grep -v 'unit/orchestrate'))
    declare -a array3=( $(ls -d tests/{unit}/orchestrate/*/ | grep -v '__pycache__'))
    declare -a array4=( $(ls -d tests/{unit}/serve/*/ | grep -v '__pycache__'))
    dest1=( "${array2[@]}" "${array3[@]}" "${array4[@]}" )
    printf '%s\n' "${dest1[@]}" | jq -R . | jq -cs .

else

    declare -a init_tests

    getalltests() {
        declare -a testpatharray=( $(ls -F $1 | grep -v '/$' | grep -v '__init__.py' | grep -v 'test_config.py' | grep -v -E '^_[a-z_]{1,64}.py' | grep -v '__pycache__'))

        declare -a alltestpaths
        for (( i = 0; i < ${#testpatharray[@]}; i++ )) ; do
            alltestpaths[$i]=$1${testpatharray[$i]}
        done

        if echo $1 | grep -q "parallel";
        then
            parallel_tests=${alltestpaths[@]}
        else
            init_tests=${alltestpaths[@]}
        fi
    }

    init_path=tests/integration_test/

    getalltests $init_path

    dest=( "${init_tests[@]}" )

    printf '%s\n' "${dest[@]}" | jq -R . | jq -cs .

fi
