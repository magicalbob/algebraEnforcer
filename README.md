AlgebraEnforcer
===============

A simple python-Flask app that gets my son to revise algebra.

A cron job turns internet access off on his Windows gaming machine every morning using SaltStack.

The app asks 3 questions - simple linear simultaneous equations.

Once the 3 questions have been answered, the app uses salt to turn Internet access back on on his gaming computer.

Docker
======

Docker file to run it as a container.

Build it with: `docker build -t local:algebra .`

Run it with: `docker run -d -v ${PWD}:/opt/algebra -p 40000:5001 local:algebra`
