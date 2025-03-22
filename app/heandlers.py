import re
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message
from utils.external_API import create_counter
from config import WIN1_TOKEN, POKER_DOM_TOKEN, MEL_BET_TOKEN, KURV4_TOKEN
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import app.keyboards as kb

router = Router()


class Reg(StatesGroup):
    WIN1 = State()
    POKER_DOM = State()
    MEL_BET = State()
    KURV4 = State()


STATE_TO_TOKEN = {
    "Reg:WIN1": WIN1_TOKEN,
    "Reg:POKER_DOM": POKER_DOM_TOKEN,
    "Reg:MEL_BET": MEL_BET_TOKEN,
    "Reg:KURV4": KURV4_TOKEN
}


@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет, выбери аккаунт!")


domain_pattern = re.compile(r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}')


@router.message(Command("1_win"))
async def cmd_win1(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, отправьте txt файл с именами для 1_win.\n\n❌Отмена - для выбора другого акк!",
                         reply_markup=kb.cancel)
    await state.set_state(Reg.WIN1)


@router.message(Command("poker_dom"))
async def cmd_fonbet(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, отправьте txt файл с именами для Poker_dom.\n\n❌Отмена - для выбора другого акк!",
                         reply_markup=kb.cancel)
    await state.set_state(Reg.POKER_DOM)


@router.message(Command("mel_bet"))
async def cmd_joycasino(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, отправьте txt файл с именами для Mel_bet.\n\n❌Отмена - для выбора другого акк!",
                         reply_markup=kb.cancel)
    await state.set_state(Reg.MEL_BET)


@router.message(Command("KURV4"))
async def cmd_xbet1(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, отправьте txt файл с именами.\n\n❌Отмена - для выбора другого акк!",
                         reply_markup=kb.cancel)
    await state.set_state(Reg.KURV4)


@router.message(StateFilter(Reg.WIN1, Reg.POKER_DOM, Reg.MEL_BET, Reg.KURV4), F.text == "❌Отмена")
async def cancel_fsm_state(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌Отменено!")


@router.message(StateFilter(Reg.WIN1, Reg.POKER_DOM, Reg.MEL_BET, Reg.KURV4), F.document)
async def handle_document(message: Message, state: FSMContext):
    # Получаем текущее состояние
    current_state = await state.get_state()
    print(current_state)

    # Получаем токен для текущего состояния
    API_TOKEN = STATE_TO_TOKEN.get(current_state)

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
                first_counter_id = await create_counter(API_TOKEN, domain, "Сайт-1")
                second_counter_id = await create_counter(API_TOKEN, domain, "PF-1")
                if first_counter_id is None or second_counter_id is None:
                    await message.answer("Already exists!")

                await message.answer(f"Аккаунт - {current_state.split(":")[1]}\n"
                                     f"{domain}\n\n"
                                     f"✅Сайт-1 ID: {first_counter_id}\n"
                                     f"✅PF-1 ID: {second_counter_id}")


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
