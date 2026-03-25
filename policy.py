def evaluate_policy(service, claims):

    if service == "education":
        return claims.get("isStudent") == "1"

    if service == "welfare":
        return claims.get("isAdult") == "1"

    if service == "health":
        return claims.get("isHealthEligible") == "1"

    return False
