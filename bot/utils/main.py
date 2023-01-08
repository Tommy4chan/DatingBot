from geopy.geocoders import Nominatim
import logging
from aiogram.utils.markdown import hlink


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


async def add_age_ending(age):
    age = str(age)
    if age[1] == '1':
        return age + " рік"
    elif age[1] == '2' or age[1] == '3' or age[1] == '4':
        return age + " роки"
    else:
        return age + " років"


async def get_instagram_status(instagram):
    if instagram == None:
        return "Користувач не прикріпив Instagram"
    else:
        return f'<a href="https://www.instagram.com/{instagram}/">@{instagram}</a>'


async def get_questionnaire_status(status):
    if status:
        return "Підтверджена"
    else:
        return "Непідтверджена"


async def get_questionnaire(user_data, is_questionnaire_full):
    if is_questionnaire_full:
        return f"🌆 {user_data['name']}, {await add_age_ending(user_data['age'])}, {user_data['location']}\n\nПро себе - {user_data['description']}\n\nІнстаграм - {await get_instagram_status('tommy4chan')}\nСтатус анкети - {await get_questionnaire_status(1)}"
    else:
        return f"🌆 {user_data['name']}, {await add_age_ending(user_data['age'])}, {user_data['location']}\n\nПро себе - {user_data['description']}"