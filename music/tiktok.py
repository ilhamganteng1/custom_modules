from pyrogram import Client, filters, enums
from pyrogram.types import Message
from utils.misc import modules_help, prefix
from utils.scripts import interact_with, interact_with_to_delete, format_exc


@Client.on_message(filters.command("tt", prefix) & filters.me)
async def tiktok(client: Client, message: Message):
    if len(message.command) > 1:
        link = message.command[1]
    elif message.reply_to_message:
        link = message.reply_to_message.text
    else:
        await message.edit(
            "<b>Link isn't provided</b>", parse_mode=enums.ParseMode.HTML
        )
        return

    try:
        await message.edit("<b>Downloading...</b>", parse_mode=enums.ParseMode.HTML)
        await client.unblock_user("@downloader_tiktok_bot")
        msg = await interact_with(
            await client.send_message("@downloader_tiktok_bot", link)
        )
        await client.send_video(
            message.chat.id, msg.video.file_id, caption=f"<b>Link: {link}</b>"
        )
    except Exception as e:
        await message.edit(format_exc(e), parse_mode=enums.ParseMode.HTML)
    else:
        await message.delete()
        await client.delete_messages("@downloader_tiktok_bot", interact_with_to_delete)
        interact_with_to_delete.clear()


modules_help["tiktok"] = {
    "tt [link|reply]*": "download video from tiktok",
}
