#!/bin/bash

echo "Ejecutando migraciones..."
python manage.py migrate

echo "Ejecutando collectstatic..."
python manage.py collectstatic --noinput
