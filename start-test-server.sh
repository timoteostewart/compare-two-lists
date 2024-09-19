#!/usr/bin/env bash

# debugging switches
# set -o errexit   # abort on nonzero exit status; same as set -e
# set -o nounset   # abort on unbound variable; same as set -u
# set -o pipefail  # don't hide errors within pipes
# set -o xtrace  # show commands being executed; same as set -x
# set -o verbose # verbose mode; same as set -v

venv_python_binary="/srv/compare-two-lists-project/.venv/bin/python"
manage_py_path="/srv/compare-two-lists-project/compare_two_lists/manage.py"
ip_address="192.168.1.186"
port="8000"

"${venv_python_binary}" "${manage_py_path}" runserver "${ip_address}:${port}"
