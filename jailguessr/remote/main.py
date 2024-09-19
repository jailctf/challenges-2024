#!/usr/local/bin/python3
flag = open('flag.txt').read()

nearest_jail = 'southernqueenslandcorrectionalcentre'

x = input("What is the nearest jail to the image? Please enter it as it appears on google maps but without any punctuation, spaces, or capitalization (e.g. adxflorence)\n> ").lower()
if x == nearest_jail:
  print("Good job! Here is your flag:", flag)
else:
  print("Try again.")
