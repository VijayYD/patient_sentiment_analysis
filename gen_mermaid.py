import google.genai as genai
import os
from google.genai import Client, types

# --- Configuration ---
# You need to set your API key as an environment variable
# or replace os.getenv("GEMINI_API_KEY") with your actual API key string.
# NEVER hardcode your API key in production code!
os.environ["GEMINI_API_KEY"] = "AIzaSyC6wjp4A7lNky9I85DdKQad_LnX2a4UHpM"
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set. Please set your API key.")

client = Client()

# --- Choose your model ---
# Use the appropriate model for your needs. 'gemini-pro' is a good general-purpose model.
# For more detailed model information, refer to the Google AI documentation.
#model = genai.GenerativeModel('gemini-pro') # Or 'gemini-1.5-flash-latest' if you have access

def generate_mermaid_diagram_syntax(diagram_type, scenario_description):
    """
    Generates Mermaid diagram syntax based on the scenario description.
    """
    prompt = f"Generate a Mermaid {diagram_type} diagram syntax for the following scenario: {scenario_description}"
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Content(
                parts=[
                    types.Part(text=prompt)
                ]
            )
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.2,
        )
    )
    return response.text

def generate_test_cases(functionality_description):
    """
    Generates test cases based on the functionality description, formatted as a markdown table.
    """
    prompt = f"""
    Generate detailed test cases for the "{functionality_description}" functionality of an online banking system.
    Include positive, negative, and edge cases.
    Format them as a markdown table with columns: Test Case ID, Feature, Test Objective, Preconditions, Test Steps, Expected Result.
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Content(
                parts=[
                    types.Part(text=prompt)
                ]
            )
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.2,
        )
    )
    return response.text

# --- Example Usage ---
if __name__ == "__main__":
    banking_scenario_class = """
    An online banking system with classes: User (userID, username, password, login(), logout()),
    Account (accountID, accountNumber, balance, accountType, deposit(), withdraw(), getBalance()),
    Transaction (transactionID, fromAccount, toAccount, amount, timestamp, type, recordTransaction()).
    Relationships: User has many Accounts, Account records many Transactions.
    """
    banking_scenario_sequence = """
    A user logs into an online banking system, navigates to the fund transfer page,
    enters transfer details, and the system processes the transfer involving
    web browser, web server, application layer, database, and an external bank system.
    """
    login_functionality = "Login"
    fund_transfer_functionality = "Fund Transfer"

    print("Generating Mermaid Class Diagram Syntax...")
    class_diagram_syntax = generate_mermaid_diagram_syntax("class", banking_scenario_class)
    print("\n--- Mermaid Class Diagram Syntax ---\n")
    print(class_diagram_syntax)
    print("\n-----------------------------------\n")

    print("Generating Mermaid Sequence Diagram Syntax...")
    sequence_diagram_syntax = generate_mermaid_diagram_syntax("sequence", banking_scenario_sequence)
    print("\n--- Mermaid Sequence Diagram Syntax ---\n")
    print(sequence_diagram_syntax)
    print("\n-------------------------------------\n")

    print("Generating Test Cases for Login...")
    login_test_cases = generate_test_cases(login_functionality)
    print("\n--- Login Test Cases ---\n")
    print(login_test_cases)
    print("\n-------------------------\n")

    print("Generating Test Cases for Fund Transfer...")
    transfer_test_cases = generate_test_cases(fund_transfer_functionality)
    print("\n--- Fund Transfer Test Cases ---\n")
    print(transfer_test_cases)
    print("\n------------------------------\n")

    print("To visualize the diagrams, copy the Mermaid syntax into the Mermaid Live Editor (https://mermaid.live/).")