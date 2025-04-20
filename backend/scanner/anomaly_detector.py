from sklearn.ensemble import IsolationForest
import numpy as np

def detect_anomalies(request_times):
    if len(request_times) < 2:
        return []

    data = np.array(request_times).reshape(-1, 1)
    model = IsolationForest(contamination=0.1)
    preds = model.fit_predict(data)

    anomalies = [i for i, val in enumerate(preds) if val == -1]
    return anomalies
