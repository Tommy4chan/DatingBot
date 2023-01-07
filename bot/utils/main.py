from geopy.geocoders import Nominatim
import logging

async def decode_callback_data(callback):
    return callback.data.split('_')[1]

async def get_location_by_coordinates(latitude, longitude):
    geolocator = Nominatim(user_agent="dating_bot")
    location = geolocator.reverse(str(latitude) + "," + str(longitude), language='ua')
    address = location.raw['address']
    location_data = ""
    if address.get('city') != None:
        location_data += f"{address.get('city')}, "
    elif address.get('town') != None:
        location_data += f"{address.get('town')}, "
    else:
        location_data += f"{address.get('village')}, "
    if address.get('state') != None:
        location_data += f"{address.get('state')}, "
    location_data += f"{address.get('country')}"
    print(location_data)
    return location_data

async def get_location_by_name(city):
    geolocator = Nominatim(user_agent="dating_bot")
    try:
        location = geolocator.geocode(city, language='ua')
        return await get_location_by_coordinates(location.latitude, location.longitude)
    except Exception as e:
        logging.info(e)
        return "not found"