DROP DATABASE IF EXISTS faers;
CREATE DATABASE IF NOT EXISTS faers CHARACTER SET utf8;
DROP TABLE IF EXISTS faers.ther15q4;
CREATE TABLE IF NOT EXISTS faers.ther15q4 (primaryid BIGINT UNSIGNED NOT NULL PRIMARY KEY, end_dt INT, dur_cod VARCHAR(500), caseid BIGINT UNSIGNED, dur INT, dsg_drug_seq INT, start_dt INT);
DROP TABLE IF EXISTS faers.indi15q4;
CREATE TABLE IF NOT EXISTS faers.indi15q4 (primaryid BIGINT UNSIGNED NOT NULL PRIMARY KEY, indi_pt VARCHAR(1000), caseid BIGINT UNSIGNED, indi_drug_seq INT);
DROP TABLE IF EXISTS faers.demo15q4;
<<<<<<< HEAD
CREATE TABLE IF NOT EXISTS faers.demo15q4 (rept_cod VARCHAR(9), occp_cod VARCHAR(300), mfr_num VARCHAR(500), to_mfr VARCHAR(100), event_dt INT, e_sub VARCHAR(1), rept_dt INT, fda_dt INT, occr_country VARCHAR(2), primaryid BIGINT UNSIGNED NOT NULL PRIMARY KEY, age_cod VARCHAR(7), mfr_dt INT, reporter_country VARCHAR(500), age DECIMAL(12,2), wt DECIMAL(14,5), mfr_sndr VARCHAR(300), caseversion INT, caseid BIGINT UNSIGNED, age_grp VARCHAR(15), init_fda_dt INT, auth_num VARCHAR(500), i_f_code VARCHAR(1), sex VARCHAR(5), lit_ref VARCHAR(1000), wt_cod VARCHAR(20));
DROP TABLE IF EXISTS faers.drug15q4;
CREATE TABLE IF NOT EXISTS faers.drug15q4 (val_vbm INT, route VARCHAR(25), role_cod VARCHAR(22), dose_unit VARCHAR(50), primaryid BIGINT UNSIGNED NOT NULL PRIMARY KEY, dose_amt VARCHAR(15), dose_vbm VARCHAR(300), drugname VARCHAR(500), cum_dose_chr VARCHAR(15), rechal VARCHAR(20), caseid BIGINT UNSIGNED, nda_num INT, prod_ai VARCHAR(500), lot_num VARCHAR(1000), dechal VARCHAR(20), dose_freq VARCHAR(50), exp_dt INT, cum_dose_unit VARCHAR(50), drug_seq INT, dose_form VARCHAR(50));
DROP TABLE IF EXISTS faers.ther15q4;
CREATE TABLE IF NOT EXISTS faers.ther15q4 (dsg_drug_seq INT, end_dt INT, primaryid BIGINT UNSIGNED NOT NULL PRIMARY KEY, dur INT, dur_cod VARCHAR(500), caseid BIGINT UNSIGNED, start_dt INT);
DROP TABLE IF EXISTS faers.reac15q4;
CREATE TABLE IF NOT EXISTS faers.reac15q4 (pt VARCHAR(500), caseid BIGINT UNSIGNED, primaryid BIGINT UNSIGNED NOT NULL PRIMARY KEY, drug_rec_act VARCHAR(500));
DROP TABLE IF EXISTS faers.rpsr15q4;
CREATE TABLE IF NOT EXISTS faers.rpsr15q4 (rpsr_cod VARCHAR(32), caseid BIGINT UNSIGNED, primaryid BIGINT UNSIGNED NOT NULL PRIMARY KEY);
DROP TABLE IF EXISTS faers.indi15q4;
CREATE TABLE IF NOT EXISTS faers.indi15q4 (indi_pt VARCHAR(1000), caseid BIGINT UNSIGNED, primaryid BIGINT UNSIGNED NOT NULL PRIMARY KEY, indi_drug_seq INT);
DROP TABLE IF EXISTS faers.outc15q4;
CREATE TABLE IF NOT EXISTS faers.outc15q4 (outc_cod VARCHAR(4000), caseid BIGINT UNSIGNED, primaryid BIGINT UNSIGNED NOT NULL PRIMARY KEY);
=======
CREATE TABLE IF NOT EXISTS faers.demo15q4 (mfr_sndr VARCHAR(300), occp_cod VARCHAR(300), caseid BIGINT UNSIGNED, to_mfr VARCHAR(100), occr_country VARCHAR(2), init_fda_dt INT, i_f_code VARCHAR(1), event_dt INT, wt_cod VARCHAR(20), wt DECIMAL(14,5), sex VARCHAR(5), mfr_dt INT, e_sub VARCHAR(1), primaryid BIGINT UNSIGNED NOT NULL PRIMARY KEY, rept_cod VARCHAR(9), age DECIMAL(12,2), mfr_num VARCHAR(500), lit_ref VARCHAR(1000), rept_dt INT, fda_dt INT, caseversion INT, reporter_country VARCHAR(500), auth_num VARCHAR(500), age_cod VARCHAR(7), age_grp VARCHAR(15));
DROP TABLE IF EXISTS faers.outc15q4;
CREATE TABLE IF NOT EXISTS faers.outc15q4 (primaryid BIGINT UNSIGNED NOT NULL PRIMARY KEY, outc_cod VARCHAR(4000), caseid BIGINT UNSIGNED);
DROP TABLE IF EXISTS faers.reac15q4;
CREATE TABLE IF NOT EXISTS faers.reac15q4 (pt VARCHAR(500), primaryid BIGINT UNSIGNED NOT NULL PRIMARY KEY, drug_rec_act VARCHAR(500), caseid BIGINT UNSIGNED);
DROP TABLE IF EXISTS faers.drug15q4;
CREATE TABLE IF NOT EXISTS faers.drug15q4 (role_cod VARCHAR(22), dose_form VARCHAR(50), drugname VARCHAR(500), dose_freq VARCHAR(50), dose_vbm VARCHAR(300), caseid BIGINT UNSIGNED, prod_ai VARCHAR(500), dose_amt VARCHAR(15), route VARCHAR(25), rechal VARCHAR(20), drug_seq INT, primaryid BIGINT UNSIGNED NOT NULL PRIMARY KEY, cum_dose_chr VARCHAR(15), dose_unit VARCHAR(50), lot_num VARCHAR(1000), nda_num INT, dechal VARCHAR(20), exp_dt INT, val_vbm INT, cum_dose_unit VARCHAR(50));
DROP TABLE IF EXISTS faers.rpsr15q4;
CREATE TABLE IF NOT EXISTS faers.rpsr15q4 (primaryid BIGINT UNSIGNED NOT NULL PRIMARY KEY, caseid BIGINT UNSIGNED, rpsr_cod VARCHAR(32));
>>>>>>> a238b655e0e344e4a32f07961abf3b22807d72f0
USE faers;