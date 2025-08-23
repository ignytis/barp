#!/usr/bin/env bash
set -eu

GREEN='\033[0;32m' 
BLUE='\033[0;34m' 
NOCOLOR='\033[0m'

echo -e "${BLUE}Setting up environment...${NOCOLOR}"
#cp -R /app /install
pip install ".[cli,runtime]"

echo -e "${BLUE}Running a simple command which prints profile vars...${NOCOLOR}"
export BARP_PROFILE=/app/docs/examples/barp.d/profiles/local.cfg
barp run file://$PWD/docs/examples/barp.d/task_templates/command.cfg?command.print_profile_vars

echo -e "${BLUE}Trying the same command, but with plugins installed...${NOCOLOR}"
pip install -e /app/docs/examples/plugins/event_listeners/example_listener/
barp run file://$PWD/docs/examples/barp.d/task_templates/command.cfg?command.print_profile_vars
echo -e "${BLUE}Cleaning up and verifying...${NOCOLOR}"
pip uninstall --yes example_listener
barp run file://$PWD/docs/examples/barp.d/task_templates/command.cfg?command.print_profile_vars

echo -e "${GREEN}All tests passed.${NOCOLOR}"