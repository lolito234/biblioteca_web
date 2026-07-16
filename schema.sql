--
-- PostgreSQL database dump
--


-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: devoluciones; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.devoluciones (
    id_devolucion integer NOT NULL,
    id_reserva integer NOT NULL,
    id_usuario integer NOT NULL,
    id_libro integer NOT NULL,
    fecha_solicitud date DEFAULT CURRENT_DATE,
    fecha_verificacion date,
    estado_libro character varying(20),
    observaciones text
);


--
-- Name: devoluciones_id_devolucion_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.devoluciones_id_devolucion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: devoluciones_id_devolucion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.devoluciones_id_devolucion_seq OWNED BY public.devoluciones.id_devolucion;


--
-- Name: libros; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.libros (
    id_libro integer NOT NULL,
    titulo character varying(150) NOT NULL,
    autor character varying(100) NOT NULL,
    categoria character varying(50),
    stock integer DEFAULT 1,
    descripcion text,
    imagen_url text,
    imagen character varying(255),
    estado character varying(20) DEFAULT 'bueno'::character varying
);


--
-- Name: libros_id_libro_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.libros_id_libro_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: libros_id_libro_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.libros_id_libro_seq OWNED BY public.libros.id_libro;


--
-- Name: reservas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.reservas (
    id_reserva integer NOT NULL,
    id_usuario integer,
    id_libro integer,
    fecha_reserva date DEFAULT CURRENT_DATE,
    estado character varying(20) DEFAULT 'reservado'::character varying,
    fecha_limite date
);


--
-- Name: reservas_id_reserva_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.reservas_id_reserva_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: reservas_id_reserva_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.reservas_id_reserva_seq OWNED BY public.reservas.id_reserva;


--
-- Name: sanciones; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sanciones (
    id_sancion integer NOT NULL,
    id_usuario integer NOT NULL,
    id_devolucion integer,
    motivo text,
    fecha_emision date DEFAULT CURRENT_DATE,
    multa numeric(10,2) DEFAULT 0,
    estado character varying(20) DEFAULT 'pendiente'::character varying
);


--
-- Name: sanciones_id_sancion_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.sanciones_id_sancion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: sanciones_id_sancion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.sanciones_id_sancion_seq OWNED BY public.sanciones.id_sancion;


--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.usuarios (
    id_usuario integer NOT NULL,
    nombre character varying(100) NOT NULL,
    correo character varying(100) NOT NULL,
    contrasena character varying(255) NOT NULL,
    rol character varying(20) DEFAULT 'usuario'::character varying
);


--
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.usuarios_id_usuario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.usuarios_id_usuario_seq OWNED BY public.usuarios.id_usuario;


--
-- Name: devoluciones id_devolucion; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.devoluciones ALTER COLUMN id_devolucion SET DEFAULT nextval('public.devoluciones_id_devolucion_seq'::regclass);


--
-- Name: libros id_libro; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.libros ALTER COLUMN id_libro SET DEFAULT nextval('public.libros_id_libro_seq'::regclass);


--
-- Name: reservas id_reserva; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reservas ALTER COLUMN id_reserva SET DEFAULT nextval('public.reservas_id_reserva_seq'::regclass);


--
-- Name: sanciones id_sancion; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sanciones ALTER COLUMN id_sancion SET DEFAULT nextval('public.sanciones_id_sancion_seq'::regclass);


--
-- Name: usuarios id_usuario; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id_usuario SET DEFAULT nextval('public.usuarios_id_usuario_seq'::regclass);


--
-- Data for Name: devoluciones; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.devoluciones (id_devolucion, id_reserva, id_usuario, id_libro, fecha_solicitud, fecha_verificacion, estado_libro, observaciones) FROM stdin;
\.


--
-- Data for Name: libros; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.libros (id_libro, titulo, autor, categoria, stock, descripcion, imagen_url, imagen, estado) FROM stdin;
15	Sapiens	Yuval Noah Harari	Historia	9	Evolución humana	\N	\N	bueno
16	Hábitos atómicos	James Clear	Autoayuda	12	Mejora personal	\N	\N	bueno
17	Padre rico padre pobre	Robert Kiyosaki	Finanzas	11	Educación financiera	\N	\N	bueno
7	La Odisea	Homero	Épico	1	Viaje de Ulises	\N	\N	bueno
9	El Señor de los Anillos	J.R.R. Tolkien	Fantasía	7	Aventura épica	\N	\N	bueno
10	Los juegos del hambre	Suzanne Collins	Distopía	6	Supervivencia	\N	\N	bueno
6	Don Quijote de la Mancha	Miguel de Cervantes	Novela	6	Clásico español	\N	\N	bueno
8	Harry Potter y la piedra filosofal	J.K. Rowling	Fantasía	10	Magia	\N	\N	bueno
11	Orgullo y prejuicio	Jane Austen	Romance	6	Clásico romántico	\N	\N	bueno
12	Crimen y castigo	Fiódor Dostoyevski	Novela	5	Psicológico	\N	\N	bueno
14	El código Da Vinci	Dan Brown	Misterio	5	Conspiraciones	\N	\N	bueno
13	It	Stephen King	Terror	3	Payaso aterrador	\N	\N	bueno
1	Cien años de soledad	Gabriel Garcia Marquez	Novela	5	Obra clasica	\N	\N	bueno
2	1984	George Orwell	Distopia	4	Novela politica	\N	\N	bueno
5	El Principito	Antoine de Saint-Exupéry	Fabula	2	Historia reflexiva	\N	\N	bueno
\.


--
-- Data for Name: reservas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.reservas (id_reserva, id_usuario, id_libro, fecha_reserva, estado, fecha_limite) FROM stdin;
16	11	14	2026-07-15	reservado	\N
17	11	13	2026-07-15	reservado	\N
\.


--
-- Data for Name: sanciones; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.sanciones (id_sancion, id_usuario, id_devolucion, motivo, fecha_emision, multa, estado) FROM stdin;
\.


--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.usuarios (id_usuario, nombre, correo, contrasena, rol) FROM stdin;
11	adriano joshua	adrianochaconh@gmail.com	scrypt:32768:8:1$phbfGxaBiYSNJclH$6333f5ff3b43fa92a527fe3bf16a93ee1c425bdfafa2e55b5cbea9014297d6af60ca660ae59c6931b8711cdebffaed70b1b5e4d74e033a07dfb121d6302c6ba0	admin
12	lolito 	adrianojoshua30@gmail.com	scrypt:32768:8:1$rxzZed9S2tJvyrvp$92216ba05baa09a1bf78a0a6252f037f34bf79014267e8934adf8aa6024f95305658a348edfeea4420497e8c626a0d3bbaab01aa6e1dda31858f7bb5893ad056	usuario
\.


--
-- Name: devoluciones_id_devolucion_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.devoluciones_id_devolucion_seq', 2, true);


--
-- Name: libros_id_libro_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.libros_id_libro_seq', 17, true);


--
-- Name: reservas_id_reserva_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.reservas_id_reserva_seq', 20, true);


--
-- Name: sanciones_id_sancion_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.sanciones_id_sancion_seq', 1, true);


--
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.usuarios_id_usuario_seq', 14, true);


--
-- Name: devoluciones devoluciones_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.devoluciones
    ADD CONSTRAINT devoluciones_pkey PRIMARY KEY (id_devolucion);


--
-- Name: libros libros_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.libros
    ADD CONSTRAINT libros_pkey PRIMARY KEY (id_libro);


--
-- Name: reservas reservas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reservas
    ADD CONSTRAINT reservas_pkey PRIMARY KEY (id_reserva);


--
-- Name: sanciones sanciones_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sanciones
    ADD CONSTRAINT sanciones_pkey PRIMARY KEY (id_sancion);


--
-- Name: usuarios usuarios_correo_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_correo_key UNIQUE (correo);


--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id_usuario);


--
-- Name: devoluciones devoluciones_id_libro_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.devoluciones
    ADD CONSTRAINT devoluciones_id_libro_fkey FOREIGN KEY (id_libro) REFERENCES public.libros(id_libro);


--
-- Name: devoluciones devoluciones_id_reserva_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.devoluciones
    ADD CONSTRAINT devoluciones_id_reserva_fkey FOREIGN KEY (id_reserva) REFERENCES public.reservas(id_reserva);


--
-- Name: devoluciones devoluciones_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.devoluciones
    ADD CONSTRAINT devoluciones_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario);


--
-- Name: reservas reservas_id_libro_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reservas
    ADD CONSTRAINT reservas_id_libro_fkey FOREIGN KEY (id_libro) REFERENCES public.libros(id_libro);


--
-- Name: reservas reservas_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reservas
    ADD CONSTRAINT reservas_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario);


--
-- Name: sanciones sanciones_id_devolucion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sanciones
    ADD CONSTRAINT sanciones_id_devolucion_fkey FOREIGN KEY (id_devolucion) REFERENCES public.devoluciones(id_devolucion);


--
-- Name: sanciones sanciones_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sanciones
    ADD CONSTRAINT sanciones_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario);


--
-- PostgreSQL database dump complete
--


