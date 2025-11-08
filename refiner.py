import google.generativeai as genai
from dotenv import load_dotenv
import os
import time
import logging
from datetime import datetime

# Load environment variables
load_dotenv()
API_KEY = os.environ.get("Gem_api3")
if not API_KEY:
    raise ValueError("Gem_api3 not found in .env file")

genai.configure(api_key=API_KEY)

# Model & folders
MODEL_NAME = "gemini-2.5-flash-lite"
INPUT_FOLDER = "Conv"
OUTPUT_FOLDER = "Refined_Conv"

# Rate limiting (free tier: 15 RPM)
REQUESTS_PER_MINUTE = 15
SLEEP_BETWEEN = 60.0 / REQUESTS_PER_MINUTE  # ~4 seconds

# Logging setup
log_file = f"refine_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()  # Also print to console
    ]
)
logger = logging.getLogger()

def read_conversation_file(file_path):
    """Read the conversation script from a text file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().strip()
    
    return content

def refine_conversation(content):
    """Use Gemini to refine the conversation script for Indian context."""
    model = genai.GenerativeModel(MODEL_NAME)
    
    prompt = f"""
    You are an expert scriptwriter specializing in **Indian scam call scenarios** in Hindi-speaking regions (North India, urban & semi-urban settings).

    **TASK**: Refine the given conversation script to make it **100% authentic to Indian context**, including language, culture, currency, references, and scam tactics.

    **MANDATORY OUTPUT FORMAT**:
    1. **First line**: A single-line summary of the scam scenario in English:
    SCENARIO: [Clear, concise description, e.g., "Relative-in-emergency bank details fraud"]
    2. **Then**: The full refined dialogue in the format:
    caller: [Hindi dialogue]
    receiver: [Hindi dialogue]
    **REFINEMENT RULES**:
    - **Identify the scam type** from the script (e.g., bank fraud, tech support, lottery, IRS, KYC, UPI scam).
    - **Preserve core plot**: Scammer builds trust, creates urgency, asks for sensitive info; receiver resists wisely.
    - **Indianize everything**:
    - **Currency**: Euro/Dollar → **Rupees (₹)**, e.g., "500 Euros" → "₹40,000"
    - **Names**: John, Smith → **Rahul, Rajesh, Priya, Anjali**
    - **Locations**: USA, London → **Delhi, Mumbai, Lucknow, Patna**
    - **Institutions**: IRS, FBI → **Income Tax Dept, Cyber Cell, SBI, HDFC**
    - **Apps/Tech**: PayPal, Zelle → **PhonePe, Google Pay, UPI, Paytm**
    - **References**: Add **chai, paan shop, auto-rickshaw, family functions, Aadhaar, PAN**, etc., where natural.
    - **Language**: Natural **Hinglish** (Hindi + English code-switching), regional slang (e.g., *bhaiya, yaar, arey, pakka, jaldi*), emotional tone.
    - **Cultural Nuances**:
    - Caller uses **family bonding** ("bhai, behen, mama ji"), urgency ("emergency hai"), guilt ("tu mera bhai hai na?").
    - Receiver shows **scam awareness** ("ye toh fraud lag raha hai", "cyber cell ko bol dunga"), suggests **meet in person** or **bank visit**.
    - **Length**: 5–8 balanced turns. Concise but vivid. Under 2000 characters total.
    - **Tone**: Caller = manipulative, emotional; Receiver = firm, cautious, polite but smart.

    **Original Script**:
    {content}
"""
    
    while True:
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            error_msg = str(e).lower()
            if "429" in error_msg or "quota" in error_msg:
                logger.warning("Quota exceeded. Waiting 65 seconds before retry...")
                time.sleep(65)
                continue
            else:
                logger.error(f"Gemini API error: {e}")
                raise RuntimeError(f"Error generating response: {e}")

def save_refined_script(refined_content, output_file):
    """Save the refined script to a new text file."""
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(refined_content)
    logger.info(f"Saved: {output_file}")

# Main execution
if __name__ == "__main__":
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    if not os.path.exists(INPUT_FOLDER):
        raise FileNotFoundError(f"Input folder not found: {INPUT_FOLDER}")
    
    conv_files = sorted([
        f for f in os.listdir(INPUT_FOLDER)
        if f.startswith("conv_") and f.endswith(".txt")
    ])
    
    if not conv_files:
        logger.error(f"No conv_*.txt files found in {INPUT_FOLDER}")
    else:
        logger.info(f"Found {len(conv_files)} files to process.")
        
        for idx, filename in enumerate(conv_files, 1):
            input_file = os.path.join(INPUT_FOLDER, filename)
            output_filename = f"refined_{filename}"
            output_file = os.path.join(OUTPUT_FOLDER, output_filename)
            
            try:
                logger.info(f"[{idx}/{len(conv_files)}] Processing: {filename}")
                
                original = read_conversation_file(input_file)
                refined = refine_conversation(original)
                
                # Extract scenario for log
                scenario_line = refined.split('\n')[0] if refined else "Unknown"
                logger.info(f"Scenario: {scenario_line}")

                save_refined_script(refined, output_file)
                
                # Respect rate limit
                if idx < len(conv_files):
                    time.sleep(SLEEP_BETWEEN)
                    
            except Exception as e:
                logger.error(f"Failed {filename}: {e}")
                # Optional: continue or break
                continue

        logger.info("All files processed successfully!")