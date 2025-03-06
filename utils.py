import pandas as pd
from datetime import timedelta


def process_csv(df):

    df = df.drop_duplicates(subset="title", keep="first", ignore_index=True)

    df["date"] = pd.to_datetime(df["startTime"]).dt.date
    df = df.drop_duplicates(subset="startTime", keep="first", ignore_index=True)
    group = df.groupby("date")["startTime"].apply(list).reset_index(name="startTimes")

    def minimize_check_sessions(day_time_list):
        times = sorted(pd.to_datetime(day_time_list))
        start_hour, end_hour = 8, 19
        times = [t for t in times if start_hour <= t.hour < end_hour]

        if not times:
            return {"check_times": [], "num_checks": 0, "coverage_verification": []}

        check_times = []
        coverage_verification = []
        i = 0

        while i < len(times):
            start_idx = i
            latest_idx = i

            while i < len(times) and times[i] <= times[start_idx] + timedelta(
                minutes=15
            ):
                latest_idx = i
                i += 1

            current_check = times[latest_idx]
            check_times.append(current_check)

            covered_classes = []
            for j in range(start_idx, i):
                minutes_after_start = (current_check - times[j]).total_seconds() / 60
                covered_classes.append((times[j], minutes_after_start))

            coverage_verification.append(covered_classes)

        all_classes = []
        for check_idx, covered in enumerate(coverage_verification):
            for class_time, minutes_after_start in covered:
                all_classes.append(
                    {
                        "class_start": class_time,
                        "checked_at": check_times[check_idx],
                        "minutes_after_start": minutes_after_start,
                        "within_15_min": minutes_after_start <= 15,
                        "already_started": minutes_after_start >= 0,
                    }
                )

        return {
            "check_times": check_times,
            "num_checks": len(check_times),
            "coverage_verification": all_classes,
        }

    results = group["startTimes"].apply(minimize_check_sessions)
    group["num_checks"] = results.apply(lambda x: x["num_checks"])
    group["check_times"] = results.apply(lambda x: x["check_times"])

    calendar_df = pd.DataFrame(
        columns=[
            "Subject",
            "Start Date",
            "Start Time",
            "End Date",
            "End Time",
            "All Day Event",
            "Description",
            "Location",
            "Private",
        ]
    )

    for date, check_times in zip(group["date"], group["check_times"]):
        for check_time in check_times:
            new_row = {
                "Subject": "Epiphan Check",
                "Start Date": date.strftime("%m/%d/%Y"),
                "Start Time": check_time.strftime("%I:%M %p"),
                "End Date": date.strftime("%m/%d/%Y"),
                "End Time": (check_time + timedelta(minutes=15)).strftime("%I:%M %p"),
                "All Day Event": False,
                "Description": "Epiphan check sessions 15 minutes",
                "Location": "Media Center",
                "Private": True,
            }
            calendar_df.loc[len(calendar_df)] = new_row

    return calendar_df
