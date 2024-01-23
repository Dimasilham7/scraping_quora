import json
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://id.quora.com/Mengapa-bahasa-Inggris-sulit-untuk-dipelajari"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract question
    question_element = soup.find("title")
    question = question_element.text.replace(" - Quora", "")

    # Extract answers
    answers_element = soup.find("script", {"type": "application/ld+json"})
    if answers_element:
        answers_data = json.loads(answers_element.text)
        suggested_answers = answers_data.get("mainEntity", {}).get("suggestedAnswer", [])

        # Create a dictionary to store the extracted data
        quora_data = {
            "question": question,
            "answers": []
        }

        # Extract information from each suggested answer
        for answer in suggested_answers:
            answer_data = {
                "dateCreated": answer.get("dateCreated", ""),
                "text": answer.get("text", ""),
                "upvoteCount": answer.get("upvoteCount", 0)
            }
            quora_data["answers"].append(answer_data)

        # Save the data to a JSON file
        with open('quora_data.json', 'w', encoding='utf-8') as outfile:
            json.dump(quora_data, outfile, indent=4)

        print("Data successfully extracted and saved to quora_data.json")

    else:
        print("No answers found on the page.")
else:
    print(f"Error: Unable to fetch the page. Status code: {response.status_code}")


with open('quora_data.json', 'r') as f:
  data = json.load(f)

# Output: {'name': 'Bob', 'languages': ['English', 'French']}
df = pd.json_normalize(data['answers'])
df.to_excel("mengapa bahasa inggris sulit untuk dipelajari.xlsx")