"""Main module runs telegram bot, receives inputs and displays answer"""

from aiogram import Bot, types, Dispatcher, executor
import json

from validation import validate
from tokens import bot_token
from connection import connection_to_db, aggregate_data
import tokens


bot = Bot(token=bot_token)
dispatcher = Dispatcher(bot)


@dispatcher.message_handler(commands=['start'])
async def start_command(message: types.Message):
    """Function generates welcome message at the start command"""
    await message.reply('Добрый день! Введите сходные данные в формате JSON')


@dispatcher.message_handler()
async def get_data(message: types.Message):
    """Function receives input data and returns tre aggregated result"""
    try:
        validated_data = validate(input_string=message.text)
        data_to_display = aggregate_data(
            dt_from=validated_data['dt_from'],
            dt_upto=validated_data['dt_upto'],
            group_type=validated_data['group_type'],
            coll=connection_to_db(
                token=tokens.mongoDB_token,
                password=tokens.mongoDB_password
            )
        )
        await message.reply(json.dumps(data_to_display))
    except ValueError:
        await message.reply('Проверьте корректность ввода')


if __name__ == '__main__':
    executor.start_polling(dispatcher)
