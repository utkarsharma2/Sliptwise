"""Util functions"""

def checkRequired(requiredParams, prams):
    missingParams = []
    for requiredParam in requiredParams:
        if requiredParam not in prams:
            missingParams.append(requiredParam)
    return missingParams