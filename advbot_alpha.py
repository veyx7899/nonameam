import json

while True:
    try:
        import os
        import random
        import pyfiglet
        import colorama
        import aminofix

        break
    except ModuleNotFoundError as e:
        os.system(f'pip install {e.name}')

print(colorama.Fore.YELLOW + pyfiglet.figlet_format('anon', font='smslant').rstrip())
print(colorama.Fore.RESET + pyfiglet.figlet_format('gaysex', font='smslant').rstrip())
accountlines = list(map(str.split, open('аккаунты.txt').readlines()))
links = list(set(map(str.strip, open('ссылки.txt').readlines())))
message = open('сообщение.txt', encoding='utf-8').read()
privates, title = json.loads(open('конфиг.json').read()).values()
content = open('описание чата.txt', encoding='utf-8').read()
profile_content = open('описание профиля.txt', encoding='utf-8').read()

def renew_account():
    if not accountlines:
        print(f"{colorama.Fore.RED}> {colorama.Fore.RESET}Аккаунтов {colorama.Fore.RED}не осталось.")
        return
    else:
        while True:
            try:
                account = random.choice(accountlines)
                accountlines.remove(account)
                client = aminofix.Client(deviceId=aminofix.helpers.update_deviceId(account[2]))
                client.login(email=account[0], password=account[1])
                break
            except Exception as e:
                print(e)
                pass
        return client


client = renew_account()
while True:
    if not links or not accountlines:
        break
    try:
        link = random.choice(links)
        com_info = client.get_from_code(code=link)
        name = com_info.comName
        comId = com_info.comId
        links.remove(link)
        try:
            client.join_community(comId=comId)
            sub_client = aminofix.SubClient(comId=comId, profile=client.profile)
            sub_client.edit_profile(nickname=nickname, content=profile_content)
            print(f"\n{colorama.Fore.YELLOW}> {colorama.Fore.RESET}Зашли в {colorama.Fore.YELLOW}{name}.")
            for _ in range(privates):
                blockers = client.get_blocker_users(start=0, size=100)
                onlines = sub_client.get_online_users(start=_ * 100, size=100).profile
                online_users_to_adv = []
                for userId, role in zip(onlines.userId, onlines.role):
                    if not role:
                        online_users_to_adv.append(userId)
                recents = sub_client.get_all_users(start=_ * 100, size=100).profile
                recent_users_to_adv = []
                for userId, role in zip(recents.userId, recents.role):
                    if not role:
                        recent_users_to_adv.append(userId)
                for elem in blockers:
                    if elem in online_users_to_adv:
                        online_users_to_adv.remove(elem)
                    if elem in recent_users_to_adv:
                        recent_users_to_adv.remove(elem)

                if recent_users_to_adv:
                    try:
                        chat = sub_client.start_chat(userId=recent_users_to_adv, message=message)['thread']['threadId']
                        sub_client.edit_chat(chatId=chat, viewOnly=True, title=title, content=content)
                        if privates > 1:
                            print(
                                f"{colorama.Fore.YELLOW}> {colorama.Fore.RESET}Волна {colorama.Fore.YELLOW}({_ + 1}): {colorama.Fore.RESET}Приватка на {colorama.Fore.YELLOW}({len(recent_users_to_adv)}){colorama.Fore.RESET} недавно вступивших людей создана.")
                        else:
                            print(
                                f"{colorama.Fore.YELLOW}> {colorama.Fore.RESET}Приватка на {colorama.Fore.YELLOW}({len(recent_users_to_adv)}){colorama.Fore.RESET} недавно вступивших людей создана.")
                    except aminofix.exceptions.ChatInvitesDisabled:
                        pass
                    except aminofix.exceptions.YouAreBanned:
                        pass
                    except Exception as e:
                        print(json.loads(e)['api:message'])
                if online_users_to_adv:
                    try:
                        chat = sub_client.start_chat(userId=online_users_to_adv, message=message)['thread']['threadId']
                        sub_client.edit_chat(chatId=chat, viewOnly=True, title=title, content=content)
                        if privates > 1:
                            print(
                                f"{colorama.Fore.YELLOW}> {colorama.Fore.RESET}Волна {colorama.Fore.YELLOW}({_ + 1}): {colorama.Fore.RESET}Приватка на {colorama.Fore.YELLOW}({len(online_users_to_adv)}){colorama.Fore.RESET} людей в сети создана.")
                        else:
                            print(
                                f"{colorama.Fore.YELLOW}> {colorama.Fore.RESET}Приватка на {colorama.Fore.YELLOW}({len(online_users_to_adv)}){colorama.Fore.RESET} людей в сети создана.")
                    except aminofix.exceptions.ChatInvitesDisabled:
                        pass
                    except aminofix.exceptions.YouAreBanned:
                        pass
                    except Exception as e:
                        exception = json.loads(str(e).replace("'", '"'))['api:message']
                        if privates > 1:
                            print(
                                f"{colorama.Fore.RED}> Волна ({_ + 1}){colorama.Fore.RESET} Возникла ошибка: {colorama.Fore.RED}{exception}")
                        else:
                            print(
                                f"{colorama.Fore.RED}> {colorama.Fore.RESET}Возникла ошибка: {colorama.Fore.RED}{exception}")

        except aminofix.exceptions.InvalidCodeOrLink:
            pass
        except aminofix.exceptions.YouAreBanned:
            pass
        except aminofix.exceptions.CommunityDisabled:
            pass
        except aminofix.exceptions.AccountDisabled:
            client = renew_account()
        except aminofix.exceptions.TooManyRequests:
            client
    except aminofix.exceptions.InvalidCodeOrLink:
        pass
    except aminofix.exceptions.CommunityDisabled:
        pass
