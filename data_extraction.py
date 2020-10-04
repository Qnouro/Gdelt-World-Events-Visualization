#!/usr/bin/env python

from scraper import create_data_folder
import pandas as pd
import numpy as np
import matplotlib as plt
import os
import sys
import sqlite3


def main():
    # Dummy example
    csv_name = "20201003210000.gkg.csv"
    txt_name = "20201003210000.txt"
    df = read_data(csv_name)
    sanitized_dataframe = extract_event_information(df)
    # save_dataframe_to_txt(sanitized_dataframe, f"./extracted_data/{txt_name}")
    create_data_folder("extracted_data")
    save_dataframe_to_sqlite(sanitized_dataframe, "./extracted_data/test.db")


def read_data(csv_name):
    """
    Reads the csv file given and returns the associated dataframe.
    @Param csv_name: Name of the csv file to read.
    @Return: Dataframe containing the csv information.
    """
    print("Reading the csv file...")

    data_dir = "./data/"
    csv = data_dir + csv_name

    dataframe = pd.read_csv(csv,
                            delimiter = "\t",
                            names=["ID", "event_date", "source_identifier", "source_name", "document_id", "V1Counts_10", "V2_1Counts", "V1Themes", "V2EnhancedThemes", "V1Locations", "V2EnhancedLocations", "V1Persons",
                                   "V2EnhancedPersons", "V1organizations", "V2EnhancedOrganizations", "V1_5tone", "V2_1EnhancedDates", "V2GCam", "V2_1SharingImage", "V2_1RelatedImages", "V2_1SocialImageEmbeds", "V2_1SocialVideoEmbeds",
                                   "V2_1Quotations", "V2_1AllNames", "V2_1Amounts", "V2_1TranslationInfo", "V2ExtrasXML"],
                            encoding="ISO-8859-1")
    return dataframe


def extract_event_information(dataframe):
    """
    Extracts the information related to the events from the dataframe and returns a transformed dataframe.
    The new dataframe contains information related to the event type, its importance and position (lat, long).
    @Params dataframe: represents all the information contained in the initial csv.
    @Return: dataframe containing the extracted information regarding the events.
    """
    print("Extracting information from the csv file...")
    events_columns = ["event", "event_importance", "event_latitude", "event_longitude"]
    sanitized_dataframe = pd.DataFrame(columns=events_columns)

    # Removing NaN events
    main_dataframe = dataframe["V1Counts_10"].copy()
    main_series = main_dataframe.dropna(0)


    for idx, row in main_series.items():
        row = row.split("#")
        event_dict = {}
        event_dict["event"] = row[0]
        event_dict["event_importance"] = row[1]
        event_dict["event_latitude"] = row[7]
        event_dict["event_longitude"] = row[8]
        sanitized_dataframe = sanitized_dataframe.append(event_dict, ignore_index=True)

    return sanitized_dataframe


def save_dataframe_to_sqlite(sanitized_dataframe, destination_file):
    """
    Saves the dataframe information to a sqlite3 database.
    @Param sanitized_dataframe: Dataframe containing the information to save.
    @Param destination_file: Path to the database to save the information in.
                             If the database doesn't exist, creates it.
    """
    conn = sqlite3.connect(destination_file)
    c = conn.cursor()

    # Create table
    try:
        c.execute('''CREATE TABLE events
                     (type text, importance text, lat real, long real)''')
        print("Created event table")
    except Exception as e:
        print(e)


    for idx, row in sanitized_dataframe.iterrows():
        event_dict = {}
        event_dict["event"] = row[0]
        event_dict["event_importance"] = row[1]
        event_dict["event_latitude"] = row[2]
        event_dict["event_longitude"] = row[3]

        c.execute(f"INSERT INTO events VALUES ('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}')")

    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()



def save_dataframe_to_txt(sanitized_dataframe, destination_file):
    """
    Saves the dataframe information to a txt file.
    @Param sanitized_dataframe: Dataframe containing the information to save.
    @Param destination_file: Path to the file to save the information in.
    """
    # TODO: Change to a sqlite database ?

    print("Storing the event information into a txt file...")
    np.savetxt(destination_file, sanitized_dataframe.values, fmt='%s', delimiter="\t",
            header="event\tevent_importance\tevent_latitude\tevent_longitude")


if __name__ == "__main__":
    main()
