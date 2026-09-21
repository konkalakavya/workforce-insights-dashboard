from models.attrition_model import predict_attrition
from models.promotion_model import predict_promotion


def attrition(payload, df):
    return predict_attrition(payload, df)


def promotion(payload, df):
    return predict_promotion(payload)
