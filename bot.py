import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import asyncio

TOKEN = "7881028995:AAGMKA5a3tDWcLRAW8VgLmOscjswCow_rB4"

# Sherlock Username Lookup (All Sites, Real-Time Streaming)
async def check_sherlock(update: Update, context: CallbackContext) -> None:
    username = update.message.text.strip()

    if not username:
        await update.message.reply_text("Please provide a username.")
        return

    await update.message.reply_text(f"🔍 Searching for username: {username} across all sites...")

    # Run Sherlock as a subprocess and stream results
    process = await asyncio.create_subprocess_exec(
        "sherlock", username, "--print-found", "--timeout", "10",
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    # Read and send each line of output in real-time
    results_found = False
    while True:
        line = await process.stdout.readline()
        if not line:
            break  # No more output
        output = line.decode().strip()
        if "http" in output:  # Only send URLs
            results_found = True
            await update.message.reply_text(f"🕵️ Found: {output}")

    await process.wait()

    if not results_found:
        await update.message.reply_text("❌ No results found using Sherlock.")

# Start command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("OSINT Bot is live! Send a username to check its presence across all sites.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_sherlock))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
