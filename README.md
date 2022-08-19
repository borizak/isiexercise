# isiexercise 
(19.08.22)

This is a Read-only REST-api service for the (mock) ISI Ship DataBase.
It exposes 2 types of query: 
Ships from a Country of origin, 
and Ships within a radius of a coordinate.


## API Reference

#### Get ships from a Country of origin

```http
  GET /country/ships
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `country` | `string` | **Required**.Not Case Sensitive              |

#### Get Ships located in an area

```http
  GET /area/ships
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `point`   | `json` | **Required**. Contains 2 floats: `lat`, `lon`, the center of the area|
| `radius_km`|`float`|**Required**. Determines the area around `point`|

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


## Authors

- [@Ben Izakson](https://github.com/borizak)

