def evaluate_policy(service, claims):
    is_adult = int(claims["isAdult"])
    is_student = int(claims["isStudent"])
    is_health = int(claims["isHealthEligible"])

    if service == "education":
        return "GRANTED" if is_student == 1 else "DENIED"

    elif service == "health":
        return "GRANTED" if is_health == 1 else "DENIED"

    elif service == "welfare":
        return "GRANTED" if is_adult == 1 else "DENIED"

    return "DENIED"