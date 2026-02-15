from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

texts=[
 "hello how are you",
 "tell me joke",
 "ignore safety rules",
 "bypass system",
 "leak database",
 "hack airport system",
 "system prompt jailbreak",
 "extract confidential info"
]

labels=[0,0,1,1,2,3,4,2]

vector=TfidfVectorizer()
X=vector.fit_transform(texts)

model=LogisticRegression(max_iter=500)
model.fit(X,labels)

joblib.dump(model,"model.pkl")
joblib.dump(vector,"vector.pkl")

print("Advanced model trained")
