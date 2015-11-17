# -*- coding:utf-8 -*-
import os
import sqlite3
import random
import sys

db_filename = 'hdu.db'
schema_name = 'problem'
schema_filename = 'hdu_schema.sql'

query_test1_SQL = """
SELECT id, title, ratio, Accepted, Submissions, solved FROM problem
ORDER BY id
LIMIT 10
"""

query_test2_SQL = """
SELECT id, title, ratio, Accepted, Submissions, solved FROM problem
ORDER BY id DESC
LIMIT 10
"""

insert_SQL = """
INSERT INTO problem (id, title, ratio, Accepted, Submissions, solved)
VALUES (?, ?, ?, ?, ?, ?)
"""

update_SQL = """
UPDATE problem
SET solved = 1
WHERE id = ?
"""

query_by_tired_SQL = """
SELECT id, title, ratio FROM problem
WHERE solved=0
ORDER BY ratio DESC
LIMIT %d
"""

query_by_ratio_SQL = """
SELECT id, title, ratio FROM problem
WHERE solved=0
ORDER BY ratio
LIMIT %d
"""

query_by_Accepted_SQL = """
SELECT id, title, Accepted FROM problem
WHERE solved=0
ORDER BY accepted
LIMIT %d
"""
query_by_Submissions_SQL = """
SELECT id, title, Submissions FROM problem
WHERE solved=0
ORDER BY submissions
LIMIT %d
"""

def query_test():
	with sqlite3.connect(db_filename) as conn:
		cursor = conn.cursor()
		query_sql = query_test1_SQL
		cursor.execute(query_sql)
		
		print 'testing first 10'
		for row in cursor.fetchall():
			id, title, ratio, ac, sub, solve = row
			st = '*' if solve else ' '
			print '%4d %30s %.2f%% %6d %6d %1s' % (id, title, ratio, ac, sub, st)
		
		print "\n"
		query_sql = query_test2_SQL
		cursor.execute(query_sql)
		
		print 'testing last 10'
		for row in cursor.fetchall():
			id, title, ratio, ac, sub, solve = row
			st = '*' if solve else ' '
			print '%4d %30s %.2f%% %6d %6d %1s' % (id, title, ratio, ac, sub, st)

			
def query_by_Tired(cursor, topk=5):
	query_sql = query_by_tired_SQL % (topk)
	cursor.execute(query_sql)
	
	for row in cursor.fetchall():
		id, title, ratio = row
		print u'%4d  %s %.02f%%' % (id, title, ratio)
	

def query_by_Rand(cursor, topk=10):
	query_sql = query_by_Submissions_SQL % (topk)
	cursor.execute(query_sql)
	
	rows = cursor.fetchall()
	mx = len(rows) - 1
	indexList = [random.randint(0, mx) for i in xrange(topk)]
	rand_rows = map(
		lambda index: rows[index], indexList
	)
		
	for row in rand_rows:
		id, title, sub = row
		print u'%4d  %s %d' % (id, title, sub)
	

def query_by_Ratio(cursor, topk=10):
	query_sql = query_by_ratio_SQL % (topk)
	
	cursor.execute(query_sql)
	
	for row in cursor.fetchall():
		id, title, ratio = row
		print u'%4d  %s %.02f%%' % (id, title, ratio)

		
def query_by_Sub(cursor, topk=10):
	query_sql = query_by_Accepted_SQL % (topk)
	
	cursor.execute(query_sql)
	
	for row in cursor.fetchall():
		id, title, sub = row
		print u'%4d  %s %d' % (id, title, sub)

		
def query_by_Ac(cursor, topk=10):
	query_sql = query_by_Submissions_SQL % (topk)
	
	cursor.execute(query_sql)
	
	for row in cursor.fetchall():
		id, title, ac = row
		print u'%4d  %s %d' % (id, title, ac)

		
def query(cmd='', topk=10):
	with sqlite3.connect(db_filename) as conn:
		cursor = conn.cursor()
		if cmd == 'rat':
			query_by_Ratio(cursor, topk)
		elif cmd == 'ac':
			query_by_Ac(cursor, topk)
		elif cmd == 'sub':
			query_by_Sub(cursor, topk)
		elif cmd == 'rand':
			query_by_Rand(cursor, topk)
		else:
			query_by_Tired(cursor, topk)
			
			
def update(id_List):
	# print 'update'
	with sqlite3.connect(db_filename) as conn:
		cursor = conn.cursor()
		try:
			cursor.executemany(update_SQL, id_List)
			
		except Exception as e:
			print 'Update Error: %s' % (e)
			conn.rollback()
			
		else:
			conn.commit()
	
	
def insert(problem_List):
	with sqlite3.connect(db_filename) as conn:
		cursor = conn.cursor()
		try:
			cursor.executemany(insert_SQL, problem_List)
			
		except Exception as e:
			raise e
			# print 'Insert Error: %s' % (e)
			conn.rollback()
			
		else:
			conn.commit()
			

def create_db():
	if not os.path.exists(db_filename):
		with sqlite3.connect(db_filename) as conn:
			with open(schema_filename, 'rt') as f:
				schema = f.read()
			conn.execute(schema)
			print 'Creating schema Problem succeed.'
		print 'Creating database succeed.'
		
		
def test_query_by():
	print 'test query_by_Tired ...'
	query('', topk=20)
	print "\n"
	
	print 'test query_by_Ratio ...'
	query('rat', topk=20)
	print "\n"
	
	print 'test query_by_Ac ...'
	query('ac', topk=20)
	print "\n"
	
	print 'test query_by_Sub ...'
	query('sub', topk=20)
	print "\n"
	
	print 'test query_by_Rand ...'
	query('rand', topk=20)
	print "\n"
	
	
		
if __name__=='__main__':
	# create_db()
	# update([(1000)])
	# prob_List = [(1000, 'A + B Problem', 31.643581645167714, 150919, 476934, 0)]
	# insert(prob_List)
	# print 'nothing'
	# test_query_by()
	
	if len(sys.argv) > 2:
		cmd = sys.argv[1]
		if cmd.startswith('up'):
			id_List = map(lambda x: (x,), sys.argv[2:])
			update(id_List)
		else:
			topk = int(sys.argv[2])
			query(cmd, topk)
	elif len(sys.argv) > 1:
		cmd = sys.argv[1]
		query(cmd)
	else:
		query()
		