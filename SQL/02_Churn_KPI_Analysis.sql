-- =============================================
-- Database Selection
-- =============================================
USE db_Churn;
GO

-- =============================================
-- 1. Gender-wise Customer Distribution
-- =============================================
-- Shows number of customers by gender and their percentage share
SELECT 
    Gender,
    COUNT(*) AS TotalByGender,
    SUM(COUNT(*)) OVER() AS TotalCustomers,
    CAST(100.0 * COUNT(*) / SUM(COUNT(*)) OVER() AS DECIMAL(5,2)) AS Percentage
FROM dbo.stg_Churn
GROUP BY Gender;


-- =============================================
-- 2. Contract-wise Customer Distribution
-- =============================================
-- Analyzes how customers are distributed across contract types
SELECT 
    Contract,
    COUNT(*) AS TotalbyCategory,
    SUM(COUNT(*)) OVER() AS Total,
    CAST(100.0 * COUNT(*) / SUM(COUNT(*)) OVER() AS DECIMAL(5,2)) AS Percentage
FROM dbo.stg_Churn
GROUP BY Contract;


-- =============================================
-- 3. Gender + Contract Segmentation
-- =============================================
-- Multi-dimensional analysis of customers by gender and contract type
SELECT
    Gender,
    Contract,
    COUNT(*) AS TotalbyCategory,
    CAST(100.0 * COUNT(*) / SUM(COUNT(*)) OVER() AS DECIMAL(5,2)) AS Percentage
FROM dbo.stg_Churn
GROUP BY Contract, Gender;


-- =============================================
-- 4. State-wise Customer Distribution
-- =============================================
-- Shows geographic distribution of customers by state
SELECT
    State,
    COUNT(*) AS TotalbyCategory,
    CAST(100.0 * COUNT(*) / SUM(COUNT(*)) OVER() AS DECIMAL(5,2)) AS Percentage
FROM dbo.stg_Churn
GROUP BY State
ORDER BY TotalbyCategory DESC;


-- =============================================
-- 5. Revenue by Customer Status
-- =============================================
-- Business KPI: Revenue contribution from active vs churned customers
SELECT
    Customer_Status,
    COUNT(*) AS TotalCount,
    SUM(Total_Revenue) AS TotalRevByStatus,
    CAST(
        100.0 * SUM(Total_Revenue) / 
        (SELECT SUM(Total_Revenue) FROM dbo.stg_Churn)
    AS DECIMAL(5,2)) AS Percentage
FROM dbo.stg_Churn
GROUP BY Customer_Status
ORDER BY TotalRevByStatus;


-- =============================================
-- 6. Distinct Internet Types
-- =============================================
-- Identifies available internet service categories in dataset
SELECT 
    DISTINCT Internet_Type
FROM dbo.stg_Churn;