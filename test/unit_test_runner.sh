#!/bin/bash


# Set global parameters
SCRIPT_FULL_PATH=$(readlink -f "${0}")
SCRIPT_DIR="${SCRIPT_FULL_PATH%/*}"
readonly VENV_PATH="${SCRIPT_DIR}/../venv"

# Print debug variables
echo "[DEBUG] - SCRIPT_FULL_PATH=${SCRIPT_FULL_PATH}"
echo "[DEBUG] - SCRIPT_DIR=${SCRIPT_DIR}"

echo "[INFO] - Starting to check the status of Python virtual environment."
if [[ ! -d "${VENV_PATH}" ]]; then
    echo "[WARNING] - The python virtual environment folder doesn't exist: ${VENV_PATH}"

    echo "[INFO] - Trying to generate it!"
    if ! python3 -m venv "${VENV_PATH}"; then
        echo "[ERROR] - Cannot generate the Python3 virtual environment. Please do it by hand! Path: ${VENV_PATH}" 1>&2
        exit 1
    fi
fi

echo "[INFO] - Starting to activate (source) the Python virtual environment"
if ! source "${VENV_PATH}/bin/activate"; then
    echo "[ERROR] - Cannot source the Python executable. Path: ${VENV_PATH}/bin/activate" 1>&2
    exit 1
fi

echo "[INFO] - Used Python executable path:"
which python

echo "[INFO] - Starting to install the required packages in the Python virtual environment"
if ! pip install -r "${VENV_PATH}/../requirements.txt"; then
    echo "[ERROR] - Cannot install requirements from '${VENV_PATH}/bin/activate'" 1>&2
    exit 1
fi

echo "[INFO] - Start to run the UnitTests and the coverage"
coverage run --rcfile=.coverage_rc -m unittest discover -s test -p *_ut.py -v || { echo "[ERROR] - Failed 'coverage run'" 1>&2; exit 1; }
coverage combine --rcfile=.coverage_rc || { echo "[ERROR] - Failed 'coverage combine'" 1>&2; exit 1; }
coverage xml --rcfile=.coverage_rc || { echo "[ERROR] - Failed 'coverage xml'" 1>&2; exit 1; }
coverage html --rcfile=.coverage_rc || { echo "[ERROR] - Failed 'coverage html'" 1>&2; exit 1; }
