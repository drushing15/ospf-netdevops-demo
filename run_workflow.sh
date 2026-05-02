#!/bin/bash

echo "===== PRE-CHECK ====="
python3 tests/validate_ospf.py pre

echo "===== DEPLOY CHANGE ====="
ansible-playbook -i inventory/hosts.yml playbooks/add_loopback.yml

echo "===== POST-CHECK ====="
python3 tests/validate_ospf.py post