#!/bin/bash

command=$1
projectDir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 "$projectDir/kvantum.py" "$command"