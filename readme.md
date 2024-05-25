# Func Grab

Store the metadata of the functions from your python repo

## Table of Contents

- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)

## Installation

- Install the necessary packages
- Run the following command:
  > pip3 install fast-api firebase-admin sqlalchemy tree-sitter tree-sitter-python

## Setup

- Run the following command to create an python env:
  > python3 -m venv env
- Create a firebase app enable email authentication
- Generate the private key under service accounts and add that to serviceAccountKey.json
- Get the firebaseConfig from the admin sdk and replace the config in firebase.py file
- Run the comman: fastapi dev main.py

## Usage

- Signup and login and get the idToken
- Now send that token along with the other apis through authorization token
- /url/{github_url}: Send your github repo link with python files
- /functions/{function_name}: Send the function name you want to search and get the code
