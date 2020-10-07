#!/usr/bin/env python

from scraper import create_data_folder
import pandas as pd
import numpy as np
import matplotlib as plt
import os
import sys
import sqlite3
from collections import OrderedDict


def main():
    # Dummy example
    csv_name = "20201005120000.gkg.csv"
    df = read_data(csv_name)
    sanitized_dataframe = extract_event_information(df)
    # save_dataframe_to_txt(sanitized_dataframe, f"./extracted_data/{txt_name}")
    create_data_folder("extracted_data")
    save_dataframe(sanitized_dataframe, "test")


def save_dataframe(df, df_root_name):
    """
    Handles all the saving process into SQL and CSV formats.
    @Param df: dataframe to save.
    @Param df_root_name: name of the file to create without the extension.
    """
    save_dataframe_to_sqlite(df, f"./extracted_data/{df_root_name}.db")
    save_dataframe_to_csv(f"./extracted_data/{df_root_name}.db", f"./extracted_data/{df_root_name}.csv")


def save_dataframe_to_csv(db_path, save_path):
    """
    Saves the dataframe as csv in the given path. Makes sure to merge the
    values with those already existing at the same location.
    @Param df: dataframe to save.
    @Param db_path: path to the database.
    @Param save_path: path to the csv file to create.
    """
    # read the database
    db = sqlite3.connect(db_path)
    db_df = pd.read_sql_query("SELECT * FROM events", db)

    db_df["event_document"] = db_df["event_document"].apply(lambda x: [x])
    db_df["event_date"] = db_df["event_date"].apply(lambda x: [x])
    db_df["event_importance"] = db_df["event_importance"].apply(lambda x: [x])
    db_df["event_source_name"] = db_df["event_source_name"].apply(lambda x: [x])

    # read csv file
    # existing_df = read_data(save_path, add_root_dir=False)
    #
    # df = pd.concat([existing_df, df], sort=False)  # Concatenate with old csv
    #

    # merge lines with identical position and event.
    db_df = db_df.groupby(["event", "event_latitude", "event_longitude"], as_index=False).aggregate({'event_document':np.sum, "event_importance": np.sum, "event_date": np.sum, "event_source_name": np.sum})

    # # Drop the rows having the same event, position, importance, and EVENT_DOCUMENT
    # df.drop_duplicates(subset=["event", "event_latitude", "event_longitude", "event_importance", "event_document", "event_source_name"], keep="last")

    db_df.to_csv(save_path, mode='w', index=False)

    db.commit()
    db.close()


def read_data(csv_name, add_root_dir=True):
    """
    Reads the csv file given and returns the associated dataframe.
    @Param csv_name: Name of the csv file to read.
    @Return: Dataframe containing the csv information.
    """
    print("Reading the csv file...")

    csv = csv_name
    if add_root_dir:
        data_dir = "./data/"
        csv = data_dir + csv_name
    pd.set_option('display.float_format', lambda x: '%.3f' % x)  # Avoid scientific notation
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
    main_dataframe = dataframe[["event_date", "V1Counts_10", "source_name", "document_id"]].copy()
    main_series = main_dataframe.dropna(0)


    for idx, row in main_series.iterrows():
        event_date = row[0]
        event_source_name = row[2]
        event_document = row[3]
        event_details = row[1].split("#")
        event_dict = OrderedDict()
        event_dict["event_date"] = event_date
        event_dict["event_source_name"] = event_source_name
        event_dict["event_document"] = event_document
        event_dict["event"] = event_details[0]
        event_dict["event_importance"] = event_details[1]
        event_dict["event_latitude"] = event_details[7]
        event_dict["event_longitude"] = event_details[8]

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
                     (event text, event_importance text, event_latitude real, event_longitude real, event_date integer, event_document text, event_source_name text, unique(event_source_name, event_document, event, event_importance, event_latitude, event_longitude))''')
        print("Created event table")
    except Exception as e:
        print(e)

    # Populating the database
    for idx, row in sanitized_dataframe.iterrows():
        try:
            c.execute(f"INSERT INTO events VALUES ('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}', '{row[5]}', '{row[6]}')")
        except sqlite3.IntegrityError as e:
            # Duplicated row
            pass
        except:
            print("omigod")
            print("Unexpected error:", sys.exc_info()[0])
            exit(1)
    # Save (commit) the changes
    conn.commit()

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
