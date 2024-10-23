import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import os
from dotenv import load_dotenv


# Load environment variables from the .env file
load_dotenv()

# Access the OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY') or st.secrets["openai"]["api_key"]

# Now you can use the openai_api_key in your application
print(f"Your OpenAI API key is: {openai_api_key}")

# Initialize the LangChain ChatOpenAI instance
chat = ChatOpenAI(model="gpt-4o-2024-08-06", openai_api_key=openai_api_key)

# Streamlit app title
st.title("AI Model Generating Minutes of Meeting (MoM) and Action Items")

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

            # Define the detailed prompt for LangChain ChatOpenAI with zero-shot instructions
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
                # Create a message for the conversation using HumanMessage schema
                messages = [HumanMessage(content=prompt)]

                # Generate response using LangChain ChatOpenAI
                response = chat(messages)

                # Extract the response text
                output = response.content.strip()

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
