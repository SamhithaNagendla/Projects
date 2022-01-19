create table users (
   username   varchar(10) primary key,
   password   varchar(32),
   fullname   varchar(45),
   email      varchar(45)
);

create table friends (
   user     varchar(10) references users (username),
   friend   varchar(10) references users (username)
);
