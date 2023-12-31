import time
import random
from pyppeteer import launch
from dhooks import Webhook, Embed
import asyncio
import json
import config
from os import system


# Short function to update top tab for user
def updatetab(game, number, points, message):
    system(
        "title " + f"WLG PLAYER [1.01][{message}][CURRENT GAME: {game}][{number} NUMBER OF GAMES PLAYED][{points} POINTS GAINED]")


# Sets up all data
json_file = open("userdata.txt", "r", encoding="utf-8")
data = json.load(json_file)
site = data["user_settings"]["home_link"]
user = data["user_settings"]["name"]
setName = data["user_settings"]["setName"]
userhook = data["user_settings"]["discordWebhook"]
browsargs = []


# Function for Webhook sent upon completion
def webhook():
    hook = Webhook(userhook)

    embed = Embed(
        description=f"{config.number} GAMES COMPLETED",
        color=0x00FF00,
        timestamp='now'  # sets the timestamp to current time
    )

    image1 = 'https://media.discordapp.net/attachments/857442371581771836/925632996252459098/IMG_2054.png?width=697&height=650'
    embed.set_author(name='WLG PLAYER V1.01', icon_url=image1)
    embed.add_field(name='GAME PLAYED:', value=config.game)
    embed.add_field(name='POINTS GAINED:', value=config.points)
    embed.set_footer(text='Mode: HUMAN ACTIVITY', icon_url=image1)
    embed.set_thumbnail(image1)
    hook.send(embed=embed)


async def run_vocab():
    # Change config
    config.game = "Vocab Game"
    config.message = "CURRENTLY ACTIVE"
    updatetab(config.game, config.number, config.points, config.message)
    # Prompt user for game # then run for that amount
    numberOfGames = int(input("Enter Game amount:"))
    print("Getting Browser Ready(This will take a few seconds)")
    x = 0
    while x != numberOfGames:
        browser = await launch(headless=True, args=browsargs)
        page = await browser.newPage()
        await page.goto(site)
        try:
            await page.select('[id="Student"]', user)
        except:
            print("Please Check User Settings to Make Sure Your Student Name is Correct!")
            exit()
        await page.click('[id="l1"]')
        element = await page.xpath(
            '/html/body/form/font/table[2]/tbody/tr/td/div[2]/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[3]/table/tbody/tr[14]/td/label')
        # Special case here, opening new tabs can be an issue but this solves it
        result_page = asyncio.get_event_loop().create_future()
        browser.once('targetcreated', lambda target: result_page.set_result(target))
        await element[0].click()
        page_in_new_tab = await (await result_page).page()
        total = 0
        time.sleep(3)
        try:
            element = await page_in_new_tab.xpath('/html/body/form/label/u')
            result_page = asyncio.get_event_loop().create_future()
            browser.once('targetcreated', lambda target: result_page.set_result(target))
            await element[0].click()
            page_in_new_tab = await (await result_page).page()
        except:
            pass
        await asyncio.sleep(5)
        link = await page_in_new_tab.evaluate('window.location.href', force_expr=True)

        # This will catch if the user set the set name incorrectly
        try:
            json_file2 = open(f"{setName}.txt", "r", encoding="utf-8")
            data2 = json.load(json_file2)
        except:
            print("Please Check User Settings to Make Sure Your Set Name is Correct!")
            exit()

        try:
            question = 0
            time.sleep(10)
            print("Question number reset")
            # The code below is for one single Vocab Game
            while question != 12:
                question = question + 1
                print(f'Question:{question}')
                try:
                    try:
                        element = await page_in_new_tab.querySelector(
                            f'[id="QLabel00{question}"]')
                        item_price = await page_in_new_tab.evaluate(
                            '(element) => element.textContent', element)
                    except:
                        element = await page_in_new_tab.querySelector(
                            f'[id="QLabel0{question}"]')
                        item_price = await page_in_new_tab.evaluate(
                            '(element) => element.textContent', element)
                    print(item_price)
                    try:
                        pinyin = (data2[item_price]['pinyin'])
                    except:
                        try:
                            new = item_price.replace('  ', '')
                            pinyin = (data2[new]['pinyin'])
                        except:
                            pass
                    print(pinyin)
                    element = await page_in_new_tab.xpath(
                        f'''//input[@onfocus="ShortAnswerTextAreaFocus('Spelling{question}');"]''')
                    await element[0].type(pinyin)
                except:
                    print(
                        f'failed trying to type[{pinyin}] inside question box[{question}] question was:[{item_price}]')
                time.sleep(random.randint(4, 8))
            element = await page_in_new_tab.xpath('//*[@id="myBody"]/b/form/span/center[2]/h2/b/button')
            await element[0].click()
            x = x + 1
        except:
            print(
                "Error This is most likely a network or set list problem(Check that your list number matches the number of terms)")
        try:
            # Wait for page to show game completion
            await page_in_new_tab.waitForXPath('/html/body/form/label/u')
            print("Game Completed")
            config.points += 5
            config.number += 1
            updatetab(config.game, config.number, config.points, config.message)
            await browser.close()
        except:
            # This catches an error for closing the game and sending the webhook
            print("Error, Webhook might be wrong")
    print(f"{numberOfGames} Games Completed!")
    webhook()
    config.message = 'CURRENTLY INACTIVE'
    updatetab(config.game, config.number, config.points, config.message)
