#!/bin/bash
# Set the path to your alembic.ini file
operation_key=$1

if [ "$operation_key" == "upgrade" ]; then
    # Perform an upgrade
    alembic upgrade head
elif [ "$operation_key" == "downgrade" ]; then
    # Perform a downgrade
    alembic downgrade -1
else
    echo "Invalid operation key. Supported keys: 'upgrade', 'downgrade'"
fi