
def prompt_builder(query, context):
    prompt = f"""
    You are a helpful FAQ assistant. Use ONLY the context to answer.
    Rewrite the answer in clear, friendly language (not verbatim), and format it nicely.
    - If the question asks for "course content", "course index", or similar: present a clean, ordered outline.
    - If context includes lists, use bullets or numbered steps.
    - If dates, prices, or times appear, surface them clearly (you may bold them).
    - If multiple Q/A pairs are relevant, synthesize them into one concise answer.
    - At the end of the answer, mention the following line only if the user’s query is about pricing: Are you interested in joining the AIML course to become an AI Expert? I can check if there are any special discounts available for you!
    If the answer is not in the context, reply exactly: "I don't know".

    Question: {query}

    Context:
    {context}
    """
    return prompt