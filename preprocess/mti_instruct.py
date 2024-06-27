import json
import argparse

def combine_and_format_instructions_outputs_corrected(json_file_paths, output_file_path):
    """
    Combine and format instructions and outputs from multiple JSON files,
    ensuring not to exceed the list bounds.
    
    Parameters:
    - json_file_paths: List of strings, paths to the input JSON files for each task.
    - output_file_path: String, path for the output JSON file containing combined instructions and outputs.
    """
    combined_tasks = []

    for file_index, file_path in enumerate(json_file_paths):
        with open(file_path, 'r') as file:
            tasks_data = json.load(file)

            for i, task_data in enumerate(tasks_data):
                if file_index == 0:
                    combined_tasks.append({
                        "instruction": "", 
                        "input": task_data["input"],
                        "output": "",
                        "history": []
                    })
                    combined_tasks[i]["instruction"] += "Read the following text, and follow the given subtasks.\n"
                    
                combined_tasks[i]["instruction"] += f"#{file_index + 1} {task_data['instruction']} After completing, wrap your answer within <task{file_index + 1}></task{file_index + 1}>.\n"
                combined_tasks[i]["output"] += f"<task{file_index + 1}>{task_data['output']}</task{file_index + 1}>\n\n"

    # Save the combined and formatted tasks to a new JSON file
    with open(output_file_path, 'w') as outfile:
        json.dump(combined_tasks, outfile, indent=4)

    print(f"Combined and formatted tasks saved to: {output_file_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Combine and format instructions and outputs from multiple JSON files.')
    parser.add_argument('--json_files', nargs='+', help='List of paths to the input JSON files for each task.', required=True)
    parser.add_argument('--output', type=str, help='Path for the output JSON file containing combined instructions and outputs.', required=True)
    args = parser.parse_args()
    combine_and_format_instructions_outputs_corrected(args.json_files, args.output)

