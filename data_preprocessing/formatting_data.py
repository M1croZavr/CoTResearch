from __future__ import annotations

from pathlib import Path
import numpy as np
import re
import json


class FormattedPrompts:
    """
    Samples and stores formatted prompts for model to generate from
    """

    def __init__(
            self, data_path: str | Path, n_exemplars: int, random_seed: int = 123, calc_annotations: bool = False
    ) -> None:
        self.data_path = data_path
        self.n_exemplars = n_exemplars
        self.random_seed = random_seed
        self.calc_annotations = calc_annotations
        self.prompts = ''

    def sample_prompts(self) -> str:
        """
        Samples prompts from data file according to parameters
        Returns:
            prompts (str): total string of chains of thought
        """
        with open(self.data_path) as file:
            json_lines = file.readlines()
        for json_line_idx in self.__get_exemplars_indices(len(json_lines)):
            exemplar = json.loads(json_lines[json_line_idx])
            question = self.preprocess_text(exemplar['question'])
            answer = self.preprocess_text(exemplar['answer'])
            prompt = f'Q: {question}\nA: {answer}.\n\n'
            self.prompts += prompt
        return self.prompts

    def __get_exemplars_indices(self, n_total: int) -> np.ndarray:
        """
        Generates random indices for sampling prompts
        Parameters:
            n_total (int): total number of lines in data file
        Returns:
            random_indices (np.ndarray): array containing indices
        """
        np.random.seed(self.random_seed)
        random_indices = np.random.randint(0, n_total, (self.n_exemplars, ))
        return random_indices

    def preprocess_text(self, text: str) -> str:
        """
        Preprocesses text before adding to a prompt
        Parameters:
            text (str): text to preprocess
        Returns:
            preprocessed text
        """
        if not self.calc_annotations:
            text = re.sub(r'<<.+>>', '', text)
        text = text.replace('.\n####', '. The answer is ').replace('\n####', '. The answer is ')
        text = text.replace('.\n', '. ').replace('\n', '. ')
        text = text.replace('  ', ' ')
        return text


class FormattedInputs:
    """
    Preprocesses and stores ground truths and inputs for text generation
    """

    def __init__(self, formatted_prompts: FormattedPrompts) -> None:
        self.formatted_prompts = formatted_prompts
        self.inputs = []
        self.ground_truths = []

    def sample_input(self, data_point: str) -> str:
        """
        Samples input and gt from data point
        Parameters:
            data_point (str): data point (json line of GSM8K dataset)
        Returns:
            input (str): input for the language model to generate from
        """
        exemplar = json.loads(data_point)
        question = self.formatted_prompts.preprocess_text(exemplar['question'])
        answer = self.formatted_prompts.preprocess_text(exemplar['answer'])
        input_ = f'{self.formatted_prompts.prompts}Q: {question}\nA: '
        self.inputs.append(input_)
        self.ground_truths.append(answer)
        return input_


if __name__ == '__main__':
    prompts = FormattedPrompts(Path('../GSM8K_data/train_data.jsonl'), 2, calc_annotations=True)
    prompts.sample_prompts()
    some_inputs = FormattedInputs(prompts)
    with open(Path('../GSM8K_data/test_data.jsonl')) as file:
        print(some_inputs.sample_input(file.readline()))
        print(some_inputs.ground_truths[-1])
    with open(Path('../GSM8K_data/test_data.jsonl')) as file:
        print(len(file.readlines()))
    with open(Path('../GSM8K_data/train_data.jsonl')) as file:
        print(len(file.readlines()))
