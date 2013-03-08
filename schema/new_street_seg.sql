
CREATE TABLE "street_segment_long" (
"id" int4 DEFAULT nextval('pksq'),
"source_pk" varchar(255),
"source" text,
"start_house_number" int4,
"end_house_number" int4,
"odd_even_both" oddevenenum,
"start_apartment_number" varchar(20),
"end_apartment_number" varchar(20),
"non_house_address" int4,
"non_house_address_long" varchar(255),
"precinct_id" int4,
"precinct_id_long" varchar(255),
"precinct_split_id" int4,
"precinct_split_id_long" varchar(255),
-- Having non-house-addresses keyed out was creating far too many transactions on import
"nha_is_standardized" bool,
"nha_is_geocoded" bool,
"nha_house_number" int4,
"nha_house_number_prefix" varchar(50),
"nha_house_number_suffix" varchar(50),
"nha_street_name" varchar(50),
"nha_street_direction" varchar(50),
"nha_street_suffix" varchar(50),
"nha_address_direction" varchar(50),
"nha_location_name" varchar(255),
"nha_line3" varchar(255),
"nha_line2" varchar(255),
"nha_line1" varchar(255),
"nha_city" varchar(255),
"nha_state" varchar(255),
"nha_zip4" varchar(4),
"nha_zip" varchar(10),
"nha_xcoord" varchar(255),
"nha_ycoord" varchar(255),
"nha_apartment" varchar(255),
PRIMARY KEY ("id") ,
CONSTRAINT "new_street_segment__id" UNIQUE ("id")
);