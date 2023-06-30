# IPtables to World Chart

This project provides a visualization tool to view IPtable country-specific filtering rules on a world map. It is a Flask application that periodically generates an image of a world map, coloring the countries based on the rules set in your IPtables.

The purpose of this tool is not to make political statements or to support any form of discrimination based on nationality. It is merely a tool to visualize and manage traffic from countries where the user doesn't anticipate any interaction, based on their use case at the time of the code writing. The countries being blocked in the code are just examples, and the tool is fully customizable to suit the user's needs.

Here's a sample of the [output image](./worldmap.png) produced by the application. This default representation can be easily customized within the application itself.

## Installation

Before running the application, install the required packages using pip:

```
pip install -r requirements.txt
```

In order for the application to work as expected, the IPtables tools must be installed and properly configured. This might involve complex setup procedures and requires superuser privileges. Therefore, it is recommended to have an advanced understanding of your system's network configuration before proceeding.

## Running the Application

You can run the Flask application locally using the command:

```
python app.py
```

To host the application with Gunicorn, use the following command:

```
gunicorn -w 4 -b 0.0.0.0:5000 app:application --preload
```

The `-w 4` option specifies the number of worker processes, and the `-b 0.0.0.0:5000` option specifies the binding address and port. 

The `--preload` option is important because without it, each worker would generate its own version of the cached image. By preloading the application, we ensure that all workers share the same instance of the application, thereby sharing the same cached image. 

Please note that this application is meant to be run in a secure, isolated environment as it runs IPtables commands which require superuser privileges. This tool is a proof-of-concept demonstrating the potential use cases and is not intended for critical operational deployment.