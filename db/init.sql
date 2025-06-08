CREATE TABLE IF NOT EXISTS roles (
    id serial NOT NULL PRIMARY KEY,
    description varchar(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS chats_erGPT (
    id serial NOT NULL PRIMARY KEY,
    userID bigint NOT NULL UNIQUE,
    chatID bigint NOT NULL UNIQUE,
    createdAt timestamp with time zone NOT NULL,
    updatedAt timestamp with time zone NOT NULL
);

CREATE TABLE IF NOT EXISTS news (
    id serial NOT NULL PRIMARY KEY,
    header varchar(100) NOT NULL,
    text varchar(255) NOT NULL,
    authorID bigint NOT NULL,
    createdAt timestamp with time zone NOT NULL
);

CREATE TABLE IF NOT EXISTS staff (
    id serial NOT NULL PRIMARY KEY,
    name varchar(255) NOT NULL,
    surname varchar(255) NOT NULL,
    phone varchar(12) NOT NULL, -- формат с +7
    isEmployed boolean NOT NULL
);

CREATE TABLE IF NOT EXISTS "userss" (
    id integer NOT NULL PRIMARY KEY,
    phone varchar(12) NOT NULL, -- формат с +7
    telegramID varchar(100) NOT NULL,
    roleID bigint NOT NULL DEFAULT 2, -- default обычный пользователь
    staffID bigint NOT NULL
);

CREATE TABLE IF NOT EXISTS "logs" (
	"id" serial NOT NULL PRIMARY KEY,
	"userID" bigint NOT NULL,
	"commandID" bigint NOT NULL,
	"createdAt" timestamp with time zone NOT NULL
);

CREATE TABLE IF NOT EXISTS "commands" (
	"id" serial NOT NULL PRIMARY KEY,
	"description" varchar(100) NOT NULL
);

ALTER TABLE "logs" ADD CONSTRAINT "logs_fk1" FOREIGN KEY ("userID") REFERENCES "users"("id");
ALTER TABLE "logs" ADD CONSTRAINT "logs_fk2" FOREIGN KEY ("commandID") REFERENCES "commands"("id");

CREATE INDEX IF NOT EXISTS "users_logs_hash_idx" ON "logs" USING HASH ("userID");
CREATE INDEX IF NOT EXISTS "users_logs_times_hash_idx" ON "logs"("createdAt");

CREATE INDEX IF NOT EXISTS "users_telegramID_hash_idx" ON "userss" USING HASH (telegramID);
CREATE INDEX IF NOT EXISTS "users_phoneNumber_idx" ON "userss" (phone);
CREATE INDEX IF NOT EXISTS "staff_phoneNumber_idx" ON "staff" (phone);


ALTER TABLE chats_erGPT ADD CONSTRAINT "chats_erGPT_fk1" FOREIGN KEY (userID) REFERENCES userss(id);
ALTER TABLE news ADD CONSTRAINT "news_fk3" FOREIGN KEY (authorID) REFERENCES userss(id);
ALTER TABLE userss ADD CONSTRAINT "users_fk5" FOREIGN KEY (roleID) REFERENCES roles(id);
ALTER TABLE userss ADD CONSTRAINT "users_fk6" FOREIGN KEY (staffID) REFERENCES staff(id);


INSERT INTO roles(description) VALUES('Admin');
INSERT INTO roles(description) VALUES('Default');