import os
import django
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram import InputMediaPhoto


# Django setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portal_backend.settings")
django.setup()
from core.models import GalleryImage, AlumniReview

from core.models import AlumniReview

# Логирование
logging.basicConfig(level=logging.INFO)

TOKEN = '7331193855:AAEt3ick0AKs5ou5u3Z9GySUPfLAtuWYvs4'
ADMIN_CHAT_ID = 729995094
# Отправка нового отзыва админу
async def send_new_review(review):
    keyboard = [
        [
            InlineKeyboardButton("✅ Одобрить", callback_data=f"approve_{review.id}"),
            InlineKeyboardButton("❌ Отклонить", callback_data=f"reject_{review.id}")
        ]
    ]
    text = f"🆕 Новый отзыв от {review.name} ({review.graduation_year}):\n\n{review.text}"
    markup = InlineKeyboardMarkup(keyboard)
    await app.bot.send_message(chat_id=ADMIN_CHAT_ID, text=text, reply_markup=markup)

# Обработка кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action, review_id = query.data.split("_")
    review = AlumniReview.objects.get(id=review_id)

    if action == "approve":
        review.is_approved = True
        review.save()
        await query.edit_message_text("✅ Отзыв одобрен.")
    elif action == "reject":
        review.delete()
        await query.edit_message_text("❌ Отзыв отклонён и удалён.")

# Команда для теста
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Ваш chat_id: {chat_id}")

# Запуск бота
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

if __name__ == "__main__":
    print("Бот запущен...")
    app.run_polling()

async def send_gallery_image(gallery_image: GalleryImage):
    keyboard = [
        [
            InlineKeyboardButton("✅ Одобрить", callback_data=f"approve_img_{gallery_image.id}"),
            InlineKeyboardButton("❌ Отклонить", callback_data=f"reject_img_{gallery_image.id}")
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    caption = f"🖼 Новое изображение в галерею\nЗаголовок: {gallery_image.title or '(без названия)'}"

    image_path = f"{os.environ.get('BASE_URL')}{gallery_image.image.url}"  # BASE_URL = http://127.0.0.1:8000

    await app.bot.send_photo(
        chat_id=ADMIN_CHAT_ID,
        photo=image_path,
        caption=caption,
        reply_markup=markup
    )