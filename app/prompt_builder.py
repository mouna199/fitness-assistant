prompt_template = """
You are a fitness coach. Answer the QUESTION based on the CONTEXT.
Use only the facts from the CONTEXT when answering the QUESTION.
If the CONTEXT doesn't contain the answer, output I don't know.

Format your response in a clear, structured way:
- Start with a brief introduction
- Present each exercise in a separate section with:
  • Exercise name as a title
  • Equipment needed
  • Target muscles
  • Clear, step-by-step instructions
- Use simple, encouraging language
- Avoid repetitive technical details

QUESTION: {question}
CONTEXT:
{context}
""".strip()

entry_template = """
**{exercise_name}**


type_of_activity: {type_of_activity}
type_of_equipment: {type_of_equipment}
body_part: {body_part}
type: {type}
muscle_groups_activated: {muscle_groups_activated}
instructions: {instructions}
""".strip()

def build_prompt(results, question):
    context = "\n\n\n".join(entry_template.format(**doc) for doc in results)
    return prompt_template.format(question=question, context=context)
