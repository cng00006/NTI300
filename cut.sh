#! /bin/bash

who | cut -d' ' -f1
#This allows you to cut out the list of users by their name. It helps allow automation in the example that followed by sending the user
#name to mail.
