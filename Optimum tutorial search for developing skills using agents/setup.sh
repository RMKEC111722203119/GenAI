#!/bin/bash

# Create the Streamlit configuration directory
mkdir -p ~/.streamlit/

# Write the Streamlit configuration file
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
[theme]\n\
primaryColor = '#d33682'\n\
backgroundColor = '#002b36'\n\
secondaryBackgroundColor = '#586e75'\n\
textColor = '#fff'\n\
" > ~/.streamlit/config.toml

# Install the necessary Python packages


