#!/bin/bash
# Auteur J-P Perroud
# novembre 2021

# go est un script shell pour sycroniser git et github
# Il faut donner en quelques mots entre parenthèses 
# le motif de la mofication 

if [ -z $1 ]

then
    echo "Donner un texte, merci "
else
    echo "Le texte passé est : " $1
    git add .
    git commit -m "$1"
    git push -u origin main
fi

