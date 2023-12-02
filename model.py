import sqlite3

class schedule():
	connection = 0
	cursor = ''
	last_id = 2
	def __init__(self):
		self.connection = sqlite3.connect('schedule.db', check_same_thread=False)
		self.cursor = self.connection.cursor()


		self.cursor.execute('CREATE TABLE IF NOT EXISTS'+
                       '`day` ('+
	                   '`id` INT NOT NULL,'+
	                   '`date` DATE NOT NULL,'+
	                   '`lessons_count` int NOT NULL,'+
	                   '`place` varchar NOT NULL,'+
	                   '`lessons` varchar NOT NULL,'+
	                   'PRIMARY KEY (`id`)'+
                       ');')

		self.cursor.execute('CREATE TABLE IF NOT EXISTS' +
						'`lesson` (' +
						'`id` INT NOT NULL,' +
						'`teacher` varchar NOT NULL,' +
						'`theme` varchar NOT NULL,' +
						'`time` varchar NOT NULL,' +
						'`home_work` varchar NOT NULL,' +
						'`replace` varchar NOT NULL,' +
						'PRIMARY KEY (`id`)' +
						');')


	def create_day(self, date, lessons_count, place, lessons):
		self.cursor.execute('INSERT INTO day(id,date,lessons_count,place,lessons)'+
							f' VALUES({self.last_id}, "{date}",{lessons_count},"{place}","{lessons}")')
		self.connection.commit()
		self.last_id = self.last_id + 1
	def select_all_days(self):
		self.cursor.execute('SELECT * from day')
		return self.cursor.fetchall()

	def select_day_by_date(self, date):
		self.cursor.execute(f'SELECT * from day WHERE date="{date}"')
		return self.cursor.fetchall()

	def delete_by_date(self, date):
		self.cursor.execute(f'DELETE FROM day WHERE date="{date}"')
		self.connection.commit()
