import os
import streamlit as st
from modules import db_mysql, api_requests
import json
import pandas as pd
import logging
from configparser import ConfigParser
from pathlib import Path
import os

# Read configuration file
current_directory = Path.cwd()
CONFIG_FILE = f"{current_directory}/config.ini"
config = ConfigParser()
config.read(CONFIG_FILE)


# Setup in test mode"
if config["testing"]["testing"] == "True":
    os.environ["testing"] = "Testing"

# Set loging
logger = logging.getLogger(__name__)

# Create object variables
msql = db_mysql.MySql()
VR = api_requests.VvRest()

# Create database if not exists
msql.create_database()
# Create table if not exists
msql.create_table()
# Create a conn
conn = msql.get_conn()
# Create a cursor
cursor = msql.get_cursor(conn)


# Streamlit app
def app():
    # Streamlit headings
    st.title("HGVS Variant Tracker")
    st.subheader("Input and Find DNA Variants using HGVS Nomenclature")

    # Input variant description
    hgvs_description = st.text_input("HGVS Description:")
    genome_build = st.text_input("Genome Build:")
    variant_id = st.text_input("Variant ID:")

    # Add validate button
    if st.button("Validate Variant and add to database"):
        # Send request to VV API LOVD endpoint
        response = VR.lovd(genome_build, hgvs_description, return_format="json")
        if response.status_code != 200:
            # Warn if error recieved and print url so user can spot issues
            if response.status_code == 500:
                st.error(f"Error code returned for url {response.url}")
        else:
            response_dictionary = response.json()

            # Filter the response to get the required dictionary
            data = {}
            metadata = response_dictionary["metadata"]
            try:
                for key, value in response_dictionary.items():
                    if type(response_dictionary[key]) == dict and key != "metadata":
                        inner = response_dictionary[key]
                        for k, v in inner.items():
                            if type(inner[k]) == dict:
                                data = inner[k]

                # Warn of genomic variant issues
                if data["genomic_variant_error"] is not None:
                    st.error(data["genomic_variant_error"].replace(":", "\:"))

                # Extract the required data
                genomic_hgvs = data['g_hgvs']
                t_and_p = data["hgvs_t_and_p"]
                t_with_p = []
                for each_tx in t_and_p:
                    mane = "False"
                    for key in t_and_p[each_tx]["select_status"].keys():
                        if "mane" in key:
                            mane = key
                    t_with_p.append([t_and_p[each_tx]["t_hgvs"], t_and_p[each_tx]["p_hgvs_tlc"],
                                     t_and_p[each_tx]["gene_info"]["symbol"],
                                     t_and_p[each_tx]["gene_info"]["hgnc_id"], mane])

                # Store variant description in the database
                for transcript in t_with_p:
                    cursor.execute("""INSERT INTO hgvs_variants (variant_id, g_hgvs_description, c_hgvs_description,
                                   p_hgvs_description, mane, gene_symbol, hgnc_id, metadata) VALUES (%s, %s, %s, %s,
                                   %s,%s, %s, %s)""", (variant_id, genomic_hgvs, transcript[0], transcript[1],
                                   transcript[-1], transcript[2], transcript[3], json.dumps(metadata)))
                    conn.commit()
                st.success("Variant added successfully!")

            # Exceptions that are returned for failed variants
            except TypeError as e:
                logger.error(f"{str(e)}:{hgvs_description}:{genome_build}")
            except KeyError as e:
                logger.error(f"{str(e)}:{hgvs_description}:{genome_build}")

    # Search for stored variants
    st.subheader("Search Variants")
    search_by = st.selectbox("Search By:", ["Variant ID",
                                            "g. HGVS Description",
                                            "c. HGVS Description",
                                            "p. HGVS Description"])
    search_term = st.text_input("Search Term:")

    # Add section to search database
    if st.button("Search database"):
        if search_by == "Variant ID":
            cursor.execute("SELECT * FROM hgvs_variants WHERE variant_id LIKE %s", (f"%{search_term}%",))
        elif search_by == "g. HGVS Description":
            cursor.execute("SELECT * FROM hgvs_variants WHERE g_hgvs_description LIKE %s", (f"%{search_term}%",))
        elif search_by == "c. HGVS Description":
            cursor.execute("SELECT * FROM hgvs_variants WHERE c_hgvs_description LIKE %s", (f"%{search_term}%",))
        elif search_by == "p. HGVS Description":
            cursor.execute("SELECT * FROM hgvs_variants WHERE p_hgvs_description LIKE %s", (f"%{search_term}%",))

        results = cursor.fetchall()

        # get headers
        if len(results) > 0:
            # Get table headers and insert into front of results tuple list
            field_names = [i[0] for i in cursor.description[1:-1]]
            results = [i[1:-1] for i in results]
            st.write("Search Results:")
            # Put the return values into a pandas dataframe
            df = pd.DataFrame(results, columns=field_names)
            st.table(df)
        else:
            st.warning("No results found.")


# Run the Streamlit app
if __name__ == '__main__':
    app()
