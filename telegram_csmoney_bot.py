from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from main import collect_data
import json
import time

bot = Bot(token='---', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# базавые настройки
discount = 0.15
min_price = 0
max_price = 100000000


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Информация', 'Настройки', 'Начать поиск']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Выберите категорию', reply_markup=keyboard)


@dp.message_handler(Text(equals='Назад'))
async def start(message: types.Message):
    start_buttons = ['Информация', 'Настройки', 'Начать поиск']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Выберите категорию', reply_markup=keyboard)


@dp.message_handler(Text(equals='Начать поиск'))
async def start(message: types.Message):
    gun_buttons = [
        'Ножи',
        'Штурмовые винтовки',
        'AWP',
        'Пистолеты',
        'Пистолеты-пулемёты',
        'Дробовики',
        'Пулемёты',
        'Назад'
    ]

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*gun_buttons)

    await message.answer('Выберите категорию', reply_markup=keyboard)


@dp.message_handler(Text(equals='Информация'))
async def info(message: types.Message):
    await message.answer('С целью упрощения поиска позиций со скидками на сайте "csmoney", данный бот был создан.'
                         ' Рекомендуется начать с настройки фильтров поиска.'
                         'Важно заметить, '
                         'что использование слишком широкого диапазона поиска может привести к возникновению ошибок.')


@dp.message_handler(Text(equals='Настройки'))
async def info(message: types.Message):
    await message.answer(f'Настойки сейчас:\n'
                         f'Минимальная цена: {min_price}$\n'
                         f'Максимальная цена: {max_price}$\n'
                         f'Размер скидки: {discount * 100}%')

    settings_buttons = ['Скидка', 'Цена', 'Назад']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*settings_buttons)

    await message.answer('Выберите, что хотите изменить.', reply_markup=keyboard)



@dp.message_handler(Text(equals='Цена'))
async def info(message: types.Message):
    discount_buttons = ['min', 'max', 'Назад']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*discount_buttons)

    await message.answer('Выберите, min и max.', reply_markup=keyboard)


@dp.message_handler(Text(equals='min'))
async def info(message: types.Message):
    await message.answer("Введите минимальную цену(в $): ")

    @dp.message_handler(content_types=["text"])
    async def minimum(message: types.Message):
        global min_price
        min_price = int(message.text)
        await message.answer(f'Минимальная цена: {min_price}$')


@dp.message_handler(Text(equals='max'))
async def info(message: types.Message):
    await message.answer("Введите максимальную цену(в $): ")

    @dp.message_handler(content_types=["text"])
    async def minimum(message: types.Message):
        global max_price
        max_price = int(message.text)
        await message.answer(f'Максимальная цена: {max_price}$')


@dp.message_handler(Text(equals='Скидка'))
async def discounts(message: types.Message):
    discount_buttons = ['15%', '20%', '25%', '30%', 'Назад']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*discount_buttons)

    await message.answer('Выберите, скидку.', reply_markup=keyboard)


@dp.message_handler(Text(equals='15%'))
async def discount_15(message: types.Message):
    global discount
    discount = 0.15
    await message.answer('Скидка 15% выбрана')


@dp.message_handler(Text(equals='20%'))
async def discount_20(message: types.Message):
    global discount
    discount = 0.20
    await message.answer('Скидка 20% выбрана')


@dp.message_handler(Text(equals='25%'))
async def discount_25(message: types.Message):
    global discount
    discount = 0.25
    await message.answer('Скидка 25% выбрана')


@dp.message_handler(Text(equals='30%'))
async def discount_25(message: types.Message):
    global discount
    discount = 0.30
    await message.answer('Скидка 30% выбрана')

@dp.message_handler(Text(equals='Ножи'))
async def get_knife(message: types.Message):
    await message.answer('Собираем информацию...')

    collect_data(gun_type=2, discount=discount, max_price=max_price, min_price=min_price)

    with open('result.json', 'r', encoding='utf8') as file:
        data = json.load(file)

    for index, item in enumerate(data):
        card = f'{hlink(item.get("full_name"), item.get("3d"))}\n' \
            f'{hbold("Скидка: ")}{item.get("discount")}%\n' \
            f'{hbold("Цена: ")}{item.get("price")}'

        if index % 10 == 0:
            time.sleep(4)

        await message.answer(card)


@dp.message_handler(Text(equals='Штурмовые винтовки'))
async def get_big_guns(message: types.Message):
    await message.answer('Собираем информацию...')

    collect_data(gun_type=3, discount=discount, max_price=max_price, min_price=min_price)

    with open('result.json', 'r', encoding='utf8') as file:
        data = json.load(file)

    for index, item in enumerate(data):
        card = f'{hlink(item.get("full_name"), item.get("3d"))}\n' \
            f'{hbold("Скидка: ")}{item.get("discount")}%\n' \
            f'{hbold("Цена: ")}{item.get("price")}'

        if index % 10 == 0:
            time.sleep(4)

        await message.answer(card)


@dp.message_handler(Text(equals='AWP'))
async def get_awp(message: types.Message):
    await message.answer('Собираем информацию...')

    collect_data(gun_type=4, discount=discount, max_price=max_price, min_price=min_price)

    with open('result.json', 'r', encoding='utf8') as file:
        data = json.load(file)

    for index, item in enumerate(data):
        card = f'{hlink(item.get("full_name"), item.get("3d"))}\n' \
            f'{hbold("Скидка: ")}{item.get("discount")}%\n' \
            f'{hbold("Цена: ")}{item.get("price")}'

        if index % 10 == 0:
            time.sleep(4)

        await message.answer(card)


@dp.message_handler(Text(equals='Пистолеты'))
async def get_pistol(message: types.Message):
    await message.answer('Собираем информацию...')

    collect_data(gun_type=5, discount=discount, max_price=max_price, min_price=min_price)

    with open('result.json', 'r', encoding='utf8') as file:
        data = json.load(file)

    for index, item in enumerate(data):
        card = f'{hlink(item.get("full_name"), item.get("3d"))}\n' \
            f'{hbold("Скидка: ")}{item.get("discount")}%\n' \
            f'{hbold("Цена: ")}{item.get("price")}'

        if index % 10 == 0:
            time.sleep(4)

        await message.answer(card)


@dp.message_handler(Text(equals='Пистолеты-пулемёты'))
async def get_pistol_pistol(message: types.Message):
    await message.answer('Собираем информацию...')

    collect_data(gun_type=6, discount=discount, max_price=max_price, min_price=min_price)

    with open('result.json', 'r', encoding='utf8') as file:
        data = json.load(file)

    for index, item in enumerate(data):
        card = f'{hlink(item.get("full_name"), item.get("3d"))}\n' \
            f'{hbold("Скидка: ")}{item.get("discount")}%\n' \
            f'{hbold("Цена: ")}{item.get("price")}'

        if index % 10 == 0:
            time.sleep(4)

        await message.answer(card)


@dp.message_handler(Text(equals='Дробовики'))
async def get_drobovic(message: types.Message):
    await message.answer('Собираем информацию...')

    collect_data(gun_type=7, discount=discount, max_price=max_price, min_price=min_price)

    with open('result.json', 'r', encoding='utf8') as file:
        data = json.load(file)

    for index, item in enumerate(data):
        card = f'{hlink(item.get("full_name"), item.get("3d"))}\n' \
            f'{hbold("Скидка: ")}{item.get("discount")}%\n' \
            f'{hbold("Цена: ")}{item.get("price")}'

        if index % 10 == 0:
            time.sleep(4)

        await message.answer(card)


@dp.message_handler(Text(equals='Пулемёты'))
async def get_minigun(message: types.Message):
    await message.answer('Собираем информацию...')

    collect_data(gun_type=8, discount=discount, max_price=max_price, min_price=min_price)

    with open('result.json', 'r', encoding='utf8') as file:
        data = json.load(file)

    for index, item in enumerate(data):
        card = f'{hlink(item.get("full_name"), item.get("3d"))}\n' \
            f'{hbold("Скидка: ")}{item.get("discount")}%\n' \
            f'{hbold("Цена: ")}{item.get("price")}'

        if index % 10 == 0:
            time.sleep(4)

        await message.answer(card)


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()