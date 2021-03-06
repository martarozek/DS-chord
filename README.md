
# Implementation of CHORD protocol in Python

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
## Authors
_Marta Rozek, Anastasios Sidiropoulos, Davide Mariotti, Marios Evangelos Kanakis_
## Introduction
This project implements a key-value store based on the Chord protocol.
It supports nodes joining and leaving dynamically but not node failures.
It uses finger tables to achieve lookups in logarithmic time.
## How it works
Have a look at _Chord: A Scalable Peer-to-peer Lookup Protocol for Internet Applications_
## Running the app
* start the app
```
python app.py
```
* start several nodes
```
python node.py --port=8042
python node.py --port=8043
python node.py --port=8044
```
* run tests, e.g.
```
python multiple_nodes_test.py
```
## Performance
This project has not been implemented with performance in mind. We used Python and XML-RPC, which are known to provide lower performance than, say, C++ and its rpclib. Also, the app serves requests sequentially, so the more nodes, the more communication overhead, but not more speed. We focused on readability and simplicity.

## Notes
To update requirements, add a new line with the package name you want to add (without version) to the `requirements.in` file and then run:
```
pip-compile requirements.in
```
This will generate a new version of the requirements.txt file. Push both files to the repo.
