--
-- PostgreSQL database dump
--

-- Dumped from database version 16.9 (Ubuntu 16.9-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.9 (Ubuntu 16.9-0ubuntu0.24.04.1)

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
-- Name: clockeventtypes; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.clockeventtypes AS ENUM (
    'IN',
    'OUT'
);


ALTER TYPE public.clockeventtypes OWNER TO postgres;

--
-- Name: jobopportunityabilityimportance; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.jobopportunityabilityimportance AS ENUM (
    'REQUERIDA',
    'DESEADA'
);


ALTER TYPE public.jobopportunityabilityimportance OWNER TO postgres;

--
-- Name: jobopportunitystatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.jobopportunitystatus AS ENUM (
    'ACTIVO',
    'NO_ACTIVO'
);


ALTER TYPE public.jobopportunitystatus OWNER TO postgres;

--
-- Name: jobopportunityworkmode; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.jobopportunityworkmode AS ENUM (
    'REMOTO',
    'HIBRIDO',
    'PRESENCIAL'
);


ALTER TYPE public.jobopportunityworkmode OWNER TO postgres;

--
-- Name: paytype; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.paytype AS ENUM (
    'PAYABLE',
    'NOT_PAYABLE',
    'ARCHIVED',
    'PENDING_VALIDATION'
);


ALTER TYPE public.paytype OWNER TO postgres;

--
-- Name: postulationstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.postulationstatus AS ENUM (
    'PENDIENTE',
    'ACEPTADA',
    'NO_ACEPTADA',
    'CONTRATADO'
);


ALTER TYPE public.postulationstatus OWNER TO postgres;

--
-- Name: registertype; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.registertype AS ENUM (
    'AUSENCIA',
    'PRESENCIA',
    'DIA_NO_HABIL'
);


ALTER TYPE public.registertype OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: ability; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ability (
    name character varying(50) NOT NULL,
    description character varying(100),
    id integer NOT NULL
);


ALTER TABLE public.ability OWNER TO postgres;

--
-- Name: ability_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ability_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ability_id_seq OWNER TO postgres;

--
-- Name: ability_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ability_id_seq OWNED BY public.ability.id;


--
-- Name: clock_events; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clock_events (
    id integer NOT NULL,
    employee_id integer,
    event_date timestamp without time zone NOT NULL,
    event_type public.clockeventtypes NOT NULL,
    source character varying NOT NULL,
    device_id character varying NOT NULL
);


ALTER TABLE public.clock_events OWNER TO postgres;

--
-- Name: clock_events_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.clock_events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.clock_events_id_seq OWNER TO postgres;

--
-- Name: clock_events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.clock_events_id_seq OWNED BY public.clock_events.id;


--
-- Name: concept; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.concept (
    id integer NOT NULL,
    description character varying NOT NULL,
    is_deletable boolean NOT NULL
);


ALTER TABLE public.concept OWNER TO postgres;

--
-- Name: concept_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.concept_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.concept_id_seq OWNER TO postgres;

--
-- Name: concept_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.concept_id_seq OWNED BY public.concept.id;


--
-- Name: configuration; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.configuration (
    id integer NOT NULL,
    company_name character varying NOT NULL,
    primary_color character varying,
    secondary_color character varying,
    logo character varying,
    favicon character varying,
    email character varying NOT NULL,
    phone character varying NOT NULL
);


ALTER TABLE public.configuration OWNER TO postgres;

--
-- Name: configuration_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.configuration_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.configuration_id_seq OWNER TO postgres;

--
-- Name: configuration_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.configuration_id_seq OWNED BY public.configuration.id;


--
-- Name: country; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.country (
    id integer NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.country OWNER TO postgres;

--
-- Name: country_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.country_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.country_id_seq OWNER TO postgres;

--
-- Name: country_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.country_id_seq OWNED BY public.country.id;


--
-- Name: document; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.document (
    id integer NOT NULL,
    employee_id integer NOT NULL,
    name character varying(50) NOT NULL,
    extension character varying(5) NOT NULL,
    creation_date date NOT NULL,
    file bytea NOT NULL,
    active boolean NOT NULL
);


ALTER TABLE public.document OWNER TO postgres;

--
-- Name: document_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.document_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.document_id_seq OWNER TO postgres;

--
-- Name: document_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.document_id_seq OWNED BY public.document.id;


--
-- Name: employee; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employee (
    id integer NOT NULL,
    user_id character varying(100) NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    dni character varying(50) NOT NULL,
    type_dni character varying(10) NOT NULL,
    personal_email character varying(100) NOT NULL,
    active boolean NOT NULL,
    role_id integer,
    password character varying(100),
    phone character varying(20) NOT NULL,
    salary numeric NOT NULL,
    job_id integer,
    birth_date date NOT NULL,
    hire_date date NOT NULL,
    photo bytea,
    address_street character varying(100) NOT NULL,
    address_city character varying(100) NOT NULL,
    address_cp character varying(100) NOT NULL,
    address_state_id integer,
    address_country_id integer,
    shift_id integer
);


ALTER TABLE public.employee OWNER TO postgres;

--
-- Name: employee_hours; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employee_hours (
    id integer NOT NULL,
    employee_id integer,
    concept_id integer,
    shift_id integer NOT NULL,
    check_count integer NOT NULL,
    work_date date NOT NULL,
    register_type public.registertype NOT NULL,
    first_check_in time without time zone,
    last_check_out time without time zone,
    sumary_time time without time zone,
    extra_hours time without time zone,
    payroll_status public.paytype NOT NULL,
    notes character varying NOT NULL
);


ALTER TABLE public.employee_hours OWNER TO postgres;

--
-- Name: employee_hours_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.employee_hours_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.employee_hours_id_seq OWNER TO postgres;

--
-- Name: employee_hours_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.employee_hours_id_seq OWNED BY public.employee_hours.id;


--
-- Name: employee_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.employee_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.employee_id_seq OWNER TO postgres;

--
-- Name: employee_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.employee_id_seq OWNED BY public.employee.id;


--
-- Name: face_recognition; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.face_recognition (
    id integer NOT NULL,
    employee_id integer NOT NULL,
    embedding json
);


ALTER TABLE public.face_recognition OWNER TO postgres;

--
-- Name: face_recognition_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.face_recognition_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.face_recognition_id_seq OWNER TO postgres;

--
-- Name: face_recognition_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.face_recognition_id_seq OWNED BY public.face_recognition.id;


--
-- Name: job; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.job (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    sector_id integer NOT NULL
);


ALTER TABLE public.job OWNER TO postgres;

--
-- Name: job_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.job_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.job_id_seq OWNER TO postgres;

--
-- Name: job_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.job_id_seq OWNED BY public.job.id;


--
-- Name: job_opportunity; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.job_opportunity (
    owner_employee_id integer NOT NULL,
    status public.jobopportunitystatus NOT NULL,
    work_mode public.jobopportunityworkmode NOT NULL,
    title character varying(100) NOT NULL,
    description character varying(1000) NOT NULL,
    budget integer NOT NULL,
    budget_currency_id character varying(3) NOT NULL,
    state_id integer NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.job_opportunity OWNER TO postgres;

--
-- Name: job_opportunity_ability; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.job_opportunity_ability (
    job_opportunity_id integer NOT NULL,
    ability_id integer NOT NULL,
    ability_type public.jobopportunityabilityimportance NOT NULL
);


ALTER TABLE public.job_opportunity_ability OWNER TO postgres;

--
-- Name: job_opportunity_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.job_opportunity_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.job_opportunity_id_seq OWNER TO postgres;

--
-- Name: job_opportunity_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.job_opportunity_id_seq OWNED BY public.job_opportunity.id;


--
-- Name: leave; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.leave (
    id integer NOT NULL,
    employee_id integer NOT NULL,
    request_date date NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    file character varying,
    leave_type_id integer NOT NULL,
    reason character varying,
    document_status character varying NOT NULL,
    request_status character varying NOT NULL,
    observations character varying,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.leave OWNER TO postgres;

--
-- Name: leave_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.leave_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.leave_id_seq OWNER TO postgres;

--
-- Name: leave_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.leave_id_seq OWNED BY public.leave.id;


--
-- Name: leave_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.leave_type (
    id integer NOT NULL,
    type character varying NOT NULL,
    justification_required boolean NOT NULL
);


ALTER TABLE public.leave_type OWNER TO postgres;

--
-- Name: leave_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.leave_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.leave_type_id_seq OWNER TO postgres;

--
-- Name: leave_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.leave_type_id_seq OWNED BY public.leave_type.id;


--
-- Name: permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.permission (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    description character varying(100) NOT NULL
);


ALTER TABLE public.permission OWNER TO postgres;

--
-- Name: permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.permission_id_seq OWNER TO postgres;

--
-- Name: permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.permission_id_seq OWNED BY public.permission.id;


--
-- Name: postulation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.postulation (
    id integer NOT NULL,
    job_opportunity_id integer NOT NULL,
    name character varying(50) NOT NULL,
    surname character varying(50) NOT NULL,
    email character varying(100) NOT NULL,
    phone_number character varying(100) NOT NULL,
    address_country_id integer NOT NULL,
    address_state_id integer NOT NULL,
    cv_file character varying NOT NULL,
    evaluated_at timestamp without time zone,
    suitable boolean NOT NULL,
    ability_match json,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    status public.postulationstatus NOT NULL,
    motive character varying
);


ALTER TABLE public.postulation OWNER TO postgres;

--
-- Name: postulation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.postulation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.postulation_id_seq OWNER TO postgres;

--
-- Name: postulation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.postulation_id_seq OWNED BY public.postulation.id;


--
-- Name: role; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.role (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    description character varying(100) NOT NULL
);


ALTER TABLE public.role OWNER TO postgres;

--
-- Name: role_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.role_id_seq OWNER TO postgres;

--
-- Name: role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.role_id_seq OWNED BY public.role.id;


--
-- Name: role_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.role_permission (
    role_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.role_permission OWNER TO postgres;

--
-- Name: sector; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sector (
    id integer NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.sector OWNER TO postgres;

--
-- Name: sector_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sector_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sector_id_seq OWNER TO postgres;

--
-- Name: sector_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sector_id_seq OWNED BY public.sector.id;


--
-- Name: shift; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.shift (
    id integer NOT NULL,
    description character varying NOT NULL,
    type character varying NOT NULL,
    working_hours double precision NOT NULL,
    working_days integer NOT NULL
);


ALTER TABLE public.shift OWNER TO postgres;

--
-- Name: shift_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.shift_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.shift_id_seq OWNER TO postgres;

--
-- Name: shift_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.shift_id_seq OWNED BY public.shift.id;


--
-- Name: state; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.state (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    country_id integer NOT NULL
);


ALTER TABLE public.state OWNER TO postgres;

--
-- Name: state_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.state_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.state_id_seq OWNER TO postgres;

--
-- Name: state_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.state_id_seq OWNED BY public.state.id;


--
-- Name: work_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.work_history (
    id integer NOT NULL,
    employee_id integer NOT NULL,
    job_id integer NOT NULL,
    from_date date NOT NULL,
    to_date date NOT NULL,
    company_name character varying(40) NOT NULL,
    notes character varying(100) NOT NULL
);


ALTER TABLE public.work_history OWNER TO postgres;

--
-- Name: work_history_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.work_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.work_history_id_seq OWNER TO postgres;

--
-- Name: work_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.work_history_id_seq OWNED BY public.work_history.id;


--
-- Name: ability id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ability ALTER COLUMN id SET DEFAULT nextval('public.ability_id_seq'::regclass);


--
-- Name: clock_events id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clock_events ALTER COLUMN id SET DEFAULT nextval('public.clock_events_id_seq'::regclass);


--
-- Name: concept id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.concept ALTER COLUMN id SET DEFAULT nextval('public.concept_id_seq'::regclass);


--
-- Name: country id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.country ALTER COLUMN id SET DEFAULT nextval('public.country_id_seq'::regclass);


--
-- Name: document id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.document ALTER COLUMN id SET DEFAULT nextval('public.document_id_seq'::regclass);


--
-- Name: employee id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee ALTER COLUMN id SET DEFAULT nextval('public.employee_id_seq'::regclass);


--
-- Name: employee_hours id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee_hours ALTER COLUMN id SET DEFAULT nextval('public.employee_hours_id_seq'::regclass);


--
-- Name: face_recognition id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.face_recognition ALTER COLUMN id SET DEFAULT nextval('public.face_recognition_id_seq'::regclass);


--
-- Name: job id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job ALTER COLUMN id SET DEFAULT nextval('public.job_id_seq'::regclass);


--
-- Name: job_opportunity id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_opportunity ALTER COLUMN id SET DEFAULT nextval('public.job_opportunity_id_seq'::regclass);


--
-- Name: leave id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leave ALTER COLUMN id SET DEFAULT nextval('public.leave_id_seq'::regclass);


--
-- Name: leave_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leave_type ALTER COLUMN id SET DEFAULT nextval('public.leave_type_id_seq'::regclass);


--
-- Name: permission id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permission ALTER COLUMN id SET DEFAULT nextval('public.permission_id_seq'::regclass);


--
-- Name: postulation id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.postulation ALTER COLUMN id SET DEFAULT nextval('public.postulation_id_seq'::regclass);


--
-- Name: role id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role ALTER COLUMN id SET DEFAULT nextval('public.role_id_seq'::regclass);


--
-- Name: sector id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sector ALTER COLUMN id SET DEFAULT nextval('public.sector_id_seq'::regclass);


--
-- Name: shift id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shift ALTER COLUMN id SET DEFAULT nextval('public.shift_id_seq'::regclass);


--
-- Name: state id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.state ALTER COLUMN id SET DEFAULT nextval('public.state_id_seq'::regclass);


--
-- Name: work_history id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.work_history ALTER COLUMN id SET DEFAULT nextval('public.work_history_id_seq'::regclass);


--
-- Name: ability ability_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ability
    ADD CONSTRAINT ability_name_key UNIQUE (name);


--
-- Name: ability ability_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ability
    ADD CONSTRAINT ability_pkey PRIMARY KEY (id);


--
-- Name: clock_events clock_events_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clock_events
    ADD CONSTRAINT clock_events_pkey PRIMARY KEY (id);


--
-- Name: concept concept_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.concept
    ADD CONSTRAINT concept_pkey PRIMARY KEY (id);


--
-- Name: country country_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.country
    ADD CONSTRAINT country_pkey PRIMARY KEY (id);


--
-- Name: document document_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.document
    ADD CONSTRAINT document_pkey PRIMARY KEY (id);


--
-- Name: employee employee_dni_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT employee_dni_key UNIQUE (dni);


--
-- Name: employee_hours employee_hours_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee_hours
    ADD CONSTRAINT employee_hours_pkey PRIMARY KEY (id);


--
-- Name: employee employee_personal_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT employee_personal_email_key UNIQUE (personal_email);


--
-- Name: employee employee_phone_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT employee_phone_key UNIQUE (phone);


--
-- Name: employee employee_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT employee_pkey PRIMARY KEY (id);


--
-- Name: employee employee_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT employee_user_id_key UNIQUE (user_id);


--
-- Name: face_recognition face_recognition_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.face_recognition
    ADD CONSTRAINT face_recognition_pkey PRIMARY KEY (id);


--
-- Name: job_opportunity_ability job_opportunity_ability_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_opportunity_ability
    ADD CONSTRAINT job_opportunity_ability_pkey PRIMARY KEY (job_opportunity_id, ability_id);


--
-- Name: job_opportunity job_opportunity_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_opportunity
    ADD CONSTRAINT job_opportunity_pkey PRIMARY KEY (id);


--
-- Name: job job_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job
    ADD CONSTRAINT job_pkey PRIMARY KEY (id);


--
-- Name: leave leave_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leave
    ADD CONSTRAINT leave_pkey PRIMARY KEY (id);


--
-- Name: leave_type leave_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leave_type
    ADD CONSTRAINT leave_type_pkey PRIMARY KEY (id);


--
-- Name: permission permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permission
    ADD CONSTRAINT permission_pkey PRIMARY KEY (id);


--
-- Name: postulation postulation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.postulation
    ADD CONSTRAINT postulation_pkey PRIMARY KEY (id);


--
-- Name: role_permission role_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_permission
    ADD CONSTRAINT role_permission_pkey PRIMARY KEY (role_id, permission_id);


--
-- Name: role role_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_pkey PRIMARY KEY (id);


--
-- Name: sector sector_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sector
    ADD CONSTRAINT sector_pkey PRIMARY KEY (id);


--
-- Name: shift shift_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shift
    ADD CONSTRAINT shift_pkey PRIMARY KEY (id);


--
-- Name: state state_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.state
    ADD CONSTRAINT state_pkey PRIMARY KEY (id);


--
-- Name: work_history work_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.work_history
    ADD CONSTRAINT work_history_pkey PRIMARY KEY (id);


--
-- Name: ix_ability_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_ability_id ON public.ability USING btree (id);


--
-- Name: ix_country_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_country_id ON public.country USING btree (id);


--
-- Name: ix_country_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_country_name ON public.country USING btree (name);


--
-- Name: ix_document_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_document_id ON public.document USING btree (id);


--
-- Name: ix_employee_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_employee_id ON public.employee USING btree (id);


--
-- Name: ix_face_recognition_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_face_recognition_id ON public.face_recognition USING btree (id);


--
-- Name: ix_job_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_job_id ON public.job USING btree (id);


--
-- Name: ix_job_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_job_name ON public.job USING btree (name);


--
-- Name: ix_job_opportunity_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_job_opportunity_id ON public.job_opportunity USING btree (id);


--
-- Name: ix_leave_document_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_leave_document_status ON public.leave USING btree (document_status);


--
-- Name: ix_leave_employee_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_leave_employee_id ON public.leave USING btree (employee_id);


--
-- Name: ix_leave_end_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_leave_end_date ON public.leave USING btree (end_date);


--
-- Name: ix_leave_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_leave_id ON public.leave USING btree (id);


--
-- Name: ix_leave_request_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_leave_request_date ON public.leave USING btree (request_date);


--
-- Name: ix_leave_request_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_leave_request_status ON public.leave USING btree (request_status);


--
-- Name: ix_leave_start_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_leave_start_date ON public.leave USING btree (start_date);


--
-- Name: ix_leave_type_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_leave_type_id ON public.leave_type USING btree (id);


--
-- Name: ix_leave_type_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_leave_type_type ON public.leave_type USING btree (type);


--
-- Name: ix_permission_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_permission_id ON public.permission USING btree (id);


--
-- Name: ix_postulation_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_postulation_id ON public.postulation USING btree (id);


--
-- Name: ix_role_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_role_id ON public.role USING btree (id);


--
-- Name: ix_role_permission_permission_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_role_permission_permission_id ON public.role_permission USING btree (permission_id);


--
-- Name: ix_role_permission_role_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_role_permission_role_id ON public.role_permission USING btree (role_id);


--
-- Name: ix_sector_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_sector_id ON public.sector USING btree (id);


--
-- Name: ix_sector_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_sector_name ON public.sector USING btree (name);


--
-- Name: ix_state_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_state_id ON public.state USING btree (id);


--
-- Name: ix_state_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_state_name ON public.state USING btree (name);


--
-- Name: ix_work_history_company_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_work_history_company_name ON public.work_history USING btree (company_name);


--
-- Name: ix_work_history_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_work_history_id ON public.work_history USING btree (id);


--
-- Name: clock_events clock_events_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clock_events
    ADD CONSTRAINT clock_events_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employee(id) ON DELETE CASCADE;


--
-- Name: document document_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.document
    ADD CONSTRAINT document_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employee(id) ON DELETE CASCADE;


--
-- Name: employee employee_address_country_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT employee_address_country_id_fkey FOREIGN KEY (address_country_id) REFERENCES public.country(id);


--
-- Name: employee employee_address_state_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT employee_address_state_id_fkey FOREIGN KEY (address_state_id) REFERENCES public.state(id);


--
-- Name: employee_hours employee_hours_concept_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee_hours
    ADD CONSTRAINT employee_hours_concept_id_fkey FOREIGN KEY (concept_id) REFERENCES public.concept(id);


--
-- Name: employee_hours employee_hours_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee_hours
    ADD CONSTRAINT employee_hours_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employee(id) ON DELETE CASCADE;


--
-- Name: employee_hours employee_hours_shift_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee_hours
    ADD CONSTRAINT employee_hours_shift_id_fkey FOREIGN KEY (shift_id) REFERENCES public.shift(id);


--
-- Name: employee employee_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT employee_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.job(id);


--
-- Name: employee employee_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT employee_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.role(id);


--
-- Name: employee employee_shift_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT employee_shift_id_fkey FOREIGN KEY (shift_id) REFERENCES public.shift(id);


--
-- Name: face_recognition face_recognition_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.face_recognition
    ADD CONSTRAINT face_recognition_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employee(id);


--
-- Name: job_opportunity_ability job_opportunity_ability_ability_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_opportunity_ability
    ADD CONSTRAINT job_opportunity_ability_ability_id_fkey FOREIGN KEY (ability_id) REFERENCES public.ability(id);


--
-- Name: job_opportunity_ability job_opportunity_ability_job_opportunity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_opportunity_ability
    ADD CONSTRAINT job_opportunity_ability_job_opportunity_id_fkey FOREIGN KEY (job_opportunity_id) REFERENCES public.job_opportunity(id);


--
-- Name: job_opportunity job_opportunity_owner_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_opportunity
    ADD CONSTRAINT job_opportunity_owner_employee_id_fkey FOREIGN KEY (owner_employee_id) REFERENCES public.employee(id) ON DELETE CASCADE;


--
-- Name: job job_sector_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job
    ADD CONSTRAINT job_sector_id_fkey FOREIGN KEY (sector_id) REFERENCES public.sector(id);


--
-- Name: leave leave_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leave
    ADD CONSTRAINT leave_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employee(id);


--
-- Name: leave leave_leave_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leave
    ADD CONSTRAINT leave_leave_type_id_fkey FOREIGN KEY (leave_type_id) REFERENCES public.leave_type(id);


--
-- Name: postulation postulation_address_country_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.postulation
    ADD CONSTRAINT postulation_address_country_id_fkey FOREIGN KEY (address_country_id) REFERENCES public.country(id);


--
-- Name: postulation postulation_address_state_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.postulation
    ADD CONSTRAINT postulation_address_state_id_fkey FOREIGN KEY (address_state_id) REFERENCES public.state(id);


--
-- Name: postulation postulation_job_opportunity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.postulation
    ADD CONSTRAINT postulation_job_opportunity_id_fkey FOREIGN KEY (job_opportunity_id) REFERENCES public.job_opportunity(id);


--
-- Name: role_permission role_permission_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_permission
    ADD CONSTRAINT role_permission_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.permission(id) ON DELETE CASCADE;


--
-- Name: role_permission role_permission_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_permission
    ADD CONSTRAINT role_permission_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.role(id) ON DELETE CASCADE;


--
-- Name: state state_country_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.state
    ADD CONSTRAINT state_country_id_fkey FOREIGN KEY (country_id) REFERENCES public.country(id);


--
-- Name: work_history work_history_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.work_history
    ADD CONSTRAINT work_history_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employee(id) ON DELETE CASCADE;


--
-- Name: work_history work_history_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.work_history
    ADD CONSTRAINT work_history_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.job(id);


--
-- PostgreSQL database dump complete
--

