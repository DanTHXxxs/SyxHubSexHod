import discord
from discord.ext import commands
from discord.ui import Button, View

# โหลด TOKEN จากไฟล์ env.txt
def load_token_from_file(filename):
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith("DISCORD_TOKEN="):
                return line.strip().split("=", 1)[1]
    return None

TOKEN = load_token_from_file("env.txt")

if not TOKEN:
    raise ValueError("ไม่พบ TOKEN ในไฟล์ env.txt กรุณาเพิ่ม DISCORD_TOKEN=... ลงในไฟล์")

# ตั้งค่า Intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# สร้างบอท
bot = commands.Bot(command_prefix="!", intents=intents)

# ---------- ตั้งค่า ----------
WELCOME_CHANNEL_ID = 1370363838351937687
ROLE_CHANNEL_ID = 1370362731093299320
ROLE_ID = 1043503260016848978  # <-- จะกำหนดเมื่อใช้คำสั่ง !ดึงยศ
# ----------------------------

@bot.event
async def on_ready():
    print(f'บอทออนไลน์แล้ว: {bot.user}')

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title=f"ยินดีต้อนรับ {member.name}!",
            description="ขอให้สนุกกับการอยู่ในเซิร์ฟเวอร์นะครับ",
            color=discord.Color.green()
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1043516730477117440/1370397368389734502/anime-anime-ending.gif")
        await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title=f"{member.name} ได้ออกจากเซิร์ฟเวอร์...",
            description="ลาก่อน ขอให้โชคดีนะครับ",
            color=discord.Color.red()
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1043516730477117440/1370397391135703070/anime-ending-anime.gif")
        await channel.send(embed=embed)

@bot.command()
async def ดึงยศ(ctx, message_id: int):
    global ROLE_ID
    try:
        msg = await ctx.channel.fetch_message(message_id)
        if msg.role_mentions:
            role = msg.role_mentions[0]
            ROLE_ID = role.id
            await ctx.send(f"Role ID ที่ถูกแท็กคือ: {ROLE_ID}")
        else:
            await ctx.send("ไม่พบการแท็กยศในข้อความนี้")
    except:
        await ctx.send("ไม่พบข้อความหรือเกิดข้อผิดพลาด")

@bot.command()
async def สร้างปุ่ม(ctx):
    if ctx.channel.id != ROLE_CHANNEL_ID:
        await ctx.send("กรุณาใช้คำสั่งนี้ในช่องที่ถูกต้อง")
        return

    if ROLE_ID is None:
        await ctx.send("ยังไม่ได้ตั้งค่า ROLE_ID กรุณาใช้คำสั่ง !ดึงยศ ก่อน")
        return

    embed = discord.Embed(
        title="กดรับยศที่นี่!",
        description="หากคุณต้องการยศ คลิกที่ปุ่มด้านล่างเลยครับ",
        color=discord.Color.blue()
    )

    button = Button(label="รับยศ", style=discord.ButtonStyle.green)

    async def button_callback(interaction: discord.Interaction):
        role = interaction.guild.get_role(ROLE_ID)
        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("คุณได้รับยศเรียบร้อยแล้ว!", ephemeral=True)
        else:
            await interaction.response.send_message("ไม่พบยศที่กำหนด", ephemeral=True)

    button.callback = button_callback

    view = View()
    view.add_item(button)

    await ctx.send(embed=embed, view=view)

bot.run(TOKEN)