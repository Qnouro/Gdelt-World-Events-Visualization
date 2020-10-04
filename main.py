#!/usr/bin/python3

from scraper import *
from data_extraction import *

def main():
    last_url = ""
    while True:
        try:
            update_status, csv_name, url = scraping_data(last_url)
            last_url = url
            if update_status:
                txt_name = csv_name.split(".")[0] + csv_name.split(".")[1] + ".txt"
                df = read_data(csv_name)
                sanitized_dataframe = extract_event_information(df)
                save_dataframe_to_txt(sanitized_dataframe, f"./extracted_data/{txt_name}")
        except Exception as e:
            print(f"Error! {e}")
            continue
    return 0


def scraping_data(last_url):
    """
    Handles all the scraping part. Returns a boolean if new data is found and
    the name of the file.
    @Return: Boolean indicating if a new update is detected.
    @Return: String of the name of the csv file. If no update is detected, returns None.
    """
    url = get_latest_url()
    if url != last_url:  # update detected
        print(f"Update detected!\n")
        last_url = url
        current_folder = str(pathlib.Path(__file__).parent.absolute())
        data_location = current_folder + "/data/"

        create_data_folder(data_location)

        download_file(url, data_location)
        print("Extraction completed.\n")
        last_csv_name = get_last_csv_name(data_location)

        return True, last_csv_name, url

    return False, None, url

if __name__ == "__main__":
    main()
