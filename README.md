# Extracting-Business-Card-Data-with-OCR
1. Imports and Database Connection:
Import necessary libraries, including easyocr, sqlalchemy, re, streamlit, PIL, numpy, pandas, and mysql.connector.
Create a connection to a MySQL database named "business_card_data" hosted on the local machine.
2. Streamlit Page Configuration and Menu:
Set up Streamlit's page configuration to have a wide layout.
Define a menu bar with options: "Home," "Upload Image," "Modify," and "Delete." Each option is associated with an icon.
3. Home Menu:
If the "Home" option is selected:
Display a business card expo image.
Provide a title for the application: "Extracting Business Card Data with OCR."
4. Image Upload and OCR:
If the "Upload Image" option is selected:
Create a file uploader widget for users to upload images (PNG, JPG, or JPEG).
When an image is uploaded:
Display the uploaded image.
Use the easyocr library to perform Optical Character Recognition (OCR) on the image.
Extract text from the image and process it to identify various pieces of information:
Company name
Card holder name
Designation
Mobile number
Email address
Website URL
Area
City
State
Pin code
Store this extracted data in lists.
Create a Pandas DataFrame from the extracted data.
Display the DataFrame in the Streamlit app.
Provide a button to upload the extracted data to a MySQL database.
5. Modify Data:
If the "Modify" option is selected:
Retrieve data from the "business_data" table in the MySQL database.
Display the data in a Pandas DataFrame.
Allow the user to select a row to modify by entering the row number.
For the selected row, display the existing data and text input fields to modify it.
Update the database with the modified data upon user request.
6. Delete Data:
If the "Delete" option is selected:
Retrieve data from the "business_data" table in the MySQL database.
Display the data in a Pandas DataFrame.
Allow the user to select a row to delete by entering the row number.
Delete the selected row from the database upon user request.
This code provides a comprehensive business card data extraction and management application using Streamlit, OCR, and a MySQL database. Users can upload images of business cards, extract relevant information, modify existing records, and delete records as needed. The application is designed to facilitate the efficient handling of business card data.
