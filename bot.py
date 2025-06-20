import os
import django
import logging
import requests
from io import BytesIO
import asyncio
from asgiref.sync import sync_to_async
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram import InputMediaPhoto

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portal_backend.settings")
django.setup()
from core.models import GalleryImage, AlumniReview

logging.basicConfig(level=logging.INFO)

TOKEN = '7331193855:AAEt3ick0AKs5ou5u3Z9GySUPfLAtuWYvs4'
ADMIN_CHAT_ID = 729995094

if not asyncio.get_event_loop().is_running():
    asyncio.set_event_loop(asyncio.new_event_loop())

@sync_to_async
def get_review_by_id(review_id):
    return AlumniReview.objects.get(pk=review_id)

@sync_to_async
def save_review(review):
    review.save()

@sync_to_async
def delete_review(review):
    review.delete()

@sync_to_async
def get_image_by_id(image_id):
    return GalleryImage.objects.get(pk=image_id)

@sync_to_async
def save_image(image):
    image.save()

@sync_to_async
def delete_image(image):
    image.delete()

async def send_new_review(review):
    keyboard = [
        [
            InlineKeyboardButton("✅ Одобрить", callback_data=f"approve_{review.id}"),
            InlineKeyboardButton("❌ Отклонить", callback_data=f"reject_{review.id}")
        ]
    ]
    text = f"🆕 Новый отзыв от {review.name} ({review.graduation_year}):\n\n{review.text}"
    markup = InlineKeyboardMarkup(keyboard)
    if review.photo:
        image_url = f"http://127.0.0.1:8000{review.photo.url}"
        logging.info(f"Отправка фотографии по URL: {image_url}")
        try:
            await app.bot.send_photo(
                chat_id=ADMIN_CHAT_ID,
                photo=image_url,
                caption=text,
                reply_markup=markup
            )
        except Exception as e:
            logging.error(f"Ошибка при отправке фотографии: {e}")
            await app.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=f"{text}\n\n(Фото не удалось отправить)",
                reply_markup=markup
            )
    else:
        await app.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=text,
            reply_markup=markup
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    logging.info(f"DEBUG: Получены данные: {data}")
    try:
        if data.startswith("approve_") or data.startswith("reject_"):
            prefix, review_id_raw = data.split("_", 1)
            try:
                review_id = int(review_id_raw)
            except ValueError:
                msg = "❌ Ошибка: ID должен быть числом."
                if query.message.text:
                    await query.edit_message_text(msg)
                else:
                    await query.answer(msg, show_alert=True)
                return
            if prefix == "approve":
                review = await get_review_by_id(review_id)
                review.is_approved = True
                await save_review(review)
                result_text = f"✅ Отзыв {review_id} одобрен."
            else:
                review = await get_review_by_id(review_id)
                await delete_review(review)
                result_text = f"❌ Отзыв {review_id} отклонён."
            if query.message.text:
                await query.edit_message_text(result_text)
            else:
                await query.answer(result_text, show_alert=True)
        else:
            await query.answer("Неподдерживаемое действие.", show_alert=True)
    except Exception as e:
        logging.error(f"❗ Ошибка в button_handler: {e}")
        await query.answer("Произошла внутренняя ошибка.", show_alert=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Ваш chat_id: {chat_id}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

if __name__ == "__main__":
    print("Бот запущен...")
    app.run_polling()

async def send_gallery_image(media):
    keyboard = [
        [
            InlineKeyboardButton("✅ Одобрить", callback_data=f"approve_img_{media.id}"),
            InlineKeyboardButton("❌ Отклонить", callback_data=f"reject_img_{media.id}")
        ]
    ]
    caption = f"🖼 Новое изображение в галерею\nЗаголовок: {media.title or '(без названия)'}"

    image_url = f"http://127.0.0.1:8000{media.file.url}"

    try:
        response = requests.get(image_url)
        response.raise_for_status()
        image_bytes = BytesIO(response.content)

        await app.bot.send_photo(
            chat_id=ADMIN_CHAT_ID,
            photo=image_bytes,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        print(f"Ошибка при отправке изображения: {e}")