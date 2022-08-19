# isiexercise 
(19.08.22)

This is a Read-only REST-api service for the (mock) ISI Ship DataBase.
It exposes 2 types of query: 
Ships from a Country of origin, 
and Ships within a radius of a coordinate.


## API Reference

#### Get ships from a Country of origin

```http
  GET /ships/country/<string:country>
```

#### Get Ships located in an area

```http
  GET ships/area/radius_km/<float:radius>/point/lat/<float:lat>/lon/<float:lon>/
```

## Run Locally

To run the service as a docker ,
make sure you have git and Docker installed on the machine.
Start the docker up simply from cli:


```bash
    git clone https://github.com/borizak/isiexercise.git

    cd ./isiexercise
    
    ./docker.sh
```

- You can now access the endpoints from 'http://HOSTNAME:5000/'


## Author

- [@Ben Izakson](https://github.com/borizak)

