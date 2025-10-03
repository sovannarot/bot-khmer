import os
import re
import matplotlib.pyplot as plt
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Function to render LaTeX to PNG
def render_latex_to_png(latex_code, filename="latex.png"):
    plt.figure(figsize=(2, 2))
    plt.text(0.5, 0.5, f"${latex_code}$", fontsize=20, ha='center', va='center')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.2)
    plt.close()

# Handler for messages
async def handle_tex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Only respond to text messages in groups
    if not update.message or not update.message.text:
        return

    # Look for \tex <latex code>
    match = re.search(r'\\tex\s+(.+)', update.message.text, re.DOTALL)
    if match:
        latex_code = match.group(1).strip()
        filename = f"latex_{update.message.message_id}.png"
        render_latex_to_png(latex_code, filename)

        # Send the PNG to the group
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=open(filename, 'rb')
        )

        # Remove the file after sending
        os.remove(filename)

if __name__ == "__main__":
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        raise Exception("BOT_TOKEN environment variable not set")

    app = ApplicationBuilder().token(TOKEN).build()

    # Handle text messages in groups
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_tex))

    app.run_polling()
