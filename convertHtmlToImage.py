from selenium import webdriver
import time

NUM = 5
driver = webdriver.Chrome('chromedriver')
driver.set_window_size(1024, 600)
driver.maximize_window()

# images for query1
for i in range(NUM):
    path = 'static/query1_' + str(i)
    driver.get('file:///home/antony/Desktop/Data-Mining-2/' + path + '.html')
    time.sleep(4)
    driver.save_screenshot(path + '.png')


# image for query2
for k in range(2):
    method = ('DTW' if k == 0 else 'LCS')

    for i in range(NUM):
        path = 'static/query2_' + method + '_' + str(i)
        driver.get('file:///home/antony/Desktop/Data-Mining-2/' + path + '.html')
        time.sleep(4)
        driver.save_screenshot(path + '.png')
        
        for j in range(NUM):
            path = 'static/query2_' + method + '_' + str(i) + '_' + str(j)
            driver.get('file:///home/antony/Desktop/Data-Mining-2/' + path + '.html')
            time.sleep(4)
            driver.save_screenshot(path + '.png')

driver.quit()
