DROP type FloodedMonths cascade;
create type FloodedMonths as enum ('No','From0To1', 'From1To3', 'From3To6');

DROP type type_soil cascade;
create type type_soil as enum ('Clay', 'SiltyClay', 'SlityClayLoam','SandyClay', 'SandyClayLoam', 'ClayLoam', 'ilt');



drop table if exists regions cascade;
create table if not exists regions (
	id serial PRIMARY KEY,
	name varchar,
	bounds float[][],
	center float[]

);

drop table if exists params cascade;
CREATE TABLE IF NOT exists params (
	id serial PRIMARY KEY,
	min_relief_aspect float,
	max_relief_aspect float,
	avg_relief_aspect float,
	min_relief_height float,
	max_relief_height float,
	avg_relief_height float,
	min_relief_slope float,
	max_relief_slope float,
	avg_relief_slope float,
	avg_sunny_days float,
	max_sunny_days float,
	min_sunny_days float,
	water_seasonlyty int,
	flooded FloodedMonths,
	forest boolean,
	soil type_soil,
	scoring float
);

drop table if exists "polygon" cascade;
CREATE TABLE IF NOT exists "polygon" (
  id serial PRIMARY KEY,
  geo float[][],
  scoring float,
  bounds float[][],
  center float[],
  area int,
  free_area int,
  param_id INTEGER references "params" (id) on delete cascade on update cascade,
  region_id INTEGER references regions(id) on delete cascade on update cascade
);

drop table if exists details cascade;
CREATE TABLE IF NOT exists details (
	id serial PRIMARY KEY,
	"month" varchar,
	tavg float,
	tmax float,
	tmin float,
	pavg float,
	pmax float,
	pmin float,
	param_id INTEGER references params (id) on delete cascade on update cascade
);




drop table if exists markers cascade;
create table if not exists markers (
	id serial PRIMARY KEY,
  	"center" float[],
  	scoring float,
  	bounds float[][],
  	param_id INTEGER references "params" (id) on delete cascade on update cascade,
  	region_id INTEGER references regions(id) on delete cascade on update cascade
);
