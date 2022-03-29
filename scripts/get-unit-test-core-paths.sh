#!/usr/bin/env bash

set -ex
if [[ $1 == "windows" ]]; then

    declare -a array2=( $(ls -d tests/{unit,system}/*/ | grep -v '__pycache__'| grep -v 'unit/serve' | grep -v 'unit/orchestrate'))
    declare -a array3=( $(ls -d tests/{unit}/orchestrate/*/ | grep -v '__pycache__'))
    declare -a array4=( $(ls -d tests/{unit}/serve/*/ | grep -v '__pycache__'))
    dest1=( "${array2[@]}" "${array3[@]}" "${array4[@]}" )
    printf '%s\n' "${dest1[@]}" | jq -R . | jq -cs .

else

    declare -a array1=(
    "tests/unit_test/_singletons.py"
    )

    declare -a init_tests
    declare -a basic_api_tests
    declare -a parallel_tests
    declare -a concurrent_tests
    declare -a coroutine_tests
    declare -a factory_tests
    declare -a apis_tests
    declare -a adapter_tests

    getalltests() {
        declare -a testpatharray=( $(ls -F $1 | grep -v '/$' | grep -v '__init__.py' | grep -v 'test_config.py' | grep -v -E '^_[a-z_]{1,64}.py' | grep -v '__pycache__'))

        declare -a alltestpaths
        for (( i = 0; i < ${#testpatharray[@]}; i++ )) ; do
            alltestpaths[$i]=$1${testpatharray[$i]}
        done

        if echo $1 | grep -q "parallel";
        then
            parallel_tests=${alltestpaths[@]}
        elif echo $1 | grep -q "concurrent";
        then
            concurrent_tests=${alltestpaths[@]}
        elif echo $1 | grep -q "coroutine";
        then
            coroutine_tests=${alltestpaths[@]}
        elif echo $1 | grep -q "factory";
        then
            factory_tests=${alltestpaths[@]}
        elif echo $1 | grep -q "api";
        then
            apis_tests=${alltestpaths[@]}
        elif echo $1 | grep -q "adapter";
        then
            adapter_tests=${alltestpaths[@]}
        else
            init_tests=${alltestpaths[@]}
        fi
    }

    init_path=tests/unit_test/
    parallelpath=tests/unit_test/parallel/
    concurrentpath=tests/unit_test/concurrent/
    coroutinepath=tests/unit_test/coroutine/
    factory_path=tests/unit_test/factory/
    api_path=tests/unit_test/api/
    adapter_path=tests/unit_test/adapter/

    getalltests $init_path
    getalltests $parallelpath
    getalltests $parallelpath
    getalltests $concurrentpath
    getalltests $coroutinepath
    getalltests $factory_path
    getalltests $api_path
    getalltests $adapter_path

    dest=( "${array1[@]} ${init_tests[@]} ${parallel_tests[@]} ${concurrent_tests[@]} ${coroutine_tests[@]} ${factory_tests[@]} ${apis_tests[@]} ${adapter_tests[@]}" )

    printf '%s\n' "${dest[@]}" | jq -R . | jq -cs .

fi
