CREATE EXTENSION postgis;

CREATE OR REPLACE FUNCTION DISTANCE(point, point)
RETURNS float8 as $$
    SELECT ST_Distance($1.geometry, $2.geometry);
$$
LANGUAGE 'sql' IMMUTABLE STRICT PARALLEL SAFE;
