--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5 (Ubuntu 14.5-1.pgdg20.04+1)
-- Dumped by pg_dump version 14.5 (Ubuntu 14.5-0ubuntu0.22.04.1)

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
-- Name: heroku_ext; Type: SCHEMA; Schema: -; Owner: u9osjafbq65ukv
--

CREATE SCHEMA heroku_ext;


ALTER SCHEMA heroku_ext OWNER TO u9osjafbq65ukv;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: Admins; Type: TABLE; Schema: public; Owner: wylkhmgvtlywtp
--

CREATE TABLE public."Admins" (
    id SERIAL PRIMARY KEY,
    email text
);


ALTER TABLE public."Admins" OWNER TO wylkhmgvtlywtp;

--
-- Name: Admins_id_seq; Type: SEQUENCE; Schema: public; Owner: wylkhmgvtlywtp
--

CREATE SEQUENCE public."Admins_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Admins_id_seq" OWNER TO wylkhmgvtlywtp;

--
-- Name: Admins_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER SEQUENCE public."Admins_id_seq" OWNED BY public."Admins".id;


--
-- Name: Categories; Type: TABLE; Schema: public; Owner: wylkhmgvtlywtp
--

CREATE TABLE public."Categories" (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text NOT NULL,
    content_links json,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


ALTER TABLE public."Categories" OWNER TO wylkhmgvtlywtp;

--
-- Name: Categories_id_seq; Type: SEQUENCE; Schema: public; Owner: wylkhmgvtlywtp
--

CREATE SEQUENCE public."Categories_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Categories_id_seq" OWNER TO wylkhmgvtlywtp;

--
-- Name: Categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER SEQUENCE public."Categories_id_seq" OWNED BY public."Categories".id;


--
-- Name: Category_results; Type: TABLE; Schema: public; Owner: wylkhmgvtlywtp
--

CREATE TABLE public."Category_results" (
    id integer NOT NULL,
    "categoryId" integer NOT NULL,
    text character varying(255),
    cutoff_from_maxpoints double precision,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


ALTER TABLE public."Category_results" OWNER TO wylkhmgvtlywtp;

--
-- Name: Category_results_id_seq; Type: SEQUENCE; Schema: public; Owner: wylkhmgvtlywtp
--

CREATE SEQUENCE public."Category_results_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Category_results_id_seq" OWNER TO wylkhmgvtlywtp;

--
-- Name: Category_results_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER SEQUENCE public."Category_results_id_seq" OWNED BY public."Category_results".id;


--
-- Name: Industries; Type: TABLE; Schema: public; Owner: wylkhmgvtlywtp
--

CREATE TABLE public."Industries" (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


ALTER TABLE public."Industries" OWNER TO wylkhmgvtlywtp;

--
-- Name: Industries_id_seq; Type: SEQUENCE; Schema: public; Owner: wylkhmgvtlywtp
--

CREATE SEQUENCE public."Industries_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Industries_id_seq" OWNER TO wylkhmgvtlywtp;

--
-- Name: Industries_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER SEQUENCE public."Industries_id_seq" OWNED BY public."Industries".id;


--
-- Name: Organizations; Type: TABLE; Schema: public; Owner: wylkhmgvtlywtp
--

CREATE TABLE public."Organizations" (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


ALTER TABLE public."Organizations" OWNER TO wylkhmgvtlywtp;

--
-- Name: Question_answers; Type: TABLE; Schema: public; Owner: wylkhmgvtlywtp
--

CREATE TABLE public."Question_answers" (
    id integer NOT NULL,
    text character varying(255) NOT NULL,
    points integer NOT NULL,
    "questionId" integer NOT NULL,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


ALTER TABLE public."Question_answers" OWNER TO wylkhmgvtlywtp;

--
-- Name: Question_answers_id_seq; Type: SEQUENCE; Schema: public; Owner: wylkhmgvtlywtp
--

CREATE SEQUENCE public."Question_answers_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Question_answers_id_seq" OWNER TO wylkhmgvtlywtp;

--
-- Name: Question_answers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER SEQUENCE public."Question_answers_id_seq" OWNED BY public."Question_answers".id;


--
-- Name: Questions; Type: TABLE; Schema: public; Owner: wylkhmgvtlywtp
--

CREATE TABLE public."Questions" (
    id integer NOT NULL,
    text character varying(255) NOT NULL,
    "surveyId" integer NOT NULL,
    category_weights jsonb,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


ALTER TABLE public."Questions" OWNER TO wylkhmgvtlywtp;

--
-- Name: Questions_id_seq; Type: SEQUENCE; Schema: public; Owner: wylkhmgvtlywtp
--

CREATE SEQUENCE public."Questions_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Questions_id_seq" OWNER TO wylkhmgvtlywtp;

--
-- Name: Questions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER SEQUENCE public."Questions_id_seq" OWNED BY public."Questions".id;


--
-- Name: Survey_results; Type: TABLE; Schema: public; Owner: wylkhmgvtlywtp
--

CREATE TABLE public."Survey_results" (
    id integer NOT NULL,
    "surveyId" integer NOT NULL,
    text character varying(255) NOT NULL,
    cutoff_from_maxpoints double precision,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


ALTER TABLE public."Survey_results" OWNER TO wylkhmgvtlywtp;

--
-- Name: Survey_results_id_seq; Type: SEQUENCE; Schema: public; Owner: wylkhmgvtlywtp
--

CREATE SEQUENCE public."Survey_results_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Survey_results_id_seq" OWNER TO wylkhmgvtlywtp;

--
-- Name: Survey_results_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER SEQUENCE public."Survey_results_id_seq" OWNED BY public."Survey_results".id;


--
-- Name: Survey_user_groups; Type: TABLE; Schema: public; Owner: wylkhmgvtlywtp
--

CREATE TABLE public."Survey_user_groups" (
    id uuid NOT NULL,
    group_name character varying(255),
    "surveyId" integer NOT NULL,
    "organizationId" integer,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


ALTER TABLE public."Survey_user_groups" OWNER TO wylkhmgvtlywtp;

--
-- Name: Surveys; Type: TABLE; Schema: public; Owner: wylkhmgvtlywtp
--

CREATE TABLE public."Surveys" (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


ALTER TABLE public."Surveys" OWNER TO wylkhmgvtlywtp;

--
-- Name: Surveys_id_seq; Type: SEQUENCE; Schema: public; Owner: wylkhmgvtlywtp
--

CREATE SEQUENCE public."Surveys_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Surveys_id_seq" OWNER TO wylkhmgvtlywtp;

--
-- Name: Surveys_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER SEQUENCE public."Surveys_id_seq" OWNED BY public."Surveys".id;


--
-- Name: User_answers; Type: TABLE; Schema: public; Owner: wylkhmgvtlywtp
--

CREATE TABLE public."User_answers" (
    id integer NOT NULL,
    "userId" integer NOT NULL,
    "questionAnswerId" integer NOT NULL,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL,
    "QuestionAnswerId" integer
);


ALTER TABLE public."User_answers" OWNER TO wylkhmgvtlywtp;

--
-- Name: User_answers_id_seq; Type: SEQUENCE; Schema: public; Owner: wylkhmgvtlywtp
--

CREATE SEQUENCE public."User_answers_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."User_answers_id_seq" OWNER TO wylkhmgvtlywtp;

--
-- Name: User_answers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER SEQUENCE public."User_answers_id_seq" OWNED BY public."User_answers".id;


--
-- Name: Users; Type: TABLE; Schema: public; Owner: wylkhmgvtlywtp
--

CREATE TABLE public."Users" (
    id integer NOT NULL,
    email character varying(255),
    "groupId" uuid,
    "industryId" integer,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


ALTER TABLE public."Users" OWNER TO wylkhmgvtlywtp;

--
-- Name: Users_id_seq; Type: SEQUENCE; Schema: public; Owner: wylkhmgvtlywtp
--

CREATE SEQUENCE public."Users_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Users_id_seq" OWNER TO wylkhmgvtlywtp;

--
-- Name: Users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER SEQUENCE public."Users_id_seq" OWNED BY public."Users".id;


--
-- Name: Admins id; Type: DEFAULT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."Admins" ALTER COLUMN id SET DEFAULT nextval('public."Admins_id_seq"'::regclass);


--
-- Name: Categories id; Type: DEFAULT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."Categories" ALTER COLUMN id SET DEFAULT nextval('public."Categories_id_seq"'::regclass);


--
-- Name: Category_results id; Type: DEFAULT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."Category_results" ALTER COLUMN id SET DEFAULT nextval('public."Category_results_id_seq"'::regclass);


--
-- Name: Industries id; Type: DEFAULT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."Industries" ALTER COLUMN id SET DEFAULT nextval('public."Industries_id_seq"'::regclass);


--
-- Name: Question_answers id; Type: DEFAULT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."Question_answers" ALTER COLUMN id SET DEFAULT nextval('public."Question_answers_id_seq"'::regclass);


--
-- Name: Questions id; Type: DEFAULT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."Questions" ALTER COLUMN id SET DEFAULT nextval('public."Questions_id_seq"'::regclass);


--
-- Name: Survey_results id; Type: DEFAULT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."Survey_results" ALTER COLUMN id SET DEFAULT nextval('public."Survey_results_id_seq"'::regclass);


--
-- Name: Surveys id; Type: DEFAULT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."Surveys" ALTER COLUMN id SET DEFAULT nextval('public."Surveys_id_seq"'::regclass);


--
-- Name: User_answers id; Type: DEFAULT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."User_answers" ALTER COLUMN id SET DEFAULT nextval('public."User_answers_id_seq"'::regclass);


--
-- Name: Users id; Type: DEFAULT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."Users" ALTER COLUMN id SET DEFAULT nextval('public."Users_id_seq"'::regclass);


--
-- Data for Name: Admins; Type: TABLE DATA; Schema: public; Owner: wylkhmgvtlywtp
--

COPY public."Admins" (id, email) FROM stdin;
2	rami.piik@gmail.com
3	antti.vainikka36@gmail.com
4	jatufin@gmail.com
5	me@juan.fi
6	niemi.leo@gmail.com
7	oskar.sjolund93@gmail.com
8	siljaorvokki@gmail.com
\.


--
-- Data for Name: Categories; Type: TABLE DATA; Schema: public; Owner: wylkhmgvtlywtp
--

COPY public."Categories" (id, name, description, content_links, "createdAt", "updatedAt") FROM stdin;
\.


--
-- Data for Name: Category_results; Type: TABLE DATA; Schema: public; Owner: wylkhmgvtlywtp
--

COPY public."Category_results" (id, "categoryId", text, cutoff_from_maxpoints, "createdAt", "updatedAt") FROM stdin;
\.


--
-- Data for Name: Industries; Type: TABLE DATA; Schema: public; Owner: wylkhmgvtlywtp
--

COPY public."Industries" (id, name, "createdAt", "updatedAt") FROM stdin;
\.


--
-- Data for Name: Organizations; Type: TABLE DATA; Schema: public; Owner: wylkhmgvtlywtp
--

COPY public."Organizations" (id, name, "createdAt", "updatedAt") FROM stdin;
\.


--
-- Data for Name: Question_answers; Type: TABLE DATA; Schema: public; Owner: wylkhmgvtlywtp
--

COPY public."Question_answers" (id, text, points, "questionId", "createdAt", "updatedAt") FROM stdin;
\.


--
-- Data for Name: Questions; Type: TABLE DATA; Schema: public; Owner: wylkhmgvtlywtp
--

COPY public."Questions" (id, text, "surveyId", category_weights, "createdAt", "updatedAt") FROM stdin;
\.


--
-- Data for Name: Survey_results; Type: TABLE DATA; Schema: public; Owner: wylkhmgvtlywtp
--

COPY public."Survey_results" (id, "surveyId", text, cutoff_from_maxpoints, "createdAt", "updatedAt") FROM stdin;
\.


--
-- Data for Name: Survey_user_groups; Type: TABLE DATA; Schema: public; Owner: wylkhmgvtlywtp
--

COPY public."Survey_user_groups" (id, group_name, "surveyId", "organizationId", "createdAt", "updatedAt") FROM stdin;
\.


--
-- Data for Name: Surveys; Type: TABLE DATA; Schema: public; Owner: wylkhmgvtlywtp
--

COPY public."Surveys" (id, name, "createdAt", "updatedAt") FROM stdin;
1	Survey 1	2022-09-20 12:28:09.613+00	2022-09-20 12:28:09.613+00
2	Survey 2	2022-09-20 12:36:57.525+00	2022-09-20 12:36:57.525+00
\.


--
-- Data for Name: User_answers; Type: TABLE DATA; Schema: public; Owner: wylkhmgvtlywtp
--

COPY public."User_answers" (id, "userId", "questionAnswerId", "createdAt", "updatedAt", "QuestionAnswerId") FROM stdin;
\.


--
-- Data for Name: Users; Type: TABLE DATA; Schema: public; Owner: wylkhmgvtlywtp
--

COPY public."Users" (id, email, "groupId", "industryId", "createdAt", "updatedAt") FROM stdin;
\.


--
-- Name: Admins_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wylkhmgvtlywtp
--

SELECT pg_catalog.setval('public."Admins_id_seq"', 8, true);


--
-- Name: Categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wylkhmgvtlywtp
--

SELECT pg_catalog.setval('public."Categories_id_seq"', 1, false);


--
-- Name: Category_results_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wylkhmgvtlywtp
--

SELECT pg_catalog.setval('public."Category_results_id_seq"', 1, false);


--
-- Name: Industries_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wylkhmgvtlywtp
--

SELECT pg_catalog.setval('public."Industries_id_seq"', 1, false);


--
-- Name: Question_answers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wylkhmgvtlywtp
--

SELECT pg_catalog.setval('public."Question_answers_id_seq"', 1, false);


--
-- Name: Questions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wylkhmgvtlywtp
--

SELECT pg_catalog.setval('public."Questions_id_seq"', 1, false);


--
-- Name: Survey_results_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wylkhmgvtlywtp
--

SELECT pg_catalog.setval('public."Survey_results_id_seq"', 1, false);


--
-- Name: Surveys_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wylkhmgvtlywtp
--

SELECT pg_catalog.setval('public."Surveys_id_seq"', 1, false);


--
-- Name: User_answers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wylkhmgvtlywtp
--

SELECT pg_catalog.setval('public."User_answers_id_seq"', 1, false);


--
-- Name: Users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wylkhmgvtlywtp
--

SELECT pg_catalog.setval('public."Users_id_seq"', 1, false);


--
-- Name: Admins Admins_pkey; Type: CONSTRAINT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."Admins"
    ADD CONSTRAINT "Admins_pkey" PRIMARY KEY (id);


--
-- Name: Categories Categories_pkey; Type: CONSTRAINT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."Categories"
    ADD CONSTRAINT "Categories_pkey" PRIMARY KEY (id);


--
-- Name: Category_results Category_results_pkey; Type: CONSTRAINT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."Category_results"
    ADD CONSTRAINT "Category_results_pkey" PRIMARY KEY (id);


--
-- Name: Industries Industries_pkey; Type: CONSTRAINT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."Industries"
    ADD CONSTRAINT "Industries_pkey" PRIMARY KEY (id);


--
-- Name: Organizations Organizations_pkey; Type: CONSTRAINT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."Organizations"
    ADD CONSTRAINT "Organizations_pkey" PRIMARY KEY (id);


--
-- Name: Question_answers Question_answers_pkey; Type: CONSTRAINT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."Question_answers"
    ADD CONSTRAINT "Question_answers_pkey" PRIMARY KEY (id);


--
-- Name: Questions Questions_pkey; Type: CONSTRAINT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."Questions"
    ADD CONSTRAINT "Questions_pkey" PRIMARY KEY (id);


--
-- Name: Survey_results Survey_results_pkey; Type: CONSTRAINT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."Survey_results"
    ADD CONSTRAINT "Survey_results_pkey" PRIMARY KEY (id);


--
-- Name: Survey_user_groups Survey_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."Survey_user_groups"
    ADD CONSTRAINT "Survey_user_groups_pkey" PRIMARY KEY (id);


--
-- Name: Surveys Surveys_pkey; Type: CONSTRAINT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."Surveys"
    ADD CONSTRAINT "Surveys_pkey" PRIMARY KEY (id);


--
-- Name: User_answers User_answers_pkey; Type: CONSTRAINT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."User_answers"
    ADD CONSTRAINT "User_answers_pkey" PRIMARY KEY (id);


--
-- Name: Users Users_pkey; Type: CONSTRAINT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."Users"
    ADD CONSTRAINT "Users_pkey" PRIMARY KEY (id);


--
-- Name: Category_results Category_results_categoryId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."Category_results"
    ADD CONSTRAINT "Category_results_categoryId_fkey" FOREIGN KEY ("categoryId") REFERENCES public."Categories"(id) ON UPDATE CASCADE;


--
-- Name: Question_answers Question_answers_questionId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."Question_answers"
    ADD CONSTRAINT "Question_answers_questionId_fkey" FOREIGN KEY ("questionId") REFERENCES public."Questions"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: Questions Questions_surveyId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."Questions"
    ADD CONSTRAINT "Questions_surveyId_fkey" FOREIGN KEY ("surveyId") REFERENCES public."Surveys"(id) ON UPDATE CASCADE;


--
-- Name: Survey_results Survey_results_surveyId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."Survey_results"
    ADD CONSTRAINT "Survey_results_surveyId_fkey" FOREIGN KEY ("surveyId") REFERENCES public."Surveys"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: Survey_user_groups Survey_user_groups_organizationId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."Survey_user_groups"
    ADD CONSTRAINT "Survey_user_groups_organizationId_fkey" FOREIGN KEY ("organizationId") REFERENCES public."Organizations"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: Survey_user_groups Survey_user_groups_surveyId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."Survey_user_groups"
    ADD CONSTRAINT "Survey_user_groups_surveyId_fkey" FOREIGN KEY ("surveyId") REFERENCES public."Surveys"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: User_answers User_answers_QuestionAnswerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."User_answers"
    ADD CONSTRAINT "User_answers_QuestionAnswerId_fkey" FOREIGN KEY ("QuestionAnswerId") REFERENCES public."Question_answers"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: User_answers User_answers_questionAnswerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."User_answers"
    ADD CONSTRAINT "User_answers_questionAnswerId_fkey" FOREIGN KEY ("questionAnswerId") REFERENCES public."Question_answers"(id) ON UPDATE CASCADE;


--
-- Name: User_answers User_answers_userId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."User_answers"
    ADD CONSTRAINT "User_answers_userId_fkey" FOREIGN KEY ("userId") REFERENCES public."Users"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: Users Users_groupId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."Users"
    ADD CONSTRAINT "Users_groupId_fkey" FOREIGN KEY ("groupId") REFERENCES public."Survey_user_groups"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: Users Users_industryId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wylkhmgvtlywtp
--

ALTER TABLE ONLY public."Users"
    ADD CONSTRAINT "Users_industryId_fkey" FOREIGN KEY ("industryId") REFERENCES public."Industries"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: SCHEMA heroku_ext; Type: ACL; Schema: -; Owner: u9osjafbq65ukv
--

GRANT USAGE ON SCHEMA heroku_ext TO wylkhmgvtlywtp;


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: wylkhmgvtlywtp
--

REVOKE ALL ON SCHEMA public FROM postgres;
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO wylkhmgvtlywtp;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- Name: LANGUAGE plpgsql; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON LANGUAGE plpgsql TO wylkhmgvtlywtp;


--
-- PostgreSQL database dump complete
--

