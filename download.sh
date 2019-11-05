#!/bin/bash

username=$(whoami)

wget http://143.107.183.175:22980/download.php?file=embeddings/glove/glove_s100.zip
mkdir -p "models"
unzip glove_s100.zip -d /models
rm glove_s100.zip

wget http://nlp.stanford.edu/software/stanfordnlp_models/0.2.0/pt_bosque_models.zip
unzip pt_bosque_models.zip -d /home/$username
rm pt_bosque_models.zip

echo "Done!!"
