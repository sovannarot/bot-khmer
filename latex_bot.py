import os
import re
import matplotlib.pyplot as plt
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Function to render LaTeX to PNG
def render_latex_to_png(latex_code, filename):
    plt.figure(figsize=(2, 2))
    plt.text(0.5, 0.5, f"${latex_code}$", fontsize=20, ha='center', va='center')
    plt.axis('off')
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.1)
    plt.close()

async def handle_tex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    match = re.search(r'\\tex\s+(.+)', update.message.text)
    if match:
        latex_code = match.group(1)
        filename = 'latex.png'
        render_latex_to_png(latex_code, filename)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(filename, 'rb'))
        os.remove(filename)

if __name__ == '__main__':
    TOKEN = os.getenv('BOT_TOKEN')
    if not TOKEN:
        raise Exception("BOT_TOKEN environment variable not set")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_tex))
    app.run_polling()