--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5 (Ubuntu 14.5-1.pgdg20.04+1)
-- Dumped by pg_dump version 14.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: heroku_ext; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA heroku_ext;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: Admins; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."Admins" (
    id integer NOT NULL,
    email text
);


--
-- Name: Admins_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."Admins_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: Admins_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."Admins_id_seq" OWNED BY public."Admins".id;


--
-- Name: Categories; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."Categories" (
    id integer NOT NULL,
    name text NOT NULL,
    description text NOT NULL,
    content_links json,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


--
-- Name: Categories_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."Categories_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: Categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."Categories_id_seq" OWNED BY public."Categories".id;


--
-- Name: Category_results; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."Category_results" (
    id integer NOT NULL,
    "categoryId" integer NOT NULL,
    text text,
    cutoff_from_maxpoints double precision,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


--
-- Name: Category_results_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."Category_results_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: Category_results_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."Category_results_id_seq" OWNED BY public."Category_results".id;


--
-- Name: Industries; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."Industries" (
    id integer NOT NULL,
    name text NOT NULL,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


--
-- Name: Industries_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."Industries_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: Industries_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."Industries_id_seq" OWNED BY public."Industries".id;


--
-- Name: Organizations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."Organizations" (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


--
-- Name: Question_answers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."Question_answers" (
    id integer NOT NULL,
    text text NOT NULL,
    points integer NOT NULL,
    "questionId" integer NOT NULL,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


--
-- Name: Question_answers_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."Question_answers_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: Question_answers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."Question_answers_id_seq" OWNED BY public."Question_answers".id;


--
-- Name: Questions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."Questions" (
    id integer NOT NULL,
    text text NOT NULL,
    "surveyId" integer NOT NULL,
    category_weights jsonb,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


--
-- Name: Questions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."Questions_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: Questions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."Questions_id_seq" OWNED BY public."Questions".id;


--
-- Name: Survey_results; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."Survey_results" (
    id integer NOT NULL,
    "surveyId" integer NOT NULL,
    text text NOT NULL,
    cutoff_from_maxpoints double precision,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


--
-- Name: Survey_results_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."Survey_results_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: Survey_results_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."Survey_results_id_seq" OWNED BY public."Survey_results".id;


--
-- Name: Survey_user_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."Survey_user_groups" (
    id uuid NOT NULL,
    group_name character varying(255),
    "surveyId" integer NOT NULL,
    "organizationId" integer,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


--
-- Name: Surveys; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."Surveys" (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL,
    title_text text,
    survey_text text
);


--
-- Name: Surveys_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."Surveys_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: Surveys_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."Surveys_id_seq" OWNED BY public."Surveys".id;


--
-- Name: User_answers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."User_answers" (
    id integer NOT NULL,
    "userId" integer NOT NULL,
    "questionAnswerId" integer NOT NULL,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL,
    "QuestionAnswerId" integer
);


--
-- Name: User_answers_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."User_answers_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: User_answers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."User_answers_id_seq" OWNED BY public."User_answers".id;


--
-- Name: Users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."Users" (
    id integer NOT NULL,
    email character varying(255),
    "groupId" uuid,
    "industryId" integer,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


--
-- Name: Users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."Users_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: Users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."Users_id_seq" OWNED BY public."Users".id;


--
-- Name: Admins id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Admins" ALTER COLUMN id SET DEFAULT nextval('public."Admins_id_seq"'::regclass);


--
-- Name: Categories id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Categories" ALTER COLUMN id SET DEFAULT nextval('public."Categories_id_seq"'::regclass);


--
-- Name: Category_results id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Category_results" ALTER COLUMN id SET DEFAULT nextval('public."Category_results_id_seq"'::regclass);


--
-- Name: Industries id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Industries" ALTER COLUMN id SET DEFAULT nextval('public."Industries_id_seq"'::regclass);


--
-- Name: Question_answers id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Question_answers" ALTER COLUMN id SET DEFAULT nextval('public."Question_answers_id_seq"'::regclass);


--
-- Name: Questions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Questions" ALTER COLUMN id SET DEFAULT nextval('public."Questions_id_seq"'::regclass);


--
-- Name: Survey_results id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Survey_results" ALTER COLUMN id SET DEFAULT nextval('public."Survey_results_id_seq"'::regclass);


--
-- Name: Surveys id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Surveys" ALTER COLUMN id SET DEFAULT nextval('public."Surveys_id_seq"'::regclass);


--
-- Name: User_answers id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."User_answers" ALTER COLUMN id SET DEFAULT nextval('public."User_answers_id_seq"'::regclass);


--
-- Name: Users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Users" ALTER COLUMN id SET DEFAULT nextval('public."Users_id_seq"'::regclass);


--
-- Data for Name: Admins; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public."Admins" VALUES (2, 'rami.piik@gmail.com');
INSERT INTO public."Admins" VALUES (3, 'antti.vainikka36@gmail.com');
INSERT INTO public."Admins" VALUES (4, 'jatufin@gmail.com');
INSERT INTO public."Admins" VALUES (5, 'me@juan.fi');
INSERT INTO public."Admins" VALUES (6, 'niemi.leo@gmail.com');
INSERT INTO public."Admins" VALUES (7, 'oskar.sjolund93@gmail.com');
INSERT INTO public."Admins" VALUES (8, 'siljaorvokki@gmail.com');


--
-- Data for Name: Categories; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public."Categories" VALUES (1, 'Category 1', 'Static descriptive text about the category 1.', '[{"url":"https://www.eficode.com/cases/hansen","type":"Case Study"},{"url":"https://www.eficode.com/cases/basware","type":"Case Study"}]', '2022-09-26 14:03:28.613+00', '2022-09-26 14:03:28.613+00');
INSERT INTO public."Categories" VALUES (2, 'Category 2', 'Static descriptive text about the category 2.', '[{"url":"https://www.eficode.com/cases/hansen","type":"Case Study"},{"url":"https://www.eficode.com/cases/basware","type":"Case Study"}]', '2022-09-26 14:03:28.613+00', '2022-09-26 14:03:28.613+00');
INSERT INTO public."Categories" VALUES (3, 'Category 3', 'Static descriptive text about the category 3.', '[{"url":"https://www.eficode.com/cases/hansen","type":"Case Study"},{"url":"https://www.eficode.com/cases/basware","type":"Case Study"}]', '2022-09-26 14:03:28.613+00', '2022-09-26 14:03:28.613+00');
INSERT INTO public."Categories" VALUES (4, 'Category 4', 'Static descriptive text about the category 4.', '[{"url":"https://www.eficode.com/cases/hansen","type":"Case Study"},{"url":"https://www.eficode.com/cases/basware","type":"Case Study"}]', '2022-09-26 14:03:28.613+00', '2022-09-26 14:03:28.613+00');
INSERT INTO public."Categories" VALUES (5, 'Category 5', 'Static descriptive text about the category 5.', '[{"url":"https://www.eficode.com/cases/hansen","type":"Case Study"},{"url":"https://www.eficode.com/cases/basware","type":"Case Study"}]', '2022-09-26 14:03:28.613+00', '2022-09-26 14:03:28.613+00');


--
-- Data for Name: Category_results; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public."Category_results" VALUES (11, 4, 'Dynamically fetched feedback text for category score.', 0.8, '2022-09-26 14:17:29.755+00', '2022-09-26 14:17:29.755+00');
INSERT INTO public."Category_results" VALUES (12, 4, 'Dynamically fetched feedback text for category score.', 1, '2022-09-26 14:17:29.755+00', '2022-09-26 14:17:29.755+00');
INSERT INTO public."Category_results" VALUES (13, 5, 'Dynamically fetched feedback text for category score.', 0.4, '2022-09-26 14:17:29.755+00', '2022-09-26 14:17:29.755+00');
INSERT INTO public."Category_results" VALUES (14, 5, 'Dynamically fetched feedback text for category score.', 0.8, '2022-09-26 14:17:29.755+00', '2022-09-26 14:17:29.755+00');
INSERT INTO public."Category_results" VALUES (15, 5, 'Dynamically fetched feedback text for category score.', 1, '2022-09-26 14:17:29.755+00', '2022-09-26 14:17:29.755+00');
INSERT INTO public."Category_results" VALUES (1, 1, 'Dynamically fetched feedback text for category score.', 0.4, '2022-09-26 14:17:29.755+00', '2022-09-26 14:17:29.755+00');
INSERT INTO public."Category_results" VALUES (2, 1, 'Dynamically fetched feedback text for category score.', 0.8, '2022-09-26 14:17:29.755+00', '2022-09-26 14:17:29.755+00');
INSERT INTO public."Category_results" VALUES (3, 1, 'Dynamically fetched feedback text for category score.', 1, '2022-09-26 14:17:29.755+00', '2022-09-26 14:17:29.755+00');
INSERT INTO public."Category_results" VALUES (4, 2, 'Dynamically fetched feedback text for category score.', 0.4, '2022-09-26 14:17:29.755+00', '2022-09-26 14:17:29.755+00');
INSERT INTO public."Category_results" VALUES (5, 2, 'Dynamically fetched feedback text for category score.', 0.8, '2022-09-26 14:17:29.755+00', '2022-09-26 14:17:29.755+00');
INSERT INTO public."Category_results" VALUES (6, 2, 'Dynamically fetched feedback text for category score.', 1, '2022-09-26 14:17:29.755+00', '2022-09-26 14:17:29.755+00');
INSERT INTO public."Category_results" VALUES (7, 3, 'Dynamically fetched feedback text for category score.', 0.4, '2022-09-26 14:17:29.755+00', '2022-09-26 14:17:29.755+00');
INSERT INTO public."Category_results" VALUES (8, 3, 'Dynamically fetched feedback text for category score.', 0.8, '2022-09-26 14:17:29.755+00', '2022-09-26 14:17:29.755+00');
INSERT INTO public."Category_results" VALUES (9, 3, 'Dynamically fetched feedback text for category score.', 1, '2022-09-26 14:17:29.755+00', '2022-09-26 14:17:29.755+00');
INSERT INTO public."Category_results" VALUES (10, 4, 'Dynamically fetched feedback text for category score.', 0.4, '2022-09-26 14:17:29.755+00', '2022-09-26 14:17:29.755+00');


--
-- Data for Name: Industries; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public."Industries" VALUES (1, 'IT/Software development', '2022-09-26 14:03:28.604+00', '2022-09-26 14:03:28.604+00');
INSERT INTO public."Industries" VALUES (2, 'Financial services', '2022-09-26 14:03:28.604+00', '2022-09-26 14:03:28.604+00');
INSERT INTO public."Industries" VALUES (3, 'Telecommunications', '2022-09-26 14:03:28.604+00', '2022-09-26 14:03:28.604+00');
INSERT INTO public."Industries" VALUES (4, 'Insurance', '2022-09-26 14:03:28.604+00', '2022-09-26 14:03:28.604+00');
INSERT INTO public."Industries" VALUES (5, 'Automotive', '2022-09-26 14:03:28.604+00', '2022-09-26 14:03:28.604+00');
INSERT INTO public."Industries" VALUES (6, 'Business services', '2022-09-26 14:03:28.604+00', '2022-09-26 14:03:28.604+00');
INSERT INTO public."Industries" VALUES (7, 'Manufacturing', '2022-09-26 14:03:28.604+00', '2022-09-26 14:03:28.604+00');
INSERT INTO public."Industries" VALUES (8, 'Retail', '2022-09-26 14:03:28.604+00', '2022-09-26 14:03:28.604+00');
INSERT INTO public."Industries" VALUES (9, 'Oil & energy', '2022-09-26 14:03:28.604+00', '2022-09-26 14:03:28.604+00');
INSERT INTO public."Industries" VALUES (10, 'Logistics & supply chain', '2022-09-26 14:03:28.604+00', '2022-09-26 14:03:28.604+00');


--
-- Data for Name: Organizations; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: Question_answers; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public."Question_answers" VALUES (1, 'Strongly Disagree', 0, 1, '2022-09-26 14:17:29.764+00', '2022-09-26 14:17:29.764+00');
INSERT INTO public."Question_answers" VALUES (2, 'Disagree', 1, 1, '2022-09-26 14:17:29.764+00', '2022-09-26 14:17:29.764+00');
INSERT INTO public."Question_answers" VALUES (3, 'Do not disagree or agree', 2, 1, '2022-09-26 14:17:29.764+00', '2022-09-26 14:17:29.764+00');
INSERT INTO public."Question_answers" VALUES (4, 'Agree', 3, 1, '2022-09-26 14:17:29.764+00', '2022-09-26 14:17:29.764+00');
INSERT INTO public."Question_answers" VALUES (5, 'Strongly Agree', 4, 1, '2022-09-26 14:17:29.764+00', '2022-09-26 14:17:29.764+00');
INSERT INTO public."Question_answers" VALUES (6, 'Strongly Disagree', 0, 2, '2022-09-26 14:17:29.764+00', '2022-09-26 14:17:29.764+00');
INSERT INTO public."Question_answers" VALUES (7, 'Disagree', 1, 2, '2022-09-26 14:17:29.764+00', '2022-09-26 14:17:29.764+00');
INSERT INTO public."Question_answers" VALUES (8, 'Do not disagree or agree', 2, 2, '2022-09-26 14:17:29.764+00', '2022-09-26 14:17:29.764+00');
INSERT INTO public."Question_answers" VALUES (9, 'Agree', 3, 2, '2022-09-26 14:17:29.764+00', '2022-09-26 14:17:29.764+00');
INSERT INTO public."Question_answers" VALUES (10, 'Strongly Agree', 4, 2, '2022-09-26 14:17:29.764+00', '2022-09-26 14:17:29.764+00');
INSERT INTO public."Question_answers" VALUES (11, 'Strongly Disagree', 0, 3, '2022-09-26 14:17:29.764+00', '2022-09-26 14:17:29.764+00');
INSERT INTO public."Question_answers" VALUES (12, 'Disagree', 1, 3, '2022-09-26 14:17:29.764+00', '2022-09-26 14:17:29.764+00');
INSERT INTO public."Question_answers" VALUES (13, 'Do not disagree or agree', 2, 3, '2022-09-26 14:17:29.764+00', '2022-09-26 14:17:29.764+00');
INSERT INTO public."Question_answers" VALUES (14, 'Agree', 3, 3, '2022-09-26 14:17:29.764+00', '2022-09-26 14:17:29.764+00');
INSERT INTO public."Question_answers" VALUES (15, 'Strongly Agree', 4, 3, '2022-09-26 14:17:29.764+00', '2022-09-26 14:17:29.764+00');
INSERT INTO public."Question_answers" VALUES (16, 'Strongly Disagree', 0, 4, '2022-09-26 14:17:29.764+00', '2022-09-26 14:17:29.764+00');
INSERT INTO public."Question_answers" VALUES (17, 'Disagree', 1, 4, '2022-09-26 14:17:29.764+00', '2022-09-26 14:17:29.764+00');
INSERT INTO public."Question_answers" VALUES (18, 'Do not disagree or agree', 2, 4, '2022-09-26 14:17:29.764+00', '2022-09-26 14:17:29.764+00');
INSERT INTO public."Question_answers" VALUES (19, 'Agree', 3, 4, '2022-09-26 14:17:29.764+00', '2022-09-26 14:17:29.764+00');
INSERT INTO public."Question_answers" VALUES (20, 'Strongly Agree', 4, 4, '2022-09-26 14:17:29.764+00', '2022-09-26 14:17:29.764+00');
INSERT INTO public."Question_answers" VALUES (21, 'Strongly Disagree', 0, 5, '2022-09-26 14:17:29.764+00', '2022-09-26 14:17:29.764+00');
INSERT INTO public."Question_answers" VALUES (22, 'Disagree', 1, 5, '2022-09-26 14:17:29.764+00', '2022-09-26 14:17:29.764+00');
INSERT INTO public."Question_answers" VALUES (23, 'Do not disagree or agree', 2, 5, '2022-09-26 14:17:29.764+00', '2022-09-26 14:17:29.764+00');
INSERT INTO public."Question_answers" VALUES (24, 'Agree', 3, 5, '2022-09-26 14:17:29.764+00', '2022-09-26 14:17:29.764+00');
INSERT INTO public."Question_answers" VALUES (25, 'Strongly Agree', 4, 5, '2022-09-26 14:17:29.764+00', '2022-09-26 14:17:29.764+00');
INSERT INTO public."Question_answers" VALUES (26, 'Strongly Disagree', 0, 6, '2022-09-26 14:17:29.764+00', '2022-09-26 14:17:29.764+00');
INSERT INTO public."Question_answers" VALUES (27, 'Disagree', 1, 6, '2022-09-26 14:17:29.764+00', '2022-09-26 14:17:29.764+00');
INSERT INTO public."Question_answers" VALUES (28, 'Do not disagree or agree', 2, 6, '2022-09-26 14:17:29.764+00', '2022-09-26 14:17:29.764+00');
INSERT INTO public."Question_answers" VALUES (29, 'Agree', 3, 6, '2022-09-26 14:17:29.764+00', '2022-09-26 14:17:29.764+00');
INSERT INTO public."Question_answers" VALUES (30, 'Strongly Agree', 4, 6, '2022-09-26 14:17:29.764+00', '2022-09-26 14:17:29.764+00');


--
-- Data for Name: Questions; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public."Questions" VALUES (1, 'Question 1', 1, '[{"category": "Category 1", "multiplier": 1}, {"category": "Category 2", "multiplier": 1}, {"category": "Category 3", "multiplier": 0}, {"category": "Category 4", "multiplier": 0}, {"category": "Category 5", "multiplier": 0}]', '2022-09-26 14:17:29.76+00', '2022-09-26 14:17:29.76+00');
INSERT INTO public."Questions" VALUES (2, 'Question 2', 1, '[{"category": "Category 1", "multiplier": 0}, {"category": "Category 2", "multiplier": 1}, {"category": "Category 3", "multiplier": 1}, {"category": "Category 4", "multiplier": 0}, {"category": "Category 5", "multiplier": 0}]', '2022-09-22 21:03:09.628167+00', '2022-09-22 21:03:09.628167+00');
INSERT INTO public."Questions" VALUES (7, 'Question7', 1, NULL, '2022-09-26 19:16:45.279882+00', '2022-09-26 19:16:45.279882+00');
INSERT INTO public."Questions" VALUES (8, 'Question 8', 1, NULL, '2022-09-26 19:33:13.8708+00', '2022-09-26 19:33:13.8708+00');
INSERT INTO public."Questions" VALUES (9, 'Which one is best: 1) Game of Thrones, 2) Breaking Bad, or 3) Narcos? ', 1, NULL, '2022-09-29 21:34:03.33838+00', '2022-09-29 21:34:03.33838+00');
INSERT INTO public."Questions" VALUES (3, 'Question 3', 1, '[{"category": "Category 1", "multiplier": 0}, {"category": "Category 2", "multiplier": 0}, {"category": "Category 3", "multiplier": 1}, {"category": "Category 4", "multiplier": 1}, {"category": "Category 5", "multiplier": 0}]', '2022-09-22 21:03:22.124125+00', '2022-09-22 21:03:22.124125+00');
INSERT INTO public."Questions" VALUES (4, 'Question 4', 1, '[{"category": "Category 1", "multiplier": 0}, {"category": "Category 2", "multiplier": 0}, {"category": "Category 3", "multiplier": 0}, {"category": "Category 4", "multiplier": 1}, {"category": "Category 5", "multiplier": 1}]', '2022-09-22 21:31:09.984421+00', '2022-09-22 21:31:09.984421+00');
INSERT INTO public."Questions" VALUES (5, 'Question 5', 1, '[{"category": "Category 1", "multiplier": 1}, {"category": "Category 2", "multiplier": 0}, {"category": "Category 3", "multiplier": 0}, {"category": "Category 4", "multiplier": 0}, {"category": "Category 5", "multiplier": 1}]', '2022-09-26 14:17:29.76+00', '2022-09-26 14:17:29.76+00');
INSERT INTO public."Questions" VALUES (6, 'Question 6', 1, '[{"category": "Category 1", "multiplier": 1}, {"category": "Category 2", "multiplier": 1}, {"category": "Category 3", "multiplier": 1}, {"category": "Category 4", "multiplier": 1}, {"category": "Category 5", "multiplier": 1}]', '2022-09-26 14:17:29.76+00', '2022-09-26 14:17:29.76+00');


--
-- Data for Name: Survey_results; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public."Survey_results" VALUES (1, 1, 'Dynamically fetched result text 1', 0.5, '2022-09-26 14:03:28.609+00', '2022-09-26 14:03:28.609+00');
INSERT INTO public."Survey_results" VALUES (2, 1, 'Dynamically fetched result text 2', 1, '2022-09-26 14:03:28.609+00', '2022-09-26 14:03:28.609+00');
INSERT INTO public."Survey_results" VALUES (3, 1, 'Dynamically fetched result text 3', 0.7, '2022-09-26 14:03:28.609+00', '2022-09-26 14:03:28.609+00');


--
-- Data for Name: Survey_user_groups; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: Surveys; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public."Surveys" VALUES (1, 'Survey 1', '2022-09-20 12:28:09.613+00', '2022-09-20 12:28:09.613+00', 'This will be survey title text', 'This will be survey flavor text');
INSERT INTO public."Surveys" VALUES (2, 'Survey 2', '2022-09-20 12:36:57.525+00', '2022-09-20 12:36:57.525+00', 'This will be survey title text', 'This will be survey flavor text');
INSERT INTO public."Surveys" VALUES (3, 'Paras ohjelmointikieli', '2022-09-30 06:55:00.222057+00', '2022-09-30 06:55:00.222057+00', 'Mikä on paras ohjelmointikieli?', 'Onko se python? Vaiko Java?');


--
-- Data for Name: User_answers; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: Users; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Name: Admins_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."Admins_id_seq"', 8, true);


--
-- Name: Categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."Categories_id_seq"', 1, false);


--
-- Name: Category_results_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."Category_results_id_seq"', 1, false);


--
-- Name: Industries_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."Industries_id_seq"', 1, false);


--
-- Name: Question_answers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."Question_answers_id_seq"', 1, false);


--
-- Name: Questions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."Questions_id_seq"', 9, true);


--
-- Name: Survey_results_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."Survey_results_id_seq"', 1, false);


--
-- Name: Surveys_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."Surveys_id_seq"', 3, true);


--
-- Name: User_answers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."User_answers_id_seq"', 1, false);


--
-- Name: Users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."Users_id_seq"', 1, false);


--
-- Name: Admins Admins_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Admins"
    ADD CONSTRAINT "Admins_pkey" PRIMARY KEY (id);


--
-- Name: Categories Categories_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Categories"
    ADD CONSTRAINT "Categories_pkey" PRIMARY KEY (id);


--
-- Name: Category_results Category_results_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Category_results"
    ADD CONSTRAINT "Category_results_pkey" PRIMARY KEY (id);


--
-- Name: Industries Industries_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Industries"
    ADD CONSTRAINT "Industries_pkey" PRIMARY KEY (id);


--
-- Name: Organizations Organizations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Organizations"
    ADD CONSTRAINT "Organizations_pkey" PRIMARY KEY (id);


--
-- Name: Question_answers Question_answers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Question_answers"
    ADD CONSTRAINT "Question_answers_pkey" PRIMARY KEY (id);


--
-- Name: Questions Questions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Questions"
    ADD CONSTRAINT "Questions_pkey" PRIMARY KEY (id);


--
-- Name: Survey_results Survey_results_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Survey_results"
    ADD CONSTRAINT "Survey_results_pkey" PRIMARY KEY (id);


--
-- Name: Survey_user_groups Survey_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Survey_user_groups"
    ADD CONSTRAINT "Survey_user_groups_pkey" PRIMARY KEY (id);


--
-- Name: Surveys Surveys_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Surveys"
    ADD CONSTRAINT "Surveys_pkey" PRIMARY KEY (id);


--
-- Name: User_answers User_answers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."User_answers"
    ADD CONSTRAINT "User_answers_pkey" PRIMARY KEY (id);


--
-- Name: Users Users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Users"
    ADD CONSTRAINT "Users_pkey" PRIMARY KEY (id);


--
-- Name: Category_results Category_results_categoryId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Category_results"
    ADD CONSTRAINT "Category_results_categoryId_fkey" FOREIGN KEY ("categoryId") REFERENCES public."Categories"(id) ON UPDATE CASCADE;


--
-- Name: Question_answers Question_answers_questionId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Question_answers"
    ADD CONSTRAINT "Question_answers_questionId_fkey" FOREIGN KEY ("questionId") REFERENCES public."Questions"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: Questions Questions_surveyId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Questions"
    ADD CONSTRAINT "Questions_surveyId_fkey" FOREIGN KEY ("surveyId") REFERENCES public."Surveys"(id) ON UPDATE CASCADE;


--
-- Name: Survey_results Survey_results_surveyId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Survey_results"
    ADD CONSTRAINT "Survey_results_surveyId_fkey" FOREIGN KEY ("surveyId") REFERENCES public."Surveys"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: Survey_user_groups Survey_user_groups_organizationId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Survey_user_groups"
    ADD CONSTRAINT "Survey_user_groups_organizationId_fkey" FOREIGN KEY ("organizationId") REFERENCES public."Organizations"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: Survey_user_groups Survey_user_groups_surveyId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Survey_user_groups"
    ADD CONSTRAINT "Survey_user_groups_surveyId_fkey" FOREIGN KEY ("surveyId") REFERENCES public."Surveys"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: User_answers User_answers_QuestionAnswerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."User_answers"
    ADD CONSTRAINT "User_answers_QuestionAnswerId_fkey" FOREIGN KEY ("QuestionAnswerId") REFERENCES public."Question_answers"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: User_answers User_answers_questionAnswerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."User_answers"
    ADD CONSTRAINT "User_answers_questionAnswerId_fkey" FOREIGN KEY ("questionAnswerId") REFERENCES public."Question_answers"(id) ON UPDATE CASCADE;


--
-- Name: User_answers User_answers_userId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."User_answers"
    ADD CONSTRAINT "User_answers_userId_fkey" FOREIGN KEY ("userId") REFERENCES public."Users"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: Users Users_groupId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Users"
    ADD CONSTRAINT "Users_groupId_fkey" FOREIGN KEY ("groupId") REFERENCES public."Survey_user_groups"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: Users Users_industryId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Users"
    ADD CONSTRAINT "Users_industryId_fkey" FOREIGN KEY ("industryId") REFERENCES public."Industries"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: SCHEMA heroku_ext; Type: ACL; Schema: -; Owner: -
--

GRANT USAGE ON SCHEMA heroku_ext TO wylkhmgvtlywtp;


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: -
--

REVOKE ALL ON SCHEMA public FROM postgres;
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO wylkhmgvtlywtp;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- Name: LANGUAGE plpgsql; Type: ACL; Schema: -; Owner: -
--

GRANT ALL ON LANGUAGE plpgsql TO wylkhmgvtlywtp;


--
-- PostgreSQL database dump complete
--

