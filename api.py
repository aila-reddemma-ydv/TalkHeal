import google.generativeai as genai
genai.configure(api_key="AIzaSyAgtTtPjJzTaNSrXaWFkMEJKIpMiFI3QNw")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Hello!")
print(response.text)
