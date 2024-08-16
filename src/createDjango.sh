#!/bin/bash

# Install Python and Django
brew install python
pip install django

# Ask for the project name
echo "Enter your Django project name:"
read project_name

# Create a new Django project
django-admin startproject $project_name

# Navigate to the project directory
cd $project_name

# Ask for the app name
echo "Enter your Django app name:"
read app_name

# Create a new Django app
python manage.py startapp $app_name

# Open the project in VS Code
code .

# Start the Django development server
python manage.py runserver