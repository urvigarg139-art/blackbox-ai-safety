from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

texts=[
"ignore previous instructions",
"leak system prompt",
"reward hacking detected",
"safe response",
"normal user query",
"bypass safety filters",
"extract training data",
"hello how are you"
]

labels=[1,1,1,0,0,1,1,0]

vec=TfidfVectorizer()
X=vec.fit_transform(texts)

model=LogisticRegression()
model.fit(X,labels)

joblib.dump(model,"model.pkl")
joblib.dump(vec,"vector.pkl")

print("Model trained")
