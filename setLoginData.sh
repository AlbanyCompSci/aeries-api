#!/bin/sh
echo -n "Enter email: "
read email
echo -n "Enter password: "
read -s password
echo
echo -e "$email\n$password" > "MyLoginData"
