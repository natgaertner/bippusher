select co.* from contest as co join candidate_in_contest as cic on co.id=cic.contest_id left join candidate as ca on cic.candidate_id = ca.id where name is null;
select co.* from contest as co join electoral_district as ed on co.electoral_district_id = ed.id where name is null;
select * from contest where ed_matched='t' and electoral_district_id is null;
select count(electoral_district_type),electoral_district_type,ed_matched from contest group by electoral_district_type,ed_matched order by electoral_district_type;
select count(office_level), d.* from (select office_level, state, case when office_level='Statewide' then office else 'office' end as office from contest where ed_matched='f') as d group by office_level, state, office order by state, office_level;
