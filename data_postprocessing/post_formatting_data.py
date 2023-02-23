import re
import json
from collections import Counter


class AnswersList(list):
    """
    List consisting of predicted answers and ground truth samples
    """

    def add_answer(self, predicted_answers: str, gt_answer: str) -> None:
        """
        Adds answer to the list
        Parameters:
            predicted_answers (str): string or list of text generations
            gt_answer (str): string of ground truth answer
        Returns:
            None
        """
        digits = {str(digit) for digit in range(10)}
        answer_is_re = re.compile(r'the answer is[^\d+-]*([+-]?\d+[.,]?\d*)\D*')
        common_re = re.compile(r'[^\d+-]*([+-]?\d+[.,]?\d*)\D*')
        predicted_answer_number = []
        if not isinstance(predicted_answers, list):
            predicted_answers = [predicted_answers]
        for predicted_answer in predicted_answers:
            if 'Q:' in predicted_answer:
                predicted_answer = predicted_answer.split('Q:')[-1]
            if 'A:' in predicted_answer:
                predicted_answer = predicted_answer.split('A:')[-1]
            if not any(digit in predicted_answer for digit in digits):
                predicted_answer_number.append(None)
            else:
                try:
                    predicted_answer_number.append(answer_is_re.findall(predicted_answer.lower())[-1])
                except IndexError:
                    predicted_answer_number.append(common_re.findall(predicted_answer.lower())[-1])
        try:
            gt_answer_number = answer_is_re.findall(gt_answer.lower())[-1]
        except IndexError:
            gt_answer_number = common_re.findall(gt_answer.lower())[-1]
        self.append(
            {
                'predicted_answers': predicted_answers,
                'predicted': predicted_answer_number,
                'ground_truth': gt_answer_number
            }
        )

    def write_to_file(self, filename: str) -> None:
        """
        Writes result in jsonl format file
        Parameters:
            filename (str): filename to save
        """
        with open(filename, "w") as file:
            file.writelines([json.dumps(jsonable) + '\n' for jsonable in self])

    def calculate_accuracy(self) -> float:
        """
        Calculates accuracy for the values of list
        Returns:
            accuracy (float): total accuracy
        """
        correct_counter = 0
        total_counter = 0
        if not self:
            return None
        else:
            for example in self:
                if self.__prediction_gt_eq(example['predicted'], example['ground_truth']):
                    correct_counter += 1
                total_counter += 1
        return correct_counter / total_counter

    @staticmethod
    def __prediction_gt_eq(prediction: list, gt: str) -> bool:
        """
        Equality of prediction and gt samples
        Parameters:
            prediction (list): list of predictions
            gt (str): ground truth sample
        Returns:
            true if equal else False
        """
        max_value = Counter(prediction).most_common(1)[0][0]
        gt = gt.replace(',', '.')
        max_value = max_value.replace(',', '.')
        try:
            prediction = float(max_value)
            gt = float(gt)
        except ValueError:
            prediction = max_value
        return prediction == gt


if __name__ == '__main__':
    predicted_one = ' Keegan earned $83 in 3 hours, so he earned $83 / 3 = $27 per hour. Tasha earned $91 in 3 hours, so she earned $91 / 3 = $28 per hour. They need to earn $200 / 2 = $100 for the two of them. So they need to earn $27 + $28 = $55 per hour. $55 / 3 = $17.5. The answer is $17.5.\n\n'
    gt_one = 'Janet sells 16 - 3 - 4 = 9 duck eggs a day. She makes 9 * 2 = $18 every day at the farmer’s market. The answer is 18'
    answers_list = AnswersList()
    answers_list.add_answer(
        predicted_one,
        gt_one
    )
    print(answers_list)
    print(answers_list.calculate_accuracy())
    answers_list.write_to_file("../test.jsonl")
