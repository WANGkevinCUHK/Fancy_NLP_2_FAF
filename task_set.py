import csv


def setup_tasklist(file_name, task_numbers):
    r"""
    从sample中提取任务名字
    :param task_numbers:
    :param file_name:
    :return:
    """
    with open(file_name, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader, None)
        for row in csv_reader:
            first_colum = row[0]
            task_token = first_colum[:4]
            task_numbers.append(f"{task_token}")


def find_task_rely_file(task_id, file_name, curr_task_dict):
    r"""
    搭建任务
    :param curr_task_dict:
    :param task_id:
    :param file_name:
    :return:
    """

    task_token = f"{task_id}.HK"
    curr_task_dict["task_token"] = task_token
    with open(file_name, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row[0] == task_token:
                curr_task_dict["basic_report"] = row[1]
                middle_and_annual = row[2].split('\n')
                if len(middle_and_annual) >= 2:
                    curr_task_dict["middle_report"] = middle_and_annual[0]
                    curr_task_dict["annual_report"] = middle_and_annual[1]
                else:
                    curr_task_dict['middle_report'] = row[2]
                curr_task_dict["report_base"] = row[3]
                return None

