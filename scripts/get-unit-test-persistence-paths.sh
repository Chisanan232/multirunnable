#!/usr/bin/env bash

set -ex
if [[ $1 == "windows" ]]; then

    declare -a array2=( $(ls -d tests/{unit,system}/*/ | grep -v '__pycache__'| grep -v 'unit/serve' | grep -v 'unit/orchestrate'))
    declare -a array3=( $(ls -d tests/{unit}/orchestrate/*/ | grep -v '__pycache__'))
    declare -a array4=( $(ls -d tests/{unit}/serve/*/ | grep -v '__pycache__'))
    dest1=( "${array2[@]}" "${array3[@]}" "${array4[@]}" )
    printf '%s\n' "${dest1[@]}" | jq -R . | jq -cs .

else

    declare -a persistence_database_tests
    declare -a persistence_file_tests

    getalltests() {
        declare -a testpatharray=( $(ls -F $1 | grep -v '/$' | grep -v '__init__.py' | grep -v 'test_config.py' | grep -v -E '^_[a-z_]{1,64}.py' | grep -v '__pycache__'))

        declare -a alltestpaths
        for (( i = 0; i < ${#testpatharray[@]}; i++ )) ; do
            alltestpaths[$i]=$1${testpatharray[$i]}
        done

        if echo $1 | grep -q "database";
        then
            persistence_database_tests=${alltestpaths[@]}
        elif echo $1 | grep -q "file";
        then
            persistence_file_tests=${alltestpaths[@]}
        else
            return 0
        fi
    }

    persistence_database_path=tests/unit_test/persistence/database/
    persistence_file_path=tests/unit_test/persistence/file/

    getalltests $persistence_database_path
    getalltests $persistence_file_path

    dest=( "${persistence_database_tests[@]}" "${persistence_file_tests[@]}" )

    printf '%s\n' "${dest[@]}" | jq -R . | jq -cs .

fi
