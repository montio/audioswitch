#!/bin/bash

NAME="audioswitch"
cd "./$NAME"
zip -r "../$NAME.plasmoid" .
cd ..

#plasmapkg -i "pulse control.plasmoid"

plasmoidviewer "$NAME"
