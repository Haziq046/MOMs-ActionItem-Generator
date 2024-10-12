import streamlit as st
import os
from dotenv import load_dotenv
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT  # Import Anthropic's API

# Load environment variables from the .env file
load_dotenv()

# Access the Claude API key
claude_api_key = os.getenv('CLAUDE_API_KEY') or st.secrets["claude"]["api_key"]

# Initialize the Claude client
claude = Anthropic(api_key=claude_api_key)

# Streamlit app title
st.title("Minutes of Meeting & Action Item Extractor")

# Input text box for meeting text with placeholder instead of pre-filled text
meeting_text = st.text_area(
    "Enter Meeting Text",
    placeholder="Type or paste your meeting notes here...")

# CSS to style the button
st.markdown("""
    <style>
    div.stButton > button:first-child {
        display: block;
        margin: 0 auto;
        background-color: #ADD8E6;
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

# Centered and styled Generate button
if st.button("Generate MOM and Action Items"):
    if meeting_text:
        with st.spinner("Processing..."):
            # Calculate the max word count for the MOM and Action Items (10% of input length)
            max_word_count = int(len(meeting_text.split()) * 0.10)

            # Define the detailed prompt for Claude API with zero-shot instructions
            prompt = (f"As a Natural Language Processing expert, please generate a structured summary from the following meeting notes. "
                      f"The summary should include both Minutes of Meeting (MOM) and Action Items, adhering to the following guidelines:\n\n"
                      f"1. **Concise Output:**\n"
                      f"   - Ensure that the total length of the MOM and Action Items does not exceed {max_word_count} words.\n"
                      f"   - Focus only on key points, providing a brief yet comprehensive summary without additional details or explanation.\n\n"
                      f"2. **Minutes of Meeting (MOM):**\n"
                      f"   - List only the essential outcomes, decisions, and agreements reached in the meeting.\n"
                      f"   - Avoid summarizing discussion points; instead, state the final conclusions or results as the MOM.\n\n"
                      f"3. **Action Items:**\n"
                      f"   - List specific, actionable tasks that arose from the meeting, clearly outlining any responsibilities mentioned.\n"
                      f"   - Each action item should be directly tied to the decisions or outcomes noted in the MOM.\n\n"
                      f"The output should begin with \"MOM:\" followed by numbered points for each item. After MOM, provide the \"Action Items:\" as a separate list, also with numbered points.\n\n"
                      f"Meeting Notes:\n{meeting_text}\n\n"
                      f"Generate the MOM and Action Items based on these instructions.")

            try:
                # Use the Claude API to get a response
                response = claude.completions.create(
                    model="claude-v1",
                    prompt=f"{HUMAN_PROMPT} {prompt} {AI_PROMPT}",
                    max_tokens=1000,  # Adjust as needed
                    temperature=0.7
                )

                # Extract the response text
                output = response['completion'].strip()

                # Display the results
                st.subheader("Minutes of the Meeting (MOM)")
                st.write(output.split("Action Items:")[0].strip())

                st.subheader("Action Items")
                action_items = output.split("Action Items:")[1].strip() if "Action Items:" in output else "No action items identified."
                st.write(action_items)

            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter the meeting text before generating MOM and Action Items.")
