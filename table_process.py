import csv
import os
import re

DEFAULT_PROMPT_FOR_TABLE = """Please reconstruct the following text into a standard table and notes format, for table, 
    please in csv format, for notes, please in remark format, and demonstrate them in sequential use neighbour code 
    block. Here, you may encounter 2 or more tables, then, see `table + note' as a group. Show different groups in a 
    sequential. When show a group, before the csv and mark down,you need to use a paragraph of txt to summarize the 
    table and notation. The format is: 
    Summary: ```txt\nhere is summary\n```
    Reconstructed table: ```csv\ntitle,title,title\nA,B,C\n```
    Notes: ```md\n1. a [Note 1a]\n   b [Note 1b]\n2. [Note 2]\n```
    Noted that all groups are not necessary. Only groups relating to descriptions of, or changes in, substantial 
    shareholders' holdings are retained. Shareholders here include descriptions of individuals as well as organizations
    such as funds.
    for example, {univ namerankcuh\nk 37 thunote116\nnote1 thu don't cons\nider medicine dept univencodeptrank\nc\nuhknote 119!th\nu5\nnote1
    use dataof cU before 2024}
    then, need to reconstruct and summarize to:
    Group 1:\n
    Summary: ```txt\n this is table group 1, about university total rank ```
    Reconstructed format: ```csv\nuniv name, rank\ncuhk, 37\nthu, 16```
    Notes:```1. thu don't consider medicine dept```
    Group2:\n
    Summary: ```txt\n this is table group 2, about university economics department rank ```
    Reconstructed format: ```csv\nuniv name, rank\ncuhk, 19\nthu, 5```
    Notes:```1. use data of cu before 2024 ```
    Those Groups are not retained because they are not related to shareholder of any company. For groups related to share,
    outputting streamlined language without loss of precision
    """


def design_prompt(task_id, report_name, DEFAULT_CASE=True):
    if DEFAULT_CASE:
        return DEFAULT_PROMPT_FOR_TABLE
    else:
        return None


def prompt_simplified_report(task_id, file_name):
    r"""
    实现prompt化的report文本
    :param task_id:
    :param file_name:
    :return:
    """

    # Extract the report name from the file path
    report_name = os.path.basename(os.path.dirname(file_name))

    # Construct the save directory and file path
    save_dir = os.path.join("Info_txt", task_id, report_name)
    os.makedirs(save_dir, exist_ok=True)

    # Modify the file name to include "prompted_"
    write_file_path = file_name.replace("simplified", "prompted")

    # Extract prompt
    prompt = design_prompt(task_id, report_name)

    # Read the simplified report content

    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"File not found: {file_name}")
        return None

    # Combine prompt and content
    result = f"{prompt}\nNow the content you need to extract is: {{\n{content}\n}}"

    # Write the result to the new file
    with open(write_file_path, 'w', encoding='utf-8') as file:
        file.write(result)
        file.flush()
        os.fsync(file.fileno())
    print(f"Text prompted successfully for task: {task_id}_{report_name}")

    return True


def process_ai_table(task_id, file_name):
    r"""
    Extract AI answers from RESULT_ANS_DOCKER and save to a specified file.
    """

    # Extract the report name from the directory path
    report_name = os.path.basename(os.path.dirname(file_name))

    # Construct the save directory and file path
    save_dir = os.path.join("Info_txt", task_id, report_name)
    os.makedirs(save_dir, exist_ok=True)

    # Modify the file name to include "ai_sorted_"
    write_file_path = file_name.replace("simplified", "ai_sorted")

    # Read the contents of RESULT_ANS_DOCKER
    try:
        with open('RESULT_ANS_DOCKER', 'r', encoding='utf-8') as file:
            ai_content = file.read()
    except FileNotFoundError:
        print("RESULT_ANS_DOCKER file not found.")
        return None

    # Write the AI content to the new file
    with open(write_file_path, 'w', encoding='utf-8') as file:
        file.write(ai_content)
        file.flush()
        os.fsync(file.fileno())
    print(f"AI content processed successfully for task: {task_id}_{report_name}")

    with open('RESULT_ANS_DOCKER', 'w', encoding='utf-8') as file:
        file.write("")
        file.flush()
        os.fsync(file.fileno())
    print("RESULT_ANS_DOCKER has been cleared.")

    return True


if __name__ == "__main__":
    pass
    #prompt_simplified_report("0011", "Info_txt/0011/annual_report/simplified_annual_report_1.txt")
    #prompt_simplified_report("0011", "Info_txt/0011/annual_report/simplified_annual_report_2.txt")
    #process_ai_table("0011", "Info_txt/0011/annual_report/simplified_annual_report_2.txt")