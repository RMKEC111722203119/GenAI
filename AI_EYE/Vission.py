import cv2
import hashlib
import google.generativeai as genai
from PIL import Image
import io
import pyttsx3
import streamlit as st

# Initialize previous_image_hash globally
previous_image_hash = None

def speak_fast(text):
  
  engine = pyttsx3.init()
  engine.setProperty('rate', engine.getProperty('rate') * 0.8)
  voices = engine.getProperty('voices')
  engine.setProperty('voice', voices[0].id) 
  engine.say(text)
  engine.runAndWait()
  engine.stop()
  #engine.shutdown()

def get_image_hash(image):
    """
    Calculates a perceptual hash for the image.
    """
    # Convert to grayscale and resize to a smaller size for hashing
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (8, 8), interpolation=cv2.INTER_AREA)
    avg = resized.mean()
    hash_string = ''.join(['1' if i > avg else '0' for i in resized.flatten()])
    return hashlib.sha256(hash_string.encode()).hexdigest()

def describe_image_with_gemini(image, previous_image_hash):
    """
    Uses Gemini Pro Vision to describe the image, considering similarity.
    """


    # Convert image to RGB and encode as bytes
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image_rgb)

    # Convert PIL Image to bytes
    image_bytes = io.BytesIO()
    pil_image.save(image_bytes, format='JPEG')
    image_bytes = image_bytes.getvalue()

    # Initialize Gemini model
    genai.configure(api_key=st.secrets["your_api"]) # Set your API key here
    model = genai.GenerativeModel('gemini-1.5-flash')
    

    if not previous_image_hash or previous_image_hash != get_image_hash(image):
        # Generate description if no previous image or if the image has changed
        
        description = "Do not mention input as photo or image instead say you are watching if required.You are viki who acts as a eye for user.Your output should not prolong more than 4 seconds."
        response = model.generate_content(
            [pil_image,description],
        )
        previous_image_hash = get_image_hash(image)
        return response.text
    

def ImageDescription(frame):
    """
    Processes the captured frame, calculates hash, and generates description.
    """
    descr = describe_image_with_gemini(frame, previous_image_hash)
    st.write(descr)
    print(descr)
    speak_fast(descr)

def capture_and_process_image():
    """
    Captures video frames and calls the description function for each frame.
    """
    # Open the camera
    cap = cv2.VideoCapture()
    if not cap.isOpened():
        print("Error: Cannot open camera")
        return
    
    speak_fast("Hello I am Viki your AI assistant. I am ready to be your AI eye.")
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame")
            break
        
        # Display the resulting frame
        cv2.imshow('frame', frame)
        
        # Process the captured image
        ImageDescription(frame)
    
        
        # Wait for a key press or time interval
        if cv2.waitKey(10000) & 0xFF == ord('q'):  # 10 seconds interval
            break
    
    # When everything done, release the captureq111
    cap.release()
    cv2.destroyAllWindows()

def stlit():
    st.title("VIKI AI VISION")
    st.write("Welcome to VIKI Vision! This is an AI assistant that describes the live video feed from your camera.")
    

    # Add a button to start the live video feed
    capture_and_process_image()
        
if __name__ == "__main__":
        stlit()
           
    
