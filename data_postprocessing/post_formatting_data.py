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
        # answer_is_re = re.compile(r'the answer is[^\d+-]*([+-]?\d+[.,]?\d*)\D*')
        common_re = re.compile(r'[^+\-\d]*([+-]?\d+[.,]\d+|[+-]?\d+)[^+\-\d]*')
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
                continue
            if 'the answer is' in predicted_answer.lower():
                predicted_answer = predicted_answer.lower().split('the answer is')[-1]
            predicted_answer_number.append(common_re.findall(predicted_answer.lower())[-1])
            # else:
            #     try:
            #         predicted_answer_number.append(answer_is_re.findall(predicted_answer.lower())[-1])
            #     except IndexError:
            #         predicted_answer_number.append(common_re.findall(predicted_answer.lower())[-1])
        if 'the answer is' in gt_answer.lower():
            gt_answer = gt_answer.lower().split('the answer is')[-1]
        gt_answer_number = common_re.findall(gt_answer.lower())[-1]
        # try:
        #     gt_answer_number = answer_is_re.findall(gt_answer.lower())[-1]
        # except IndexError:
        #     gt_answer_number = common_re.findall(gt_answer.lower())[-1]
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
    predicted1 = 'keawieajw. The answer is 10 + 1 = 11. '
    predicted2 = 'sadwaw. The answer is $10.\n\n'
    predicted3 = 'dads. The answer is -10.\n\n'
    predicted4 = 'dawwwg. faw. The answer is 18.5'
    predicted5 = 'dawi. The answer is 9,357'
    predicted6 = 'dsdawd. The answer is 999.\n\n'
    predicted7 = 'keke. The answer is -8000/10 = -800. \n\n'
    predicted8 = 'weake. The answer is 11 + 8 + 16 = 31 slices. \n\n'
    predicted9 = 'sadwdaw. 10 + 1 = 12'
    gt_one = 'Keafijwafjagw. The answer is 100.\n\n'
    answers_list = AnswersList()
    answers_list.add_answer(predicted1, gt_one)
    answers_list.add_answer(predicted2, gt_one)
    answers_list.add_answer(predicted3, gt_one)
    answers_list.add_answer(predicted4, gt_one)
    answers_list.add_answer(predicted5, gt_one)
    answers_list.add_answer(predicted6, gt_one)
    answers_list.add_answer(predicted7, gt_one)
    answers_list.add_answer(predicted8, gt_one)
    answers_list.add_answer(predicted9, gt_one)

    print(answers_list)
    print(answers_list.calculate_accuracy())
    answers_list.write_to_file("../test.jsonl")
