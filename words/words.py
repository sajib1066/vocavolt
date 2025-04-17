import json
from openai import OpenAI
from django.conf import settings
from flashcards.models import WordPack, Word

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def generate_word_entry(wordpack_id, word):
    try:
        wordpack = WordPack.objects.get(id=wordpack_id)
    except WordPack.DoesNotExist:
        print(f"❌ Wordpack with ID {wordpack_id} does not exist.")
        return None

    prompt = f"""
    Generate a JSON object for a vocabulary word with the following structure:
    - word: "{word}"
    - part_of_speech: noun, verb, adjective, or adverb
    - translation: a simple Bengali translation
    - synonyms: 2–4 synonyms (comma-separated string)
    - antonyms: 2–4 antonyms (comma-separated string)
    - description: a brief English explanation
    - examples: 1–3 example English sentences as a JSON list

    Output only the JSON object with no additional text or formatting.

    Example for word "happy":
    {{
      "word": "happy",
      "part_of_speech": "adjective",
      "translation": "খুশি",
      "synonyms": "joyful, cheerful, glad",
      "antonyms": "sad, unhappy, gloomy",
      "description": "Feeling or showing pleasure or contentment.",
      "examples": [
        "She felt happy after getting the good news.",
        "They looked happy on their wedding day."
      ]
    }}

    Now generate for: "{word}"
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}  # Ensure JSON response
        )
        content = response.choices[0].message.content.strip()
        
        # Debug: Print raw response
        print(f"Raw API response content: {content}")

        data = json.loads(content)

        word_obj = Word.objects.create(
            word_pack=wordpack,
            word=data["word"],
            part_of_speech=data["part_of_speech"],
            translation=data["translation"],
            synonyms=data.get("synonyms", ""),
            antonyms=data.get("antonyms", ""),
            description=data["description"],
            examples=data["examples"]
        )

        print(f"✅ Word '{word}' created successfully in WordPack ID {wordpack_id}")
        return word_obj

    except (json.JSONDecodeError, KeyError) as e:
        print(f"❌ Failed to parse or save word: {e}")
        print(f"Error occurred with content: {content}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None



# from words.words import generate_word_entry