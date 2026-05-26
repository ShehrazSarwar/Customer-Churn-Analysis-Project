USE db_Churn;
GO

-- =============================================
-- View: Churn + Retained Customers
-- Purpose: Used for churn analysis, KPIs, and BI dashboarding
-- =============================================
IF OBJECT_ID('dbo.vw_ChurnData', 'V') IS NOT NULL
    DROP VIEW dbo.vw_ChurnData;
GO

CREATE VIEW dbo.vw_ChurnData AS
SELECT *
	FROM dbo.prod_Churn
WHERE Customer_Status IN ('Churned', 'Stayed');
GO

-- =============================================
-- View: Newly Joined Customers
-- Purpose: Used for customer acquisition analysis
-- =============================================
IF OBJECT_ID('dbo.vw_JoinData', 'V') IS NOT NULL
    DROP VIEW dbo.vw_JoinData;
GO

CREATE VIEW dbo.vw_JoinData AS
SELECT *
	FROM dbo.prod_Churn
WHERE Customer_Status = 'Joined';
GO