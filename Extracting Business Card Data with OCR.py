# imports
import easyocr
from sqlalchemy import create_engine
import re
import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
from streamlit_option_menu import option_menu
import mysql.connector as sql
# Sql connection
mydb = sql.connect(host="localhost", user="root", password="", database="business_card_data")
mycursor = mydb.cursor(buffered=True)
# Page configuration
st.set_page_config(layout="wide", page_icon=Image.open(r"D:\business card\business icon.png"),
                   page_title="Business card Extraction")
# Manu bar
selected = option_menu(None, ["Home", "Upload Image", "Modify", "Delete"], icons=["house", "upload", "pencil-square ",
                                                                                  "trash"])
# Selecting Home Menu
if selected == 'Home':
    # Open the image
    image = Image.open(r"D:\business card\business icon.png")

    # Resize the image to the desired dimensions
    new_width = 300  # Set your desired width
    new_height = 200  # Set your desired height
    resized_image = image.resize((new_width, new_height))
    # Display the resized image
    st.image(resized_image, caption="Business card expo")
    st.title('Extracting Business Card Data with OCR')
company_name_list = []
card_holder_name_list = []
designation_list = []
mobile_number_list = []
email_address_list = []
website_url_list = []
area_list = []
city_list = []
state_list = []
pin_code_list = []

# Selecting Upload Image Menu
if selected == 'Upload Image':
    col1, col2, col3 = st.columns([4.5, 3, 0.5])
    with col1:
        st.write("-> UPLOAD IMAGE")
        image = st.file_uploader(label='choose a file', type=['png', 'jpg', 'jpeg'])
    if image is not None:
        input_image = Image.open(image)  # read image
        with col2:
            st.write("## YOUR IMAGE")
            st.image(input_image)  # display image
        reader = easyocr.Reader(['en'])
        text_read = reader.readtext(np.array(input_image))
        result = []  # empty list for results
        for data in text_read:
            result.append(data[1])
        for ind, i in enumerate(result):
            # To get WEBSITE_URL
            if "www " in i.lower() or "www." in i.lower():
                website_url_list.append(i)
            elif "WWW" in i:
                website_url_list.append(result[ind] + "." + result[ind + 1])

            # To get EMAIL ID
            elif "@" in i:
                email_address_list.append(i)

            # To get MOBILE NUMBER
            elif "-" in i:
                mobile_number_list.append(i)
                if len(mobile_number_list) > 1:
                    mobile_number_list = " & ".join(mobile_number_list)

            # To get COMPANY NAME
            elif ind == len(result) - 1:
                company_name_list.append(i)

            # To get CARD_HOLDER_NAME
            elif ind == 0:
                card_holder_name_list.append(i)

            # To get DESIGNATION
            elif ind == 1:
                designation_list.append(i)

            # To get AREA
            if re.findall("^[0-9].+, [a-zA-Z]+", i):
                area_list.append(i.split(",")[0])
            elif re.findall("[0-9] [a-zA-Z]+", i):
                area_list.append(i)

            # To get CITY NAME

            match1 = re.findall(".+St , ([a-zA-Z]+).+", i)
            match2 = re.findall(".+St,, ([a-zA-Z]+).+", i)
            match3 = re.findall("^[E].*", i)
            if match1:
                city = match1[0]  # Assign the matched city value
                city_list.append(city)
            elif match2:
                city = match2[0]  # Assign the matched city value
                city_list.append(city)
            elif match3:
                city = match3[0]  # Assign the matched city value
                city_list.append(city)

            # To get STATE
            state_match = re.findall("[a-zA-Z]{9} +[0-9]", i)
            if state_match:
                state_list.append(i[:9])
            elif re.findall("^[0-9].+, ([a-zA-Z]+);", i):
                state_list.append(i.split()[-1])
            if len(state_list) == 2:
                state_list.pop(0)

            # To get PINCODE
            if len(i) >= 6 and i.isdigit():
                pin_code_list.append(i)
            elif re.findall("[a-zA-Z]{9} +[0-9]", i):
                pin_code_list.append(i[10:])

        # Create a DataFrame using the lists
        data = {
            'company_name': company_name_list,
            'card_holder_name': card_holder_name_list,
            'designation': designation_list,
            'mobile_number': mobile_number_list,
            'email_address': email_address_list,
            'website_url': website_url_list,
            'area': area_list,
            'city': city_list,
            'state': state_list,
            'pin_code': pin_code_list
        }
        with st.spinner('Wait for it...'):
            df = pd.DataFrame(data)
            st.dataframe(df)

        col4, col5, col6 = st.columns([4, 3.5, 0.5])
        with col4:
            if st.button('Upload to Database'):
                db_connection_str = 'mysql+mysqlconnector://root:@localhost/business_card_data'
                db_connection = create_engine(db_connection_str)
                table_name1 = 'business_data'
                df.to_sql(table_name1, con=db_connection, if_exists='append', index=False)
                st.write('........ done ........')
                with col5:
                    mycursor.execute('SELECT * FROM business_data ORDER BY card_holder_name')
                    df1 = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
                    st.dataframe(df1)

if selected == "Modify":
    mycursor.execute("SHOW COLUMNS FROM business_data LIKE 'id'")
    try:
        mycursor.execute("ALTER TABLE business_data DROP COLUMN id")
    except:
        pass
    mycursor.execute('ALTER TABLE business_data ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY')
    mycursor.execute('SELECT id, company_name, card_holder_name, designation, mobile_number,'
                     ' email_address, website_url, area, city, state,'
                     ' pin_code FROM business_data ORDER BY card_holder_name')
    business_data = mycursor.fetchall()
    column_names = mycursor.column_names

    # Create a DataFrame with the fetched data
    df = pd.DataFrame(business_data, columns=column_names)

    # Sort the DataFrame by 'id' in descending order
    df.sort_values(by='id', ascending=True, inplace=True)
    st.dataframe(df)
    # Allow the user to select a row to modify
    row_to_modify = st.number_input("Enter the row number to modify", min_value=1, max_value=len(business_data),
                                    value=1)

    if st.button("Modify Selected Row"):
        # Assuming that the user wants to modify the row selected by 'row_to_modify'
        if 1 <= row_to_modify <= len(business_data):
            selected_row = business_data[row_to_modify - 1]  # Get the selected row as a tuple

            modified_data = {}  # Create a dictionary to store modified data
            for col_name, col_value in zip(column_names, selected_row):
                if col_name != 'id':  # Skip the 'id' column if it exists
                    new_value = st.text_input(f"New {col_name}", value=col_value)
                    modified_data[col_name] = new_value

            # Get the 'id' from the selected row
            selected_id = selected_row[0]

            # Update the selected row with modified data
            update_query = "UPDATE business_data SET "
            update_query += ", ".join([f"{key} = '{value}'" for key, value in modified_data.items()])
            update_query += f" WHERE id = {selected_id}"
            mycursor.execute(update_query)
            mydb.commit()

            st.success("Row modified successfully!")
        else:
            st.error("Invalid row number. Please enter a valid row number.")

if selected == "Delete":
    mycursor.execute('SELECT id, company_name, card_holder_name, designation, mobile_number,'
                     ' email_address, website_url, area, city, state,'
                     ' pin_code FROM business_data ORDER BY card_holder_name')
    business_data = mycursor.fetchall()
    column_names = mycursor.column_names

    # Create a DataFrame with the fetched data
    df = pd.DataFrame(business_data, columns=column_names)

    # Sort the DataFrame by 'id' in descending order
    df.sort_values(by='id', ascending=True, inplace=True)
    st.dataframe(df)
    # Allow the user to select a row to delete
    row_to_delete = st.number_input("Enter the row number to delete", min_value=1, max_value=len(business_data),
                                    value=1)

    if st.button("Delete Selected Row"):
        # Assuming that the user wants to delete the row selected by 'row_to_delete'
        if 1 <= row_to_delete <= len(business_data):
            selected_row = business_data[row_to_delete - 1]  # Get the selected row as a tuple

            # Get the 'id' from the selected row
            selected_id = selected_row[0]

            # Delete the selected row from the table
            delete_query = f"DELETE FROM business_data WHERE id = {selected_id}"
            mycursor.execute(delete_query)
            mydb.commit()

            st.success("Row deleted successfully!")
        else:
            st.error("Invalid row number. Please enter a valid row number.")
