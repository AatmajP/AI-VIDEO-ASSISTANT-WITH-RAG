from dotenv import load_dotenv

load_dotenv()
from langchain_groq import ChatGroq
model = ChatGroq(model="openai/gpt-oss-20b")
response = model.invoke("full form of irctc") #we can also use the model.invoke_async() method to get the response asynchronously
print(response.content)