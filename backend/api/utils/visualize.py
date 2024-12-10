#FOR FIXATION ONLY
from .submissionFileProccessing import *

def getVisualizationData(submission_fileContent, task) -> dict:

    metric_names = [f.__name__ for f in METRICS[task]]
    scores = pd.DataFrame(0.0, index=SCORE_AGGREGATIONS, columns=metric_names)

    benchmark_file_name = f"testEEGEyeNet_{task}_test.json" 
    relative_path = os.path.join("api", "media", "benchmarks", benchmark_file_name)
    file_path = os.path.abspath(relative_path)

    with open(file_path, "r") as file:
        benchmark_fileContent = json.load(file)

   
    benchmark_entries = benchmark_fileContent.get(f"EEGEyeNet_{task}_test", [])
    submission_entries = submission_fileContent.get(f"EEGEyeNet_{task}_test", [])
    #RAISE AN ERROR IF IT CANNOT GET THE ENTRIES

    
    print("SUBMISSION FILE ENTRIES")
    print(submission_entries)

    predictions = []
    benchmarks = []

    n = len(benchmark_entries)
    for i in range(n):
        x_pred = submission_entries[i]["output"]["label_x_position"]
        x_real = benchmark_entries[i]["output"]["label_x_position"]

        y_pred = submission_entries[i]["output"]["label_y_position"]
        y_real = benchmark_entries[i]["output"]["label_y_position"] 

        predictions.append([x_pred, y_pred])
        benchmarks.append([x_real, y_real])


    result = {
        "predictions": predictions,
        "benchmarks": benchmarks
    }

    resultJSON = json.dumps(result)

    print("resultJSON: ")
    print(resultJSON)

    return resultJSON