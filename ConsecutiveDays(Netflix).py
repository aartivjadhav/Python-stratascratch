# Find all the users who were active for 3 consecutive days or more.

"""Identifies users active for a minimum number of consecutive days.

    Parameters:
    -----------
    sf_events : pd.DataFrame
        Input data containing user activity with columns: 'user_id', 'record_date'.
    consecutive_days : int, default 3
        Minimum consecutive days threshold.

    Returns:
    --------
    pd.DataFrame
        A DataFrame containing a single column 'user_id' with the qualifying users.
    """
        
import pandas as pd

# Remove duplicate user-date combinations to avoid counting
# multiple events on the same day.
events = (
    sf_events
    .drop_duplicates(subset=["user_id", "record_date"])
    .sort_values(["user_id", "record_date"])
)

# Calculate the difference in days between consecutive activities
events["day_diff"] = (
    events.groupby("user_id")["record_date"]
    .diff()
    .dt.days
)
# Create a unique group whenever the activity is not on the next day
events["streak_group"] = (
    events["day_diff"].ne(1)
    .groupby(events["user_id"])
    .cumsum()
)
# Count the length of each consecutive streak
streaks = (
    events
    .groupby(["user_id", "streak_group"])
    .size()
    .reset_index(name="streak_length")
)

# Return users with at least one streak of 3 or more consecutive days
result = (
    streaks.loc[streaks["streak_length"] >= 3, ["user_id"]]
    .drop_duplicates()
)
