import re
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from utils.external_API import create_counter
from config import API_TOKEN

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет")


domain_pattern = re.compile(r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}')


@router.message(F.document)
async def handle_document(message: Message):
    document = message.document

    # Проверяем, что файл является текстовым
    if not document.file_name.endswith('.txt'):
        await message.answer("Пожалуйста, отправьте файл с расширением .txt")
        return

    # Получаем file_id документа
    file_id = document.file_id
    from run import bot
    try:
        # Получаем информацию о файле
        file_info = await bot.get_file(file_id)

        # Скачиваем файл в память
        file_content = await bot.download_file(file_info.file_path)
    finally:
        await bot.session.close()
    try:
        # Декодируем содержимое файла (предполагаем UTF-8)
        content = file_content.read().decode('utf-8')

        # Ищем доменные имена в файле
        domains = domain_pattern.findall(content)

        if domains:
            unique_domains = list(set(domains))  # Убираем дубликаты
            for domain in unique_domains:
                first_counter_id = await create_counter(API_TOKEN, domain, 1)
                second_counter_id = await create_counter(API_TOKEN, domain, 2)
                if first_counter_id is None or second_counter_id is None:
                    await message.answer("Got something wrong!")

                await message.answer(f"{domain}\n\n"
                                     f"First Counter ID: {first_counter_id}\n"
                                     f"Second Counter ID: {second_counter_id}")

    except UnicodeDecodeError:
        await message.answer(
            "Файл содержит недопустимую кодировку. Пожалуйста, отправьте текстовый файл в формате UTF-8.")

# @router.message()
# async def check_domain(message: Message):
#     if domain_pattern.match(message.text):
#         first_counter_id = await create_counter(API_TOKEN, message.text, 1)
#         second_counter_id = await create_counter(API_TOKEN, message.text, 2)
#         if first_counter_id is None or second_counter_id is None:
#             await message.answer("Got something wrong!")
#
#         await message.answer(f"Domain name: {message.text}\n"
#                              f"Created First Counter ID: {first_counter_id}\n"
#                              f"Created Second Counter ID: {second_counter_id}")
#     else:
#         await message.reply("Это не доменное имя. Пожалуйста, введите корректное доменное имя.")
