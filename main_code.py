try:
    # from selenium import webdriver
    import getpass
    from conf import INSTA_PASSWORD,INSTA_USERNAME
    from selenium import webdriver
    import time
    import requests
    from urllib.parse import urlparse
    import os

except Exception as e:
    print("Some modules are missing {}".format(e))


# my_password = getpass.getpass("What is your password?\n")

# print(my_password)

# Creating a browser
browser = webdriver.Chrome()

# Target url
url = "https://www.instagram.com"

browser.get(url)

# Sleep time 2 sec
time.sleep(2)

# finding the username input field
username_el = browser.find_element_by_name("username")
username_el.send_keys(INSTA_USERNAME)

# finding the password input field
password_el = browser.find_element_by_name("password")
password_el.send_keys(INSTA_PASSWORD)

# sleep time 1.5 sec
time.sleep(1.5)

# finding the button field
submit_btn_el = browser.find_element_by_css_selector("button[type='submit']")
# click login button
submit_btn_el.click()


# For parsing down the html page
'''
body_el = browser.find_element_by_css_selector("body")
html_text = body_el.get_attribute("innerHTML")
print(html_text)

'''


# browser.find_element_by_css_selector("button")
#Xpath

# my_button_xpath = "//button[contains(text(), 'Follow')][not contains(text(), 'Following']"
# follow_btn_elements = browser.find_elements_by_xpath(my_button_xpath)

# my_button_xpath = "//a[contains(text(), 'Follow')][not contains(text(), 'Following']"
# follow_btn_elements = browser.find_elements_by_xpath(my_button_xpath)


def click_to_follow(browser):

    my_button_xpath = "//*[contains(text(), 'Follow')] [not (contains(text(), 'Following'))]"
    follow_btn_elements = browser.find_elements_by_xpath(my_button_xpath)

    for btn in follow_btn_elements:
        time.sleep(2) #self-throttle

        try:
            btn.click()

        except:
            pass

# new_user = "https://www.instagram.com/goodgirlipsi/"
# browser.get(new_user)
# click_to_follow(browser)

## Scraping Content from a Post

time.sleep(2)
the_user_url = "https://www.instagram.com/sanjana.n_/"
browser.get(the_user_url)

post_url_pattern = "https://www.instagram.com/p/<post-slug-id>"
path_xpath_str = "//a[contains(@href, '/p/')]"
post_links_ele = browser.find_elements_by_xpath(path_xpath_str)
post_link_ele = None


if len(post_links_ele) > 0:
    post_link_ele = post_links_ele[0]

if post_link_ele != None:
    post_link = post_link_ele.get_attribute("href")
    browser.get(post_link)

# Obtaining the Video

video_ele = browser.find_elements_by_xpath("//video")


# Obtaining the Images

image_ele = browser.find_elements_by_xpath("//img")


# image directory

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "data")
os.makedirs(data_dir, exist_ok=True)


def scrape_and_save(elements):
    for ele in elements:
        url = ele.get_attribute('src')
        base_url = urlparse(url).path
        filename = os.path.basename(base_url)
        filepath = os.path.join(data_dir,filename)

        if os.path.exists(filepath):
            continue
        
        #Download the large file with stable connection

        with requests.get(url,stream=True) as r:
            try:
                r.raise_for_status()
            except:
                continue
            
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)


"""
Use ML to classify the post's
image or Video
and then commnet in a relavent fashion

"""

# For Comment

"""<textarea aria-label="Add a comment…" placeholder="Add a comment…" class="Ypffh" autocomplete="off" autocorrect="off" style="height: 18px;"></textarea>
"""

def automate_comment(content="That is cool!"):
    time.sleep(3)
    comment_xpath_str = "//textarea[contains(@placeholder, 'Add a comment')]"
    comment_el = browser.find_element_by_xpath(comment_xpath_str)
    comment_el.send_keys(content)
    submit_btns_xpath = "button[type='submit']"
    submit_btns_els = browser.find_elements_by_css_selector(submit_btns_xpath)
    time.sleep(2)
    for btn in submit_btns_els:
        try:
            btn.click()
        except:
            pass


# Automated Like
def automate_likes(browser):
    like_heart_svg_xpath = "//*[contains(@aria-label, 'Like')]"
    all_like_hearts_elements = browser.find_elements_by_xpath(like_heart_svg_xpath)
    max_heart_h = -1
    for heart_el in all_like_hearts_elements:
        h = heart_el.get_attribute("height")
        current_h = int(h)
        if current_h > max_heart_h:
            max_heart_h = current_h
    all_like_hearts_elements = browser.find_elements_by_xpath(like_heart_svg_xpath)
    for heart_el in all_like_hearts_elements:
        h = heart_el.get_attribute("height")
        if h == max_heart_h or h == f"{max_heart_h}":
            parent_button = heart_el.find_element_by_xpath('..')
            time.sleep(2)
            try:
                parent_button.click()
            except:
                pass


if __name__ == "__main__":
    click_to_follow(browser) #// To follow the person using username
    scrape_and_save(image_ele) #// To scrape data and save to a local directory
    automate_comment()
    automate_likes(browser)