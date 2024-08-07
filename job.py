import random
import models


def split_teams(db, event_db):
		parts = [i[0] for i in db.query(models.Registration.user_id).filter(models.Registration.event_id == event_db.id).all()]
		n = event_db.team_size
		db.query(models.Teams).delete()
		db.commit()

		random.shuffle(parts)
		if len(parts) <= n:
				ans = []
				tmp = []
				for i in range(len(parts) // 2):
						tmp.append(parts[i])
				ans.append(tmp)
				tmp = []
				for i in range(len(parts) // 2, len(parts)):
						tmp.append(parts[i])
				ans.append(tmp)
				add_to_tabl(ans, db, event_db.id)
				return
		subarrays = []
		current_subarray = []
		count = 0
		for part in parts:
				current_subarray.append(part)
				count += 1
				if count == n:
						subarrays.append(current_subarray)
						current_subarray = []
						count = 0
		if current_subarray:
				subarrays.append(current_subarray)
		ind = len(subarrays) - 2
		while len(subarrays[-2]) - len(subarrays[-1]) > 0:
				if ind < 0:
						ind = len(subarrays) - 2
				subarrays[-1].append(subarrays[ind][-1])
				subarrays[ind].pop()
				ind -= 1
		add_to_tabl(subarrays, event_db.id)


def add_to_tabl(array, db, event_id):
		for i in array:
				team = models.Teams(event_id=event_id)
				db.add(team)
				db.commit()
				for people in i:
						user = db.query(models.Users).filter(models.Users.id == people).first()
						user.team_id = team.id
						db.commit()
				db.commit()

