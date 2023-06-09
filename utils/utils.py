import requests

def get_proxy():
    try:
        response = requests.get("https://proxy.sodalab.dev/random")
        if response.status_code == 200:
            proxy = response.text
            return proxy
        return None
    except requests.ConnectionError:
        return None

def scroll_down(driver):
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        return False
    return True