import websocket
import cloudscraper
import requests
import time
from fake_useragent import UserAgent
import threading


BloxFlipToken = "bloxflip token"
CapSolverApiKey = "cap solver api key here"
ua = UserAgent()
user_agent = ua.random 

print("""



░                    █▀▀█ ─█▀▀█ ▀█▀ ░█▀▀▄ 　 ───░█ ░█▀▀▀█ ▀█▀ ░█▄─░█ ░█▀▀▀ ░█▀▀█ 
                    ░█▄▄▀ ░█▄▄█ ░█─ ░█─░█ 　 ─▄─░█ ░█──░█ ░█─ ░█░█░█ ░█▀▀▀ ░█▄▄▀ 
                  ░  █─░█ ░█─░█ ▄█▄ ░█▄▄▀ 　 ░█▄▄█ ░█▄▄▄█ ▄█▄ ░█──▀█ ░█▄▄▄ ░█─░█
     
    Asura make this shit. | warning do not host this with 2 account up. result will make ur both account get rain mute!
""")

def check_capsolver_balance():
    try:
        response = requests.post("https://api.capsolver.com/getBalance", json={"clientKey": CapSolverApiKey})
        response.raise_for_status()
        balance_data = response.json()
        if balance_data.get("errorId") == 0:
            balance = balance_data.get("balance", 0)
            print(f"CapSolverbalance: ${balance}")

            if balance < 0.0016:
                print("your bal dose not engouh for even one hcaptcha")
                exit() 
        else:
            print(f"{balance_data.get('errorDescription')} | your api key might be invailed")
            exit() 
    except requests.exceptions.RequestException as e:
        print(f"{str(e)}")
        exit() 


def capsolver(retries=100):
    site_key = "2ce02d80-0c81-4b28-8af5-e4cdfc08bed9"
    site_url = "https://bloxflip.com/"

    while retries > 0:
        payload = {
            "clientKey": CapSolverApiKey,
            "task": {
                "type": 'HCaptchaTaskProxyLess',
                "websiteKey": site_key,
                "websiteURL": site_url,
                "user-agent": user_agent
            }
        }

        try:
            res = requests.post("https://api.capsolver.com/createTask", json=payload)
            res.raise_for_status()
            resp = res.json()
            task_id = resp.get("taskId")

            if not task_id:
                print("Failed to create task:", res.text)
                retries -= 1
                continue

            while True:
                time.sleep(1)
                result_payload = {"clientKey": CapSolverApiKey, "taskId": task_id}
                result_res = requests.post("https://api.capsolver.com/getTaskResult", json=result_payload)
                result_res.raise_for_status()
                result_resp = result_res.json()

                if result_resp.get("status") == "ready":
                    print("Captcha solved successfully!")
                    return result_resp.get("solution", {}).get('gRecaptchaResponse')

                if result_resp.get("status") == "failed" or result_resp.get("errorId"):
                    retries -= 1
                    break 

        except requests.exceptions.RequestException as e:
            print(f"{str(e)}")
            retries -= 1
            if retries == 0:
                return None

    return None 


def get_user_info():
    scraper = cloudscraper.create_scraper()
    headers = {
        "x-auth-token": BloxFlipToken,
        "User-Agent": user_agent, 
    }
    
    try:
        response = scraper.get("https://api.bloxflip.com/user", headers=headers)
        response.raise_for_status()
        user_data = response.json()
        
        if 'user' in user_data:
            roblox_id = user_data['user']['robloxId']
            roblox_username = user_data['user']['robloxUsername']
            print(f"username: {roblox_username} | robloxid: {roblox_id}")
            return roblox_id
        else:
            print("unknow error or failed to get ur info")
            exit() 
            
    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 400:
            print("invalid token")
            exit() 
        else:
            print(f"{err}")
            exit()
    except requests.exceptions.RequestException as e:
        print(f"{str(e)}")
        exit() 




def keepconnection(ws):
    while True:
        try:
            ws.send("2")
        except websocket.WebSocketConnectionClosedException:
            break
        except Exception as e:
            print(f"{e}")
            break
        time.sleep(25) 

def send_data(BloxFlipToken, roblox_id):
    scraper = cloudscraper.create_scraper()
    scraper.get("https://bloxflip.com")
    
    headers = {
        "Origin": "https://bloxflip.com",
        "Host": "ws.bloxflip.com",
        "User-Agent": user_agent, 
    }
    websocketuri = "wss://ws.bloxflip.com/socket.io/?EIO=3&transport=websocket"

    while True:
        try:
            ws = websocket.create_connection(websocketuri, header=headers)
            print("WebSocket connected")
            ws.send('40/chat,')         
            ws.send('40/cloud-games,')
            ws.send('40/cups,')
            ws.send('40/blackjack,')
            ws.send('40/jackpot,')
            ws.send('40/rouletteV2,')
            ws.send('40/roulette,')
            ws.send('40/crash,')
            ws.send('40/wallet,')
            ws.send('40/marketplace,')
            ws.send('40/case-battles,')
            ws.send('40/mod-queue,')
            ws.send('40/feed,')
            ws.send(f'42/chat,["auth","{BloxFlipToken}"]')
            ws.send(f'42/cups,["auth","{BloxFlipToken}"]')
            ws.send(f'42/blackjack,["auth","{BloxFlipToken}"]')
            ws.send(f'42/jackpot,["auth","{BloxFlipToken}"]')
            ws.send(f'42/rouletteV2,["auth","{BloxFlipToken}"]')
            ws.send(f'42/roulette,["auth","{BloxFlipToken}"]')
            ws.send(f'42/crash,["auth","{BloxFlipToken}"]')
            ws.send(f'42/wallet,["auth","{BloxFlipToken}"]')
            ws.send(f'42/marketplace,["auth","{BloxFlipToken}"]')
            ws.send(f'42/case-battles,["auth","{BloxFlipToken}"]')
            ws.send(f'42/mod-queue,["auth","{BloxFlipToken}"]')
            ws.send(f'42/feed,["auth","{BloxFlipToken}"]')

            connection = threading.Thread(target=keepconnection, args=(ws,))
            connection.start()

            while True:
                try:
                    message = ws.recv()
                except websocket.WebSocketTimeoutException:
                    continue
                if '42/chat,["rain-state-changed",' in message:
                    if '42/chat,["rain-state-changed",false]' in message:
                        print("rain ended")
                    else:
                        print("Rain detected! | Joining")
                        captcha_token = capsolver()
                        if captcha_token:
                            ws.send(f'42/chat,["enter-rain",{{"captchaToken":"{captcha_token};;scope"}}]')
                            print(f"Solved : {captcha_token}")
                            joined_rain = False
                            while True:
                                message = ws.recv()

                                if f'42/chat,["rain-state-added",{roblox_id}]' in message:
                                    print("Successfully joined rain!")
                                    joined_rain = True
                                    break 
                                if '42/chat,["rain-state-changed",false]' in message:
                                    print("cannot check if you join or nahs")
                                    break
                            if not joined_rain:
                                print("failed to join. waitting for new one")
                        else:
                            print("captcha failed.")

        except websocket.WebSocketConnectionClosedException:
            print("reconnecting in 10 seconds...")
            time.sleep(10)
        except Exception as e:
            print(f"{str(e)}")
            time.sleep(10)
        finally:
            try:
                ws.close()
            except Exception:
                pass
            print("webSocket disconnected. trying reconnecting...")


check_capsolver_balance()
roblox_id = get_user_info()
send_data(BloxFlipToken, roblox_id)
