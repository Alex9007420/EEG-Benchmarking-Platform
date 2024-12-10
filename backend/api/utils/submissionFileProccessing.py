import json
import math
import os
import numpy as np
import pandas as pd

from .metrics import *

SCORE_AGGREGATIONS = [
    "Overall", "Overall Hardware1", "Overall Hardware2", "Overall Dots", 
    "Overall Movie", "Hardware1 Dots", "Hardware2 Dots",
    "Hardware1 Movie", "Hardware2 Movie", "Hardware1 Reading"
]

METRICS = {
    "LR": [accuracy],
    "Saccade": [],
    "Fixation": [euclidean_distance_sum, l1_distance_sum],
    "Segmentation": [],
    "Scanpath": []
}

def process(submission_fileContent, task) -> dict:

    metric_names = [f.__name__ for f in METRICS[task]]
    scores = pd.DataFrame(0.0, index=SCORE_AGGREGATIONS, columns=metric_names)

    print("TASK: " + task)

    benchmark_file_name = f"testEEGEyeNet_{task}_test.json" 
    relative_path = os.path.join("api", "media", "benchmarks", benchmark_file_name)
    file_path = os.path.abspath(relative_path)

    with open(file_path, "r") as file:
        benchmark_fileContent = json.load(file)

   
    benchmark_entries = benchmark_fileContent.get(f"EEGEyeNet_{task}_test", [])
    submission_entries = submission_fileContent.get(f"EEGEyeNet_{task}_test", [])
    #RAISE AN ERROR IF IT CANNOT GET THE ENTRIES

    aggregated_benchmark_entries = get_aggregated_entries(benchmark_entries)
    aggregated_submission_entries = get_aggregated_entries(submission_entries)

    print("AGGREGATED BENCHMARKS")
    print(aggregated_benchmark_entries)
    print("")
    print("AGGREGATED SUBMISSION")
    print(aggregated_submission_entries)

    for aggregation in SCORE_AGGREGATIONS:
        for metricFunction in METRICS[task]:
            predictions = aggregated_submission_entries[aggregation]
            print(aggregation)
            print(predictions)
            benchmarks = aggregated_benchmark_entries[aggregation]
            score = metricFunction(predictions, benchmarks)
            # aggregated_scores[aggregation] = score
            scores.at[aggregation, metricFunction.__name__] = score
    
    scoresJSON = scores.to_json(orient="split")
    scores_dict = json.loads(scoresJSON)

    print("scoresJSON: ")
    print(scoresJSON)

    return scores_dict


def get_aggregated_entries(entries) -> dict:

    aggregated_entries = {key: [] for key in SCORE_AGGREGATIONS}
    # aggregated_benchmarks = {key: [] for key in score_aggregations} #MAKE THIS STATIC IN THE FUTURE

    for entry in entries:

        value = entry["output"]

        for aggregation in SCORE_AGGREGATIONS:

            match aggregation:

                case "Overall": #1
                    aggregated_entries[aggregation].append(value)

                case "Overall Hardware1": #2
                    if "Hardware1" in entry["input"][0]:
                        aggregated_entries[aggregation].append(value)
                
                case "Overall Hardware2": #3
                    if "Hardware2" in entry["input"][0]:
                        aggregated_entries[aggregation].append(value)

                case "Overall Dots": #4
                    if "Dots" in entry["input"][0]:
                        aggregated_entries[aggregation].append(value)

                case "Hardware1 Dots": #5
                    if "Hardware1-Dots" in entry["input"][0]:
                        aggregated_entries[aggregation].append(value)

                case "Hardware2 Dots": #6
                    if "Hardware2-Dots" in entry["input"][0]:
                        aggregated_entries[aggregation].append(value)

                case "Hardware1 Movie": #7
                    if "Hardware1-Movie" in entry["input"][0]:
                        aggregated_entries[aggregation].append(value)

                case "Hardware2 Movie": #8
                    if "Hardware2-Movie" in entry["input"][0]:
                        aggregated_entries[aggregation].append(value)

                case "Overall Movie": #9
                    if "Movie" in entry["input"][0]:
                        aggregated_entries[aggregation].append(value)

                case "Hardware1 Reading": #10
                    if "Hardware1-Reading" in entry["input"][0]:
                        aggregated_entries[aggregation].append(value)

    return aggregated_entries

def metric_evaluation(submission_outputs, benchmark_outputs, task):

    if(len(submission_outputs) == 0): return 0
    
    match task:
        case "LR":
            correct = 0
            for i in range(len(submission_outputs)):
                if (
                    submission_outputs[i]["label_LR"] == benchmark_outputs[i]["label_LR"]
                ):
                    correct += 1  
            accuracy = (correct / len(submission_outputs))
            accuracy_truncated = math.trunc(accuracy * 10_000) / 10_000
            return accuracy_truncated
        
        case "Saccade": 
            pass

        case "Fixation": 
            total_length = 0
            for i in range(len(submission_outputs)):
                x1 = submission_outputs[i]["label_x_position"]
                x2 = benchmark_outputs[i]["label_x_position"]

                y1 = submission_outputs[i]["label_y_position"]
                y2 = benchmark_outputs[i]["label_y_position"] 

                total_length += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)               
            return total_length

        case "Segmentation":
            pass

