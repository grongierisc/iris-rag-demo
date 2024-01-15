#!/bin/bash

set -m

iris session iris -U%SYS '##class(Security.Users).UnExpireUserPasswords("*")'

iop --init

iop --migrate /irisdev/app/src/python/settings.py

iop --start Chat.Production --detach

streamlit run /irisdev/app/src/python/rag/app.py --server.port=8051 --server.address=0.0.0.0

fg %1