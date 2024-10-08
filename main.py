import os

from table_process import *
from task_set import *
from text_reterive import *
from ai_ans_process import *

TYPE = "P"

DOCUMENT_FILENAME = "url_file/faf_documents.csv"

INDEX = 11

TASK_NUMBERS = []
CURR_TASK_DICT = {}


def set_env_up():
    setup_tasklist(DOCUMENT_FILENAME, TASK_NUMBERS)


def perform_one_task(task_id):
    find_task_rely_file(task_id, DOCUMENT_FILENAME, CURR_TASK_DICT)
    print(CURR_TASK_DICT)
    for i in range(2, 4):
        Key_list = list(CURR_TASK_DICT.keys())
        download_and_convert_pdf(CURR_TASK_DICT[Key_list[i]], task_id, Key_list[i])
        for j in range(1, 3):
            file_name = os.path.join("Info_txt", task_id, Key_list[i], f"simplified_{Key_list[i]}_{j}.txt")
            prompt_simplified_report(task_id, file_name)
            input("Press Enter to continue for Prompt level 1: table...")
            process_ai_table(task_id, file_name)
        ai_file_name = os.path.join("Info_txt", task_id, Key_list[i], f"ai_sorted_{Key_list[i]}.txt")
        prompt_ai_ans(task_id, ai_file_name)
        input("Press Enter to continue for Prompt level 2: message...")
        process_ai_message(task_id, ai_file_name)
    prompt_ai_FAF(task_id)
    input("Press Enter to continue for Prompt level 3: FAF...")
    process_FAF(task_id)



def validation_code():
    pass
    # setup_tasklist(DOCUMENT_FILENAME, TASK_NUMBERS)
    # find_task_rely_file("0002",DOCUMENT_FILENAME,CURR_TASK_DICT)
    # print(CURR_TASK_DICT)

    # create_table_prompt_csv()
    # process_ai_ans("0038", "Middle_report")


if __name__ == '__main__':
    if TYPE == "P":
        set_env_up()
        perform_one_task("0806")
        #process_FAF("0806")

    else:
        validation_code()
