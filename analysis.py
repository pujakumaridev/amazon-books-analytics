import pandas as pd

# Read the CSV file
data = pd.read_csv("books.csv")

# Display book data
print(data)
print(data.head())
print("Total Books:", len(data))
print("Average Rating:", data["User_Rating"].mean())
highest = data["User_Rating"].max()

print(data[data["User_Rating"] == highest])
highest = data["User_Rating"].max()
most_reviewed = data["Reviews"].max()

print(data[data["Reviews"] == most_reviewed])
print("Average Price:", data["Price"].mean())
print(data["Genre"].value_counts())

import matplotlib.pyplot as plt

# Book names and ratings
plt.bar(data["Name"], data["User_Rating"])

plt.xlabel("Book Names")
plt.ylabel("Ratings")
plt.title("Amazon Best Selling Books")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()