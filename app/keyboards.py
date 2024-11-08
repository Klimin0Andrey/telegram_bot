from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)

from app.database.requests import get_categories
from aiogram.utils.keyboard import InlineKeyboardBuilder

main = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Меню категорий', callback_data='menu_categories')],
                     [InlineKeyboardButton(text='Информация о компании', callback_data='company_info')],
                     [InlineKeyboardButton(text='Поддержка', callback_data='support')]])

back_btn = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Назад', callback_data='back')]])

catalog = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Разработка корпоративных приложений',
                                                                      callback_data='development_of_enterprise_applications')],
                                                [InlineKeyboardButton(text='Системы контроля за сотрудниками',
                                                                      callback_data='employee_monitoring_systems')],
                                                [InlineKeyboardButton(text='Системы лояльности и бонусов',
                                                                      callback_data='loyalty_and_bonus_systems')],
                                                [InlineKeyboardButton(text='Разработка сайтов',
                                                                      callback_data='website_development')],
                                                [InlineKeyboardButton(text='Приложения для карт и бонусов',
                                                                      callback_data='card_and_bonus_apps')],
                                                [InlineKeyboardButton(text='Другое', callback_data='other')],
                                                [InlineKeyboardButton(text='Назад', callback_data='back')]])

get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер', request_contact=True)]],
                                 resize_keyboard=True)
