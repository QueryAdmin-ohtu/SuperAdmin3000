CREATE TABLE public."Admins" (
    id integer NOT NULL,
    email text
);
CREATE TABLE public."Categories" (
    id integer NOT NULL,
    name text NOT NULL,
    description text NOT NULL,
    content_links json,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);
CREATE TABLE public."Category_results" (
    id integer NOT NULL,
    "categoryId" integer NOT NULL,
    text text,
    cutoff_from_maxpoints double precision,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);
CREATE TABLE public."Industries" (
    id integer NOT NULL,
    name text NOT NULL,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);
CREATE TABLE public."Organizations" (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);
CREATE TABLE public."Question_answers" (
    id integer NOT NULL,
    text text NOT NULL,
    points integer NOT NULL,
    "questionId" integer NOT NULL,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);
CREATE TABLE public."Questions" (
    id integer NOT NULL,
    text text NOT NULL,
    "surveyId" integer NOT NULL,
    category_weights jsonb,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);
CREATE TABLE public."Survey_results" (
    id integer NOT NULL,
    "surveyId" integer NOT NULL,
    text text NOT NULL,
    cutoff_from_maxpoints double precision,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);
CREATE TABLE public."Survey_user_groups" (
    id uuid NOT NULL,
    group_name character varying(255),
    "surveyId" integer NOT NULL,
    "organizationId" integer,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);
CREATE TABLE public."Surveys" (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL,
    title_text text,
    survey_text text
);
CREATE TABLE public."User_answers" (
    id integer NOT NULL,
    "userId" integer NOT NULL,
    "questionAnswerId" integer NOT NULL,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL,
    "QuestionAnswerId" integer
);
CREATE TABLE public."Users" (
    id integer NOT NULL,
    email character varying(255),
    "groupId" uuid,
    "industryId" integer,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);
