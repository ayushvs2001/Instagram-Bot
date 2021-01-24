from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import  expected_conditions as EC #use in explicit wait
from selenium.common.exceptions import NoSuchElementException

try:
    root = Tk()
    file = PhotoImage(file='inst.png')
    headingIcon = Label(root, image=file)
    headingIcon.grid(row=0, column=0)

    name_label = Label(root, text="INSTAGRAM BOT", font="arial", bg="cyan", fg= "blue")
    name_label.grid(row=0, column=1)

    root.configure(background='black')
    root.title("INSTAGRAM BOT")

    name_label = Label(root, text="NAME :",font="arial")
    name_label.grid(row=2, column=0)

    name = Entry(root, width=25, font="arial")
    name.grid(row=2, column=1, pady=(10,0))

    password_label = Label(root, text="PASSWORD :",font="arial")
    password_label.grid(row=3, column=0, padx= (0,10))

    password = Entry(root, width=25, font="arial")
    password.grid(row=3, column=1, pady=(10, 0))


    def new_window(username, pw):
        driver = webdriver.Chrome()
        driver.get("https://www.instagram.com/")
        time.sleep(3)

        # username
        user_name = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
        user_name.send_keys(username)

        # password
        password = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
        password.send_keys(pw)

        # logging
        log_in = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div')
        log_in.click()
        time.sleep(2)

        try:
            not_Now = WebDriverWait(driver, 15).until(lambda d: d.find_element_by_xpath('//button[text()="Not Now"]'))
            not_Now.click()
            time.sleep(2)

            messagebox.showinfo("INFO", "LOGIN SUCCESSFUL! \n WAIT TWO MINUTE")

            not_Now2 = WebDriverWait(driver, 15).until(lambda d: d.find_element_by_xpath('//button[text()="Not Now"]'))
            not_Now2.click()
            time.sleep(3)

            try:
                name_tab = driver.find_element_by_xpath(
                    "/html/body/div[1]/section/main/section/div[3]/div[1]/div/div/div[2]/div[1]/div/div/a")
                name_tab.click()
                time.sleep(3)

                time.sleep(2)

                def fun(count):
                    try:
                        # followers
                        def fun_1():
                            try:
                                try:
                                    time.sleep(2)

                                    f = driver.find_elements_by_css_selector('a.-nal3 ')
                                    f[count].click()
                                except:
                                    time.sleep(2)
                                    if count == 0:
                                        f = driver.find_element_by_xpath(
                                            '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')
                                        '''                             //*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a'''
                                    else:
                                        f = driver.find_element_by_xpath(
                                            '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a')
                                    f.click()
                            except:
                                fun_1()  # callling function fun_2 until we get element

                        fun_1()
                        time.sleep(2)
                        global followers
                        global flag
                        global last_name
                        global i
                        driver.maximize_window()
                        time.sleep(2)
                        followers = driver.find_elements_by_tag_name('a')
                        last_name = followers[-1].text
                        flag = True
                        no_followers = int((followers[int(count) + 1].text).split(" ")[0])  # Return no.s of followers
                        i = 0

                        def scroll():
                            global flag
                            global followers
                            global last_name
                            driver.execute_script("arguments[0].scrollIntoView();", followers[-1])
                            time.sleep(2)
                            wait = WebDriverWait(driver, 10)
                            followers = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))

                            flag = (last_name != followers[-1].text)
                            last_name = followers[-1].text

                        def refresh():
                            global i
                            if i % 2 == 0:
                                driver.minimize_window()
                                time.sleep(2)
                            else:
                                driver.maximize_window()
                                time.sleep(2)
                            i += 1

                        while (len(followers) <= (2 * no_followers + 1) or (
                                flag and len(followers) > (2 * no_followers + 1))):
                            scroll()
                            # refreshing if length of list followers is less than less than actual no of followers
                            if ((not flag) and (len(followers) <= (2 * no_followers + 1))):
                                refresh()

                        refresh()
                        scroll()

                        final_list = []
                        for x in followers:
                            final_list.append(x.text)
                        time.sleep(2)
                        driver.find_element_by_xpath(
                            '/html/body/div[5]/div/div/div[1]/div/div[2]/button').click()  # close button

                        return final_list

                    except Exception as e:
                        messagebox.showerror("ERROR", "PlEASE TRY AGAIN!")
                        driver.find_element_by_xpath(
                            '/html/body/div[4]/div/div/div[1]/div/div[2]/button').click()  # close button
                        time.sleep(2)
                        driver.close()

                # fun() function ending

                lst1 = list(fun(0))  # calling function for followers
                lst2 = list(fun(1))  # calling function for following

                followers = set(lst1[6:]) - set(["HASHTAGS", "PEOPLE","", "1"])
                following = set(lst2[6:]) - set(["HASHTAGS", "PEOPLE","","1"])
                unfollowers = following - followers
                not_follow = followers - following

                driver.close()

                messagebox.showinfo("INFO", "PROCESS COMPLETED!")

                root.withdraw()
                top = Toplevel()
                top.title("STUDENT DATABASE")
                top.configure(background='black')

                variable = StringVar(top)
                quality_combo = ttk.Combobox(top, width=27, font="arial", textvariable=variable)

                def load_data_single(data):
                    quality_combo['values'] = ()
                    quality_combo['values'] = tuple(data)

                    quality_combo.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=30)

                title_label = Label(top, text="USER INFORMATION", font="arial", bg="black", fg="cyan")
                title_label.grid(row=0, column=1, pady=(0, 20), padx=(0, 20))

                followers_btn = Button(top, text="FOLLOWERS", font="arial", fg="yellow", bg="green",
                                       command=lambda: load_data_single(followers))
                followers_btn.grid(row=1, column=0, columnspan=2, pady=10, padx=10, ipadx=67)

                following_btn = Button(top, text="FOLLOWING", font="arial", fg="blue", bg="cyan",
                                       command=lambda: load_data_single(following))
                following_btn.grid(row=2, column=0, columnspan=2, pady=10, padx=10, ipadx=67)

                btn3 = Button(top, text="FOLLOWING - FOLLOWERS", font="arial", fg="black", bg="white",
                              command=lambda: load_data_single(unfollowers))
                btn3.grid(row=3, column=0, columnspan=2, pady=10, padx=10)

                btn4 = Button(top, text="FOLLOWERS - FOLLOWING", font="arial", fg="red", bg="yellow",
                              command=lambda: load_data_single(not_follow))
                btn4.grid(row=4, column=0, columnspan=2, pady=10, padx=10)

                def hide_open2():
                    root.deiconify()
                    top.destroy()

                exit2_btn = Button(top, text="EXIT", font="arial", fg="black", bg="red", command=hide_open2)
                exit2_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=(0, 20))

            except:
                 messagebox.showerror("ERROR", "PlEASE TRY AGAIN")

        except NoSuchElementException as e:
            messagebox.showerror("ERROR", "USERNAME OR PASSWORD MUST BE CORRECT")




    login_btn = Button(root, text="LOGIN", font="arial", fg="white", bg="blue", command=lambda:new_window(name.get(), password.get()))
    login_btn.grid(row=4, column=0, columnspan=2, pady=10, padx=(100,0))

    exit_btn = Button(root, text="Exit", command=root.quit, font="arial", fg="black", bg="red", padx=20)
    exit_btn.grid(row=4, column=1, columnspan=2, pady=10, padx=(100,0))

    root.mainloop()

except:
    messagebox.showerror("ERROR", "PlEASE TRY AGAIN")


