from random import randint

def perform_experiment(no_of_people):
	frequency = [0 for i in range(365)]
	for i in range(no_of_people):
		birthday = randint(0,364)
		if frequency[birthday] == 1:
			return 1 #Atleast one pair with same birthday
		frequency[birthday] = 1
	return 0 #Every person has different birth date

def main():
	no_of_people = input("Enter the total number of people : ")
	no_of_trials = input("Enter the number of trials : ")
	success = 0  #success stores the count of trials in which atleast 2 people have same birthday
	for trial in range(no_of_trials):
		success += perform_experiment(no_of_people)
	print "Probability of atleast 2 people with the same birthday =",(float(success)/no_of_trials)

if __name__ ==  "__main__":
	main()