from data import univ_settings
from collections import OrderedDict
import os
from datetime import datetime
from state_abbr import states
pres_states = states + ['PRESIDENTIAL']
ELECTION=2013
TESTONLY=True
DEFAULT_ACTUAL_TABLE = {
        'long_fields':(),
        'long_from':(),
        'long_to':(),
        }
DEFAULT_TABLE = {
        'skip_head_lines':1,
        'format':'csv',
        'field_sep':',',
        'quotechar':'"',
        'copy_every':100000,
        'udcs':{
            },
        'elections':('2012','2013'),
        }

def nowtime():
    d = datetime.now()
    return d.strftime('%Y-%m-%dT%H:%M:%S'),

ELECTORAL_DISTRICT_IMPORT = dict(DEFAULT_TABLE)
ELECTORAL_DISTRICT_IMPORT.update({
    'sources':[s+'VF' for s in states],
    'dict_reader':True,
    'table':'electoral_district_import',
    'columns':{'election_key': 'election_key', 'updated': {'function': nowtime, 'columns': ()}, 'name': 'name', 'number': 'number', 'source': 'source', 'state_id': 'state_id', 'identifier': 'identifier', 'type': 'type', 'id': 'id'}
    })

ELECTORAL_DISTRICT_ACTUAL = dict(DEFAULT_ACTUAL_TABLE)
ELECTORAL_DISTRICT_ACTUAL.update({
    'schema_table':'electoral_district',
    'import_table':ELECTORAL_DISTRICT_IMPORT,
    'long_fields':({'long':'id_long','real':'id'},),
    'long_from':(),
    'distinct_on':(),
    })

CONTEST_IMPORT = dict(DEFAULT_TABLE)
CONTEST_IMPORT.update({
    'sources':[s+'Candidates' for s in pres_states],
    'dict_reader':True,
    'table':'contest_import',
    'columns':{'electoral_district_id': 'electoral_district_id', 'office': 'office', 'electorate_specifications': 'electorate_specifications', 'id': 'id', 'special': 'special', 'partisan': 'partisan', 'contest_type': 'contest_type', 'write_in': 'write_in', 'source': 'source', 'state': 'state', 'electoral_district_name': 'electoral_district_name', 'election_id': 'election_id', 'electoral_district_type': 'electoral_district_type', 'election_key': 'election_key', 'updated': {'function': nowtime, 'columns': ()}, 'filing_closed_date': 'filing_closed_date', 'number_voting_for': 'number_voting_for', 'custom_ballot_heading': 'custom_ballot_heading', 'ballot_placement': 'ballot_placement', 'primary_party': 'primary_party', 'type': 'type', 'office_level': 'office_level', 'ed_matched': 'ed_matched', 'identifier': 'identifier', 'number_elected': 'number_elected'}
    })

CONTEST_ACTUAL = dict(DEFAULT_ACTUAL_TABLE)
CONTEST_ACTUAL.update({
    'schema_table':'contest',
    'import_table':CONTEST_IMPORT,
    'long_fields':({'long':'id_long','real':'id'},{'long':'electoral_district_id_long','real':'electoral_district_id'},{'long':'election_id_long','real':'election_id'}),
    'distinct_on':(),
    'long_from':(),
    'long_to':(),
    })

CANDIDATE_IN_CONTEST_IMPORT = dict(DEFAULT_TABLE)
CANDIDATE_IN_CONTEST_IMPORT.update({
    'sources':[s+'Candidates' for s in pres_states],
    'dict_reader':True,
    'table':'candidate_in_contest_import',
    'columns':{'source': 'source', 'contest_id': 'contest_id', 'sort_order': 'sort_order', 'candidate_id': 'candidate_id', 'election_key': 'election_key'},
    })

CANDIDATE_IN_CONTEST_ACTUAL = dict(DEFAULT_ACTUAL_TABLE)
CANDIDATE_IN_CONTEST_ACTUAL.update({
    'schema_table':'candidate_in_contest',
    'import_table':CANDIDATE_IN_CONTEST_IMPORT,
    'long_fields':(),
    'long_to':()
    })

CANDIDATE_IMPORT = dict(DEFAULT_TABLE)
CANDIDATE_IMPORT.update({
    'sources':[s+'Candidates' for s in pres_states],
    'table':'candidate_import',
    'dict_reader':True,
    'columns':{'filed_mailing_address': 'filed_mailing_address', 'election_key': 'election_key', 'updated': {'function': nowtime, 'columns': ()}, 'name': 'name', 'source': 'source', 'mailing_address': 'mailing_address', 'facebook_url': 'facebook_url', 'youtube': 'youtube', 'email': 'email', 'candidate_url': 'candidate_url', 'phone': 'phone', 'google_plus_url': 'google_plus_url', 'twitter_name': 'twitter_name', 'incumbent': 'incumbent', 'party': 'party', 'wiki_word': 'wiki_word', 'identifier': 'identifier', 'id': 'id', 'biography': 'biography', 'photo_url': 'photo_url'}
    })

CANDIDATE_ACTUAL = dict(DEFAULT_ACTUAL_TABLE)
CANDIDATE_ACTUAL.update({
    'schema_table':'candidate',
    'import_table':CANDIDATE_IMPORT,
    'long_fields':({'long':'id_long','real':'id'},),
    'long_from':(),
    })

REFERENDUM_IMPORT = dict(DEFAULT_TABLE)
REFERENDUM_IMPORT.update({
    'sources':['referenda'],
    'dict_reader':True,
    'table':'referendum_import',
    'columns':{'election_key': 'election_key', 'updated': {'function': nowtime, 'columns': ()}, 'subtitle': 'subtitle', 'title': 'title', 'text': 'text', 'con_statement': 'con_statement', 'brief': 'brief', 'effect_of_abstain': 'effect_of_abstain', 'contest_id': 'contest_id', 'source': 'source', 'passage_threshold': 'passage_threshold', 'identifier': 'identifier', 'id': 'id', 'pro_statement': 'pro_statement'}
    })

REFERENDUM_ACTUAL = dict(DEFAULT_ACTUAL_TABLE)
REFERENDUM_ACTUAL.update({
    'schema_table':'referendum',
    'import_table':REFERENDUM_IMPORT,
    'long_fields':({'long':'id_long','real':'id'},{'long':'contest_id_long','real':'contest_id'}),
    'long_from':(),
    })
BALLOT_RESPONSE_IMPORT = dict(DEFAULT_TABLE)
BALLOT_RESPONSE_IMPORT.update({
    'sources':['referenda'],
    'dict_reader':True,
    'table':'ballot_response_import',
    'columns':{'election_key': 'election_key', 'updated': {'function': nowtime, 'columns': ()}, 'text': 'text', 'referendum_id': 'referendum_id', 'source': 'source', 'sort_order': 'sort_order', 'identifier': 'identifier', 'id': 'id'}
    })

BALLOT_RESPONSE_ACTUAL = dict(DEFAULT_ACTUAL_TABLE)
BALLOT_RESPONSE_ACTUAL.update({
    'schema_table':'ballot_response',
    'import_table':BALLOT_RESPONSE_IMPORT,
    'long_fields':({'long':'referendum_id_long','real':'referendum_id'},),
    'long_from':(),
    })

ELECTION_IMPORT = dict(DEFAULT_TABLE)
ELECTION_IMPORT.update({
    'table':'election_import',
    'dict_reader':True,
    'sources':['election'],
    'columns':{'election_key': 'election_key', 'registration_deadline': 'registration_deadline', 'name': 'name', 'identifier': 'identifier', 'statewide': 'statewide', 'absentee_ballot_info': 'absentee_ballot_info', 'is_special': 'is_special', 'registration_info': 'registration_info', 'election_type': 'election_type', 'source': 'source', 'absentee_request_deadline': 'absentee_request_deadline', 'polling_hours': 'polling_hours', 'results_url': 'results_url', 'date': 'date', 'state_id': 'state_id', 'election_day_registration': 'election_day_registration', 'id': 'id', 'updated': {'function': nowtime, 'columns': ()}}
    })

ELECTION_ACTUAL = dict(DEFAULT_ACTUAL_TABLE)
ELECTION_ACTUAL.update({
    'schema_table':'election',
    'import_table':ELECTION_IMPORT,
    'long_fields':({'long':'id_long','real':'id'},),
    'long_from':('id_long',),
    })


UNIONS = ()
GROUPS = ()
ACTUAL_TABLES = (
        CANDIDATE_ACTUAL,
        CANDIDATE_IN_CONTEST_ACTUAL,
        CONTEST_ACTUAL,
        ELECTORAL_DISTRICT_ACTUAL,
        REFERENDUM_ACTUAL,
        BALLOT_RESPONSE_ACTUAL,
        ELECTION_ACTUAL,
        )
ERSATZPG_CONFIG = {'debug':True, 'use_utf':False, 'testonly':TESTONLY}
ERSATZPG_CONFIG.update(univ_settings.DATABASE_CONFIG)
ERSATZPG_CONFIG.update({
    'tables':{
        'candidate':CANDIDATE_IMPORT,
        'contest':CONTEST_IMPORT,
        'candidate_in_contest':CANDIDATE_IN_CONTEST_IMPORT,
        'electoral_district':ELECTORAL_DISTRICT_IMPORT,
        #'referendum':REFERENDUM_IMPORT,
        #'ballot_response':BALLOT_RESPONSE_IMPORT,
        }
    })

CANDIDATE_FIELDS=OrderedDict([
    ('id', 'int4'), ('source', 'text'), ('name', 'varchar(255)'), ('party', 'varchar(255)'), ('candidate_url', 'varchar(255)'), ('biography', 'varchar(255)'), ('phone', 'varchar(255)'), ('photo_url', 'varchar(255)'), ('filed_mailing_address', 'int4'), ('mailing_address', 'text'), ('email', 'varchar(255)'), ('incumbent', 'bool'), ('google_plus_url', 'varchar(255)'), ('twitter_name', 'varchar(255)'), ('facebook_url', 'varchar(255)'), ('wiki_word', 'varchar(255)'), ('youtube', 'text'), ('election_key', 'int4'), ('identifier', 'text'), ('updated','timestamp'),
    ])

CONTEST_FIELDS = OrderedDict([
    ('id', 'int4'), ('source', 'text'), ('election_id', 'int4'), ('electoral_district_id', 'int4'), ('electoral_district_name', 'varchar(255)'), ('electoral_district_type', 'varchar(255)'), ('partisan', 'bool'), ('type', 'varchar(255)'), ('primary_party', 'varchar(255)'), ('electorate_specifications', 'varchar(255)'), ('special', 'bool'), ('office', 'varchar(255)'), ('filing_closed_date', 'date'), ('number_elected', 'int4'), ('number_voting_for', 'int4'), ('ballot_placement', 'varchar(255)'), ('contest_type', 'contestenum'), ('write_in', 'bool'), ('custom_ballot_heading', 'text'), ('election_key', 'int4'), ('state', 'varchar(5)'), ('identifier', 'text'), ('updated','timestamp'), ('office_level','varchar(255)'),('ed_matched','bool'),
    ])

CANDIDATE_IN_CONTEST_FIELDS = OrderedDict([
    ('source', 'text'), ('election_key', 'int4'), ('sort_order', 'int4'), ('contest_id', 'int4'), ('candidate_id', 'int4')
    ])

ELECTORAL_DISTRICT_FIELDS = OrderedDict([
    ('id', 'int4'), ('source', 'text'), ('name', 'varchar(255)'), ('type', 'varchar(255)'), ('number', 'int4'), ('state_id', 'int4'), ('election_key', 'int4'), ('identifier', 'text'), ('updated','timestamp'),
    ])

REFERENDUM_FIELDS = OrderedDict([
    ("id", 'int4'),
    ("source", 'text'),
    ("title", 'text'),
    ("subtitle", 'text'),
    ("brief", 'text'),
    ("text", 'varchar(255)'),
    ("pro_statement", 'varchar(255)'),
    ("con_statement", 'varchar(255)'),
    ("contest_id", 'int4'),
    ("passage_threshold", 'varchar(255)'),
    ("effect_of_abstain", 'varchar(255)'),
    ("election_key", 'int4'),
    ("updated", 'timestamp'),
    ("identifier", 'text'),])

BALLOT_RESPONSE_FIELDS = OrderedDict([
    ("id", 'int4'),
    ("source", 'text'),
    ("referendum_id", 'int4'),
    ("sort_order", 'varchar(255)'),
    ("text", 'text'),
    ("election_key", 'int4'),
    ("updated", 'timestamp'),
    ("identifier", 'text'),])

ELECTION_FIELDS = OrderedDict([
("id", 'int4'),
("source", 'text'),
("date", 'date'),
("election_type", 'electionenum'),
("state_id", 'int4'),
("statewide", 'bool'),
("is_special", 'bool'),
("name", 'text'),
("registration_info", 'varchar(255)'),
("absentee_ballot_info", 'varchar(255)'),
("results_url", 'varchar(255)'),
("polling_hours", 'varchar(255)'),
("election_day_registration", 'bool'),
("registration_deadline", 'varchar(255)'),
("absentee_request_deadline", 'varchar(255)'),
("election_key", 'int4'),
("identifier", 'text'),
("updated", 'timestamp'),
])
