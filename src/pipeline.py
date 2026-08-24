import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine


def get_engine():
    """Create a SQLAlchemy engine from the DB_URL environment variable."""
    load_dotenv()
    db_url = os.getenv("DB_URL")

    if not db_url:
        raise RuntimeError(
            "DB_URL이 설정되지 않았습니다. "
            "프로젝트 루트의 .env.example을 참고해 .env 파일을 생성하세요."
        )

    return create_engine(db_url)


def load_logs(engine):
    """Load valid 2022-2023 user logs used throughout the analysis."""
    query = """
    SELECT user_uuid, URL, timestamp, date, response_code, method
    FROM com_2022
    WHERE response_code IN ('200', '302')
    UNION ALL
    SELECT user_uuid, URL, timestamp, date, response_code, method
    FROM com_2023
    WHERE response_code IN ('200', '302')
    """

    df = pd.read_sql(query, engine)
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="mixed", utc=True)
    df["date"] = pd.to_datetime(df["date"])
    return df


def build_funnel_data(df):
    """Build user-level signup/resume/application funnel tables."""
    df_filtered = df.copy()

    acquisition = (
        df_filtered[
            df_filtered["URL"].str.split("?").str[0].isin(
                ["signup/step3/done", "complete/github"]
            )
        ][["user_uuid", "timestamp"]]
        .groupby("user_uuid")["timestamp"]
        .min()
        .reset_index()
        .rename(columns={"timestamp": "signup_time"})
    )

    resume_step1 = (
        df_filtered[
            df_filtered["URL"].str.split("?").str[0].str.contains(
                r"api/users/.+/resume/step1|@.+/resume/step1",
                regex=True,
                na=False,
            )
        ][["user_uuid", "timestamp"]]
        .groupby("user_uuid")["timestamp"]
        .min()
        .reset_index()
        .rename(columns={"timestamp": "resume_step1_time"})
    )

    resume_step2 = (
        df_filtered[
            df_filtered["URL"].str.split("?").str[0].str.contains(
                r"api/users/.+/resume/step2|@.+/resume/step2",
                regex=True,
                na=False,
            )
        ][["user_uuid", "timestamp"]]
        .groupby("user_uuid")["timestamp"]
        .min()
        .reset_index()
        .rename(columns={"timestamp": "resume_step2_time"})
    )

    apply_steps = {}
    for step in ["step1", "step2", "step3", "step4"]:
        apply_steps[step] = (
            df_filtered[
                df_filtered["URL"].str.split("?").str[0].isin(
                    [f"jobs/id/apply/{step}", f"api/jobs/id/apply/{step}"]
                )
            ][["user_uuid", "timestamp"]]
            .groupby("user_uuid")["timestamp"]
            .min()
            .reset_index()
            .rename(columns={"timestamp": f"apply_{step}_time"})
        )

    apply_complete = (
        df_filtered[
            df_filtered["URL"].str.split("?").str[0].isin(
                ["jobs/id/apply/complete"]
            )
        ][["user_uuid", "timestamp"]]
        .groupby("user_uuid")["timestamp"]
        .min()
        .reset_index()
        .rename(columns={"timestamp": "apply_complete_time"})
    )

    funnel = acquisition.copy()
    funnel = funnel.merge(resume_step1, on="user_uuid", how="left")
    funnel = funnel.merge(resume_step2, on="user_uuid", how="left")

    for step in ["step1", "step2", "step3", "step4"]:
        funnel = funnel.merge(apply_steps[step], on="user_uuid", how="left")

    funnel = funnel.merge(apply_complete, on="user_uuid", how="left")

    funnel["did_resume1"] = funnel["resume_step1_time"] >= funnel["signup_time"]
    funnel["did_resume2"] = funnel["resume_step2_time"] >= funnel["resume_step1_time"]
    funnel["did_apply1"] = funnel["apply_step1_time"] >= funnel["signup_time"]
    funnel["did_apply2"] = funnel["apply_step2_time"] >= funnel["apply_step1_time"]
    funnel["did_apply3"] = funnel["apply_step3_time"] >= funnel["apply_step2_time"]
    funnel["did_apply4"] = funnel["apply_step4_time"] >= funnel["apply_step3_time"]
    funnel["did_complete"] = funnel["apply_complete_time"] >= funnel["apply_step1_time"]

    return {
        "df_filtered": df_filtered,
        "acquisition": acquisition,
        "resume_step1": resume_step1,
        "resume_step2": resume_step2,
        "apply_steps": apply_steps,
        "apply_complete": apply_complete,
        "funnel": funnel,
    }


def categorize_url(url):
    """Map raw URL patterns to broad product-function categories."""
    if url is None:
        return "기타"
    elif "signup" in url:
        return "가입 프로세스"
    elif "resume" in url:
        return "이력서 작성"
    elif "apply" in url:
        return "지원 프로세스"
    elif "jobs" in url or "api/jobs" in url:
        return "채용공고 탐색"
    elif "companies" in url or "api/companies" in url:
        return "기업 탐색"
    elif "search" in url:
        return "검색"
    elif "users" in url or "@user" in url:
        return "프로필/설정"
    elif "notification" in url:
        return "알림"
    elif "setting" in url or "email" in url:
        return "설정"
    return "기타"
