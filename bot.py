import json
import time

from aiogram import Bot, Dispatcher, executor, types
from settings import BOT_TOKEN, WAITING_TIME
from services import get_operations

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await bot.send_message(message.chat.id, 'Одну секунду...')
    while True:
        get_operations()
        with open('operations.json', 'r', encoding='utf-8') as f:
            all_operations = json.load(f)
            for a, b in all_operations.items():

                if b['name'] == 'Покупка':
                    icon = '✅'
                elif b['name'] == 'Комиссия':
                    icon = '⚠'
                else:
                    icon = '❌'

                if b['is_new']:
                    text = f"{icon} *{b['name']}* `{b['ticket']}` ({b['organization']}) \n\n " \
                           f"Цена: {b['price']} \n " \
                           f"Количество: {b['amount']} \n " \
                           f"Сумма: {b['sum']} \n\n " \
                           f"Автор: {b['author']}"

                    await bot.send_message(message.chat.id, text, parse_mode="Markdown")
                    b['is_new'] = False

        with open('operations.json', 'w', encoding='utf-8') as f:
            json.dump(all_operations, f, indent=4, ensure_ascii=False)
        time.sleep(WAITING_TIME)


@dp.message_handler(commands=['test'])
async def reply_message(message: types.Message):
    await message.reply('test')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
