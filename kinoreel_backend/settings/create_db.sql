create schema kino;

create table kino.awards
   ( imdb_event_id varchar(10) not null
   , award varchar(10) not null
   , tstamp date not null
   , PRIMARY KEY (imdb_event_id, award)
    );

create table kino.country_codes
    ( country_code varchar(3) not null
    , country varchar(100) not null
    , PRIMARY KEY (country_code)
    , UNIQUE (country)
);

create table kino.persons
   ( person_id  serial
   , fullname varchar(250) not null
   , dob date
   , dead date
   , sex varchar(1) check (sex in ('F', 'M', 'Z'))
   , nationality varchar(3)
   , tstamp date not null default CURRENT_DATE
   , PRIMARY KEY (person_id)
   );


create table kino.companies
   ( company_id serial
   , name varchar(1000) not null
   , founded date
   , dead date
   , country varchar(3)
   , tstamp date not null default CURRENT_DATE
   , PRIMARY KEY (company_id)
   , FOREIGN KEY (country) references kino.country_codes(country)
   );

create table kino.company_roles
   ( role varchar(250) not null
   , tstamp date not null  default CURRENT_DATE
   , PRIMARY KEY (role)
);

create table kino.festivals
  ( imdb_event_id varchar(9) not null
  , name varchar(1000) not null
  , location varchar(100) not null
  , tstamp date not null  default CURRENT_DATE
  , PRIMARY KEY (imdb_event_id)
  , UNIQUE (name)
  );

create table kino.movies
    ( imdb_id varchar(10) not null
    , title varchar(1000) not null
    , runtime varchar(100) not null
    , rated varchar(15) not null
    , released varchar(15) not null
    , orig_language varchar(1000) not null
    , tstamp date not null  default CURRENT_DATE
    , PRIMARY KEY (imdb_id)
);

create table kino.movies2awards
   ( imdb_id varchar(10) not null
   , imdb_event_id varchar(10) not null
   , award varchar(10) not null
   , position varchar(1) check (position in ('N', 'W'))
   , year date not null
   , tstamp date not null
   , FOREIGN KEY (imdb_id) references kino.movies(imdb_id)
   , FOREIGN KEY (imdb_event_id, award) references kino.awards(imdb_event_id, award)
   , UNIQUE (imdb_id, award, year)
);

create table kino.movies2companies
   ( imdb_id varchar(10) not null
   , company_id integer
   , role varchar(250) not null
   , tstamp date not null default CURRENT_DATE
   , FOREIGN KEY (imdb_id) references kino.movies(imdb_id)
   , FOREIGN KEY (company_id) references kino.companies(company_id)
   , UNIQUE (imdb_id, company_id, role)
);

create table kino.movies2genres
   ( imdb_id varchar(10) not null
   , genre varchar(250) not null
   , tstamp date not null default CURRENT_DATE
   , PRIMARY KEY (imdb_id, genre)
   , FOREIGN KEY (imdb_id) references kino.movies(imdb_id)
);

create table kino.movies2keywords
   ( imdb_id varchar(10) not null
   , keyword varchar(250) not null
   , tstamp date not null default CURRENT_DATE
   , PRIMARY KEY (imdb_id, keyword)
   , FOREIGN KEY (imdb_id) references kino.movies(imdb_id)
   );

create table kino.movies2numbers
   ( imdb_id varchar(10) not null
   , type varchar(250) not null
   , value real not null
   , tstamp date not null default CURRENT_DATE
   , PRIMARY KEY (imdb_id, type)
   , FOREIGN KEY (imdb_id) references kino.movies(imdb_id)
);

create table kino.movies2persons
   ( imdb_id varchar(10) not null
   , person_id integer
   , role varchar(250) not null
   , tstamp date not null  default CURRENT_DATE
   , PRIMARY KEY (imdb_id, person_id, role)
   , FOREIGN KEY (imdb_id) references kino.movies(imdb_id)
   , FOREIGN KEY (person_id) references kino.persons(person_id)
);

create table kino.movies2posters
   ( imdb_id varchar(10) not null
   , url varchar(100) not null
   , tstamp date not null  default CURRENT_DATE
   , PRIMARY KEY (imdb_id)
   , UNIQUE (url)
   , FOREIGN KEY (imdb_id) references kino.movies(imdb_id)
);

create table kino.movies2ratings
   ( imdb_id varchar(10) not null
   , source varchar(100) not null
   , rating varchar(100) not null
   , tstamp date not null default CURRENT_DATE
   , PRIMARY KEY (imdb_id, source)
   , FOREIGN KEY (imdb_id) references kino.movies(imdb_id)
);

create table kino.movies2stats
  ( imdb_id varchar(10)
  , tmdb_vote_average real
  , tmdb_vote_count real
  , imdb_votes real
  , youtube_likes real
  , youtube_dislikes real
  , PRIMARY KEY (imdb_id)
  );

create table kino.movies2streams
   ( imdb_id varchar(10)
   , source varchar(400)
   , url varchar(1000)
   , currency varchar(100)
   , price real
   , format varchar(30)
   , purchase_type varchar(30)
   , UNIQUE (imdb_id, source, url, format, purchase_type)
   , FOREIGN KEY (imdb_id) references kino.movies(imdb_id)
   );

create table kino.movies2trailers
   ( imdb_id varchar(10)
   , url varchar(400)
   , tstamp date default current_date
   , PRIMARY KEY (imdb_id, url)
   , FOREIGN KEY (imdb_id) references kino.movies(imdb_id)
   );

  create table kino.person_roles
   ( role varchar(250) not null
   , tstamp date not null default CURRENT_DATE
   , PRIMARY KEY (role)
);
insert into kino.festivals values ('ev0000631', 'Sundance Film Festival', 'Park City, Utah, USA');
insert into kino.festivals values ('ev0000091', 'Berlin International Film Festival', 'Berlin, Germany');
insert into kino.festivals values ('ev0000147', 'Cannes Film Festival','Cannes, France');
insert into kino.festivals values ('ev0000681', 'Venice Film Festivals', 'Venice, Italy');
insert into kino.festivals values ('ev0000659', 'Toronto International Film Festival', 'Toronto, Ontario, Canada');
insert into kino.festivals values ('ev0000220', 'Edinburgh International Film Festival', 'Edinburgh, Scotland');
insert into kino.festivals values ('ev0000588', 'San Sebastian International Film Festival', 'San Sebastián, Spain');
insert into kino.festivals values ('ev0000894', 'Tribeca', 'New York, New York, USA');
insert into kino.festivals values ('ev0000025', 'Amsterdam International Documentary Festival', 'Amsterdam, Netherlands');
insert into kino.festivals values ('ev0000935', 'Raindance Film Festival', 'London, United Kingdom');
insert into kino.festivals values ('ev0000123', 'BAFTA Awards', 'London, United Kingdom');
insert into kino.festivals values ('ev0000003', 'Academy Awards', 'Los Angeles California');
insert into kino.festivals values ('ev0000331', 'Hong Kong International Film Festival', 'Hong Kong, China');