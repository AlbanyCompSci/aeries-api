#!/bin/sh
echo "Enter email:"
read email
echo "Enter password:"
read password
echo -e "$email\n$password" > "MyLoginData"
