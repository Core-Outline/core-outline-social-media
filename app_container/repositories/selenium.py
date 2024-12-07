# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium import webdriver

# def instagram_login():
#     driver = webdriver.Chrome()
#     driver.get("https://www.instagram.com")
#     wait = WebDriverWait(driver, 10)
#     wait.until(EC.presence_of_element_located((By.NAME,'username')))
#     email_input = driver.find_element(By.NAME,'username')
#     email_input.send_keys('lots.of_teddybear.hugs')
#     password_input = driver.find_element(By.NAME,'password')
#     password_input.send_keys('Tobirama1307')
#     login_button = driver.find_element(By.XPATH, '//button[@class="_acan _acap _acas _aj1-"]')
#     login_button.click()
#     wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Save Info']")))
#     save_info_button = driver.find_element(By.XPATH, "//button[text()='Save Info']")
#     save_info_button.click()
#     wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Not Now']")))
#     not_now_button = driver.find_element(By.XPATH, "//button[text()='Not Now']")
#     not_now_button.click()
#     return driver

# # instagramDriver = instagram_login()


# def instagram_user_engagement(handle, keywords=None):
#     wait = WebDriverWait(instagramDriver, 20)
#     profile_url = f'https://www.instagram.com/{handle}'
#     instagramDriver.get(profile_url.format(username=f'{handle}'))
#     instagramDriver.implicitly_wait(10)
#     instagramDriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#     post_links = instagramDriver.find_elements(By.XPATH, '//a[contains(@href, "/p/")]')
#     comments = []
#     likes = []
    
#     for post in post_links:
#         wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "/p/")]')))  # Wait for a specific element to appear on the page indicating successful login
#         instagramDriver.implicitly_wait(5)
#         post.click()
#         wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs xt0psk2 x1i0vuye xvs91rp x1s688f x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj"]')))
#         likes_element = instagramDriver.find_element(By.XPATH, '//span[@class="x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs xt0psk2 x1i0vuye xvs91rp x1s688f x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj"]')
#         instagramDriver.implicitly_wait(5)
#         likes_element.click()
#         wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="x9f619 xjbqb8w x1rg5ohu x168nmei x13lgxp2 x5pf9jr xo71vjh x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s x1q0g3np xqjyukv x6s0dn4 x1oa3qoh x1nhvcw1"]')))  # Wait for a specific element to appear on the page indicating successful login
#         likes_elements = instagramDriver.find_elements(By.XPATH, '//div[@class="x9f619 xjbqb8w x1rg5ohu x168nmei x13lgxp2 x5pf9jr xo71vjh x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s x1q0g3np xqjyukv x6s0dn4 x1oa3qoh x1nhvcw1"]')
#         instagramDriver.implicitly_wait(5)
#         likes.append([i.text for i in likes_elements if len(i.text) > 0])
#         instagramDriver.implicitly_wait(5)
#         close = instagramDriver.find_element(By.XPATH, '//div[@class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1sxyh0 xurb0ha x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"]')
#         close.click()    
#         try:
#             wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="_aacl _aaco _aacu _aacx _aad7 _aade"]')))
#             comment_elements = instagramDriver.find_elements(By.XPATH, '//span[@class="_aacl _aaco _aacu _aacx _aad7 _aade"]')
#         except:
#             print('')
#         try:
#             wait.until(EC.presence_of_element_located((By.XPATH, '//h1[@class="_aacl _aaco _aacu _aacx _aad7 _aade"]')))
#             comment_elements = instagramDriver.find_elements(By.XPATH, '//h1[@class="_aacl _aaco _aacu _aacx _aad7 _aade"]')
#         except:
#             print('')
        
#         try:
#             comments.append([i.text for i in comment_elements if len(i.text) > 0])
#         except:
#             print('')
#         close_button = instagramDriver.find_element(By.XPATH, '//div[@class="x160vmok x10l6tqk x1eu8d0j x1vjfegm"]')
#         close_button.click()
#         instagramDriver.implicitly_wait(5)

#     return { "comments": comments, "likes": likes }
