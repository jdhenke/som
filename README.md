Reifying the Principle of Noncompromise
===

This repo contains the code used for the dynamic model described in my final report for 6.868. This README walks you through how to setup and run the code to generate the figures presented in the paper.

## Getting Started

First, let's get the necessary tools.
```bash
git clone git@github.com:jdhenke/som.git
cd som
virtualenv env --no-site-packages
source env/bin/activate
pip install matplotlib
```

Now let's run the model.
```bash
python demo.py
```

This will produce each of the figures in the paper as *.png files in the current directory.

## License
Copyright (c) 2013 Joseph Henke
See LICENSE for licensing information