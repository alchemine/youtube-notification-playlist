from youtube_notification_playlist._utils import *

from os import environ
import streamlit as st


def main():
    st.title("Youtube Notification Playlist")
    st.image("asset/logo.png", width=100)

    st.header("1. Load Notifications")

    email = st.text_input("Enter your Youtube Email", value=environ.get("email"))
    password = st.text_input(
        "Enter your Youtube Password", type="password", value=environ.get("password")
    )
    if "load_notifications" not in st.session_state:
        st.session_state.load_notifications = False
    if st.button("Start"):
        st.session_state.load_notifications = True

    if st.session_state.load_notifications:
        with st.spinner("In progress.."):
            # control web browser
            try:
                driver = get_chromedriver("https://youtube.com")
            except Exception as e:
                st.error(f"{e}")
                return

            st.success("[SUCCESS] Open https://youtube.com")

            click_button_retry(
                driver, "#buttons > ytd-button-renderer > yt-button-shape > a"
            )
            st.success("[SUCCESS] Open Sign in")

            submit_text_retry(driver, email)
            st.success("[SUCCESS] Submit Email address")

            submit_text_retry(driver, password, sleep_before=4)
            st.success("[SUCCESS] Submit Password")

            click_button_retry(
                driver,
                "#button > yt-icon-badge-shape > div > div > yt-icon > span > div",
                sleep_before=4,
            )
            st.success("[SUCCESS] Open Notifications")

            scroll_notifications(driver)
            texts, links = get_notification_links(driver)
            st.success(f"[SUCCESS] Load Notifications: Latest {len(links)} videos")

            driver.close()

        st.header("")
        st.header("2. Youtube Notification Playlist")
        for text, link in zip(texts, links):
            extracted_info = extract(text)
            if not extracted_info:
                continue

            name = extracted_info["name"]
            uploader = extracted_info["uploader"]
            time = extracted_info["time"]

            cols = st.columns([1, 3])
            cols[0].video(link)
            cols[1].write(f"## {name}")
            cols[1].write(f"#### by {uploader}")
            cols[1].write(time)


if __name__ == "__main__":
    st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
    main()
