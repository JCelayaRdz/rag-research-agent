CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TYPE "document_type" AS ENUM (
  'PDF',
  'URL',
  'TXT'
);

CREATE TYPE "document_status" AS ENUM (
  'PENDING',
  'PROCESSING',
  'INDEXED',
  'ERROR'
);

CREATE TYPE "message_role" AS ENUM (
  'ASSISTANT',
  'USER'
);

CREATE TABLE "users" (
  "user_id" uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  "user_name" varchar UNIQUE NOT NULL,
  "email" varchar UNIQUE NOT NULL,
  "password" varchar NOT NULL,
  "created_at" timestamp DEFAULT (now())
);

CREATE TABLE "tokens" (
  "token_id" uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  "user_id" uuid NOT NULL,
  "token_hash" varchar UNIQUE NOT NULL,
  "created_at" timestamp NOT NULL DEFAULT (now()),
  "expires_at" timestamp NOT NULL,
  "revoked" bool NOT NULL DEFAULT false
);

CREATE TABLE "projects" (
  "project_id" uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  "project_name" varchar NOT NULL,
  "description" varchar,
  "user_id" uuid NOT NULL,
  "last_activity" timestamp,
  "created_at" timestamp DEFAULT (now())
);

CREATE TABLE "configurations" (
  "configuration_id" uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  "chunk_size" int NOT NULL DEFAULT 512,
  "overlap_size" int NOT NULL DEFAULT 50,
  "project_id" uuid UNIQUE NOT NULL
);

CREATE TABLE "documents" (
  "document_id" uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  "document_name" varchar NOT NULL,
  "type" document_type NOT NULL,
  "status" document_status NOT NULL,
  "project_id" uuid NOT NULL,
  "source_url" varchar,
  "created_at" timestamp DEFAULT (now()),
  "indexed_at" timestamp,
  "chunks_number" int DEFAULT 0,
  "file_size" int DEFAULT 0,
  "s3_key" varchar,
  "error_message" text
);

CREATE TABLE "chunks" (
  "chunk_id" uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  "document_id" uuid NOT NULL,
  "content" text NOT NULL,
  "embedding" vector(1536) NOT NULL,
  "metadata" jsonb
);

CREATE TABLE "conversations" (
  "conversation_id" uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  "project_id" uuid NOT NULL,
  "user_id" uuid NOT NULL,
  "conversation_name" varchar NOT NULL,
  "last_activity" timestamp,
  "created_at" timestamp DEFAULT (now())
);

CREATE TABLE "messages" (
  "message_id" uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  "conversation_id" uuid NOT NULL,
  "content" text NOT NULL,
  "role" message_role NOT NULL,
  "sent_at" timestamp NOT NULL
);

ALTER TABLE "tokens" 
  ADD FOREIGN KEY ("user_id") 
  REFERENCES "users" ("user_id") 
  ON DELETE CASCADE;

ALTER TABLE "projects" 
  ADD FOREIGN KEY ("user_id") 
  REFERENCES "users" ("user_id") 
  ON DELETE CASCADE;

ALTER TABLE "documents" 
  ADD FOREIGN KEY ("project_id") 
  REFERENCES "projects" ("project_id") 
  ON DELETE CASCADE;

ALTER TABLE "configurations" 
  ADD FOREIGN KEY ("project_id") 
  REFERENCES "projects" ("project_id") 
  ON DELETE CASCADE;

ALTER TABLE "chunks" 
  ADD FOREIGN KEY ("document_id") 
  REFERENCES "documents" ("document_id") 
  ON DELETE CASCADE;

ALTER TABLE "conversations" 
  ADD FOREIGN KEY ("project_id") 
  REFERENCES "projects" ("project_id") 
  ON DELETE CASCADE;

ALTER TABLE "conversations" 
  ADD FOREIGN KEY ("user_id") 
  REFERENCES "users" ("user_id") 
  ON DELETE CASCADE;

ALTER TABLE "messages" 
  ADD FOREIGN KEY ("conversation_id") 
  REFERENCES "conversations" ("conversation_id") 
  ON DELETE CASCADE;

CREATE INDEX ON "chunks" USING hnsw (embedding vector_cosine_ops);

CREATE INDEX ON "tokens" (user_id);
CREATE INDEX ON "documents"(project_id);
CREATE INDEX ON "chunks" (document_id);
CREATE INDEX ON "conversations" (project_id);
CREATE INDEX ON "conversations" (user_id);
CREATE INDEX ON "messages" (conversation_id);