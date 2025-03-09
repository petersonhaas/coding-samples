# Coding Samples
This repository includes code examples in Stata, R, and Python.


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
