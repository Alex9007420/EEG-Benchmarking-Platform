#LIST OF ALL METRIC FUNCTION PER TASK
import math
METRIC_CHOICES = [
        ('accuracy', 'Accuracy'), #Tuple: (database entry, Human Readable)
        ('f1_score', 'F1 Score'), #Different scores, mse, rmse, l1, l2, euclidean
        ('mse', 'MSE'),
        ('rmse', 'RMSE'),
        #Euclidean Error
        #L1
        #L2
        #closest l1, l2
        #Relative Euclidean error
    ]

##########  LR TASK  ###########
def accuracy(predictions, benchmarks):
    n = len(predictions)
    if n == 0: return 0
    correct = 0
    for i in range(n):
        if (
            predictions[i]["label_LR"] == benchmarks[i]["label_LR"]
        ):
            correct += 1  
    accuracy = (correct / n)
    accuracy_truncated = math.trunc(accuracy * 10_000) / 10_000
    return accuracy_truncated


##########  SACCADE TASK  ##########



##########  FIXATION TASK  ##########
def euclidean_distance_sum(predicted_coords, real_coords):
    n = len(predicted_coords)
    total_distance = 0.0
    for i in range(n):
        x_pred = predicted_coords[i]["label_x_position"]
        x_real = real_coords[i]["label_x_position"]

        y_pred = predicted_coords[i]["label_y_position"]
        y_real = real_coords[i]["label_y_position"] 

        total_distance += math.sqrt((x_real - x_pred)**2 + (y_real - y_pred)**2)               
    return total_distance

def l1_distance_sum(real_coords, predicted_coords):
    n = len(predicted_coords)
    total_distance = 0.0
    for i in range(n):
        x_pred = predicted_coords[i]["label_x_position"]
        x_real = real_coords[i]["label_x_position"]

        y_pred = predicted_coords[i]["label_y_position"]
        y_real = real_coords[i]["label_y_position"] 

        total_distance += abs(x_real - x_pred) + abs(y_real - y_pred)
    return total_distance