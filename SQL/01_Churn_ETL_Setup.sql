/** 
-- ETL Pipeline: Customer Churn Data Ingestion
-- Creates database, staging table, and loads raw CSV data into SQL Server
-- for further cleaning, transformation, and Power BI analysis. **/

USE master;
GO

-- Drop database if it already exists
IF EXISTS (SELECT 1 FROM sys.databases WHERE name = 'db_Churn')
BEGIN
    ALTER DATABASE db_Churn 
    SET SINGLE_USER WITH ROLLBACK IMMEDIATE;

    DROP DATABASE db_Churn;
END;
GO

-- Create database
CREATE DATABASE db_Churn;
GO

-- Use database
USE db_Churn;
GO

-- Create staging table
CREATE TABLE dbo.stg_Churn (

    Customer_ID VARCHAR(50),

    Gender VARCHAR(20),
    Age INT,
    Married VARCHAR(10),
    State VARCHAR(100),
    Number_of_Referrals INT,
    Tenure_in_Months INT,
    Value_Deal VARCHAR(100),

    Phone_Service VARCHAR(10),
    Multiple_Lines VARCHAR(20),

    Internet_Service VARCHAR(10),
    Internet_Type VARCHAR(50),

    Online_Security VARCHAR(10),
    Online_Backup VARCHAR(10),
    Device_Protection_Plan VARCHAR(10),
    Premium_Support VARCHAR(10),

    Streaming_TV VARCHAR(10),
    Streaming_Movies VARCHAR(10),
    Streaming_Music VARCHAR(10),

    Unlimited_Data VARCHAR(10),

    Contract VARCHAR(50),
    Paperless_Billing VARCHAR(10),
    Payment_Method VARCHAR(50),

    Monthly_Charge DECIMAL(10,2),
    Total_Charges DECIMAL(12,2),
    Total_Refunds DECIMAL(12,2),
    Total_Extra_Data_Charges DECIMAL(12,2),
    Total_Long_Distance_Charges DECIMAL(12,2),
    Total_Revenue DECIMAL(12,2),

    Customer_Status VARCHAR(50),
    Churn_Category VARCHAR(100),
    Churn_Reason VARCHAR(255)

);
GO

-- Load CSV data into staging table
BULK INSERT dbo.stg_Churn
FROM 'E:\Shehraz Documents\Python_Adv\Data Analysis\Data Analysis Projects & Case Studies\Customer Churn Analysis Project\Data & Resources\Data\Customer_Data.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    TABLOCK
);
GO