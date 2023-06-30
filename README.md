# IPtables to World Chart

This project provides a visualization tool to view IPtable country-specific filtering rules on a world map. It is a Flask application that periodically generates an image of a world map, coloring countries according to whether the traffic is allowed or blocked.

## Purpose and Statement

This tool is designed with the intention of providing a clear and intuitive way of understanding and communicating the geographically-based filtering rules implemented via IPtables. 

Please note, the traffic filtering based on country-specific rules in this project does not reflect any form of bias, discrimination, or political judgement towards the affected countries. This tool is intended for technical purposes only, focusing on the network interactions that are relevant to the user. The countries being filtered are simply those where the user, or the server this application is being deployed on, are unlikely to have any significant network interaction. This is a measure for reducing unnecessary network noise and enhancing the security posture, and not a reflection of any personal or political sentiment towards the countries involved. 

## Installation

This project relies on several Python packages. You can install these packages using pip by running `pip install -r requirements.txt`. The list of dependencies is located in the `requirements.txt` file.

## Usage

To run the Flask application, use the command `python3 app.py`. The application will start a server locally, typically on `localhost:5000`. You can view the generated map by navigating to this address in a web browser. The map will update every 90 minutes by default.