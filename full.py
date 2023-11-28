import base64
import io
from os import environ
import pyautogui
import pygetwindow
import time, datetime
import requests

# Function to encode the image
def encode_image(image):
    image_byte_array = image.tobytes()
    return base64.b64encode(image_byte_array).decode('utf-8')

# Define the window title or identifier
window_title = "Rusty Pong"

# OpenAI API Key
api_key = environ["OPENAI_API_KEY"]

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}
PROMPT = "Which direction should the right paddle move? Respond only with \"up\" or \"down\" or \"stay\"."

response = None

while True:
    # Get a list of all windows with the specified title
    windows = pyautogui.getWindowsWithTitle(window_title)
    if windows:
        target_window = windows[0]
        target_window.activate()

        # Wait for a moment to ensure the window is activated
        time.sleep(0.1)

        # Capture the screenshot of the active window
        screenshot = pyautogui.screenshot(region=target_window.box)
        
        buffer = io.BytesIO()
        screenshot.save(buffer, format="JPEG")
        timestamp = time.strftime("%Y%m%d%H%M%S")
        screenshot.save(f"imgs/screenshot_{timestamp}.png")

        base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
        # print(base64_image)

        # Define the message payload for OpenAI Chat API
        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": PROMPT
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }

        # Send the payload to OpenAI Chat API
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        # break
        # Print the response from OpenAI
        # print(response.json())
        c = response.json()['choices'][0]['message']['content'].lower()
        if c == 'up':
            pyautogui.keyUp('down')
            pyautogui.keyDown('up')
        elif c == 'down':
            pyautogui.keyUp('up')
            pyautogui.keyDown('down')
        elif c == 'stay':
            pyautogui.keyUp('up')
            pyautogui.keyUp('down')

        print(f"[{datetime.datetime.now()}]: {c}")

    else:
        print("Window not found")
        break  # Exit the loop if the window is not found

