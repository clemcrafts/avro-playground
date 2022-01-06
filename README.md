
# Avro Publisher Snippet

AVRO publisher with schemas definitions and containers exposing the registry connected to zookeeper.

## Setup

```
$ virtualenv env -p python3.8
```
Install library
```
$ pip install -r requirements.txt
```
Launch the containers (Kakfa, Schema Registry, Rest interface)

```
$ docker-compose up
```

### Run

Run a publish/consume with an over-simplified event (only one ID field)
```
$ python publish.py
```

Will publish and consume:

```
{"source_request_id": "527549db-c058-43e3-90d6-65dab31e40a1"}
```

with a `test` key.