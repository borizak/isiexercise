from flask import Flask, request, make_response, jsonify
from logging import Logger
import back
from geopy import distance

logger = Logger('main logger')
application = Flask(__name__)

@application.route('/ships/country/<string:country>', methods =['GET'])
def get_ships_from_country(country):
    status , response = None, None

    try:
        res = back.GET_by_key(key_name = 'country', key_value = country) 
        response = make_response(jsonify({"data": res}), 200)  # empty lists are acceptable

    except Exception as e:
        response = make_response(jsonify({'error':str(e)}), 500) 
        # 40X's are handled by flask
    
    return response

@application.route('/ships/location/lat/<float:lat>/lon/<float:lon>/km_radius/<float:radius>', methods = ['GET'])
def get_ships_in_radius(lat, lon,radius):
    
    # qualifier function specific for requested (lat, lon, radius).
    def within_radius(ship:dict):
        check_lat = ship['position']['coordinates'][0]
        check_lon = ship['position']['coordinates'][1]
        dist = distance.distance((lat,lon), (check_lat, check_lon))    
        return dist.kilometers <= radius
    
    try:

        data= back.GET_by_custom_qualifier(qualifier = within_radius)
        response = make_response(jsonify({'data':data}), 200) # empty lists are acceptable
    
    except Exception as e:
        response = make_response(jsonify({'error':str(e)}), 500) 
        # 40X's are handled by flask

    return response


if __name__ == "__main__":
    application.run(port=5000)