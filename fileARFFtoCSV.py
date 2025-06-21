import arff
import pandas as pd

with open("dataset_.arff", "r", encoding="utf-8") as file:
    dataset = arff.load(file)

data = dataset['data']
columns = [attr[0] for attr in dataset['attributes']]
df = pd.DataFrame(data, columns=columns)
df.to_csv("dataset_.csv", index=False)

print("✅ Successfully converted to dataset_.csv")
