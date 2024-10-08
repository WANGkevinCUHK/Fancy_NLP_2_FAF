import os

DEFAULT_PROMPT_FOR_MESSAGE = """" We are trying to trace the a company's shareholding structure and its changes, 
we have a txt file recording such information, any ``Group`` information is a description of company's shareholding 
structure or its changes consist of 3 parts, summary, main csv table, notation, where summary explain what the 
``Group`` do. main csv table is the record the current shareholding structure or the change of the current 
shareholding structure. The notation is an explanation of some entries in the main CSV table, to help us understand 
the true shareholding structure of the company, which may have: (1) Notation of a person to say he control a company 
in the CSV table (2) Notation of a company to indicate it holds shares through its subsidiaries (3) Notation to 
clarify cross-shareholding relationships between companies (4) Notation to explain indirect shareholding through 
multiple layers of companies (5) Notation to explain complex financial instruments that may convert to shares{We 
don't care about the difference between the different shares, we only care about shares end up in the hands of what 
company or whoever.}. Ultimately, you need to construct a txt file consist of entities, overview and message, 
where entities is a summary of person or company we mention in the input file in the order of equity/share percentage, we care about the shares in his hands,
overview is a overview of the share hold structure at this time, in the order of equity/share percentage. Message is change of share hold structure at this 
time. If we do not overview, then we need message, otherwise, if we do have overview now, we only need a little important 
message. Here, because our content is a combination of two files, it is possible that the same table separated 
into two groups, so you can consider the corresponding two groups merged together. Here is the format: Time:{2023.6 
if it is a middle report, 2022.12 if it is a annual report, otherwise it will be specified} Entities: ```txt\n A [
actual controller, control B company ]\n B[intermediate controller`]``\n Overview ```csv\nEntity, share number, 
per at now\nA, 10000, 10%``` Message ```txt\nA sell 5% of share (through reduce holdings by B)``` here is a real 
world example: { Group 1: Summary: ```txt This table shows the long positions in shares or underlying shares of the 
company held by substantial shareholders as of June 30, 2023. ``` Reconstructed table: ```csv Name of shareholder,
Nature of interest,Total number of Shares/underlying shares,Approximate percentage in shareholding 6 Dimensions 
Capital,Beneficial interest,119890000,17.36% 6 Dimensions Affiliates,Beneficial interest,6310000,0.91% 6 Dimensions 
Capital GP LLC,Interest in controlled corporation,126200000,18.27% Suzhou Frontline II,Beneficial interest,88340000,
12.79% Suzhou Fuyan Venture Capital Management Partnership (Limited Partnership),Interest in controlled corporation,
88340000,12.79% Suzhou 6 Dimensions,Beneficial interest,37860000,5.48% Suzhou Tongyu Investment Management 
Partnership (Limited Partnership),Interest in controlled corporation,37860000,5.48% Suzhou Yunchang Investment 
Consulting Co. Ltd.,Interest in controlled corporation,126200000,18.27% Ziqing CHEN,Interest in controlled 
corporation,126200000,18.27% Summer Iris Limited,Beneficial interest,78214230,11.32% Boyu Capital Fund IV L.P.,
Interest in controlled corporation,78214230,11.32% Boyu Capital General Partner IV Ltd.,Interest in controlled 
corporation,78214230,11.32% Boyu Capital Group Holdings Ltd.,Interest in controlled corporation,81629730,11.82% TLS 
Beta Pte. Ltd.,Beneficial interest,54169400,7.84% Temasek Life Sciences Private Limited,Interest in controlled 
corporation,54169400,7.84% Fullerton Management Pte Ltd,Interest in controlled corporation,54169400,7.84% Temasek 
Holdings (Private) Limited,Interest in controlled corporation,59446400,8.61% Capital Research and Management Company,
Beneficial interest,47735966,6.91% The Capital Group Companies Inc.,Interest in controlled corporation,47735966,
6.91% ```Notes: ```md 1. The calculation is based on the total number of 690,711,280 Shares in issue as of June 30, 
2023. 2. 6 Dimensions Capital GP, LLC, as the general partner of each of 6 Dimensions Capital and 6 Dimensions 
Affiliates, is deemed to have an interest in the Shares held by each of 6 Dimensions Capital and 6 Dimensions 
Affiliates. 3. Suzhou Fuyan Venture Capital Management Partnership (Limited Partnership) is the general partner of 
Suzhou Frontline II… 4. Boyu Capital Fund IV, L.P. (as the sole shareholder of Summer Iris Limited), Boyu Capital 
General Partner IV, Ltd. (as the general partner of Boyu Capital Fund IV, L.P.) … 5. Boyu Capital Group Holdings Ltd. 
is deemed to have an interest in the 3,415,500 Shares held … 6. TLS Beta Pte. Ltd. is a wholly-owned subsidiary of 
Temasek Life Sciences Private Limited, which is in turn a wholly-owned subsidiary of Fullerton Management Pte Ltd, 
which is in turn a wholly-owned subsidiary of Temasek Holdings (Private) Limited. Under the SFO, Temasek Life 
Sciences Private Limited, Fullerton Management Pte Ltd and Temasek Holdings (Private) Limited are deemed to be 
interested in the 54,169,400 Shares held by TLS Beta Pte. Ltd. 7. Temasek Holdings (Private) Limited is deemed to 
have an interest in the 5,277,000 Shares held by Aranda Investments Pte. Ltd., which in turn is ultimately controlled 
by Temasek Holdings (Private) Limited. 8. Capital Research and Management Company is a wholly-owned subsidiary of The 
Capital Group Companies, Inc. The Capital Group Companies, Inc. is deemed to have an interest in the 47,735,
966 Shares held by Capital Research and Management Company. ```} The output is:{ Time:{2023.6} Entities: ```txt\n [1] 
6 Dimensions [actual controller by 6 Dimensions Capital and 6 Dimensions affiliates] [2] Suzhou and Ziqing Chen  [
actually controller by Suzhou Fuyan and Suzhou yunchang and Suzhou Tongyu]… Overview:```csv\n Entities, share number, 
per of share\n 6 dimension, 12620000, 18.26%\n....``` Message:```txt\n```}"""

DEFAULT_PROMPT_FOR_FAF = """We are now trying to construct FAF (freefloat-adjusted factor), which is the proportion 
of a stock that is freely tradable in the market. Those stocks are not freely tradable is (1) stock hold by an 
individual which is equal or more than 5% (2) stock holds by mother company or other investment company with is equal 
or more than 5%. For example, Liu Ye hold 3.6%( 24,860,855 shares) Those stocks of him is tradable, but Temasek holds 
6% shares. Those stocks is not tradable. Now I want you to construct a company’s stock’s FAF with our txt file, 
which is merged from 2 files with different time stamp. The more up-to-date version is determinant. The format of 
output is {FAF: xx\nFAF(predicted by trend)xx\nFAF is calculate by (num_total-num_frozen)/num_total }. For example: text 
is { Time: 2023.6 Entities: ```txt [1] HSBC Holdings plc [Ultimate parent company, beneficial owner] ``` Overview: 
```csv Entity,Share number,Percentage of total HSBC Holdings plc,1188057371,62.14% ``` Message: ```txt 1. HSBC 
Holdings plc maintains its substantial interest of 62.14% in the Bank through its wholly-owned subsidiaries HSBC Asia 
Holdings Limited and The Hongkong and Shanghai Banking Corporation Limited.
Time: 2023.6\n…```} The output is {0.3786\n0.3786\nFAF=(..-..)/..}
"""


def prompt_ai_ans(task_id, file_name):
    """
    Merge two AI sorted files with a prompt and save the result.
    """
    # Extract the report name from the directory path
    report_name = os.path.basename(os.path.dirname(file_name))

    # Construct the save directory and file paths
    save_dir = os.path.join("Info_txt", task_id, report_name)
    os.makedirs(save_dir, exist_ok=True)

    # Construct paths for the two input files
    base_file_name = os.path.basename(file_name).replace("ai_sorted_", "")
    base_file_name = base_file_name.replace(".txt","")
    file_1 = os.path.join(save_dir, f"ai_sorted_{base_file_name}_1.txt")
    file_2 = os.path.join(save_dir, f"ai_sorted_{base_file_name}_2.txt")

    # Construct the output file path
    prompted_file_name = f"prompted_ai_sorted_{base_file_name}.txt"
    write_file_path = os.path.join(save_dir, prompted_file_name)

    # Read the contents of both AI sorted files
    try:
        with open(file_1, 'r', encoding='utf-8') as file:
            content_1 = file.read()
    except FileNotFoundError:
        print(f"File not found: {file_1}")
        return None

    try:
        with open(file_2, 'r', encoding='utf-8') as file:
            content_2 = file.read()
    except FileNotFoundError:
        print(f"File not found: {file_2}")
        return None

    # Combine prompt and contents
    combined_content = f"{DEFAULT_PROMPT_FOR_MESSAGE}\nNow the content you need to process is a {report_name}: {{\n{content_1}\n{content_2}\n}}"

    # Write the combined content to the new file
    with open(write_file_path, 'w', encoding='utf-8') as file:
        file.write(combined_content)
        file.flush()
        os.fsync(file.fileno())
    print(f"Prompted AI content saved successfully for task: {task_id}_{report_name}")

    return True


def process_ai_message(task_id, file_name):
    r"""
    Extract AI answers from RESULT_ANS_DOCKER and save to a specified file.
    """

    # Extract the report name from the directory path
    report_name = os.path.basename(os.path.dirname(file_name))

    # Construct the save directory and file path
    save_dir = os.path.join("Info_txt", task_id, report_name)
    os.makedirs(save_dir, exist_ok=True)

    # Modify the file name to include "ai_sorted_"
    write_file_path = os.path.join(save_dir, "aggregated_message")

    # Read the contents of RESULT_ANS_DOCKER
    try:
        with open('AGGREGATE', 'r', encoding='utf-8') as file:
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

    with open('AGGREGATE', 'w', encoding='utf-8') as file:
        file.write("")
        file.flush()
        os.fsync(file.fileno())
    print("AGGREGATE has been cleared.")

    return True

def prompt_ai_FAF(task_id):
    """
    Merge middle_report and annual_report aggregated messages with a prompt for FAF.
    """
    # Construct the file paths
    middle_report_path = os.path.join("Info_txt", task_id, "middle_report", "aggregated_message")
    annual_report_path = os.path.join("Info_txt", task_id, "annual_report", "aggregated_message")

    # Read the contents of both files
    try:
        with open(middle_report_path, 'r', encoding='utf-8') as file:
            middle_report_content = file.read()
    except FileNotFoundError:
        print(f"File not found: {middle_report_path}")
        return None

    try:
        with open(annual_report_path, 'r', encoding='utf-8') as file:
            annual_report_content = file.read()
    except FileNotFoundError:
        print(f"File not found: {annual_report_path}")
        return None

    # Combine prompt and contents
    combined_content = f"{DEFAULT_PROMPT_FOR_FAF}\nNow the content you need to process is: {{\n{middle_report_content}\n{annual_report_content}\n}}"

    # Construct the save directory and file path
    save_dir = os.path.join("Info_txt", task_id, "FAF")
    os.makedirs(save_dir, exist_ok=True)
    write_file_path = os.path.join(save_dir, "prompted_ai_FAF.txt")

    # Write the combined content to the new file
    with open(write_file_path, 'w', encoding='utf-8') as file:
        file.write(combined_content)
        file.flush()
        os.fsync(file.fileno())
    print(f"Prompted AI FAF content saved successfully for task: {task_id}")

    return True


def process_FAF(task_id):
    r"""
       Extract AI answers from RESULT_ANS_DOCKER and save to a specified file.
       """

    # Construct the save directory and file path
    save_dir = os.path.join("Info_txt", task_id, "FAF")
    os.makedirs(save_dir, exist_ok=True)

    # Modify the file name to include "ai_sorted_"
    write_file_path = os.path.join(save_dir, "FAF")

    # Read the contents of RESULT_ANS_DOCKER
    try:
        with open('FAF', 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print("FAF file not found.")
        return None

    # Write the AI content to the new file
    with open(write_file_path, 'w', encoding='utf-8') as file:
        file.write(content)
        file.flush()
        os.fsync(file.fileno())
    print(f"FAF content processed successfully for task: {task_id}")

    with open('FAF', 'w', encoding='utf-8') as file:
        file.write("")
        file.flush()
        os.fsync(file.fileno())
    print("FAF has been cleared.")

    return True


if __name__=="__main__":
    prompt_ai_FAF("0011")