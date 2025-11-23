import pandas as pd
import numpy as np

# Number of rows (adjust to make it "very big")
rows = 100000  

# Create complex data
data = {
    "id": np.arange(1, rows+1),
    "name": [f"User_{i}" for i in range(rows)],
    "age": np.random.randint(18, 70, size=rows),
    "city": np.random.choice(["Chennai", "Mumbai", "Delhi", "Bangalore", "Hyderabad"], size=rows),
    "email": [f"user{i}@example.com" for i in range(rows)],
    "salary": np.random.randint(20000, 200000, size=rows),
    "join_date": pd.date_range("2010-01-01", periods=rows, freq="H"),
    "department": np.random.choice(["HR", "Finance", "Engineering", "Sales", "Support"], size=rows),
    "status": np.random.choice(["Active", "Inactive", "Probation"], size=rows),
    "remarks": np.random.choice(["Excellent", "Average", "Needs Improvement", "Outstanding"], size=rows)
}

df = pd.DataFrame(data)

# Save to CSV
df.to_csv("big_input.csv", index=False)
print("big_input.csv generated with", rows, "rows")