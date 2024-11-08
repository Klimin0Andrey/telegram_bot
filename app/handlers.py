from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import app.keyboards as kb

router = Router()


class Support(StatesGroup):
    request_support = State()


class Request(StatesGroup):
    name = State()
    number = State()
    category = State()


async def hello():
    return (
        "Приветствуем вас! Мы рады помочь вам оформить заявку.\n"
        "Пожалуйста, выберите действие, которое вас интересует из списка ниже."
    )


async def info_about_company():
    return (
        "Наша компания занимается разработкой корпоративных приложений, "
        "систем контроля сотрудников, программ лояльности и бонусов, "
        "а также сайтов и приложений для карт лояльности. Наши решения "
        "помогают автоматизировать бизнес-процессы, улучшать управление "
        "и повышать клиентскую активность. Мы создаем современные и "
        "эффективные цифровые инструменты для роста и развития вашего бизнеса.\n\n"
        "Наши контакты:\n"
        "Телефон: +7 495 682-26-20\n"
        "Email: Info@ng-soft.ru\n"
        "Сайт: Разработка программного обеспечения - NG-Soft, Москва."
    )


async def support_message():
    return 'Опишите ваш вопрос, и мы передадим его в техническую поддержку. Вам ответят в ближайшее время.'


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(await hello(), reply_markup=kb.main)


@router.message(Command('about'))
async def cmd_about(message: Message):
    await message.answer(await info_about_company(), reply_markup=kb.back_btn)


@router.callback_query(F.data == 'back')
async def back_to_main_menu(callback: CallbackQuery):
    await callback.answer('Вы вернулись в главное меню')
    await callback.message.edit_text(await hello(), reply_markup=kb.main)


@router.callback_query(F.data == 'company_info')
async def company_info(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию информация о компании.')
    await callback.message.edit_text(await info_about_company(), reply_markup=kb.back_btn)


#меню категорий
@router.callback_query(F.data == 'menu_categories')
async def catalog(callback: CallbackQuery):
    await callback.answer('Вы выбрали меню категорий')
    await callback.message.edit_text(
        'Мы предлагаем следующие услуги: [описание услуг]. Выберите нужную категорию, чтобы продолжить оформление заявки.',
        reply_markup=kb.catalog
    )


CATEGORY_MESSAGES = {
    'development_of_enterprise_applications': 'Корпоративные приложения',
    'employee_monitoring_systems': 'Системы контроля за сотрудниками',
    'loyalty_and_bonus_systems': 'Система лояльности и бонусов',
    'website_development': 'Разработка сайтов',
    'card_and_bonus_apps': 'Приложения для карт и бонусов',
    'other': 'Другое.'
}


@router.callback_query(F.data.in_(CATEGORY_MESSAGES.keys()))
async def handle_category(callback: CallbackQuery, state: FSMContext):
    await state.update_data(category_id=callback.data)
    await callback.message.answer(
        f'Вы выбрали категорию "{CATEGORY_MESSAGES[callback.data]}". Продолжим оформление заявки.')
    await callback.message.answer('Для оформления заявки попросим вас указать имя и номер телефона.')
    await state.set_state(Request.name)
    await callback.message.answer('Введите ваше имя')


@router.message(Request.name)
async def request_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Request.number)
    await message.answer('Отправьте ваш номер телефона', reply_markup=kb.get_number)


@router.message(Request.number)
async def request_number(message: Message, state: FSMContext):
    if message.contact:
        await state.update_data(number=message.contact.phone_number)
    else:
        await state.update_data(number=message.text)

    data = await state.get_data()
    category_message = CATEGORY_MESSAGES.get(data.get("category_id"), "Категория не выбрана.")

    await message.answer(
        f'Ваша заявка готова. Пожалуйста, проверьте информацию:\nКатегория: {category_message}\nИмя: {data["name"]}\nКонтакты: {data["number"]}'
        , reply_markup=kb.back_btn)
    await state.clear()


@router.message(Command('support'))
async def support_one(message: Message, state: FSMContext):
    await state.set_state(Support.request_support)
    await message.answer(
        'Опишите ваш вопрос, и мы передадим его в техническую поддержку. Вам ответят в ближайшее время.')


@router.callback_query(F.data == 'support')
async def support_button(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Support.request_support)
    await callback.message.answer(
        'Опишите ваш вопрос, и мы передадим его в техническую поддержку. Вам ответят в ближайшее время.'
    )
    await callback.answer()


@router.message(Support.request_support)
async def support_two(message: Message, state: FSMContext):
    await state.update_data(request_support=message.text)
    support_data = await state.get_data()
    await message.answer(f'Ваш запрос:\n{support_data["request_support"]}')
    await message.answer('Ваш запрос был отправлен в техническую поддержку. Мы свяжемся с вами в ближайшее время.')
    await state.clear()
    await message.answer(await hello(), reply_markup=kb.main)
