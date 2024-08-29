#!/usr/bin/env sh

make -C collector --always-make --dry-run | grep -wE 'cc' | jq -nR '[inputs|{directory:".", command:., file: match(" [^ ]+$").string[1:]}]' > compile_commands.json
