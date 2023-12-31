import json
import os
from os import system
import asyncio
from PyInstaller.utils.hooks import collect_data_files
import config
from vocabGame import run_vocab
from dhooks import Webhook, Embed

datas = collect_data_files('certifi')
os.system("mode con cols=125 lines=20")

# Short test to ensure Discord Webhook is enabled correctly
def testwebhook(newHook):
    hook = Webhook(newHook)
    # Webhook configuration
    embed = Embed(
        description="Test Webhook",
        color=0xE74C3C,
        timestamp='now'
    )
    image1 = 'https://media.discordapp.net/attachments/857442371581771836/925632996252459098/IMG_2054.png?width=697&height=650'
    embed.set_author(name='WLG PLAYER', icon_url=image1)
    embed.set_footer(text='Ready', icon_url=image1)
    embed.add_field(name="Webhook is ready and Working!", value="READY")
    embed.set_thumbnail(image1)
    # Sends Webhook
    hook.send(embed=embed)
    print("Successfully Added Webhook!")
    # Changes saved Webhook in userdata.txt
    a_file = open("userdata.txt", "r")
    list_of_lines = a_file.readlines()
    list_of_lines[5] = f'    "discordWebhook": "{newHook}"\n'
    a_file = open("userdata.txt", "w")
    a_file.writelines(list_of_lines)
    a_file.close()


def main():
    print("\u001B[31mWLG PLAYER STARTING...")
    # Creates a nice interface at top allowing users to track game data
    system(
        "title " + f"WLG PLAYER [1.01][CURRENT GAME: {config.game}][{config.number} NUMBER OF GAMES PLAYED][{config.points} POINTS GAINED]")
    # Keeps menu running unit user exits
    while True:
        print("\nMenu : ")
        print("""
        1 : Select Game 
        2 : Webhook Settings
        3 : Check for Updates
        4 : View and Edit Settings
        0 : Exit"""
              )

        choice = input("\nEnter your choice : ")
        # For this github repo I have decided to only attatch one module, I have others that work in similar ways
        # Feel free to reach out to me about any questions
        if choice == '1':
            print('The following Games are Availible :')
            print("""
                    1 : Vocab Game (5 PPG)"""
                  )
            choice = input("\nEnter your choice : ")
            if choice == '1':
                asyncio.get_event_loop().run_until_complete(run_vocab())
        elif choice == '2':
            # Changes Discord Webhook that bot will use to send updates upon task completion
            newHook = input('      Enter Webhook:')
            testWebHook(newHook)
        elif choice == '3':
            print("In-Bot Updates are not yet supported, please check discord for updates")
        elif choice == '4':
            json_file2 = open(f"userdata.txt", "r", encoding="utf-8")
            data2 = json.load(json_file2)
            print('The following Settings Are Set To :')
            print(f"""
                    1 : Classroom Student Name: {data2['user_settings']['name']}
                    2 : Classroom Home Link: {data2['user_settings']['home_link']}
                    3 : Classroom Vocabulary Set: {data2['user_settings']['setName']}
                    0 : Return To Main Menu"""
                  )
            choice = input("\nEdit Setting : ")
            if choice == '1':
                # Changes the user or student name
                newName = input("\nEnter Student Name as it appears in the dropdown : ")
                a_file = open("userdata.txt", "r")
                list_of_lines = a_file.readlines()
                list_of_lines[2] = f'    "name": "{newName}",\n'
                a_file = open("userdata.txt", "w")
                a_file.writelines(list_of_lines)
                a_file.close()
                print("Succesfully Saved")
            if choice == '2':
                # Changes the home link the bot will access to start playing games
                newHome = input("\nEnter Home Name as it appears in the dropdown : ")
                a_file = open("userdata.txt", "r")
                list_of_lines = a_file.readlines()
                list_of_lines[4] = f'    "home_link": "{newHome}",\n'
                a_file = open("userdata.txt", "w")
                a_file.writelines(list_of_lines)
                a_file.close()
                print("Succesfully Saved")
            if choice == '3':
                # Changes the set name that the bot will use for its answers to game questions
                newName = input("\nEnter Set Name as saved after import(If file listed as set.txt only enter set) : ")
                a_file = open("userdata.txt", "r")
                list_of_lines = a_file.readlines()
                list_of_lines[3] = f'    "setName": "{newName}",\n'
                a_file = open("userdata.txt", "w")
                a_file.writelines(list_of_lines)
                a_file.close()
                print("Succesfully Saved")

        elif choice == '0':
            exit()


if __name__ == "__main__":
    main()
