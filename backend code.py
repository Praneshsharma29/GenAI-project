import openai
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Function to generate personalized content
def generate_content(student_profile, topic, content_type):
    prompt = f"""
    You are an educational AI assistant. Based on the following student profile:
    {student_profile}

    Create a {content_type} for the topic "{topic}":
    - Ensure it's tailored to the student's learning preferences and progress.
    - Use engaging and age-appropriate language.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful educational AI."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7,
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {e}"

# API endpoint for generating content
@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    student_profile = data.get('student_profile')
    topic = data.get('topic')
    content_type = data.get('content_type')

    if not student_profile or not topic or not content_type:
        return jsonify({"error": "Missing required fields"}), 400

    content = generate_content(student_profile, topic, content_type)
    return jsonify({"content": content})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
