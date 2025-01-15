from openai import OpenAI
from openai import OpenAIError

# Make a `openai_key.py` in `modules\` and insert your token as a string to the openai_key variable
from modules.openai_key import openai_key 

class LargeLanguageModel:
    def __init__(
        self, 
        verbose=False
    ):
        self.verbose = verbose # Toggle for debug messages

        try:
            # Start listening
            self.client = OpenAI(
                api_key=openai_key
            )

            if self.verbose: print("Client successfuly created!")

        except:
            if self.verbose: print("Could not acquire Client.")

    def chat_completion(
        self, 
        system_role,
        prompt, 
        model="gpt-4o-mini", 
        max_tokens=10,
        randomness=0,
        n_responses=1
    ):
        # Generate messages
        messages = [
            {
                "role": "system", 
                "content": system_role
            },
            {
                "role": "user", 
                "content": prompt
            }
        ]

        try:
            if self.verbose: print("Sending message...")

            # Create a request to the GPT model
            completion = self.client.chat.completions.create( 
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=randomness,
                n=n_responses
            )

            if self.verbose: print("Received response.")

            # Extract response from completion first choice
            return completion.choices[0].message.content

        except OpenAIError as e:
            if self.verbose: print(f"Chat completion failed: {e}.")

            return "" # Return empty string
        
variable = 10