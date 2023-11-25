from youtube_notification_playlist._utils import *

import streamlit as st
import re


def main():
    st.title("Youtube Notification Playlist")
    st.image("asset/logo.png", width=100)

    st.header("1. Load Notifications")

    email    = st.text_input("Enter your Youtube Email")
    password = st.text_input("Enter your Youtube Password", type='password')
    # account = yaml2dict("configs.yml")
    # email    = account['email']
    # password = account['password']

    if 'load_notifications' not in st.session_state:
        st.session_state.load_notifications = False
    if st.button("Start"):
        st.session_state.load_notifications = True

    if st.session_state.load_notifications:
        with st.spinner("In progress.."):
            # control web browser
            driver = get_chromedriver("https://youtube.com")
            click_button_retry(driver, "[aria-label='로그인']")
            submit_text_retry(driver, email)
            submit_text_retry(driver, password)
            click_button_retry(driver,"#button > yt-icon-badge-shape > div > div > yt-icon > yt-icon-shape > icon-shape > div")
            scroll_notifications(driver)
            texts, links = get_notification_links(driver)
            driver.close()

        with st_stdout("success"):
            print(f"[SUCCESS] Load Notifications: Latest {len(links)} videos")


        st.header("")
        st.header("2. Youtube Notification Playlist")

        format = r"^(.*)에서 업로드한 동영상: (.*)[\s]([0-9]+(분|시간|일|주|개월|년) 전)$"
        for text, link in zip(texts, links):
            uploader, name, time, _ = re.search(format, text).groups()
            cols = st.columns([1, 3])
            cols[0].video(link)
            cols[1].write(f"## {name}")
            cols[1].write(f"#### by {uploader}")
            cols[1].write(time)


if __name__ == '__main__':
    st.set_page_config(layout="wide", initial_sidebar_state='collapsed')
    main()
