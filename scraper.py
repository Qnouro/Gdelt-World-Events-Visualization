#!/usr/bin/python3

import requests
import zipfile
import os
import pathlib
import sys
import pickle
import urllib
from pathlib import Path


def main():
    last_url = ""
    while True:
        try:
            url = get_latest_url()

            if url != last_url:  # update detected
                print(f"Update detected!")
                last_url = url
                current_folder = str(pathlib.Path(__file__).parent.absolute())
                data_location = current_folder + "/data/"

                create_data_folder(data_location)

                download_file(url, data_location)
                print("Extraction completed.")
        except Exception as e:
            print(f"Error! {e}")
            continue
    return 0


def get_latest_url():
    """
    Returns the url to the latest available gkg file.
    """
    last_update_url = "http://data.gdeltproject.org/gdeltv2/lastupdate.txt"
    response = urllib.request.urlopen(last_update_url)
    htmlString = response.read().decode("utf-8")
    gkg_file_url = htmlString.split("\n")[2].split(" ")[-1]

    return gkg_file_url


def download_file(url, data_location):
    """
    Downloads the path for the given url, extracts it in data_location and removes
    the zip file afterwards.
    @Param url: url to the gkg.csv.zip file to download.
    @Param data_location: folder to store the csv files in.
    """
    # Downloading the data (zip format)
    print(f"Downloading {url}..")
    req = requests.get(url)


    # Writing the zip file to disk
    zipfile_location = data_location + "dummy.csv.zip"
    with open(zipfile_location, "wb") as my_zipfile:
        my_zipfile.write(req.content)

    print("Extracting zip file..")
    # Extracting the zip to get a csv file
    with zipfile.ZipFile(zipfile_location, 'r') as zip_ref:
        zip_ref.extractall(data_location)

    print("Removing zip file..")
    # Removing the zip file
    os.remove(zipfile_location)


def create_url_by_date(file_date):
    """
    Returns the url of the gkg zip file to download from the Gdelt project.
    @Param file_date: Date of the file to download in the YYYYMMDDHHMMSS format (UTC).
    @Return url to the gkg zip file.
    """
    # Url to the our data
    url_header = "http://data.gdeltproject.org/gdeltv2/"
    url_date = file_date
    url_tail = ".gkg.csv.zip"
    url = url_header + url_date + url_tail
    return url


def create_data_folder(data_location):
    """
    Creates the data folder if it does not exist
    """
    if not os.path.exists(data_location):
        os.mkdir(data_location)


def get_last_csv_name(data_location):
    """
    Returns the name of the last csv file created in the directory.
    @Return: String of the csv file name.
    """
    files = sorted(Path(data_location).iterdir(), key=os.path.getctime)
    return str(files[-1]).split("/")[-1]


if __name__ == "__main__":
    main()
