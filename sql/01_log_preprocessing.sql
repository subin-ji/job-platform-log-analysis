use job_subs;


-- 2023년 데이터 밀린 데이터 발견 수정후 테이블을 생성

-- 있으면 지우고 다시 생성
DROP TABLE IF EXISTS com_2022;

CREATE TABLE com_2022 AS
SELECT
    user_uuid,
    CASE
        WHEN method IS NOT NULL THEN URL
        ELSE SUBSTRING_INDEX(URL, ',', 1)
    END AS URL,
    CASE
        WHEN method IS NOT NULL THEN timestamp
        ELSE TRIM(SUBSTRING_INDEX(URL, ',', -1))
    END AS timestamp,
    CASE
        WHEN method IS NOT NULL THEN date
        ELSE timestamp
    END AS date,
    CASE
        WHEN method IS NOT NULL THEN response_code
        ELSE date
    END AS response_code,
    CASE
        WHEN method IS NOT NULL THEN method
        ELSE response_code
    END AS method
FROM log_2022;

-- 2023년 데이터 밀린 데이터 발견 수정후 테이블을 생성
CREATE TABLE com_2023 AS
SELECT
    user_uuid,
    CASE
        WHEN method IS NOT NULL THEN URL
        ELSE SUBSTRING_INDEX(URL, ',', 1)
    END AS URL,
    CASE
        WHEN method IS NOT NULL THEN timestamp
        ELSE TRIM(SUBSTRING_INDEX(URL, ',', -1))
    END AS timestamp,
    CASE
        WHEN method IS NOT NULL THEN date
        ELSE timestamp
    END AS date,
    CASE
        WHEN method IS NOT NULL THEN response_code
        ELSE date
    END AS response_code,
    CASE
        WHEN method IS NOT NULL THEN method
        ELSE response_code
    END AS method
FROM log_2023;

-- 1) UTC → KST 변환 + 마이크로초 제거 후 업데이트
SET SQL_SAFE_UPDATES = 0;

UPDATE com_2022
SET timestamp = DATE_FORMAT(
    DATE_ADD(
        STR_TO_DATE(TRIM(REPLACE(timestamp, 'UTC', '')), '%Y-%m-%d %H:%i:%s.%f'),
        INTERVAL 9 HOUR
    ),
    '%Y-%m-%d %H:%i:%s'
);

UPDATE com_2023
SET timestamp = DATE_FORMAT(
    DATE_ADD(
        STR_TO_DATE(TRIM(REPLACE(timestamp, 'UTC', '')), '%Y-%m-%d %H:%i:%s.%f'),
        INTERVAL 9 HOUR
    ),
    '%Y-%m-%d %H:%i:%s'
);

-- 2) 값 확인
SELECT timestamp FROM com_2022 LIMIT 5;

-- 3) DATETIME으로 타입 변환 (마이크로초 없으니 DATETIME(6) 불필요)
ALTER TABLE com_2022
MODIFY COLUMN timestamp DATETIME;

ALTER TABLE com_2023
MODIFY COLUMN timestamp DATETIME;

-- 4) 최종 확인
DESCRIBE com_2022;
SELECT timestamp FROM com_2022 LIMIT 5;

-- URL에 ''칸 제거

-- 빈칸 행 수 확인
SELECT COUNT(*) AS empty_url
FROM com_2022
WHERE TRIM(URL) = '';

-- 삭제
SET SQL_SAFE_UPDATES = 0;

DELETE FROM com_2022 WHERE TRIM(URL) = '';
DELETE FROM com_2023 WHERE TRIM(URL) = '';

SET SQL_SAFE_UPDATES = 1;

-- 확인
SELECT COUNT(*) AS total FROM com_2022;
SELECT COUNT(*) AS total FROM com_2023;

SELECT count(*) FROM com_2022;

