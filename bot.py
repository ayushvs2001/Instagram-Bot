from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import  expected_conditions as EC #use in explicit wait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import re

try:
    root = Tk()
    file = PhotoImage(file='inst.png')
    headingIcon = Label(root, image=file)
    headingIcon.grid(row=0, column=0)

    name_label = Label(root, text="INSTAGRAM BOT", font="arial", bg="cyan", fg= "blue")
    name_label.grid(row=0, column=1,ipady=20,columnspan=2)

    root.configure(background='black')
    root.title("INSTAGRAM BOT")

    name_label = Label(root, text="NAME :",font="arial")
    name_label.grid(row=2, column=0)

    name = Entry(root, width=25, font="arial")
    name.grid(row=2, column=1, columnspan=2, pady=(10,0))

    password_label = Label(root, text="PASSWORD :",font="arial")
    password_label.grid(row=3, column=0, padx= (0,10))

    password = Entry(root, show='*', width=25, font="arial")
    password.grid(row=3, column=1, columnspan=2, pady=(10, 0))

    def user_info(lst1, lst2, driver):
        try:
            followers = set(lst1) - set(["HASHTAGS", "PEOPLE", "", "1", "POSTS", "SAVED", "IGTV", "TAGGED", "Edit Profile", r".*! followers", r" .*! following"])
            following = set(lst2) - set(["HASHTAGS", "PEOPLE", "", "1","POSTS", "SAVED", "IGTV", "TAGGED", "Edit Profile", r".* followers", r" .*! following"])
            unfollowers = following - followers
            not_follow = followers - following
            root.withdraw()
            top = Toplevel()
            top.title("STUDENT DATABASE")
            top.configure(background='black')

            variable = StringVar(top)
            quality_combo = ttk.Combobox(top, width=27, font="arial", textvariable=variable)

            def search_username(username):
                 try:
                    driver.refresh()

                    current_page_user_name = driver.find_element_by_xpath(
                        "/html/body/div[1]/section/main/div/header/section/div[1]/h2")
                    current_page_user_name = current_page_user_name.text
                    
                    if current_page_user_name == username:
                        return True
                    else:
                        search_button = driver.find_element_by_xpath(
                            "/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div/div/span[2]")
                        search_button.click()
                        time.sleep(3)

                        search_box = driver.find_element_by_xpath(
                            '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
                        search_box.send_keys(username)
                        time.sleep(2)

                        search_name = driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[4]/div/a[1]/div/div[2]/div/span")
                        first_serch_name = search_name.text

                        if first_serch_name == username:
                            click_on_user = driver.find_element_by_xpath(
                                    "/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[4]/div/a[1]/div")
                            click_on_user.click()
                            time.sleep(3)
                            return True
                        else:
                            messagebox.showerror("INVALID USERNAME", "USERNAME NOT FOUND")
                            return False
                 except:
                     messagebox.showerror("ERROR", "PLEASE TRY AGAIN!")

            def find_user_info():
                no_of_post = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span")
                print(no_of_post.text)
                no_of_post = no_of_post.text

                no_of_followers = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span")
                print(no_of_followers.text)
                no_of_followers = no_of_followers.text

                no_of_following = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span")
                print(no_of_following.text)
                no_of_following = no_of_following.text

                title_label = Label(top, text="INFORMATION", font="arial", bg="black", fg="cyan")
                title_label.grid(row=2, column=2, pady=(0, 20), padx=(30, 0), ipady=5)

                # enter the data of no of post into the entry
                no_of_post_entry = Entry(top, font="arial", fg="white", bg="black")
                no_of_post_entry.grid(row=3, column=2, ipady=4, pady=10, columnspan=2, ipadx=20)
                no_of_post_entry.insert(0, f"NO OF POST : {no_of_post}")

                no_of_followers_entry = Entry(top, font="arial", fg="white", bg="black")
                no_of_followers_entry.grid(row=4, column=2, ipady=4, pady=10, columnspan=2, ipadx=20)
                no_of_followers_entry.insert(0, f"NO OF FOLLOWERS : {no_of_followers}")

                no_of_following_entry = Entry(top, font="arial", fg="white", bg="black")
                no_of_following_entry.grid(row=5, column=2, ipady=4, pady=10, columnspan=2, ipadx=20)
                no_of_following_entry.insert(0, f"NO OF FOLLOWINGS: {no_of_following}")

            def show_user_data(username):
                if search_username(username):
                    find_user_info()


            def follow(username):
                print(username not in following)
                if username not in following:
                  global unfollowers
                  global not_follow

                  if search_username(username):
                      follow_button = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/button")
                      follow_button.click()
                      time.sleep(2)
                      following.add("username")
                      unfollowers = following - followers
                      not_follow = followers - following
                else:
                    messagebox.showerror("ERROR", "YOU ALREADY FOLLOW THIS PERSON")

            def unfollow(username):
                global unfollowers
                global not_follow
                if username in following:
                   if search_username(username):
                       unfollow_enter = driver.find_element_by_xpath(
                           "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button")
                       unfollow_enter.click()
                       time.sleep(3)
                       
                       cancel_button = driver.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[1]")
                       cancel_button.click()
                       time.sleep(3)
                       

                       following.remove(username)
                       unfollowers = following - followers
                       not_follow = followers - following

                else:
                   messagebox.showerror("ERROR", "YOU ALREADY NOT FOLLOW THIS PERSON")


            def callbackFunc(event):  # this function used to get selected item from the combo box and load into oid i/p box
                """when the item choose from the combobox it load to choice"""
                choice = quality_combo.get()

                print("choice", choice)

                name_of_user = Entry(top, font="arial", fg="black", bg="white")
                name_of_user.grid(row=1, column=1, ipady=4, padx=(0, 170), pady=10, columnspan=2)

                name_of_user.insert(0, choice)

                show_data = Button(top, text="SHOW DATA", font="arial", fg="black", bg="violet", command=lambda: show_user_data(choice))
                show_data.grid(row=2, column=1, pady=10, padx=(0, 80))

                unfollow_btn = Button(top, text="UNFOLLOW", font="arial", fg="cyan", bg="green", command=lambda: unfollow(choice))
                unfollow_btn.grid(row=3, column=1, pady=10, padx=(0, 80), ipadx=4)

                follow_btn = Button(top, text="FOLLOW", font="arial", fg="black", bg="gray", command=lambda: follow(choice))
                follow_btn.grid(row=4, column=1, pady=10, padx=(0, 80), ipadx=18)

            def load_data_single(data):
                quality_combo['values'] = ()
                quality_combo['values'] = tuple(data)

                quality_combo.grid(row=5, column=0, columnspan=2,pady=10, padx=(0,20), ipadx=30)
                quality_combo.bind("<<ComboboxSelected>>", callbackFunc)

            title_label = Label(top, text="USER INFORMATION", font="arial", bg="black", fg="cyan")
            title_label.grid(row=0, column=0,columnspan=2, pady=(0,20), padx=(0,0),ipady=5)

            followers_btn = Button(top, text="FOLLOWERS", font="arial", fg="yellow", bg="green",
                                   command=lambda: load_data_single(followers))
            followers_btn.grid(row=1, column=0,  pady=10, padx=10, ipadx=67)

            following_btn = Button(top, text="FOLLOWING", font="arial", fg="blue", bg="cyan",
                                   command=lambda: load_data_single(following))
            following_btn.grid(row=2, column=0, pady=10, padx=10, ipadx=67)

            btn3 = Button(top, text="FOLLOWING - FOLLOWERS", font="arial", fg="black", bg="white",
                          command=lambda: load_data_single(unfollowers))
            btn3.grid(row=3, column=0, pady=10, padx=10)

            btn4 = Button(top, text="FOLLOWERS - FOLLOWING", font="arial", fg="red", bg="yellow",
                          command=lambda: load_data_single(not_follow))
            btn4.grid(row=4, column=0, pady=10, padx=10)


            def hide_open2():
                driver.close()
                root.deiconify()
                top.destroy()

            exit2_btn = Button(top, text="EXIT", font="arial", fg="black", bg="red", command=hide_open2)
            exit2_btn.grid(row=6, column=0, columnspan=2,pady=10, padx=(0,20), ipadx=30)
        except:
            messagebox.showerror("ERROR", "PLEASE TRY AGAIN")




    def login(username, pw):
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

                messagebox.showinfo("INFO", "PROCESS COMPLETED!")

                user_info_btn = Button(root, text="USER INFO", font="arial", fg="red", bg="yellow",command=lambda: user_info(lst1, lst2, driver))
                user_info_btn.grid(row=4, column=1, columnspan=2, pady=10, ipadx=20)

            except Exception as e:
                print(e)
                messagebox.showerror("ERROR", "PlEASE TRY AGAIN")

        except NoSuchElementException as e:
            messagebox.showerror("ERROR", "USERNAME OR PASSWORD MUST BE CORRECT")

        except TimeoutException as e:
            messagebox.showerror("ERROR", "USERNAME OR PASSWORD MUST BE CORRECT")




    login_btn = Button(root, text="LOGIN", font="arial", fg="white", bg="blue", command=lambda:login(name.get(), password.get()))
    login_btn.grid(row=5, column=1, pady=1)

    exit_btn = Button(root, text="Exit", command=root.quit, font="arial", fg="black", bg="red", padx=20)
    exit_btn.grid(row=5, column=2, pady=10)

    root.mainloop()

except Exception as e:
    print(e)
    messagebox.showerror("ERROR", "PLEASE TRY AGAIN")
