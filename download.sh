#!/bin/bash

echo "Creating embeddings folder"
mkdir -m 777 "embeddings"
echo "Done!!!"

echo "Creating output folder"
mkdir "output"
echo "Done!!!"

echo "Downloading pre-trained embeddings"
wget http://143.107.183.175:23580/glove
mv glove embeddings/glove
wget http://143.107.183.175:23580/glove.vectors.npy
mv glove.vectors.npy embeddings/glove.vectors.npy
echo "Done!!"
