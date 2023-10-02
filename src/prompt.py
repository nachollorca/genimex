from src.property import Property
import openai
import tiktoken
import streamlit as st
import os

openai.api_key = os.getenv('OPENAI_API_KEY') if os.getenv('OPENAI_API_KEY') is not None else st.secrets('OPENAI_API_KEY')
token_cost = {
    ("gpt-3.5-turbo", "input"): 0.0015 / 1000,
    ("gpt-4", "input"): 0.03 / 1000,
    ("gpt-3.5-turbo", "output"): 0.02 / 1000,
    ("gpt-4", "output"): 0.06 / 1000,
}

class Prompt:
    def __init__(
            self,
            property: Property,
            voice_tone: list = [],
            sentences: int = 4,
            paragraphs: int = 1,
            prompts: dict = {},
            style: str = None,
            use: list = [],
            avoid: list = [],
            model: str = "gpt-4",
    ):
        self.property = property.clear_nulls()
        self.voice_tone = voice_tone
        self.sentences = sentences
        self.paragraphs = paragraphs
        self.use = use
        self.avoid = avoid
        self.model = model
        self.style = style
        self.prompts = prompts


    def gen_summary(self) -> str:
        print(type(self.property))
        text = f"""
            Your task is to write a text describing the property whose data is shown delimited by backticks in this python dictionary:
            `{vars(self.property)}`
            Write exactly {self.paragraphs} paragraph(s), with at most {self.sentences} sentences per paragraph.
            Use a {self.voice_tone} tone of voice and a {self.style} style of writing.
            You do not have to use all of the data in the dictionary.
            """
        if len(self.use) > 0 :
            text = text + f"Make sure to use the word(s) {self.use}"
        if len(self.avoid) > 0:
            text = text + f"Do not use the word(s) {self.avoid}"

        self.prompts["summary"] = {}
        self.prompts["summary"]["text"] = {}
        self.prompts["summary"]["text"]["input"] = text
        return text

    def gen_location(self) -> str:
        text = f"""
            Your task is to write a text about the virtues of living in a property whose location information is shown delimited by backticks in this python dictionary:
            `{self.property.location}`
            Write exactly {self.paragraphs} paragraph(s), with at most {self.sentences} sentences per paragraph.
            Use a {self.voice_tone} tone of voice and a {self.style} style of writing.
            """
        if len(self.use) > 0 :
            text = text + f"Make sure to use the word(s) {self.use}"
        if len(self.avoid) > 0:
            text = text + f"Do not use the word(s) {self.avoid}"

        if "neighbourhood" in self.property.location.keys():
            text = text + f"Focus on the qualities of {self.property.location['neighbourhood']}"

        self.prompts["location"] = {}
        self.prompts["location"]["text"] = {}
        self.prompts["location"]["text"]["input"] = text
        return text


    def launch_prompt(self, section: str) -> str:
        input_text = self.prompts[section]["text"]["input"]

        cost = self.get_cost(input_text, "input")
        self.prompts[section]["cost"] = {}
        self.prompts[section]["cost"]["input"] = cost
        st.write(f"This prompt costs ca. {round(cost, 5)} $ to compute")

        messages = [{"role": "user", "content": input_text}]

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=0.9,  # this is the degree of randomness of the model's output
        )
        output_text = response.choices[0].message["content"]
        self.prompts[section]["text"]["output"] = output_text

        cost = self.get_cost(output_text, "output")
        self.prompts[section]["cost"]["output"] = cost
        st.write(f"This answer costs ca. {round(cost,5)} $ to compute")

        return output_text


    def get_cost(self, text: str, mode: str) -> float:
        encoding = tiktoken.encoding_for_model(self.model)
        num_tokens = len(encoding.encode(text))
        cost = num_tokens * token_cost[(self.model, mode)]
        return cost

