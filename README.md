# Coding Samples
This repository includes code examples in **Stata**, **R**, and **Python** used in my honors thesis titled "The Impact of Corporate Profits on GDI Estimates: Forecasting and Data Revisions."

## 1. Variables & Naming Convention

The variables featured in the code are:

    - GDI: Gross Domestic Income (measured in $ Billions or SAAR growth rate in %)
    - GDP: Gross Domestic Product (measured in $ Billions or SAAR growth rate in %)
    - CPW: Corporate Profits with IVA/CCAdj (measured in $ Billions or SAAR growth rate in %)
    - CP: Corporate Profits without IVA/CCAdj (measured in $ Billions or SAAR growth rate in %)
    - USREC: U.S. Recessions (1 = recession)
    - Other variables sourced from the National Income and Product Accounts (NIPAs).


The naming conventions for the computed variables/columns are as follows:

    Levels and Growth Rates
    - Nominal Levels: N{var} (eg. NGDI)  
    - Real Levels: R{var} (eg. NGDI)  
    - Nominal Growth Rate: g...N{var} (eg. g...NGDI)  
    - Real Growth Rate: g...R{var} (eg. g...RGDI)  

    Vintages
    - First (Initial) Release: Initial {var} (Initial NGDI)  
    - Second Release: Second {var} (Third NGDI)  
    - Third Release: Third {var} (Third NGDI)  
    - First Annual Revision: A1 {var} (A1 NGDI)  
    - Second Annual Revision: A2 {var} (A2 NGDI)  
    - Third Annual Revision: A3 {var} (A3 NGDI)  
    - First Comprehensive Revision: C1 {var} (C1 NGDI)  
    - Current (Final) Release: Final {var} (Final NGDI)  

    Revisions to Levels: Rev = (L - E) / E  * 100 -->  Change from the later to earlier release as a percentage of the earlier release.
    - Revision from Second to Initial Release: Rev 2:i {var} (Rev 2:i NGDI)
    - Revision from Third to Initial Release: Rev 3:i {var} (Rev 3:i NGDI)
    - Revision from A1 to Initial Release: Rev a1:i {var} (Rev a1:i NGDI)
    - Revision from A2 to Initial Release: Rev a2:i {var} (Rev a2:i NGDI)
    - Revision from A3 to Initial Release: Rev a3:i {var} (Rev a3:i NGDI)
    - Revision from C1 to Initial Release: Rev c1:i {var} (Rev c1:i NGDI)
    - Revision from Final to Initial Release: Rev f:i {var} (Rev f:i NGDI)

    Revisions to Growth Rates: Rev = %L - %E -->  Percent Change between the later and earlier growth rates.
    (Follows the same naming convention as above)
    - E.g. Revision from Final to Initial Release: gRev f:i {var} (gRev f:i NGDI)

    Earlier Estimates as Share of Final Estimate: Share = E / L * 100 -->  Levels only.
    - E.g. Initial Nominal GDI Release as a share of Final GDI Release: Share i:f {var} (Share i:f NGDI)

    Corporate Profits as Share of GDI: Share = CP / GDI * 100 -->  CP as a share of GDI under the same vintage.
    - E.g. First Annual Nominal CP as share of First Annual Nominal GDI: A1 NCP share 

## 2. Extract Revisions

The ```Extract_Revisions.ipynb``` Jupyter notebook is designed to extract key data releases and compute revisions for various economic variables published by the National Income and Product Accounts (NIPA). These variables were aggregated in historical data through the Real-Time Data Set for Macroeconomists (RTDSM) maintained by the Federal Reserve Bank of Philadelphia. The key variables used are Gross Domestic Income (GDI), Gross Domestic Product (GDP), Corporate Profits, and GDP Deflator.

**Vintages**: The notebook extracts revisions across multiple vintages or stages of data releases. These stages correspond to the different points in time at which updated data is released, reflecting revisions based on newly available data and refined methodologies:

    - Quarterly Releases: First (Initial), Second, Third Release
    - Annual Revisions: First (A1), Second (A2), Third Annual Revision (A3)
    - Comprehensive Revision: First Comprehensive Revision (C1)
    - Latest (Final) Release: Final Release
    
**Workflow**: The notebook processes these different vintages by:  

    - Deflate Nominal to Real Values: Creates columns with real terms by adjusting nominal values for inflation using the GDP deflator.
    - Extract Vintages: Extracts values for each variable from each release stage.
    - Growth Rates: Creates columns to compute SAAR growth rates for each variable using a 4-quarter lag.
    - Share of Final Release: Calculates share of earlier estimate relative to final release. 
    - Revisions to Levels: Computes percentage changes in levels between release stages to show how earlier estimates evolve.
    - Revisions to Growth Rates: Calculates changes in SAAR growth rates between vintages.
    - Corporate Profits as Share of GDI: Calculates Corporate Profits as a share of GDI for each release stage.
    - Data Merging: Merges the data from various stages into a single DataFrame for analysis.

**Output**: The final output is a comprehensive merged dataframe that contains data from all release stages. This dataframe enables detailed analysis of how GDI, GDP, and Corporate Profits have been revised over time. The extracted revisions can then be further used for visualizations, statistical analysis, and forecasting.

    - Excel: merged_releases.xlsx
    - CSV: merged_releases.csv

This notebook provides a complete workflow for extracting, processing, and analyzing the revisions to these key economic indicators.
