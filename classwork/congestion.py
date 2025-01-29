import pandas as pd

df = pd.read_csv("classwork\congestion.csv")

# print(df)

unique_values = pd.DataFrame(df["state"].unique())

unique_values = unique_values.sort_values(0)

# print(unique_values)

#########################################################################


unique_count = df.groupby("state").count()

# unique_count.sort_values('state', ascending=False)

print(unique_count.sort_values("plate", ascending=False))


#####################################################################


# trying to turn into a date time but i think the formate is all wrong...abs
# probably easiest to just drop the MM from the end and group by state and time

df["timeYYYYMMDDHHMM"] = pd.to_datetime(df["timeYYYYMMDDHHMM"])


print(df)


# # need to get the hour than you can group by state and hour
# print(df.dtypes)


hourly_data = df.resample("h", on="timeYYYYMMDDHHMM").count()

print(hourly_data)
