Data Visualisation and Insight Project
Overview
This project is a Python-based data visualisation and analysis application using Airbnb data. It processes listing and review data to generate insights.
________________________________________
Project Structure
project/

PatriziaDeCamillis_DataVis.ipynb
app.py
shared.py
listings.csv
reviews.csv
weekly_reviews.csv
requirements.txt
README.md
________________________________________
Data Source
The data used in this project comes from Inside Airbnb:
https://insideairbnb.com/get-the-data/
The original data files are downloaded directly within the .ipynb notebook used during development.
If there are any issues with accessing or reproducing the data, the datasets can be manually downloaded from the Inside Airbnb website (Dublin listings) and placed in the project folder.
Required files:
•	listings.csv.gz
•	reviews.csv.gz
________________________________________
Setup Instructions
1.	Open the project folder in Visual Studio Code.
2.	Ensure all files are located in the same folder:
o	app.py
o	shared.py
o	listings.csv
o	reviews.csv
o	weekly_reviews.csv
o	requirements.txt
________________________________________
How to Run the Project
Run the scripts in the following order:
python shared.py
python app.py
•	shared.py prepares and processes the data
•	app.py runs the main application and visualisations
________________________________________
Notes
•	Ensure all CSV files are in the same directory as the Python files.
•	If file paths are changed, update them in the code accordingly.
•	If the data is not present, download it from the source above.
________________________________________
Requirements
All required Python libraries are listed in requirements.txt.
