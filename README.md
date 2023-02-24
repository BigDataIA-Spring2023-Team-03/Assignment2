#FASTAPI Fetcher
The FASTAPI Fetcher is a web application built on Streamlit and FASTAPI that allows users to fetch NEXRAD and GEOS-18 satellite data by making FASTAPI calls. The application is dockerized into separate containers for Streamlit, FASTAPI, and Apache Airflow. Users can search for data files using two methods: file name search and field selection. The file can be downloaded or pushed into your s3 bucket.

##Features
File name search: The application generates the file URL for the s3 bucket using the string filename.
Field selection: Users can select individual fields and get the file.
Authentication: Authentication tokens are generated for each user login. The application uses JWT for authentication.
AWS Logging: The application uses AWS logging to keep track of all the log information into our S3 account.
Streamlit: The application uses Streamlit for the main front-end, which is hosted on port 8501 for localhost users. The application is paginated into several pages, including a login page, a registration page, and two main pages locked until login.
Great Expectation: The application uses Great Expectation for data quality testing. Several checkpoints have been created to check our expectations and evaluate the data quality.
Apache Airflow: Apache Airflow has been used in the project for some trigger-based automation tasks, such as updating the metadata database file containing metadata for NEXRAD and GEOS-18 data from the s3 bucket.
Docker: The application is containerized into three separate containers: front-end, back-end, and Apache Airflow. Two of these containers, the front-end and back-end containers, can communicate with each other as defined in the docker-compose.yaml file. Another container is created for our Apache Airflow DAGs, where we use Docker storage mount to share the metadata database file.

##Installation Guide
To install the application, follow these steps:

Clone the repository:
Copy code
$ git clone https://github.com/BigDataIA-Spring2023-Team-03/Assignment2.git
Open the Application folder in any IDE. For this example, we will be using Visual Studio Code.

Open a new terminal in VSCode and type the following commands:

bash
Copy code
$ docker-compose build
$ docker-compose up
Once the above commands are still running, go to http://localhost:8501/ to access the application.

Register or login to the application. Once logged in, you would be redirected to the DataFetcher page.

Acknowledgements
The FASTAPI Fetcher was built by the BigDataIA-Spring2023-Team-03 group as part of an assignment. Special thanks to the following technologies:

Streamlit
FASTAPI
Great Expectation
Apache Airflow
Docker
AWS S3 Bucket.


#### Team Information

| NAME                      |     NUID        |
|---------------------------|-----------------|
|   Raj Mehta               |   002743076     |
|   Mani Deepak Reddy Aila  |   002728148     |
|   Jared Videlefsky        |   001966442     |
|   Rumi Jha                |   002172213     |
 

#### CLAAT Link 
For Detailed documentation- [Click here](https://codelabs-preview.appspot.com/?file_id=1jWZRlWLSZw73qNv_FUd2FOhLIxVbF2EclaAxaLFgOgk#8)

- Raj Mehta - 25%
- Mani Deepak Reddy Aila - 25%
- Jared Videlefsky - 25%
- Rumi Jha - 25%


