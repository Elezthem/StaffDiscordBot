import disnake
from disnake.ext import commands

intents = disnake.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

class RecruitementModal1(disnake.ui.Modal):
    def __init__(self, arg):
        self.arg = arg  # arg - это аргумент, который передается в конструкторе класса RecruitementSelect
        components = [
            disnake.ui.TextInput(label="Ваше имя и возраст", placeholder="Пример: Артем, 19", custom_id="name"),
            disnake.ui.TextInput(label="Ваш часовой пояс", placeholder="Пример: МСК", custom_id="time"),
            disnake.ui.TextInput(label="Наличие опыта в стаффе", placeholder="Если да, то сколько?", custom_id="staff"),
            disnake.ui.TextInput(label="Расскажи о себе", placeholder="Чем больше - тем лучше!", custom_id="osebe")
        ]
        if self.arg == "helper":
            title = "Набор на должность Helper"
    
        super().__init__(title=title, components=components, custom_id="RecruitementModal1")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        name = interaction.text_values["name"]
        time = interaction.text_values["time"]
        staff = interaction.text_values["staff"]
        osebe = interaction.text_values["osebe"]
        embed = disnake.Embed(color=0xfffff1, title="<a:yes:1068525712291663925> Заявка отправлена!\n")
        embed.description = f"> {interaction.author.mention}, Благодарим вас за **заявку**!\n" \
                            f"> Если вы нам **подходите**, администрация **свяжется** с вами в ближайшее время.\n\n" 
        embed.set_thumbnail(url=interaction.author.display_avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        channel = interaction.guild.get_channel(1075833746160357416)  #  ID канала куда будут отправляться заявки
        await channel.send(f"**Новая заявка на** {self.arg} **от** {name} **|** {interaction.author.mention}\n\n**Время от мск -** {time} \n\n**Инфо о стафф -** {staff}\n\n**O себе -** {osebe}")


class RecruitementSelect(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(emoji="<a:zveKa:1081632315865833502> ",label="Helper", value="helper", description="Следящие за чатами.")
        ]
        super().__init__(
            placeholder="Выбери желаемую роль", options=options, min_values=0, max_values=1, custom_id="recruitement"
        )

    async def callback(self, interaction: disnake.MessageInteraction, timeout=None):
        if not interaction.values:
            await interaction.response.defer()
        else:
            await interaction.response.send_modal(RecruitementModal1(interaction.values[0]))


class Recruitement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistents_views_added = False

    @commands.command()
    async def recruit(self, ctx, timeout=None):
        view = disnake.ui.View()
        view.add_item(RecruitementSelect())
        helper = ctx.guild.get_role(1067827586534744115)
        embed = disnake.Embed(color=disnake.Colour.dark_purple())
        embed.set_author(name="Набор в команду нашего сервера!\n")
        embed.description = f"**<a:pin:1081632329535066112> Что от тебя требуется:**\n\n" \
                            "Знание **правил** сервера.\n" \
                            "Полных `13` лет.\n" \
                            "Стрессоустойчивость.\n" \
                            "**Возможность** уделять серверу от 2-х часов в день.\n\n" \
                            "**<a:w_coriexplode:1081626834032144454> Что тебя ждёт:**\n\n" \
                            "Возможность получить **ценный опыт** и **карьерный** рост.\n\n" \
                            "**Еженедельная** зарплата в виде серверной валюты, **Реклама ваших серверов**, Розыгрыши **nitro**.\n" \
                            "<a:moon:1081632358492536862> **Ветки:**\n\n" \
                            f"{helper.mention} — Ответственные за **модерацию текстовых каналов.\n\n"
        await ctx.send(embed=embed, view=view)
    

    @commands.Cog.listener()
    async def on_connect(self):
        if self.persistents_views_added:
            return

        view = disnake.ui.View(timeout=None)
        view.add_item(RecruitementSelect())
        self.bot.add_view(view,
                          message_id=(1109190479825875064))  # Вставить ID сообщения, которое отправится после использования с команда !recruit

@bot.event
async def on_ready():
    print("BOT connected")
    await bot.change_presence(
        status=disnake.Status.online,
        activity=disnake.Streaming(
            name="Набор в staff", url="https://www.twitch.tv/twitch"
        ),
    )


bot.add_cog(Recruitement(bot))

bot.run('Token')