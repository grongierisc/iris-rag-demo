#!/bin/bash

set -m

/iris-main "$@" &

/usr/irissys/dev/Cloud/ICM/waitISC.sh

iop --init

iop --migrate /irisdev/app/src/python/settings.py

iop --start Chat.Production --detach

fg %1