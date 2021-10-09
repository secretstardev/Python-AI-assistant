#!/usr/bin/env bash

# -----------------------------------
# Initialization
# -----------------------------------
JARVIS_DIR=$(pwd)
VIRTUAL_ENV="jarvis_virtualenv"

green=`tput setaf 2`
red=`tput setaf 1`
reset=`tput sgr0`

# -----------------------------------
# Python version compatibility check
# -----------------------------------
version=$(python3 -V 2>&1 | grep -Po '(?<=Python )(.+)')
if [[ -z "$version" ]]
then
    echo "${red} No Python 3.x.x in your system! Install Python and try again! ${reset}"
    exit 1
else
    PYTHON_PATH=$(which python3)
fi

#-----------------------------------
# System dependencies installation
#-----------------------------------
sudo apt-get update && /
sudo apt-get install python-dev python3-dev && /
sudo apt-get install build-essential && /
sudo apt-get install portaudio19-dev python3-pyaudio python3-pyaudio && /
sudo apt-get install libasound2-plugins libsox-fmt-all libsox-dev libxml2-dev libxslt-dev sox ffmpeg && /
sudo apt-get install espeak && /
sudo apt-get install python3-pip && /
sudo apt-get install python3-setuptools && /
sudo apt-get install libcairo2-dev libgirepository1.0-dev gir1.2-gtk-3.0  && /
sudo apt install mongodb && /
sudo apt-get install gnupg

# Reload local package database
sudo apt-get update

RESULT=$?
if  [ $RESULT -eq 0 ]; then
    echo "${green} System dependencies installation succeeded! ${reset}"
else
    echo "${red} System dependencies installation failed ${reset}"
    exit 1
fi

#-----------------------------------
# Install virtualenv
#-----------------------------------
pip3 install virtualenv

RESULT=$?
if  [ $RESULT -eq 0 ]; then
    echo "${green} Install virtualenv succeeded! ${reset}"
else
    echo "${red} Install virtualenv failed ${reset}"
    exit 1
fi

#-----------------------------------
# Reload PATH
#-----------------------------------
#. ~/.profile

#-----------------------------------
# Create Jarvis virtual env
#-----------------------------------
virtualenv -p $PYTHON_PATH $JARVIS_DIR/$VIRTUAL_ENV

RESULT=$?
if  [ $RESULT -eq 0 ]; then
    echo "${green} Jarvis virtual env creation succeeded! ${reset}"
else
    echo "${red} Jarvis virtual env creation failed ${reset}"
    exit 1
fi

#-----------------------------------
# Install Python dependencies
#-----------------------------------
source $JARVIS_DIR/$VIRTUAL_ENV/bin/activate

# Install pip in virtualenv
sudo apt-get install python3-pip


pip3 install --upgrade cython

# Install python requirements
pip3 install -r $JARVIS_DIR/requirements.txt

RESULT=$?
if  [ $RESULT -eq 0 ]; then
    echo "${green} Install Python dependencies succeeded! ${reset}"
else
    echo "${red} Install Python dependencies failed ${reset}"
    exit 1
fi

#-----------------------------------
# Install nltk dependencies
#-----------------------------------
python3 -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"

RESULT=$?
if  [ $RESULT -eq 0 ]; then
    echo "${green} Install nltk dependencies succeeded! ${reset}"
else
    echo "${red} Install nltk dependencies failed ${reset}"
    exit 1
fi

#-----------------------------------
# Create log access
#-----------------------------------
sudo touch /var/log/jarvis.log && \
sudo chmod 777 /var/log/jarvis.log

RESULT=$?
if  [ $RESULT -eq 0 ]; then
    echo "${green} Create log access succeeded! ${reset}"
else
    echo "${red}Create log access failed ${reset}"
    exit 1
fi

#-----------------------------------
# Deactivate virtualenv
#-----------------------------------
deactivate

#-----------------------------------
# Finished
#-----------------------------------
echo "${green} Jarvis setup succeed! ${reset}"
echo "Start Jarvis: bash run_jarvis.sh"
