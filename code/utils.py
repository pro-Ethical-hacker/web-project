filters = [
	{
		"filter_name": "Country",
		"querry": "SELECT DISTINCT coun_name FROM country ORDER BY coun_name;",
		"type": "distinct",
		"table_place": "country.coun_name",
	},
	{
		"filter_name": "Duration (years)",
		"querry": "SELECT MIN(dur_year), MAX(dur_year) FROM course_duration;",
		"type": "continuous",
		"table_place": "course_duration.dur_year",
	},
	{
		"filter_name": "Degree Level",
		"querry": "SELECT DISTINCT deg_name FROM degree_level ORDER BY deg_name;",
		"type": "distinct",
		"table_place": "degree_level.deg_name",
	},
	{
		"filter_name": "Discipline",
		"querry": "SELECT DISTINCT disc_name FROM discipline ORDER BY disc_name;",
		"type": "distinct",
		"table_place": "discipline.disc_name",
	},
	{
		"filter_name": "Fee",
		"querry": "SELECT MIN(pkr_value), MAX(pkr_value) FROM fee;",
		"type": "continuous",
		"table_place": "fee.pkr_value",
	},
	{
		"filter_name": "Institute",
		"querry": "SELECT DISTINCT ins_type FROM institute ORDER BY ins_type;",
		"type": "distinct",
		"table_place": "institute.ins_type",
	},
	{
		"filter_name": "Language",
		"querry": "SELECT DISTINCT language FROM language ORDER BY language;",
		"type": "distinct",
		"table_place": "language.language",
	}
]


def get_filter_options(cursor):
	results = []

	for filter in filters:
		cursor.execute(filter['querry'])

		result = {
			"filter_name": filter['filter_name'],
			"type": filter['type'],
		}

		if filter['type'] == 'distinct':

			opts = ["All"] + [i[0] for i in list(cursor)]
			new_ops = []
			for i, j in enumerate(opts):
				new_ops.append({
					"value": i+1,
					"label": j
				})
			result['options'] = new_ops
		else:
			ran = list(cursor)
			result['options'] = [float(ran[0][0]), float(ran[0][1])]

		results.append(result)

	return results


def clean_word(word):
	alpha = "abcdefghijklmnopqrstuvwxyz"
	new = ""
	for i in word.lower():
		if i in alpha:
			new += i
	return new


def compare_word(word1, word2):
	word1_subs = [word1[i: j]
				  for i in range(len(word1)) for j in range(i + 1, len(word1) + 1)]
	word1_subs = sorted(word1_subs, key=lambda x: len(x), reverse=True)
	word1_subs = [i for i in word1_subs if len(i) > 2]

	score = 0
	for i in word1_subs:
		if i in word2:
			score += 1

	return score


def sort_by_search(search, results):
	cleaned_search = clean_word(search)

	new_results = []
	for result in results:
		score = compare_word(cleaned_search, clean_word(result[1]))
		new_results.append([result[0], score])
	sorted_ids = [i[0]
				  for i in sorted(new_results, key=lambda x: x[1], reverse=True)]

	return sorted_ids


def get_full_info(cursor, course_id):
	dict = {}
	
	sql = "select spec_name from complete_data where course_id=%s "
	cursor.execute(sql, [course_id])
	result = cursor.fetchall()
	dict["specialization"] = result[0][0]
	
	sql = """select disc_name,description from complete_data where course_id=%s """
	cursor.execute(sql, [course_id])
	result = cursor.fetchall()
	dict["discipline"] = result[0]
	
	sql = """select language from complete_data where course_id =%s """
	cursor.execute(sql, [course_id])
	result = cursor.fetchall()
	dict["language"] = result[0][0]
	
	sql = """select `rank`,rank_type from complete_data where course_id =%s """
	cursor.execute(sql, [course_id])
	result = cursor.fetchall()
	dict["ranking"] = result
	
	sql = """select ins_name,est_date,sector,ins_type,sector,logo from complete_data where course_id =%s """
	cursor.execute(sql, [course_id])
	result = cursor.fetchall()
	dict["institute"] = result[0]

	sql = """select camp_name from complete_data where course_id =%s """
	cursor.execute(sql, [course_id])
	result = cursor.fetchall()
	dict["campus"] = result[0][0]

	sql = """select city_name from complete_data where course_id =%s """
	cursor.execute(sql, [course_id])
	result = cursor.fetchall()
	dict["city"] = result[0][0]

	sql = """select state_name from complete_data where course_id =%s """
	cursor.execute(sql, [course_id])
	result = cursor.fetchall()
	dict["state"] = result[0][0]

	sql = """select coun_name from complete_data where course_id =%s """
	cursor.execute(sql, [course_id])
	result = cursor.fetchall()
	dict["country"] = result[0][0]

	sql = """select deg_name,level_type from complete_data where course_id =%s """
	cursor.execute(sql, [course_id])
	result = cursor.fetchall()
	dict["degree_level"] = result[0]

	sql = """select pkr_value from complete_data where course_id =%s """
	cursor.execute(sql, [course_id])
	result = cursor.fetchall()
	dict["fee_in_pkr"] = result[0][0]

	sql = """select intake_month from complete_data where course_id =%s """
	cursor.execute(sql, [course_id])
	result = cursor.fetchall()
	dict["intake_months"] = result

	sql = """select deadline_month from complete_data where course_id =%s """
	cursor.execute(sql, [course_id])
	result = cursor.fetchall()
	dict["deadline_month"] = result

	sql = """select deadline_year from complete_data where course_id =%s """
	cursor.execute(sql, [course_id])
	result = cursor.fetchall()
	dict["deadline_year"] = result
	sql = """select curr_type,curr_value from complete_data where course_id =%s """

	cursor.execute(sql, [course_id])
	result = cursor.fetchall()
	dict["currency_value"] = [result[0][0], float(result[0][1])]

	sql = """select type,url from complete_data where course_id =%s """
	cursor.execute(sql, [course_id])
	result = cursor.fetchall()
	dict["source_link"] = result[0]

	sql = """select name from complete_data where course_id =%s """
	cursor.execute(sql, [course_id])
	result = cursor.fetchall()
	dict["course"] = result[0]

	sql = """select url from complete_data where course_id =%s """
	cursor.execute(sql, [course_id])
	result = cursor.fetchall()
	url = result[0][0]
	if url == None:
		url = "https://timescoursefinder.com"
	dict["url"] = url

	return dict


def get_short_info(cursor, course_ids):
	where_clause = ""
	for course_id in course_ids:
		where_clause += f"course_id = {course_id} OR "
	where_clause = where_clause[:-3]
	if where_clause.replace(" ", "") == "":
		where_clause = "false"
	query = f"""
		SELECT
			course_id, logo,
			name, language, level_type,
			deg_name, curr_value, curr_type,
			ins_name, description, intake_month,
			deadline_month, dur_year, address,
			coun_name, url
		FROM complete_data
		WHERE {where_clause}
		GROUP BY course_id
	"""
	cursor.execute(query)
	result = cursor.fetchall()
	outputs = []
	for r in result:
		outputs.append({
			"course_id": r[0],		"logo": r[1],
			"name": r[2],			"language": r[3],
			"level_type": r[4],		"deg_name": r[5],
			"curr_value": float(r[6]),		"curr_type": r[7],
			"ins_name": r[8],		"description": r[9],
			"intake_month": r[10],	"deadline_month": r[11],
			"dur_year": r[12],		"address": r[13],
			"country": r[14],		"url": r[15],
		})
	return outputs


def apply_filter(cursor, body):

	def get_distinct_query(key, val):
		if val == ["All"]:
			return " ( true ) "

		table_place = ([filter['table_place']
						for filter in filters if filter['filter_name'] == key][0])
		q = "("
		for v in val:
			q += f' {table_place} = "{v}" OR'
		q = q[:-3] + ")"

		return q

	def get_cont_query(key, val):
		table_place = [filter['table_place']
					   for filter in filters if filter['filter_name'] == key][0]
		return f' ( {table_place} >= {val[0]} AND {table_place} <= {val[1]} ) '

	def fill_condition(where_clause="true"):
		# courses.course_id, courses.name
		return f"""
			SELECT
				*
			FROM
				courses
				JOIN language ON courses.lang_id = language.lang_id
				JOIN fee ON courses.course_id = fee.course_id
				JOIN campus ON courses.campus_id = campus.campus_id
				JOIN course_duration ON courses.dur_id = course_duration.dur_id
				JOIN degree_level ON courses.deg_id = degree_level.deg_id
				JOIN location ON campus.l_id = location.loc_id
				JOIN country ON location.coun_id = country.coun_id
				JOIN specialization ON courses.spec_id = specialization.spec_id
				JOIN discipline ON specialization.disc_id = discipline.disc_id
				JOIN institute ON campus.ins_id = institute.ins_id
			WHERE
				{where_clause}
			;
		"""

	query = ""
	for filter in filters:
		if filter['type'] == "distinct":
			query += get_distinct_query(filter['filter_name'],
										body.get(filter['filter_name'], ["All"])) + " AND "
		else:
			query += get_cont_query(filter['filter_name'],
									body.get(filter['filter_name'], [0, 1e20])) + " AND "
	query = query[:-4]

	final_querry = fill_condition(query)
	cursor.execute(final_querry)

	results = cursor.fetchall()

	if body.get('search', "").replace(" ", "") == "":
		course_ids = [i[0] for i in results]
	else:
		course_ids = sort_by_search(body['search'], results)

	course_ids = course_ids[:body.get('limit', 100)]

	return get_short_info(cursor, course_ids)


"""
{
	"search": "",
	"limit": 100,

	"Country": ["All"],
	"Duration (years)": [2, 3],
	"Degree Level": ["Bachelors","Certificate","Diploma"],
	"Discipline": ["All"],
	"Fee": [1203255.96, 13068627.27],
	"Institute": ["University"],
	"Language": ["All"],
}
"""
