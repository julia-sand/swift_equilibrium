#!/usr/bin/env bash

# get cwd
cwd="$(pwd)"
base_dir="${1:-results_se}"   # default = results

# function to create dir and fail if it exists
make_dir() {
    if [ -d "$1" ]; then
        echo "A results directory already exists in this folder."
        exit 1
    fi
    mkdir -p "$1"
}

# hard penalty
make_dir "$cwd/$base_dir/hard/equil/direct"
make_dir "$cwd/$base_dir/hard/noneq/direct"
make_dir "$cwd/$base_dir/hard/stiffness_control/direct"

# log
make_dir "$cwd/$base_dir/log/equil/indirect"

# harmonic
for method in direct indirect slowfast; do
    make_dir "$cwd/$base_dir/harmonic/equil/$method"
done

make_dir "$cwd/$base_dir/harmonic/noneq/indirect"