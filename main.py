import os
import discord
import asyncio
from discord.ext import commands

from myserver import server_on

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="-", intents=intents)

# กำหนดเวลา 2 ชั่วโมงครึ่ง (9000 วินาที)
TIME_INTERVAL = 9000  # 2 ชั่วโมงครึ่ง
notification_active = False
notification_task = None  # ตัวแปรสำหรับจัดเก็บ task ของ asyncio

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# ฟังก์ชันสำหรับแจ้งเตือน
async def notify(channel):
    while notification_active:
        await channel.send("ถึงเวลาเข้าเวรแล้ว!..กรุณาเข้าเวรด้วย")
        await asyncio.sleep(TIME_INTERVAL)

# คำสั่งเริ่มการแจ้งเตือน
@bot.command()
async def start(ctx):
    global notification_active, notification_task
    if not notification_active:
        notification_active = True
        channel = ctx.channel
        notification_task = bot.loop.create_task(notify(channel))
        await ctx.send("ระบบแจ้งเตือนเริ่มต้นแล้ว!")
    else:
        await ctx.send("ระบบแจ้งเตือนทำงานอยู่แล้ว!")

# คำสั่งหยุดการแจ้งเตือน
@bot.command()
async def stop(ctx):
    global notification_active, notification_task
    if notification_active:
        notification_active = False
        if notification_task is not None:
            notification_task.cancel()  # หยุด Task ที่กำลังทำงานอยู่
        await ctx.send("ระบบแจ้งเตือนถูกหยุดแล้ว!")
    else:
        await ctx.send("ไม่มีการแจ้งเตือนที่ทำงานอยู่ในขณะนี้!")

# รันบอท
bot.run(os.getenv('TOKEN'))
