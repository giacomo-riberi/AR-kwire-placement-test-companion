-- database: c:\Users\giaco\Desktop\giacomo\scuola\università\medicine and surgery\6YEAR\_tesi\software\AR kwire placement test companion\db\positioning_test_data-(v1.27).db

-- Use the ▷ button in the top right corner to run the entire file.

-- join tables
SELECT PHASE.*, PA.*
FROM PHASE
LEFT JOIN PA ON PHASE.id = PA.PHASE_id;

-- check duration congruence
SELECT
    (SELECT SUM(PA_D) FROM PA) AS sum_PA_D,
    (SELECT SUM(ECP_D) FROM ECP) AS sum_ECP_D,
    (SELECT SUM(PHASE_D) FROM PHASE) AS sum_PHASE_D;