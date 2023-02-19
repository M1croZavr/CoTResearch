import re


class AnswersList(list):

    def add_answer(self, predicted_answers: str, gt_answer: str) -> None:
        predicted_answer_number = []
        if not isinstance(predicted_answers, list):
            predicted_answers = [predicted_answers]
        for predicted_answer in predicted_answers:
            if 'Q:' in predicted_answer:
                predicted_answer = predicted_answer.split('Q:')[-1]
            if 'A:' in predicted_answer:
                predicted_answer = predicted_answer.split('A:')[-1]
            try:
                predicted_answer_number.append(re.findall(r'the answer is\D*(\d+)\D*', predicted_answer.lower())[-1])
            except IndexError:
                predicted_answer_number.append(re.findall(r'\D*(\d+)\D*', predicted_answer.lower())[-1])
        try:
            gt_answer_number = re.findall(r'the answer is\D*(\d+)\D*', gt_answer.lower())[-1]
        except IndexError:
            gt_answer_number = re.findall(r'\D*(\d+)\D*', gt_answer.lower())[-1]
        self.append({'predicted': predicted_answer_number, 'ground_truth': gt_answer_number})

    def calculate_accuracy(self) -> float:
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
    def __prediction_gt_eq(prediction: str, gt: str) -> bool:
        try:
            prediction = float(prediction)
            gt = float(gt)
        except ValueError:
            pass
        return prediction == gt


if __name__ == '__main__':
    predicted_one = 'A:  16 eggs per day * 3 eggs for breakfast = 48 eggs per day. 48 eggs per day * 4 eggs per muffin = 192 eggs per day. 192 eggs per day * $2 per egg = $384 per day. The answer is $384.'
    gt_one = 'Janet sells 16 - 3 - 4 = 9 duck eggs a day. She makes 9 * 2 = $18 every day at the farmer’s market. The answer is 18'
    answers_list = AnswersList()
    answers_list.add_answer(
        predicted_one,
        gt_one
    )
    print(answers_list.calculate_accuracy())
