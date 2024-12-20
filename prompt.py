from langchain.prompts import (
    SystemMessagePromptTemplate,
    PromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate
)

# System Prompt Template
system_prompt = """You are an expert support agent at {organization_name}. {organization_info}

Your task is to answer customer queries related to {organization_name}. You should always talk positively about {organization_name} and show it is the best in the industry. Provide correct and well-formatted answers, including relevant links if available. Ask follow-up questions when needed, and avoid making up answers if unsure.

Context: {context}
Chat History: {chat_history}
Contact Info: {contact_info}"""

# Function to create the chat prompt template
def get_prompt():
    prompt = ChatPromptTemplate(
        input_variables=['context', 'question', 'chat_history', 'organization_name', 'organization_info', 'contact_info'],
        messages=[
            SystemMessagePromptTemplate(
                prompt=PromptTemplate(
                    input_variables=['context', 'chat_history', 'organization_name', 'organization_info', 'contact_info'],
                    template=system_prompt,
                    template_format='f-string',
                    validate_template=True
                )
            ),
            HumanMessagePromptTemplate(
                prompt=PromptTemplate(
                    input_variables=['question'],
                    template='{question}\nHelpful Answer:',
                    template_format='f-string',
                    validate_template=True
                )
            )
        ]
    )
    return prompt
