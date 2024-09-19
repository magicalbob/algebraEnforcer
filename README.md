# AlgebraEnforcer

A simple Python-Flask application designed to help my son revise algebra through interactive questioning.

## Overview

The app presents three questions involving:
- Simple linear simultaneous equations
- Expanding and simplifying algebraic expressions
- Calculating the area of triangles using Heron's formula

Once the three questions have been answered, the app utilizes SaltStack to restore internet access on his Windows gaming computer.

You can try out the app at: [Algebra Enforcer](https://algebra.ellisbs.co.uk)

## Features

- Asks three types of algebra questions.
- Tracks progress and provides feedback on answers.
- Automatically manages internet access for study sessions.

## Configuration

The application uses a `config.yaml` file for configuration settings, which includes:
- Database details
- Secret keys
- Internet restoration commands

### Example `algebra.yaml`

```yaml
database: your_database_name
secret_key: your_secret_key
internet_restore: your_command_to_restore_internet
```

### Installation
#### Requirements
Install required packages using:

```bash
pip install -r requirements.txt
```

#### Docker Support
A Dockerfile is provided to run the application as a container.

##### Building the Docker Image
To build the Docker image, run:

```bash
docker build -t local:algebra .
```

##### Running the Docker Container
To run the container, use:

```bash
docker run -d -v ${PWD}:/opt/algebra -p 40000:5001 local:algebra
```

### Usage
Start the application:

```bash
python algebraenforcer.py
```

The app will run on http://localhost:5002.

Access the application through your web browser.

Follow the prompts to answer the algebra questions.

#### Cron Job for Internet Control
A cron job can be set up to turn off internet access on the gaming machine every morning using SaltStack.

### Contributing
Feel free to submit issues and pull requests. Contributions are welcome!

License
This project is licensed under the MIT License.
