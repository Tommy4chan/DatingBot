from geopy.geocoders import GoogleV3
import os
from dotenv import load_dotenv # For local use only
import logging
import re


async def decode_callback_data(callback):
    return callback.data.split('_')[1]


async def get_location_by_coordinates(latitude, longitude):
    geolocator = GoogleV3(api_key=os.getenv('GOOGLE_API_KEY'), domain="maps.google.com.ua")
    try:
        location = geolocator.reverse(str(latitude) + "," + str(longitude))
        location_data = location.raw['address_components']
        return await form_location_data(location_data)
    except Exception as e:
        print(e)
        return "not found"


async def get_location_by_name(city):
    geolocator = GoogleV3(api_key=os.getenv('GOOGLE_API_KEY'), domain="maps.google.com.ua")
    try:
        location = geolocator.geocode(city)
        location_data = location.raw['address_components']
        return await form_location_data(location_data)
    except Exception as e:
        return "not found"


async def form_location_data(location_data):
    location = ""
    for i in range(len(location_data)):
        if location_data[i]['types'][0] == 'locality':
            location += f'{location_data[i]["long_name"]}, '
        elif location_data[i]['types'][0] == 'administrative_area_level_1':
            location += f'{location_data[i]["long_name"]}, '
        elif location_data[i]['types'][0] == 'country':
            location += f'{location_data[i]["long_name"]}'
    return location


async def add_age_ending(age):
    age = str(age)
    if age[1] == '1':
        return age + " рік"
    elif age[1] == '2' or age[1] == '3' or age[1] == '4':
        return age + " роки"
    else:
        return age + " років"


async def add_age_filter_ending(age):
    age = str(age)
    if age[1] == '1':
        return age + " року"
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


async def get_questionnaire(user_data, questionnaire_type):
    if questionnaire_type == 1:
        return f"🌆 {user_data['name']}, {await add_age_ending(user_data['age'])}, {user_data['city']}, {user_data['state']}, {user_data['country']}\n\nПро себе - {user_data['description']}\n\nІнстаграм - {await get_instagram_status(user_data['instagram'])}\nСтатус анкети - {await get_questionnaire_status(user_data['is_verified'])}"
    elif questionnaire_type == 0:
        return f"🌆 {user_data['name']}, {await add_age_ending(user_data['age'])}, {user_data['city']}, {user_data['state']}, {user_data['country']}\n\nПро себе - {user_data['description']}"
    elif questionnaire_type == 2:
        return (f"Цей користувач вами зацікавився!\n\n🌆 {user_data['name']}, {await add_age_ending(user_data['age'])}," + 
        f" {user_data['city']}, {user_data['state']}, {user_data['country']}\n\nПро себе - {user_data['description']}\n\n" + 
        f"Інстаграм - {await get_instagram_status(user_data['instagram'])}\nСтатус анкети - {await get_questionnaire_status(user_data['is_verified'])}")

def delete_old_message(func):
    async def inner_function(*args):
        try:
            callback_query = args[0]
            await callback_query.bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        except AttributeError:
            callback_query = args[0]
            await callback_query.bot.delete_message(callback_query.from_user.id, callback_query.message_id)
        except Exception as e:
            logging.warning(e)
            pass
        await func(*args)
    return inner_function


async def validate_instagram(instagram):
    if re.search("(?:(?:http|https):\/\/)?(?:www.)?(?:instagram.com|instagr.am|instagr.com)\/(\w+)", instagram):
        instagram = instagram.split("/")
        return instagram[3]
    elif instagram[0] == "@":
        return instagram[1:]
    return False


async def format_location_data(location):
    if location.count(",") == 1:
        location = location.split(", ")
        return [location[0], 'Київська область', location[1]]
    return location.split(", ")


async def format_filters_data(user_data):
    formated_data = []
    if user_data["target_gender"] == "male":
        formated_data.append("Чоловік")
    else:
        formated_data.append("Жінка")
    formated_data.append(user_data["target_age_min"])
    formated_data.append(user_data["target_age_max"])
    formated_data.append(user_data["target_city"])
    return formated_data


async def create_user_link(user_data):
    if user_data["username"] != None:
        return f'<a href="https://t.me/{user_data["username"]}">{user_data["name"]}</a>'
    else:
        return f'<a href="tg://user?id={user_data["telegram_id"]}">{user_data["name"]}</a>'
    