CREATE TABLE public.project (
	title varchar NOT NULL,
	description varchar NULL,
	project_id int8 NOT NULL GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE),
	CONSTRAINT project_pk PRIMARY KEY (project_id)
);
CREATE UNIQUE INDEX project_project_id_idx ON public.project USING btree (project_id);

CREATE TABLE public."section" (
	title varchar NOT NULL,
	project_id int8 NOT NULL,
	section_id int8 NOT NULL GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE),
	CONSTRAINT section_pk PRIMARY KEY (section_id),
	CONSTRAINT section_fk FOREIGN KEY (project_id) REFERENCES public.project(project_id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE UNIQUE INDEX section_section_id_idx ON public.section USING btree (section_id);

CREATE TABLE public.card (
	card_id int8 NOT NULL GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE),
	title varchar NOT NULL,
	description varchar NULL,
	due timestamptz NULL,
	complete timestamptz NULL,
	tags _varchar NULL,
	section_id int8 NOT NULL,
	created timestamptz NOT NULL DEFAULT now(),
	CONSTRAINT card_pk PRIMARY KEY (card_id),
	CONSTRAINT card_fk FOREIGN KEY (section_id) REFERENCES public."section"(section_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE public."user" (
	name varchar NULL,
	telegram_id varchar NOT NULL,
	user_id int8 NOT NULL GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE),
	CONSTRAINT user_pk PRIMARY KEY (user_id)
);
CREATE UNIQUE INDEX user_user_id_idx ON public."user" USING btree (user_id);

-- CREATE TYPE public."taskmgr_rights" AS ENUM (
-- 	'view_project',
-- 	'update_project',
-- 	'delete_project',
-- 	'view_section',
-- 	'update_section',
-- 	'delete_section',
-- 	'add_section',
-- 	'view_card',
-- 	'update_card',
-- 	'update_card_complete',
-- 	'delete_card',
-- 	'add_card',
-- 	'add_comment',
-- 	'view_comment',
-- 	'delete_comment',
-- 	'add_user',
-- 	'delete_user',
-- 	'view_user');

CREATE TABLE public."right" (
	right_id int8 NOT NULL GENERATED ALWAYS AS IDENTITY,
	title varchar NOT NULL,
	CONSTRAINT right_pk PRIMARY KEY (right_id)
);

INSERT INTO public."right" (title)
VALUES
	('view_project'),
	('update_project'),
	('delete_project'),
	('view_section'),
	('update_section'),
	('delete_section'),
	('add_section'),
	('view_card'),
	('update_card'),
	('update_card_complete'),
	('delete_card'),
	('add_card'),
	('add_comment'),
	('view_comment'),
	('delete_comment'),
	('add_user'),
	('delete_user'),
	('view_user');

CREATE TABLE public."role" (
	role_id int8 NOT NULL GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE),
	title varchar NOT NULL,
	description varchar NULL,
	allow_tables _varchar NOT NULL,
	-- rights public."_taskmgr_rights" NULL,
	CONSTRAINT role_pk PRIMARY KEY (role_id)
);

CREATE TABLE public.right_role (
	right_role_id int8 NOT NULL GENERATED ALWAYS AS IDENTITY,
	right_id int8 NOT NULL,
	role_id int8 NOT NULL,
	CONSTRAINT right_role_pk PRIMARY KEY (right_role_id),
	CONSTRAINT right_role_fk FOREIGN KEY (right_id) REFERENCES public."right"(right_id) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT right_role_fk_1 FOREIGN KEY (role_id) REFERENCES public."role"(role_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE public."comment" (
	comment_id int8 NOT NULL GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE),
	description varchar NOT NULL,
	user_id int8 NOT NULL,
	card_id int8 NOT NULL,
	CONSTRAINT comment_pk PRIMARY KEY (comment_id),
	CONSTRAINT comment_fk FOREIGN KEY (card_id) REFERENCES public.card(card_id) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT comment_fk_1 FOREIGN KEY (user_id) REFERENCES public."user"(user_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE public.user_card (
	user_card_id int8 NOT NULL GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE),
	user_id int8 NOT NULL,
	card_id int8 NOT NULL,
	role_id int8 NOT NULL,
	CONSTRAINT user_card_pk PRIMARY KEY (user_card_id),
	CONSTRAINT user_card_fk FOREIGN KEY (user_id) REFERENCES public."user"(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT user_card_fk_1 FOREIGN KEY (card_id) REFERENCES public.card(card_id) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT user_card_fk_2 FOREIGN KEY (role_id) REFERENCES public."role"(role_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE public.user_project (
	user_project_id int8 NOT NULL GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE),
	user_id int8 NOT NULL,
	project_id int8 NOT NULL,
	role_id int8 NOT NULL,
	CONSTRAINT user_project_pk PRIMARY KEY (user_project_id),
	CONSTRAINT user_project_fk FOREIGN KEY (user_id) REFERENCES public."user"(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT user_project_fk_1 FOREIGN KEY (project_id) REFERENCES public.project(project_id) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT user_project_fk_2 FOREIGN KEY (role_id) REFERENCES public."role"(role_id) ON DELETE CASCADE ON UPDATE CASCADE
);