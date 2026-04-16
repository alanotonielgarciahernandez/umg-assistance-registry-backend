#!/bin/bash

# Detectar si estamos en modo debug y usar servidor apropiado.
if [ "$DJANGO_DEBUG" = "True" ] || [ "$DJANGO_DEBUG" = "true" ] || [ "$DJANGO_DEBUG" = "1" ]; then
    echo "Running in DEBUG mode with Django development server..."
    python manage.py runserver 0.0.0.0:80
else
    echo "Running in PRODUCTION mode with Waitress..."
    waitress-serve --host=0.0.0.0 --port=80 wsgi:application
fi
