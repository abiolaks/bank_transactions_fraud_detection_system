| Phase                                     | Deliverable                                                   | Tools                        |
| ----------------------------------------- | ------------------------------------------------------------- | ---------------------------- |
| **Phase 1: Offline model training**       | Generate synthetic dataset, train and evaluate XGBoost        | Python, scikit-learn, MLflow |
| **Phase 2: Real-time simulator + stream** | Kafka + Python producer                                       | Kafka, Python                |
| **Phase 3: Model serving**                | FastAPI service exposing `/predict`                           | FastAPI, joblib              |
| **Phase 4: Real-time scoring pipeline**   | Python consumer reading Kafka, calling FastAPI, writing to DB | Python, psycopg2             |
| **Phase 5: Streamlit dashboard**          | Displays alerts, labels, metrics                              | Streamlit                    |
| **Phase 6: Feedback & retraining**        | Export labels, retrain model                                  | Python, cron job             |
