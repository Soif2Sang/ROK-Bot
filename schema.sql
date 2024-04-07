
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

CREATE EXTENSION IF NOT EXISTS "pg_net" WITH SCHEMA "extensions";

CREATE EXTENSION IF NOT EXISTS "pgsodium" WITH SCHEMA "pgsodium";

COMMENT ON SCHEMA "public" IS 'standard public schema';

CREATE EXTENSION IF NOT EXISTS "pg_graphql" WITH SCHEMA "graphql";

CREATE EXTENSION IF NOT EXISTS "pg_stat_statements" WITH SCHEMA "extensions";

CREATE EXTENSION IF NOT EXISTS "pgcrypto" WITH SCHEMA "extensions";

CREATE EXTENSION IF NOT EXISTS "pgjwt" WITH SCHEMA "extensions";

CREATE EXTENSION IF NOT EXISTS "supabase_vault" WITH SCHEMA "vault";

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA "extensions";

CREATE TYPE "public"."version_type" AS ENUM (
    'global',
    'brazilian'
);

ALTER TYPE "public"."version_type" OWNER TO "postgres";

CREATE OR REPLACE FUNCTION "public"."create_subscription"("user_id" "uuid", "tier" "text", "days" integer) RETURNS "void"
    LANGUAGE "plpgsql"
    AS $$
BEGIN
  IF EXISTS (
    SELECT 1
    FROM public.subscriptions
    WHERE public.subscriptions.user_id = create_subscription.user_id
      AND end_at > current_date
      AND public.subscriptions.tier = create_subscription.tier
  ) THEN
    INSERT INTO public.subscriptions (user_id, tier, start_at, end_at)
    VALUES (
      create_subscription.user_id,
      tier,
      (SELECT MAX(end_at)
       FROM public.subscriptions
       WHERE public.subscriptions.user_id = create_subscription.user_id
         AND end_at > current_date
         AND public.subscriptions.tier = create_subscription.tier
       LIMIT 1),
      (SELECT MAX(end_at)
       FROM public.subscriptions
       WHERE public.subscriptions.user_id = create_subscription.user_id
         AND end_at > current_date
         AND public.subscriptions.tier = create_subscription.tier
       LIMIT 1) + days * interval '1 day'
    );
  ELSE
    INSERT INTO public.subscriptions (user_id, tier, start_at, end_at)
    VALUES (
      create_subscription.user_id,
      tier,
      current_timestamp,
      current_timestamp + days * interval '1 day'
    );
  END IF;
END;
$$;

ALTER FUNCTION "public"."create_subscription"("user_id" "uuid", "tier" "text", "days" integer) OWNER TO "postgres";

CREATE OR REPLACE FUNCTION "public"."increase_captcha_request"() RETURNS integer
    LANGUAGE "plpgsql"
    AS $$DECLARE
    user_exists BOOLEAN;
    current_count INT;
BEGIN
    -- Check if there is a record for the current month and the given username
    SELECT EXISTS (
        SELECT 1 
        FROM captcha_request_count 
        WHERE user_id = auth.uid() 
        AND to_char(date, 'YYYYMM') = to_char(CURRENT_DATE, 'YYYYMM')
    ) INTO user_exists;

    IF user_exists THEN
        -- If the username exists for the current month, increment captcha_requests_count and get the current count
        UPDATE captcha_request_count
        SET captcha_requests_count = captcha_requests_count + 1,
            updated_at = NOW()
        WHERE user_id = auth.uid() 
        AND to_char(date, 'YYYYMM') = to_char(CURRENT_DATE, 'YYYYMM')
        RETURNING captcha_requests_count INTO current_count;
    ELSE
        -- If the username doesn't exist for the current month, create a new entry with captcha_requests_count as 1
        INSERT INTO captcha_request_count(user_id, date, captcha_requests_count, updated_at)
        VALUES(auth.uid(), CURRENT_DATE, 1, NOW())
        RETURNING captcha_requests_count INTO current_count;
    END IF;

    RETURN current_count;
END;
$$;

ALTER FUNCTION "public"."increase_captcha_request"() OWNER TO "postgres";

CREATE OR REPLACE FUNCTION "public"."insert_user_function"() RETURNS "trigger"
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
BEGIN
    INSERT INTO public.users (user_id, email, created_at)
    VALUES (NEW.id, NEW.email, CURRENT_TIMESTAMP);
    RETURN NEW;
END;
$$;

ALTER FUNCTION "public"."insert_user_function"() OWNER TO "postgres";

CREATE OR REPLACE FUNCTION "public"."update_captcha_request_count_function"() RETURNS "trigger"
    LANGUAGE "plpgsql"
    AS $$
BEGIN
  IF NEW.captcha_requests_count = OLD.captcha_requests_count + 1 THEN
    RETURN NEW;
  ELSE
    RAISE EXCEPTION 'Invalid captcha_requests_count update';
  END IF;
END;
$$;

ALTER FUNCTION "public"."update_captcha_request_count_function"() OWNER TO "postgres";

SET default_tablespace = '';

SET default_table_access_method = "heap";

CREATE TABLE IF NOT EXISTS "public"."captcha_request_count" (
    "id" bigint NOT NULL,
    "date" "date" DEFAULT CURRENT_DATE NOT NULL,
    "user_id" "uuid" NOT NULL,
    "captcha_requests_count" integer DEFAULT 0 NOT NULL,
    "updated_at" timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE "public"."captcha_request_count" OWNER TO "postgres";

ALTER TABLE "public"."captcha_request_count" ALTER COLUMN "id" ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME "public"."captcha_request_count_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE IF NOT EXISTS "public"."hwid" (
    "user_id" "uuid" NOT NULL,
    "hwid" "text"
);

ALTER TABLE "public"."hwid" OWNER TO "postgres";

CREATE TABLE IF NOT EXISTS "public"."keys" (
    "id" bigint NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "updated_at" timestamp with time zone DEFAULT "now"(),
    "name" "text",
    "auth" boolean DEFAULT true,
    "value" "text"
);

ALTER TABLE "public"."keys" OWNER TO "postgres";

ALTER TABLE "public"."keys" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."keys_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE IF NOT EXISTS "public"."log" (
    "id" bigint NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "content" "text"
);

ALTER TABLE "public"."log" OWNER TO "postgres";

ALTER TABLE "public"."log" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."log_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE IF NOT EXISTS "public"."messages" (
    "id" bigint NOT NULL,
    "start_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "end_at" timestamp with time zone DEFAULT "now"(),
    "message" "text" DEFAULT ''::"text",
    "user_id" "uuid",
    "read" boolean DEFAULT false NOT NULL
);

ALTER TABLE "public"."messages" OWNER TO "postgres";

ALTER TABLE "public"."messages" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."messages_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE IF NOT EXISTS "public"."subscriptions" (
    "id" bigint NOT NULL,
    "user_id" "uuid" NOT NULL,
    "tier" "text" DEFAULT 'tier1'::"text" NOT NULL,
    "start_at" timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "end_at" timestamp with time zone DEFAULT (CURRENT_TIMESTAMP + '30 days'::interval),
    "paused" boolean DEFAULT false,
    CONSTRAINT "subscription_tier_check" CHECK (("tier" = ANY (ARRAY['tier1'::"text", 'tier2'::"text", 'tier3'::"text", 'tier4'::"text"])))
);

ALTER TABLE "public"."subscriptions" OWNER TO "postgres";

ALTER TABLE "public"."subscriptions" ALTER COLUMN "id" ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME "public"."subscription_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE IF NOT EXISTS "public"."updates" (
    "id" bigint NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "version" "text" NOT NULL,
    "force" boolean DEFAULT false NOT NULL,
    "download_link" "text" NOT NULL,
    "changelog" "text",
    "version_type" "public"."version_type" DEFAULT 'global'::"public"."version_type"
);

ALTER TABLE "public"."updates" OWNER TO "postgres";

ALTER TABLE "public"."updates" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."updates_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE IF NOT EXISTS "public"."users" (
    "user_id" "uuid" NOT NULL,
    "email" "text" NOT NULL,
    "created_at" timestamp with time zone NOT NULL,
    "updated_at" timestamp with time zone,
    "version_type" "public"."version_type" DEFAULT 'global'::"public"."version_type"
);

ALTER TABLE "public"."users" OWNER TO "postgres";

ALTER TABLE ONLY "public"."captcha_request_count"
    ADD CONSTRAINT "captcha_request_count_pkey" PRIMARY KEY ("id");

ALTER TABLE ONLY "public"."hwid"
    ADD CONSTRAINT "hwid_pkey" PRIMARY KEY ("user_id");

ALTER TABLE ONLY "public"."keys"
    ADD CONSTRAINT "keys_pkey" PRIMARY KEY ("id");

ALTER TABLE ONLY "public"."log"
    ADD CONSTRAINT "log_pkey" PRIMARY KEY ("id");

ALTER TABLE ONLY "public"."messages"
    ADD CONSTRAINT "messages_pkey" PRIMARY KEY ("id");

ALTER TABLE ONLY "public"."subscriptions"
    ADD CONSTRAINT "subscription_pkey" PRIMARY KEY ("id");

ALTER TABLE ONLY "public"."updates"
    ADD CONSTRAINT "updates_pkey" PRIMARY KEY ("id");

ALTER TABLE ONLY "public"."users"
    ADD CONSTRAINT "users_pkey" PRIMARY KEY ("user_id");

CREATE OR REPLACE TRIGGER "trigger-update-captcha-request-count" BEFORE UPDATE ON "public"."captcha_request_count" FOR EACH ROW EXECUTE FUNCTION "public"."update_captcha_request_count_function"();

ALTER TABLE ONLY "public"."captcha_request_count"
    ADD CONSTRAINT "captcha_request_count_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth"."users"("id");

ALTER TABLE ONLY "public"."hwid"
    ADD CONSTRAINT "hwid_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth"."users"("id");

ALTER TABLE ONLY "public"."messages"
    ADD CONSTRAINT "messages_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth"."users"("id");

ALTER TABLE ONLY "public"."subscriptions"
    ADD CONSTRAINT "subscriptions_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth"."users"("id");

ALTER TABLE ONLY "public"."users"
    ADD CONSTRAINT "users_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth"."users"("id");

CREATE POLICY "Allow insert if user is a manager" ON "public"."subscriptions" FOR INSERT WITH CHECK (("auth"."uid"() = '60adf32c-dfc1-4fd6-b024-1a85ae1f3972'::"uuid"));

CREATE POLICY "Enable insert for authenticated users only" ON "public"."captcha_request_count" FOR INSERT TO "authenticated" WITH CHECK (("user_id" = "auth"."uid"()));

CREATE POLICY "Enable insert for public" ON "public"."log" FOR INSERT WITH CHECK (true);

CREATE POLICY "Enable insert for self" ON "public"."hwid" FOR INSERT TO "authenticated", "anon" WITH CHECK (("user_id" = "auth"."uid"()));

CREATE POLICY "Enable read access for all users" ON "public"."log" FOR SELECT USING (true);

CREATE POLICY "Enable read access for all users" ON "public"."updates" FOR SELECT USING (true);

CREATE POLICY "Enable read access for all users" ON "public"."users" FOR SELECT USING (true);

CREATE POLICY "Enable read for self only" ON "public"."hwid" FOR SELECT TO "authenticated" USING (("auth"."uid"() = "user_id"));

CREATE POLICY "Enable select for users based on user_id" ON "public"."subscriptions" FOR SELECT USING (((("auth"."uid"() = "user_id") AND (CURRENT_TIMESTAMP < "end_at")) OR ("auth"."uid"() = '596563b5-2920-4276-ac65-f5d559fdba3a'::"uuid")));

CREATE POLICY "Enable update for self only" ON "public"."captcha_request_count" FOR UPDATE TO "authenticated" USING (("user_id" = "auth"."uid"())) WITH CHECK (("user_id" = "auth"."uid"()));

ALTER TABLE "public"."hwid" ENABLE ROW LEVEL SECURITY;

ALTER TABLE "public"."keys" ENABLE ROW LEVEL SECURITY;

ALTER TABLE "public"."log" ENABLE ROW LEVEL SECURITY;

ALTER TABLE "public"."messages" ENABLE ROW LEVEL SECURITY;

CREATE POLICY "read_own_message_and_global" ON "public"."messages" FOR SELECT USING ((("user_id" IS NULL) OR ("user_id" = "auth"."uid"())));

CREATE POLICY "select_authenticated_keys" ON "public"."keys" FOR SELECT USING ((("auth" = true) AND (EXISTS ( SELECT 1
   FROM "public"."subscriptions"
  WHERE (("subscriptions"."user_id" = "auth"."uid"()) AND ("subscriptions"."end_at" > CURRENT_TIMESTAMP) AND ("subscriptions"."start_at" < CURRENT_TIMESTAMP) AND ("subscriptions"."paused" = false))))));

CREATE POLICY "select_unauth_keys" ON "public"."keys" FOR SELECT USING ((NOT "auth"));

ALTER TABLE "public"."subscriptions" ENABLE ROW LEVEL SECURITY;

ALTER TABLE "public"."updates" ENABLE ROW LEVEL SECURITY;

ALTER TABLE "public"."users" ENABLE ROW LEVEL SECURITY;

ALTER PUBLICATION "supabase_realtime" OWNER TO "postgres";

GRANT USAGE ON SCHEMA "public" TO "postgres";
GRANT USAGE ON SCHEMA "public" TO "anon";
GRANT USAGE ON SCHEMA "public" TO "authenticated";
GRANT USAGE ON SCHEMA "public" TO "service_role";

GRANT ALL ON FUNCTION "public"."create_subscription"("user_id" "uuid", "tier" "text", "days" integer) TO "anon";
GRANT ALL ON FUNCTION "public"."create_subscription"("user_id" "uuid", "tier" "text", "days" integer) TO "authenticated";
GRANT ALL ON FUNCTION "public"."create_subscription"("user_id" "uuid", "tier" "text", "days" integer) TO "service_role";

GRANT ALL ON FUNCTION "public"."increase_captcha_request"() TO "anon";
GRANT ALL ON FUNCTION "public"."increase_captcha_request"() TO "authenticated";
GRANT ALL ON FUNCTION "public"."increase_captcha_request"() TO "service_role";

GRANT ALL ON FUNCTION "public"."insert_user_function"() TO "anon";
GRANT ALL ON FUNCTION "public"."insert_user_function"() TO "authenticated";
GRANT ALL ON FUNCTION "public"."insert_user_function"() TO "service_role";

GRANT ALL ON FUNCTION "public"."update_captcha_request_count_function"() TO "anon";
GRANT ALL ON FUNCTION "public"."update_captcha_request_count_function"() TO "authenticated";
GRANT ALL ON FUNCTION "public"."update_captcha_request_count_function"() TO "service_role";

GRANT ALL ON TABLE "public"."captcha_request_count" TO "anon";
GRANT ALL ON TABLE "public"."captcha_request_count" TO "authenticated";
GRANT ALL ON TABLE "public"."captcha_request_count" TO "service_role";

GRANT ALL ON SEQUENCE "public"."captcha_request_count_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."captcha_request_count_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."captcha_request_count_id_seq" TO "service_role";

GRANT ALL ON TABLE "public"."hwid" TO "anon";
GRANT ALL ON TABLE "public"."hwid" TO "authenticated";
GRANT ALL ON TABLE "public"."hwid" TO "service_role";

GRANT ALL ON TABLE "public"."keys" TO "anon";
GRANT ALL ON TABLE "public"."keys" TO "authenticated";
GRANT ALL ON TABLE "public"."keys" TO "service_role";

GRANT ALL ON SEQUENCE "public"."keys_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."keys_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."keys_id_seq" TO "service_role";

GRANT ALL ON TABLE "public"."log" TO "anon";
GRANT ALL ON TABLE "public"."log" TO "authenticated";
GRANT ALL ON TABLE "public"."log" TO "service_role";

GRANT ALL ON SEQUENCE "public"."log_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."log_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."log_id_seq" TO "service_role";

GRANT ALL ON TABLE "public"."messages" TO "anon";
GRANT ALL ON TABLE "public"."messages" TO "authenticated";
GRANT ALL ON TABLE "public"."messages" TO "service_role";

GRANT ALL ON SEQUENCE "public"."messages_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."messages_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."messages_id_seq" TO "service_role";

GRANT ALL ON TABLE "public"."subscriptions" TO "anon";
GRANT ALL ON TABLE "public"."subscriptions" TO "authenticated";
GRANT ALL ON TABLE "public"."subscriptions" TO "service_role";

GRANT ALL ON SEQUENCE "public"."subscription_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."subscription_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."subscription_id_seq" TO "service_role";

GRANT ALL ON TABLE "public"."updates" TO "anon";
GRANT ALL ON TABLE "public"."updates" TO "authenticated";
GRANT ALL ON TABLE "public"."updates" TO "service_role";

GRANT ALL ON SEQUENCE "public"."updates_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."updates_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."updates_id_seq" TO "service_role";

GRANT ALL ON TABLE "public"."users" TO "anon";
GRANT ALL ON TABLE "public"."users" TO "authenticated";
GRANT ALL ON TABLE "public"."users" TO "service_role";

ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES  TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES  TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES  TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES  TO "service_role";

ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS  TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS  TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS  TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS  TO "service_role";

ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES  TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES  TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES  TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES  TO "service_role";

RESET ALL;
