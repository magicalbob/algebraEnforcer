PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS results (
  ip_addr text not null,
  timestamp date not null,
  question_cnt int,
  q1_wrong_cnt int,
  q1_timestamp date,
  q2_wrong_cnt int,
  q2_timestamp date,
  q3_wrong_cnt int,
  q3_timestamp date
);
COMMIT;
