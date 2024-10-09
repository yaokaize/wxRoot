-- 创建数据库以及用户
CREATE DATABASE myroot;

CREATE USER yaokz WITH PASSWORD 'yaokz1314';

GRANT ALL PRIVILEGES ON DATABASE myroot TO yaokz;


-- 创建schema
create schema yangming;


-- 创建表

-- 流水表
create table tb_journal
(
    id          serial
        constraint tb_journal_pk_id
            primary key,
    wx_id       varchar,
    money       numeric,
    create_time timestamp default now()
);

comment on table tb_journal is '流水表';

comment on column tb_journal.id is '自增ID';

comment on column tb_journal.wx_id is '微信号';

comment on column tb_journal.money is '流水';

comment on column tb_journal.create_time is '创建时间';

alter table tb_journal
    owner to yaokz;

create index tb_journal_wx_id_index
    on tb_journal (wx_id);


