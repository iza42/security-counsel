def read_input():
    with open ("agents_aid_inputs.txt", "r") as file:
        whole_info=[i.split(",") for i in file.readlines()]
    return whole_info

def seperate(liste):
    """seperates the commands given in the input file"""
    interrogee_name,core_accuracy,counsel,local_bomber_incidence,counsel_risk=None,None,None,None,None
    if any("create" in item for item in liste):
        for element in liste:
            if element.replace(" ","").isalpha():
                interrogee_name=element[7:].strip("\n")

            elif element.find(".")!=-1:
                core_accuracy1=float(element.strip("\n"))*100
                core_accuracy="{:.2f}".format(core_accuracy1)
            elif element.strip().strip("\n") in ("0","1"):
                if element.strip().strip("\n")=="0":
                    counsel="Not Bomber"
                else:
                    counsel="Bomber"

            elif element.find("/")!=-1:
                local_bomber_incidence=element.strip("\n ")

            else:
                counsel_risk=None
        return interrogee_name,core_accuracy,counsel,local_bomber_incidence,counsel_risk
    elif any("remove" in item for item in liste):
        for element in liste:
            interrogee_name = element[7:].strip("\n")
            return interrogee_name
    elif any("recommendation" in item for item in liste):
        for element in liste:
            interrogee_name = element[15:].strip("\n")
            return interrogee_name
    elif any("risk" in item for item in liste):
        for element in liste:
            interrogee_name = element[5:].strip("\n")
            return interrogee_name



def mother_dictionary(name, accuracy,counsel,incidence,risk,old_dictionary):
    """update the mother dictionary"""
    old_dictionary[name] = {"interrogee name": name,
         "core accuracy": accuracy,
         "counsel": counsel,
         "local bomber incidence": incidence,
         "counsel risk": risk}

    return old_dictionary

def create(name, accuracy,counsel,incidence,risk,old_dictionary):
    """if name not in the dictionary, creates it in the dictionary"""
    if name in old_dictionary:
        return f"Interrogee {name} cannot be recorded duplication."
    else:
        mother_dictionary(name, accuracy, counsel, incidence, risk, old_dictionary)
        return f"Interrogee {name} is recorded."

def remove(name, old_dictionary):
    """removes the name from the dictionary"""
    if name in old_dictionary:
        del old_dictionary[name]
        return f"Interrogee {name} is removed."
    else:
        return f"Interrogee {name }cannot be removed due to absence."


def make_list(old_dictionary):
    first_line = ("interrogee".ljust(16, " ") + "core".ljust(16, " ") + "counsel".ljust(16, " ") +
                  "local bomber".ljust(16, " ") + "counsel".ljust(16, " ")) + "\n"
    second_line = ("name".ljust(16, " ") + "accuracy".ljust(16, " ") + " ".ljust(16, " ") +
                   "incidence".ljust(16, " ") + "risk".ljust(16, " ")) + "\n"
    third_line = "-" * 93 + "\n"
    table = first_line + second_line + third_line
    fourth_line = ""

    for key, value in old_dictionary.items():
        if value["counsel risk"] == "No Risk":
            fourth_line += (
                    value["interrogee name"].ljust(16, " ") + (value["core accuracy"] + "%").ljust(16, " ") + value[
                "counsel"].ljust(16, " ") +
                    value["local bomber incidence"].ljust(16, " ") + value["counsel risk"].ljust(16, " "))
        else:
            fourth_line += (
                    value["interrogee name"].ljust(16, " ") + (value["core accuracy"] + "%").ljust(16, " ") + value[
                "counsel"].ljust(16, " ") +
                    value["local bomber incidence"].ljust(16, " ") + (str(value["counsel risk"]) + "%").ljust(16, " "))

        table += fourth_line + "\n"
        fourth_line = ""
    return table.rstrip("\n")


def risk_write(name, old_dictionary):
    if name in old_dictionary:
        risk = old_dictionary[name]["counsel risk"]
        if risk == "No Risk":  # if the risk is less than %3
            return f"Interrogee {name} has no counsel risk."
        return f"Interrogee {name} has a counsel risk of {risk}%."

    else:
        return f"Risk for {name} cannot be calculated due to absence."


def risk_calc(incidince, accuracy, counsel):
    bomber_incidince = int(incidince[:-7])
    core_accuracy = float(accuracy)
    if counsel == "Bomber":
        left = bomber_incidince * (core_accuracy / 100)
        right = (100000 - bomber_incidince) * ((100 - core_accuracy) / 100)
        risk = right / (right + left)
        if risk * 100 < 3:
            return "No Risk"
        return "{:.2f}".format(risk * 100)

    elif counsel == "Not Bomber":
        left1 = bomber_incidince - (bomber_incidince * (core_accuracy / 100))
        right1 = (100000 - bomber_incidince - ((100000 - bomber_incidince) * ((100 - core_accuracy) / 100)))
        risk1 = left1 / (right1 + left1)
        if risk1 * 100 < 3:
            return "No Risk"
        return "{:.2f}".format(risk1 * 100)


def recommendation(name, old_dictionary):
    if name in old_dictionary:
        if old_dictionary[name]["counsel"] == "Bomber":
            if float(old_dictionary[name][
                         "counsel risk"]) * 100 > 40:  # if counsel risk is bigger than 40% recommendation will be the opposite
                return f"System suggest to release {name}."
            return f"System suggest to arrest {name}."
    else:
        return f"Recommendation for {name} cannot be calculated due to absence."


def write(func):
    with open ("agents_aid_outputs.txt", "a+") as file:
        file.write(func)
        file.write("\n")


def main():
    my_dictionary=dict()
    for liste in read_input():
        if any("create" in item for item in liste):
            interrogee_name,core_accuracy,counsel,local_bomber_incidence,counsel_risk=seperate(liste)
            write(create(interrogee_name,core_accuracy,counsel,local_bomber_incidence,risk_calc(local_bomber_incidence,core_accuracy,counsel),my_dictionary))
        elif  any("remove" in item for item in liste):
            interrogee_name=seperate(liste)
            write(remove(interrogee_name,my_dictionary))
        elif  any("recommendation" in item for item in liste):
            interrogee_name = seperate(liste)
            write(recommendation(interrogee_name,my_dictionary))
        elif any("risk" in item for item in liste):
            interrogee_name = seperate(liste)
            write(risk_write(interrogee_name,my_dictionary))
        elif any("list" in item for item in liste):
            write(make_list(my_dictionary))


if __name__=="__main__":
    main()
