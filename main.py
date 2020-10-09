#!/usr/bin/python3

import re
import shutil
import datetime
import json
from time import sleep
from scraper import *
from data_extraction import *


def main():
    """
    Starting the project. We start by populating the database with the 10 last
    released csv files from the GDELT project. We extract the information, store
    it and send it to the front for visualization. We then regularly check for
    updates every minute.
    """
    csv_name = ""
    config_file = read_config()

    last_url = boot_populating_data(config_file)
    while True:
        try:
            update_status, csv_name, url = scraping_data(last_url, config_file)
            last_url = url
            if update_status:
                transform_store_data(csv_name, config_file)
            else:
                print("Checking...")
            sleep(60)
        except Exception as e:
            print(f"Error! {e}")
            continue
    return 0


def boot_populating_data(config_file):
    """
    The function aims at populating the database with 10 csv files in order to
    have a good amount of data upon the start before waiting for updates.
    @Param config_file: Configuration file.
    @Return: url of the first csv file scraped. This helps avoiding redownloading it.
    """
    print("Starting database population...")
    data_count = 0
    first_url, last_url = "", ""
    try:
        update_status, csv_name, url = scraping_data(last_url, config_file)
        first_url = url
        last_url = url
        if update_status:
            transform_store_data(csv_name, config_file)
        else:
            print("Checking...")

        data_count += 1
    except Exception as e:
        print(e)
        exit(1)

    last_csv_name = last_url.split("/")[-1].split(".")[0]
    while data_count < 10:
        try:
            # Getting the csv file that happened 15 min earlier if it exists
            last_csv_name_string = str(datetime.datetime.strptime(last_csv_name, "%Y%m%d%H%M%S") - datetime.timedelta(minutes=15))
            last_csv_name = ''.join(re.findall(r"[\w']+", last_csv_name_string))

            update_status, csv_name, url = scraping_data_by_date(last_csv_name, config_file)

            if update_status:
                transform_store_data(csv_name, config_file)

            data_count += 1

        except Exception as e:
            print(e)

    return first_url


def transform_store_data(csv_name, config_file):
    """
    Creates a sanitized dataframe and stores it.
    @Param csv_name: Name of the csv file to extract information from.
    """
    root_name = csv_name.split(".")[0] + csv_name.split(".")[1]
    txt_name = root_name + ".txt"

    # Reading data
    df = read_data(csv_name, config_file)

    # Transforming data
    sanitized_dataframe = extract_event_information(df)

    # Saving the data
    create_data_folder("extracted_data")
    save_dataframe(sanitized_dataframe, root_name[0:8], config_file)

    # Sending data to front
    send_data_to_front(root_name[0:8], config_file)


def send_data_to_front(root_name, config_file):
    """
    Sends data to front.
    """
    saved_csv_file = os.path.join(config_file["extracted_data_path"], f"{root_name}.csv")
    front_dst_file = os.path.join(config_file["front_data_path"], "data.csv")

    shutil.copyfile(saved_csv_file, front_dst_file)


def scraping_data(last_url, config_file):
    """
    Handles all the scraping part. Returns a boolean if new data is found and
    the name of the file.
    @Return: Boolean indicating if a new update is detected.
    @Return: String of the name of the csv file. If no update is detected, returns None.
    """
    url = get_latest_url()
    if url != last_url:  # update detected
        print("Update detected!")
        last_url = url
        data_location = config_file["downloaded_data_path"]
        create_data_folder(data_location)
        download_file(url, data_location)
        print("Extraction completed.")
        last_csv_name = get_last_csv_name(data_location)

        return True, last_csv_name.split("\\")[-1], url

    return False, None, url


def scraping_data_by_date(csv_date, config_file):
    """
    Handles all the scraping part. Returns a boolean if new data is found and
    the name of the file.
    @Param csv_date: name of the csv to download
    @Return: Boolean indicating if a new update is detected.
    @Return: String of the name of the csv file. If no update is detected, returns None.
    """
    url = create_url_by_date(csv_date)
    last_url = url
    data_location = config_file["downloaded_data_path"]

    create_data_folder(data_location)

    download_file(url, data_location)

    print("Extraction completed.")

    last_csv_name = get_last_csv_name(data_location)

    return True, last_csv_name, url


if __name__ == "__main__":
    main()
