from random import seed
from random import randint

class Passenger:
	# Αυτή η κλάση θα αντιπροσωπεύει τον επιβάτη.

	def __init__(self, id, start_floor, end_floor, in_lift, got_out):
		self.id = id					# Αυτή η ιδιότητα κρατάει την ταυτότητα του επιβάτη (αύξων αριθμός)
		self.start_floor = start_floor	# Αυτή η ιδιότητα κρατάει τον όροφο που θα μπει στο ασανσέρ (τυχαιός αριθμός)
		self.current_floor = start_floor	# Μας δείχνει που βρίσκεται κάθε στιγμή ο επιβάτης (για την output)
		self.end_floor = end_floor		# Αυτή η ιδιότητα κρατάει τον όροφο στον οποίο θα κατέβει (τυχαιός αριθμός)
		self.in_lift = in_lift			# Αυτή η ιδιότητα κρατάει το αν είναι μέσα στο ασανσέρ (True/False)
		self.got_out = got_out			# Αυτή η ιδιότητα κρατάει το αν κατέβηκε από το ασανσέρ (True/False)

class Building:
	# Αυτή η κλάση θα αντιπροσωπεύει ένα κτήριο.

	passengers = []				# Αυτή η ιδιότητα είναι μια λίστα που θα κρατάει τα αντικείμενα των επιβατών

	def __init__(self, floors, passengers):
		self.floors = floors            # Αυτή η ιδιότητα θα μας λέει πόσους ορόφους έχει το κτήριο
		self.lift = Lift(floors)        # Αυτή η ιδιότητα είναι το ασανσέρ (του περνάω και την πληροφορία πόσους ορόφους έχει το κτήριο)

		'''
		Όταν δημιουργώ το κτήριο θέλω να φτιαξω μια νέα λίστα επιβατών όπου
		ο κάθε επιβάτης θα έχει ένα id και θα έχει έναν τυχαιο όροφο που ξεκινάει και σταματάει
		και αρχικά όλοι οι επιβάτες ΔΕΝ θα είναι στο ασανσέρ και ΔΕΝ θα έχουν φτάσει στον οροφό τους
		'''
		for x in range(passengers):     # Ο πρώτος επιβάτης θα έχει id = 0 και ο τελευταίος θα έχει id = passengers -1 
			self.passengers.append(Passenger(x, randint(0,floors), randint(0,floors), False, False))
			
	def print_passengers(self):
		for p in self.passengers:
			print("Ο επιβάτης με id {0} θα ανέβει στον όροφο {1} και θα κατέβει στον όροφο {2}".format(p.id, p.start_floor, p.end_floor))

	def run(self):
		# Βρίσκω ποιοι επιβάτες παραμένουν στο ασανσέρ
		remainingPassengers = list(filter(self.isRemainingPassenger, self.passengers))
		# Για όσο έχω επιβάτες στο ασανσέρ, τρέξε τον αλγόριθμο...
		while len(remainingPassengers) > 0:
			self.output()
			# Για κάθε επιβάτη που απομένει έλεγξε εάν πρέπει να κατέβει ή να ανέβει στον όροφο που βρίσκεται το ασανσέρ
			for p in remainingPassengers:
				if p.start_floor == self.lift.floor and p.in_lift != True:
					self.lift.get_in(p)
				if p.end_floor == self.lift.floor and p.in_lift == True:
   					self.lift.get_out(p)

			# Μετακίνησε το ασανσέρ και ενημέρωσε την λίστα των επιβατών που απομένουν		
			self.lift.move()
			remainingPassengers = list(filter(self.isRemainingPassenger, self.passengers))
		
		self.output()	# Τελική εκτύπωση!!!
			
	def isRemainingPassenger(self, passenger):
		if passenger.got_out == False:
			return True
		else:
			return False

	def output(self):
			print("-"*80)
			print("Floor \t Passenger \t\t\t Lift")
			print("-"*80)
			# Για να τυπώσω κάνω επανάληψη σε όλους τους ορόφους
			for i in range(self.floors, -1, -1):
				# Εάν το ασανσέρ είναι στον όροφο που με ενδιαφέρει, βάζω ένα Χ, αλλιώς κενό
				if self.lift.floor == i: 
					elevator = 'X' 
				else: 
					elevator = ''
				
				# Εδώ κοιτάζω ποιοι επιβάτες είναι στον όροφο που με ενδιαφέρει και φτιάχνω ένα string
				# με τα id τους για να τους εμφανίσω
				currentFloorPassengers = ''
				for p in self.passengers:
					if p.current_floor == i:
						currentFloorPassengers = currentFloorPassengers + ' ' + str(p.id)

				print("  {0} \t {1} \t \t\t\t {2}".format(i,currentFloorPassengers,elevator))
				print("-"*80)

class Lift:
	# Αυτή η κλάση αντιπροσωπεύει το ασανσέρ.
	
	floor = 0					# Αρχικά θεωρούμε ότι το ασανσέρ είναι στο ισόγειο
	passengers_in = []			# Αυτή η ιδιότητα κρατάει την λίστα των επιβατών που είναι μέσα στο ασανσέρ
	direction = 'up'			# Αυτή η ιδιότητα δείχνει την κατεύθυνση του ασανσέρ (up/down)

	def __init__(self, floors):
    		self.floors = floors	# Αυτή η ιδιότητα κρατάει τους ορόφους του κτηρίου (για να ξέρει το ασανσέρ μέχρι που μπορεί να φτάσει)

	def move(self):
    		# Λογική μετακίνησης: Εάν η κατεύθυνση μου δείχνει προς τα επάνω αύξησε τη μεταβλητή floor μέχρι να βρώ τον τελευταίο όροφο
			#                     Εάν έχω φτάσει στον τελευταίο όροφο τότε άλλαξε την κατεύθυνση προς τα κάτω και ξεκίνα να μειώνεις τη μεταβλητή floor
			if(self.direction == 'up' and self.floor < self.floors):
					self.floor = self.floor + 1
			else:
					self.direction = 'down'

			if(self.direction == 'down' and self.floor > 0):
    				self.floor = self.floor - 1
			else:
    				self.direction = 'up'

	def get_in(self, passenger):
			# Όταν ανεβαίνει ένας επιβάτης, άλλαξε την μεταβλητή του in_lift σε True και βάλτον στη λίστα passengers_in
			passenger.in_lift = True
			self.passengers_in.append(passenger)

	def get_out(self, passenger):
			# Όταν βγαίνει ένας επιβάτης, άλλαξε την μεταβλητή του in_lift σε False και βγάλτον από την λίστα passengers_in
			# Επίσης ενημέρωσε την ιδιότητα current_floor για να εμφανίσουμε που βρίσκεται
			self.passengers_in.remove(passenger)
			passenger.in_lift = False
			passenger.got_out = True
			passenger.current_floor = self.floor

def main():
	seed(1) # Αρχικοποιώ τη γεννήτρια τυχαίων αριθμών

	# Αρχική ανάθεση των τιμών και έλεγχος ορθότητας
    
	input_OK = False    # Αυτή η μεταβλητή θα μας δείχνει αν τα στοιχεία που έβαλε ο χρήστης είναι σωστά

	while(input_OK == False):
		try:
			floors = int(input("Δώστε αριθμό ορόφων:"))
			passengers = int(input("Δώστε αριθμό επιβατών:"))

			if(floors <= 0 or passengers <=0):
				print("ΣΦΑΛΜΑ: Θα πρέπει ο αριθμός των ορόφων και ο αριθμός των επιβατών να ειναι μεγαλύτερα του μηδενός")    
				input_OK = False
			else:
				input_OK = True
            
		except:
			print("ΣΦΑΛΜΑ: Πρέπει να εισάγετε αριθμό για τους ορόφους και τους επιβάτες!!!")
			input_OK = False

	# Τώρα το πρόγραμμα θα πρέπει να φτιάξει ένα αντικείμενο τύπου Building
	myBuilding = Building(floors, passengers)
	myBuilding.print_passengers()
	myBuilding.run()

main()
