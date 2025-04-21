from main import resource_path


startDate = open(resource_path("start_date.txt"), "r")
print(startDate)
startDate.close()