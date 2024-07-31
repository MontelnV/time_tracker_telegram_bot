from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

main_keyboard = [
    [InlineKeyboardButton(text="Я пришел на работу", callback_data="start_working")]
]
main_keyboard = InlineKeyboardMarkup(inline_keyboard=main_keyboard)

main_keyboard_2 = [
    [InlineKeyboardButton(text="Я закончил работу", callback_data="end_working")],
    [InlineKeyboardButton(text="Ушел на перерыв", callback_data="go_to_break")]
]
main_keyboard_2 = InlineKeyboardMarkup(inline_keyboard=main_keyboard_2)

keyboard_allow = [
    [InlineKeyboardButton(text="Календарь", callback_data="calendar")]
]
keyboard_allow = InlineKeyboardMarkup(inline_keyboard=keyboard_allow)

new_session = [
    [InlineKeyboardButton(text="Начать новую смену", callback_data="new_session")]
]
new_session = InlineKeyboardMarkup(inline_keyboard=new_session)

success_keyboard = [
    [InlineKeyboardButton(text="Да", callback_data="success")],
    [InlineKeyboardButton(text="Нет", callback_data="fail")]
]
success_keyboard = InlineKeyboardMarkup(inline_keyboard=success_keyboard)