from ersatzpg import ersatz
from schema import process_schema, table_tools, create_partitions, create_precinct_to_ed
import determine_districts
from data.state_abbr import states
from data import univ_settings
from data import bipbuild_conf
import time, sys, imp, os, random, csv
from multiprocessing import Pool
from collections import defaultdict, OrderedDict

all_states = 'ak,al,ar,az,ca,co,ct,dc,de,fl,ga,hi,ia,id,il,in,ks,ky,la,ma,md,me,mi,mn,mo,ms,mt,nc,nd,ne,nh,nj,nm,nv,ny,oh,ok,or,pa,ri,sc,sd,tn,tx,ut,va,vt,wa,wi,wv,wy'
state_ins = sys.argv[-1].lower()
if state_ins == 'all':
    state_ins = all_states
do_all = ['-clean','-partition','-clean_import','-build','-distinct','-unions','-rekey','-export']
do_all_no_clean =['-clean_import','-build','-distinct','-unions','-rekey','-export']
if '-all' in sys.argv:
    sys.argv = sys.argv[:-1] + do_all + [sys.argv[-1]]

if '-all_no_clean' in sys.argv:
    sys.argv = sys.argv[:-1] + do_all_no_clean + [sys.argv[-1]]

tables, enums, fks, seqs = process_schema.rip_schema('schema/bip_model_reduced.sql')
#table_tools.define_long_tables(tables, fks)

if '-clean' in sys.argv:
    t =time.time()
    connection = ersatz.db_connect(univ_settings.ERSATZPG_CONFIG)
#    table_tools.delete_pksq(connection)
#    table_tools.create_pksq(connection)
    table_tools.delete_enums(connection)
    table_tools.create_enums(connection)
    table_tools.delete_tables(tables, connection)
    table_tools.create_tables(tables, connection)
    table_tools.delete_import_tables(bipbuild_conf.ACTUAL_TABLES, bipbuild_conf.UNIONS, connection)
    table_tools.create_import_tables(bipbuild_conf.ACTUAL_TABLES, tables, connection)
    connection.commit()
    connection.close()
    t = time.time() - t
    print "Elapsed: %s" % (t,)
if '-partition' in sys.argv:
    t =time.time()
    connection = ersatz.db_connect(bipbuild_conf.ERSATZPG_CONFIG)
    finished_schema_tables = []
    for table in bipbuild_conf.ACTUAL_TABLES:
        if table['schema_table'] not in finished_schema_tables:
            finished_schema_tables.append(table['schema_table'])
            od = OrderedDict([('source',table['import_table']['sources']),('election_key',table['import_table']['elections'])])
            create_partitions.create_discrete_partitions([table['schema_table']], od, connection.cursor())
            connection.commit()
    connection.close()
    t = time.time() - t
    print "Elapsed: %s" % (t,)
state_ins = state_ins.split(',')
if 'referenda' in state_ins:
    state_ins.pop(state_ins.index('referenda'))
    state_ins.append('referenda')
if 'presidential' in state_ins:
    state_ins.pop(state_ins.index('presidential'))
    state_ins.append('presidential')
if 'election' in state_ins:
    state_ins.pop(state_ins.index('election'))
    state_ins.insert(0,'election')
for state in state_ins:
    print "processing {state} out of {states}".format(state=state, states=state_ins)
    state = state.strip()
    state_location = os.path.join('/home/gaertner/Dropbox/BIP Production/candidate_to_ed_tables',state)
    candidate_location = os.path.join(state_location, 'candidate.csv')
    contest_location = os.path.join(state_location, 'contest.csv')
    cic_location = os.path.join(state_location, 'candidate_in_contest.csv')
    ed_location = os.path.join(state_location, 'electoral_district.csv')
    referendum_location = os.path.join(state_location, 'referendum.csv')
    br_location = os.path.join(state_location, 'ballot_response.csv')
    el_location = os.path.join(state_location, 'election.csv')
    candidate_source = '{state}Candidates'.format(state=state.upper())
    ed_source = '{state}VF'.format(state=state.upper())
    source = {
            'candidate':candidate_source,
            'contest': (candidate_source if state != 'referenda' else 'referenda'),
            'candidate_in_contest':candidate_source,
            'electoral_district':ed_source,
            'referendum':'referenda',
            'ballot_response':'referenda',
            'election':'election',
            }
    election= bipbuild_conf.ELECTION

    if '-clean_import' in sys.argv:
        t =time.time()
        connection = ersatz.db_connect(bipbuild_conf.ERSATZPG_CONFIG)
        table_tools.delete_import_tables(bipbuild_conf.ACTUAL_TABLES, bipbuild_conf.UNIONS, connection)
        table_tools.create_import_tables(bipbuild_conf.ACTUAL_TABLES, tables, connection)
        connection.commit()
        connection.close()
        t = time.time() - t
        print "Elapsed: %s" % (t,)
    if '-build' in sys.argv:
        t =time.time()
        connection = ersatz.db_connect(bipbuild_conf.ERSATZPG_CONFIG)
        bipbuild_conf.CONTEST_IMPORT['filename'] = contest_location
        bipbuild_conf.CANDIDATE_IMPORT['filename'] = candidate_location
        bipbuild_conf.CANDIDATE_IN_CONTEST_IMPORT['filename'] = cic_location
        bipbuild_conf.ELECTORAL_DISTRICT_IMPORT['filename'] = ed_location
        bipbuild_conf.REFERENDUM_IMPORT['filename'] = referendum_location
        bipbuild_conf.BALLOT_RESPONSE_IMPORT['filename'] = br_location
        bipbuild_conf.ELECTION_IMPORT['filename'] = el_location
        if state=='presidential':
            bipbuild_conf.ERSATZPG_CONFIG['tables'] = {
                'candidate':bipbuild_conf.CANDIDATE_IMPORT,
                'contest':bipbuild_conf.CONTEST_IMPORT,
                'candidate_in_contest':bipbuild_conf.CANDIDATE_IN_CONTEST_IMPORT,
                #'electoral_district':ELECTORAL_DISTRICT_IMPORT,
                #'referendum':REFERENDUM_IMPORT,
                #'ballot_response':BALLOT_RESPONSE_IMPORT,
                }
        elif state=='referenda':
            bipbuild_conf.ERSATZPG_CONFIG['tables'] = {
                    #'candidate':CANDIDATE_IMPORT,
                'contest':bipbuild_conf.CONTEST_IMPORT,
                #'candidate_in_contest':CANDIDATE_IN_CONTEST_IMPORT,
                #'electoral_district':ELECTORAL_DISTRICT_IMPORT,
                'referendum':bipbuild_conf.REFERENDUM_IMPORT,
                'ballot_response':bipbuild_conf.BALLOT_RESPONSE_IMPORT,
                }
        elif state=='election':
            bipbuild_conf.ERSATZPG_CONFIG['tables'] = {
                    'election':bipbuild_conf.ELECTION_IMPORT,
                    }
        else:
            bipbuild_conf.ERSATZPG_CONFIG['tables']={
                    'candidate':bipbuild_conf.CANDIDATE_IMPORT,
                    'contest':bipbuild_conf.CONTEST_IMPORT,
                    'candidate_in_contest':bipbuild_conf.CANDIDATE_IN_CONTEST_IMPORT,
                    'electoral_district':bipbuild_conf.ELECTORAL_DISTRICT_IMPORT,
                    #'referendum':REFERENDUM_IMPORT,
                    #'ballot_response':BALLOT_RESPONSE_IMPORT,
                    }

        ersatz.new_process_copies(bipbuild_conf, connection)
        for table_name in bipbuild_conf.ERSATZPG_CONFIG['tables']:
            if table_name == 'candidate_in_contest':
                continue
            FIELDS = bipbuild_conf.__dict__[table_name.upper()+'_FIELDS']
            ufields = OrderedDict(FIELDS)
            ufields.pop('updated')
            ufields = ','.join('{u}={table_name}_import.{u}'.format(u=u,table_name=table_name) for u in ufields)
            test_fields = OrderedDict(FIELDS)
            test_fields.pop('updated')
            test_fields.pop('identifier')
            actual_table = bipbuild_conf.__dict__[table_name.upper()+'_ACTUAL']
            for lfd in actual_table['long_fields']:
                test_fields.pop(lfd['real'])
            test_fields = ' or '.join('{table_name}_{source}_{election}.{u} IS DISTINCT FROM {table_name}_import.{u}'.format(u=u,source=source[table_name],election=election,table_name=table_name) for u in test_fields)
            update_timestamp = 'update {table_name}_{source}_{election} set updated={table_name}_import.updated from {table_name}_import where {table_name}_{source}_{election}.identifier = {table_name}_import.identifier and ({conditions});'.format(source=source[table_name], election=election ,conditions=test_fields,table_name=table_name)
            update_other = 'update {table_name}_{source}_{election} set {ufields} from {table_name}_import where {table_name}_{source}_{election}.identifier = {table_name}_import.identifier'.format(ufields=ufields,source=source[table_name], election=election,table_name=table_name)
            insert = 'insert into {table_name}_{source}_{election}({fields}) select {fields} from {table_name}_import where {table_name}_import.identifier not in (select identifier from {table_name}_{source}_{election} where identifier is not null);'.format(source=source[table_name],table_name=table_name, election=election,fields=','.join(FIELDS.keys()))
            delete = 'delete from {table_name}_{source}_{election} where {table_name}_{source}_{election}.identifier is null or {table_name}_{source}_{election}.identifier not in (select identifier from {table_name}_import);'.format(source=source[table_name], election=election,table_name=table_name,fields=','.join(FIELDS.keys()))
            print update_timestamp
            print update_other
            print insert
            print delete
            cursor = connection.cursor()
            cursor.execute(update_timestamp)
            cursor.execute(update_other)
            cursor.execute(insert)
            cursor.execute(delete)

        if state not in ['referenda','election']:
            clear = 'DELETE from candidate_in_contest_{source}_{election};'.format(source=candidate_source, election=election)
            insert = 'insert into candidate_in_contest_{source}_{election} select * from candidate_in_contest_import;'.format(source=candidate_source, election=election)
            print clear
            print insert
            connection.cursor().execute(clear)
            connection.cursor().execute(insert)

        connection.commit()
        connection.close()
        t = time.time() - t
        print "Elapsed: %s" % (t,)
