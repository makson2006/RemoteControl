import os
import subprocess
import pyautogui
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

API_TOKEN = "YOUR_TELEGRAM_TOKEN"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# In-memory database to store user devices (use a real database in production)
user_devices = {}

# Start command handler
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    register_button = KeyboardButton("Register Device")
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(register_button)
    await message.reply("Welcome! Please register your device to get started.", reply_markup=keyboard)

# Register device handler
@dp.message_handler(lambda message: message.text == "Register Device")
async def register_device(message: types.Message):
    user_id = message.from_user.id
    device_id = f"laptop_{user_id}"  # Example device ID
    user_devices[user_id] = device_id
    await message.reply(f"Your device '{device_id}' has been registered successfully!")
    await show_control_panel(message)

# Show control panel
async def show_control_panel(message: types.Message):
    control_buttons = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("Take Screenshot"),
        KeyboardButton("Open Terminal"),
        KeyboardButton("Shutdown")
    )
    await message.reply("Control your device:", reply_markup=control_buttons)

# Take a screenshot
@dp.message_handler(lambda message: message.text == "Take Screenshot")
async def take_screenshot(message: types.Message):
    try:
        screenshot_path = "screenshot.png"
        pyautogui.screenshot(screenshot_path)
        with open(screenshot_path, "rb") as photo:
            await bot.send_photo(chat_id=message.chat.id, photo=photo)
        os.remove(screenshot_path)
    except Exception as e:
        await message.reply(f"Failed to take screenshot: {e}")

# Open Terminal
@dp.message_handler(lambda message: message.text == "Open Terminal")
async def open_terminal(message: types.Message):
    try:
        # Open a new terminal window
        subprocess.Popen("cmd.exe", creationflags=subprocess.CREATE_NEW_CONSOLE)
        await message.reply("Terminal opened successfully.")
    except Exception as e:
        await message.reply(f"Failed to open terminal: {e}")

# Shutdown the computer
@dp.message_handler(lambda message: message.text == "Shutdown")
async def shutdown_computer(message: types.Message):
    try:
        subprocess.run("shutdown /s /t 1", shell=True)
        await message.reply("Shutting down the computer...")
    except Exception as e:
        await message.reply(f"Failed to shutdown the computer: {e}")

# Start the bot
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
