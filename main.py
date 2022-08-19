from flask import Flask, make_response, jsonify
from logging import Logger
import back
from geopy import distance as geo_distance, exc as geo_exceptions

logger = Logger('main logger')
application = Flask(__name__)

@application.route('/', methods = ['GET'])
def get_all_ships_data():
    return make_response('Not allowed to fetch all data at once', 
                        403)

@application.route('/ships/country/<string:country>', methods =['GET'])
def get_ships_from_country(country):
    code, body = None, None
    
    try:
        

        # Caching of 5 minutes on every requested index is enabled.(see back.GET_by_key)
        body = back.GET_by_key(key_name = 'country', key_value = country) 
        code = 200
    
    except Exception as e:
        code,body =500, str(e)
        raise e

    # 40X's are handled by flask
    finally: 
        body = body if isinstance(body, str) else jsonify({'json': body})
        return make_response(body, code)

@application.route('/ships/area/radius_km/<float:radius>/point/lat/<float:lat>/lon/<float:lon>', methods = ['GET'])
def get_ships_in_radius(radius : float,lat : float, lon : float):
    code, body = None, None
    
    try:
        
        # qualifier function specific for requested (lat, lon, radius).
        def within_radius(ship:dict)-> bool:
            check_lat = ship['position']['coordinates'][0]
            check_lon = ship['position']['coordinates'][1]
            dist = geo_distance.distance((lat,lon), (check_lat, check_lon))    
            return dist.kilometers <= radius

        body= back.GET_by_custom_qualifier(qualifier = within_radius)
        code = 200
            
    except geo_exceptions.GeopyError as e: # general error by geopy
            code, body =400, "Something's seems to be wrong with the coordinates or the requested radius"
            raise e     
    except Exception as e:  
            code, body= 500, str(e)
            raise e
    # 40X's are handled by flask
    finally:
        body = body if isinstance(body, str) else jsonify({'json': body})
        return make_response(body, code)


if __name__ == '__main__':
    application.run(port=5000)