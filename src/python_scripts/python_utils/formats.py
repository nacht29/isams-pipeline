from google.cloud import bigquery as bq

'''
Mandatory
'''

# content mimetype for Google Sheets ad GCP
content_data = {
	'.csv': {'content_type': 'text/csv', 'type_name': 'CSV'},
	'.txt': {'content_type': 'text/plain', 'type_name': 'Text'},
	'.xlsx': {'content_type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'type_name': 'Excel'},
	'.log': {'content_type': 'text/plain', 'type_name': 'Log'}
}

'''
BigQuery Schema
'''
applicant_schema = [
	bq.SchemaField("admissionStatus", "STRING", mode="NULLABLE"),
	bq.SchemaField("birthCounty", "STRING", mode="NULLABLE"),
	bq.SchemaField("birthplace", "STRING", mode="NULLABLE"),
	bq.SchemaField("boardingStatus", "STRING", mode="NULLABLE"),
	bq.SchemaField("currentSchoolId", "INTEGER", mode="NULLABLE"),
	bq.SchemaField("dateOfBirth", "DATETIME", mode="NULLABLE"),
	bq.SchemaField("enquiryDate", "DATETIME", mode="NULLABLE"),
	bq.SchemaField("enquiryReason", "STRING", mode="NULLABLE"),
	bq.SchemaField("enquiryType", "STRING", mode="NULLABLE"),
	bq.SchemaField("enrolmentAcademicHouseId", "INTEGER", mode="NULLABLE"),
	bq.SchemaField("enrolmentBoardingHouseId", "INTEGER", mode="NULLABLE"),
	bq.SchemaField("enrolmentDate", "DATETIME", mode="NULLABLE"),
	bq.SchemaField("enrolmentOfferType", "STRING", mode="NULLABLE"),
	bq.SchemaField("enrolmentSchoolForm", "STRING", mode="NULLABLE"),
	bq.SchemaField("enrolmentSchoolTerm", "STRING", mode="NULLABLE"),
	bq.SchemaField("enrolmentSchoolYear", "INTEGER", mode="NULLABLE"),
	bq.SchemaField("enrolmentSchoolYearGroup", "INTEGER", mode="NULLABLE"),
	bq.SchemaField("ethnicity", "STRING", mode="NULLABLE"),
	bq.SchemaField("familyId", "INTEGER", mode="NULLABLE"),
	bq.SchemaField("forename", "STRING", mode="NULLABLE"),
	bq.SchemaField("fullName", "STRING", mode="NULLABLE"),
	bq.SchemaField("gender", "STRING", mode="NULLABLE"),
	bq.SchemaField("initials", "STRING", mode="NULLABLE"),
	bq.SchemaField("isReadmission", "BOOLEAN", mode="NULLABLE"),
	bq.SchemaField("isVisaRequired", "BOOLEAN", mode="NULLABLE"),
	bq.SchemaField("labelSalutation", "STRING", mode="NULLABLE"),
	# For ARRAY<STRING>, the type is STRING and the mode is REPEATED.
	bq.SchemaField("languages", "STRING", mode="REPEATED"),
	bq.SchemaField("lastUpdated", "DATETIME", mode="NULLABLE"),
	bq.SchemaField("letterSalutation", "STRING", mode="NULLABLE"),
	bq.SchemaField("middleNames", "STRING", mode="NULLABLE"),
	bq.SchemaField("mobileNumber", "STRING", mode="NULLABLE"),
	bq.SchemaField("nationalities", "STRING", mode="REPEATED"),
	bq.SchemaField("officialName", "STRING", mode="NULLABLE"),
	bq.SchemaField("personGuid", "STRING", mode="NULLABLE"),
	bq.SchemaField("personId", "INTEGER", mode="NULLABLE"),
	bq.SchemaField("preferredName", "STRING", mode="NULLABLE"),
	bq.SchemaField("registeredDate", "DATETIME", mode="NULLABLE"),
	bq.SchemaField("religion", "STRING", mode="NULLABLE"),
	bq.SchemaField("residentCountry", "STRING", mode="NULLABLE"),
	bq.SchemaField("schoolCode", "STRING", mode="NULLABLE"),
	bq.SchemaField("schoolEmailAddress", "STRING", mode="NULLABLE"),
	bq.SchemaField("schoolId", "STRING", mode="NULLABLE"),
	bq.SchemaField("surname", "STRING", mode="NULLABLE"),
	bq.SchemaField("systemStatus", "STRING", mode="NULLABLE"),
	bq.SchemaField("title", "STRING", mode="NULLABLE"),
	bq.SchemaField("uniquePupilNumber", "STRING", mode="NULLABLE"),
	bq.SchemaField("withdrawnDate", "DATETIME", mode="NULLABLE"),
	bq.SchemaField("withdrawnReason", "STRING", mode="NULLABLE"),
	bq.SchemaField("withdrawnReasonNote", "STRING", mode="NULLABLE"),
]

students_schema = [
	bq.SchemaField("id", "INTEGER", mode="NULLABLE"),
	bq.SchemaField("academicHouse", "STRING", mode="NULLABLE"),
	bq.SchemaField("birthCounty", "STRING", mode="NULLABLE"),
	bq.SchemaField("birthplace", "STRING", mode="NULLABLE"),
	bq.SchemaField("boardingHouse", "STRING", mode="NULLABLE"),
	bq.SchemaField("boardingStatus", "STRING", mode="NULLABLE"),
	bq.SchemaField("dob", "DATE", mode="NULLABLE"),
	bq.SchemaField("enrolmentDate", "DATE", mode="NULLABLE"),
	bq.SchemaField("enrolmentStatus", "STRING", mode="NULLABLE"),
	bq.SchemaField("enrolmentTerm", "STRING", mode="NULLABLE"),
	bq.SchemaField("enrolmentYear", "INTEGER", mode="NULLABLE"),
	bq.SchemaField("ethnicity", "STRING", mode="NULLABLE"),
	bq.SchemaField("familyId", "INTEGER", mode="NULLABLE"),
	bq.SchemaField("forename", "STRING", mode="NULLABLE"),
	bq.SchemaField("formGroup", "STRING", mode="NULLABLE"),
	bq.SchemaField("fullName", "STRING", mode="NULLABLE"),
	bq.SchemaField("futureSchoolId", "INTEGER", mode="NULLABLE"),
	bq.SchemaField("gender", "STRING", mode="NULLABLE"),
	bq.SchemaField("homeAddresses", "RECORD", mode="REPEATED", fields=[
		bq.SchemaField("id", "INTEGER", mode="NULLABLE"),
		bq.SchemaField("address1", "STRING", mode="NULLABLE"),
		bq.SchemaField("address2", "STRING", mode="NULLABLE"),
		bq.SchemaField("address3", "STRING", mode="NULLABLE"),
		bq.SchemaField("country", "STRING", mode="NULLABLE"),
		bq.SchemaField("county", "STRING", mode="NULLABLE"),
		bq.SchemaField("postcode", "STRING", mode="NULLABLE"),
		bq.SchemaField("private", "BOOLEAN", mode="NULLABLE"),
		bq.SchemaField("town", "STRING", mode="NULLABLE"),
	]),
	bq.SchemaField("initials", "STRING", mode="NULLABLE"),
	bq.SchemaField("isVisaRequired", "BOOLEAN", mode="NULLABLE"),
	bq.SchemaField("labelSalutation", "STRING", mode="NULLABLE"),
	bq.SchemaField("languages", "STRING", mode="REPEATED"),
	bq.SchemaField("lastUpdated", "TIMESTAMP", mode="NULLABLE"),
	bq.SchemaField("latestPhotoId", "INTEGER", mode="NULLABLE"),
	bq.SchemaField("leavingDate", "DATE", mode="NULLABLE"),
	bq.SchemaField("leavingReason", "STRING", mode="NULLABLE"),
	bq.SchemaField("leavingYearGroup", "INTEGER", mode="NULLABLE"),
	bq.SchemaField("letterSalutation", "STRING", mode="NULLABLE"),
	bq.SchemaField("middlenames", "STRING", mode="NULLABLE"),
	bq.SchemaField("mobileNumber", "STRING", mode="NULLABLE"),
	bq.SchemaField("nationalities", "STRING", mode="REPEATED"),
	bq.SchemaField("officialName", "STRING", mode="NULLABLE"),
	bq.SchemaField("personalEmailAddress", "STRING", mode="NULLABLE"),
	bq.SchemaField("personGuid", "STRING", mode="NULLABLE"),
	bq.SchemaField("personId", "INTEGER", mode="NULLABLE"),
	bq.SchemaField("preferredName", "STRING", mode="NULLABLE"),
	bq.SchemaField("previousName", "STRING", mode="NULLABLE"),
	bq.SchemaField("religion", "STRING", mode="NULLABLE"),
	bq.SchemaField("removalGrounds", "STRING", mode="NULLABLE"),
	bq.SchemaField("residentCountry", "STRING", mode="NULLABLE"),
	bq.SchemaField("schoolCode", "STRING", mode="NULLABLE"),
	bq.SchemaField("schoolId", "STRING", mode="NULLABLE"),
	bq.SchemaField("schoolEmailAddress", "STRING", mode="NULLABLE"),
	bq.SchemaField("surname", "STRING", mode="NULLABLE"),
	bq.SchemaField("systemStatus", "STRING", mode="NULLABLE"),
	bq.SchemaField("title", "STRING", mode="NULLABLE"),
	bq.SchemaField("tutorEmployeeId", "INTEGER", mode="NULLABLE"),
	bq.SchemaField("uniquePupilNumber", "STRING", mode="NULLABLE"),
	bq.SchemaField("yearGroup", "INTEGER", mode="NULLABLE"),
]

alumni_schema = [
	bq.SchemaField("admissionStatus", "STRING", mode="NULLABLE"),
	bq.SchemaField("boardingStatus", "STRING", mode="NULLABLE"),
	bq.SchemaField("enquiryDate", "DATE", mode="NULLABLE"),
	bq.SchemaField("enrolmentDate", "DATE", mode="NULLABLE"),
	bq.SchemaField("enrolmentYear", "INTEGER", mode="NULLABLE"),
	bq.SchemaField("enrolmentYearGroup", "INTEGER", mode="NULLABLE"),
	bq.SchemaField("forename", "STRING", mode="NULLABLE"),
	bq.SchemaField("fullName", "STRING", mode="NULLABLE"),
	bq.SchemaField("futureSchoolId", "INTEGER", mode="NULLABLE"),
	bq.SchemaField("gender", "STRING", mode="NULLABLE"),
	bq.SchemaField("initials", "STRING", mode="NULLABLE"),
	bq.SchemaField("languages", "STRING", mode="REPEATED"),
	bq.SchemaField("lastUpdated", "DATETIME", mode="NULLABLE"),
	bq.SchemaField("leavingDate", "DATE", mode="NULLABLE"),
	bq.SchemaField("leavingReason", "STRING", mode="NULLABLE"),
	bq.SchemaField("leavingTerm", "STRING", mode="NULLABLE"),
	bq.SchemaField("leavingYear", "INTEGER", mode="NULLABLE"),
	bq.SchemaField("leavingYearGroup", "INTEGER", mode="NULLABLE"),
	bq.SchemaField("middlenames", "STRING", mode="NULLABLE"),
	bq.SchemaField("nationalities", "STRING", mode="REPEATED"),
	bq.SchemaField("officialName", "STRING", mode="NULLABLE"),
	bq.SchemaField("personGuid", "STRING", mode="NULLABLE"),
	bq.SchemaField("personId", "INTEGER", mode="NULLABLE"),
	bq.SchemaField("preferredName", "STRING", mode="NULLABLE"),
	bq.SchemaField("registeredDate", "DATE", mode="NULLABLE"),
	bq.SchemaField("schoolCode", "STRING", mode="NULLABLE"),
	bq.SchemaField("schoolId", "STRING", mode="NULLABLE"),
	bq.SchemaField("surname", "STRING", mode="NULLABLE"),
	bq.SchemaField("systemStatus", "STRING", mode="NULLABLE"),
	bq.SchemaField("title", "STRING", mode="NULLABLE"),
	bq.SchemaField("visitDate", "DATE", mode="NULLABLE"),
	bq.SchemaField("yearGroup", "INTEGER", mode="NULLABLE"),
]

school_terms_schema = [
	bq.SchemaField("id", "INTEGER", mode="NULLABLE"),
	bq.SchemaField("finishDate", "DATETIME", mode="NULLABLE"),
	bq.SchemaField("name", "STRING", mode="NULLABLE"),
	bq.SchemaField("schoolYear", "INTEGER", mode="NULLABLE"),
	bq.SchemaField("startDate", "DATETIME", mode="NULLABLE"),
]

year_groups_schema = [
	bq.SchemaField("assistantTutorId", "INTEGER", mode="NULLABLE"),
	bq.SchemaField("averageStartingAge", "FLOAT", mode="NULLABLE"),
	bq.SchemaField("censusYearGroup", "STRING", mode="NULLABLE"),
	bq.SchemaField("code", "STRING", mode="REQUIRED"),
	bq.SchemaField("emailAddress", "STRING", mode="NULLABLE"),
	bq.SchemaField("iscEnglandWalesYearGroup", "STRING", mode="NULLABLE"),
	bq.SchemaField("iscIrelandYearGroup", "STRING", mode="NULLABLE"),
	bq.SchemaField("iscScotlandYearGroup", "STRING", mode="NULLABLE"),
	bq.SchemaField("lastUpdated", "TIMESTAMP", mode="NULLABLE"),
	bq.SchemaField("name", "STRING", mode="REQUIRED"),
	bq.SchemaField("ncYear", "INTEGER", mode="REQUIRED"),
	bq.SchemaField("reference", "STRING", mode="NULLABLE"),
	bq.SchemaField("tutorId", "INTEGER", mode="NULLABLE"),
	bq.SchemaField("websiteAddress", "STRING", mode="NULLABLE"),
]

billing_cycles_schema = [
	bq.SchemaField("id", "INTEGER", mode="REQUIRED"),
	bq.SchemaField("active", "BOOLEAN"),
	bq.SchemaField("earlyPaymentDate", "DATETIME"),
	bq.SchemaField("endDate", "DATETIME"),
	bq.SchemaField("name", "STRING"),
	bq.SchemaField("schoolYear", "INTEGER"),
	bq.SchemaField("startDate", "DATETIME")
]

'''
iSAMS API
'''

isams_dataset_endpoints = {
	'applicants': {
		'url': '/api/admissions/applicants/students',
		'object': 'students',
		'pages': 'multi-page',
		'table_id':'taylors-data-poc.isams_data.applicants',
		'schema': applicant_schema,
		'nested_fields': None
	},

	'students': {
		'url': '/api/students',
		'object': 'students',
		'pages': 'multi-page',
		'table_id': 'taylors-data-poc.isams_data.students',
		'schema': students_schema,
	},
	
	'alumni': {
		'url': '/api/alumni',
		'object': 'alumni',
		'pages': 'multi-page',
		'table_id': 'taylors-data-poc.isams_data.alumni',
		'schema': alumni_schema,
	},
	
	'school_terms': {
		'url': '/api/school/terms',
		'object': 'terms',
		'pages': 'single-page',
		'table_id': 'taylors-data-poc.isams_data.school_terms',
		'schema': school_terms_schema
	},
	
	'year_groups' : {
		'url': '/api/school/yeargroups',
		'object': 'yearGroups',
		'pages': 'single-page',
		'table_id': 'taylors-data-poc.isams_data.year_groups',
		'schema': year_groups_schema
	},
	
	'billing_cycles' : {
		'url': '/api/billing/invoicing/cycles',
		'object': 'billingCycles',
		'pages': 'single-page',
		'table_id': 'taylors-data-poc.isams_data.billing_cycles',
		'schema': billing_cycles_schema
	}
}
