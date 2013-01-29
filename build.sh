#!/bin/bash

NAME="audioswitch"
cd "./$NAME"
zip -r "../$NAME.plasmoid" .
cd ..

#plasmapkg -i "pulse control.plasmoid"

plasmoidviewer "$NAME"


# zip -r ../hello-python.zip .

# To uninstall our applet we use plasmapkg again with its -r option.
# plasmapkg -r hello-python
