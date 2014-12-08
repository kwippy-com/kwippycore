BEGIN;
CREATE TABLE `kwippy_contactus` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `senders_email` varchar(75) NULL,
    `message` longtext NOT NULL,
    `senders_user_id` integer NULL,
    `created_at` datetime NOT NULL
)
;
CREATE TABLE `kwippy_account` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `provider_login` varchar(200) NOT NULL,
    `provider` integer NULL,
    `user_id` integer NULL,
    `registration_type` integer NOT NULL,
    `status` integer NOT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL
)
;
CREATE TABLE `kwippy_page_setting` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL UNIQUE,
    `title` varchar(100) NULL,
    `description` longtext NULL
)
;
CREATE TABLE `kwippy_quip` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `original` longtext NOT NULL,
    `formated` longtext NULL,
    `account_id` integer NOT NULL,
    `primitive_state` varchar(40) NULL,
    `is_filtered` integer NOT NULL,
    `created_at` datetime NOT NULL
)
;
CREATE TABLE `kwippy_user_profile` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL UNIQUE,
    `display_name` varchar(50) NULL,
    `age` integer NULL,
    `gender` integer NULL,
    `about_me` longtext NULL,
    `sexual_tendency` integer NULL,
    `relationship_status` integer NULL,
    `location_city` varchar(200) NULL,
    `location_country` varchar(200) NULL,
    `website` varchar(200) NULL,
    `hash` varchar(20) NOT NULL UNIQUE,
    `media_processed` integer NULL,
    `picture` varchar(100) NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL
)
;
CREATE TABLE `kwippy_favourite` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `quip_id` integer NOT NULL,
    `user_id` integer NOT NULL,
    `created_at` datetime NOT NULL
)
;
CREATE TABLE `kwippy_forgotpassword` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `reset_link` varchar(50) NOT NULL,
    `is_active` bool NOT NULL,
    `created_at` datetime NOT NULL
)
;
CREATE TABLE `kwippy_follower` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `follower_id` integer NOT NULL,
    `followee_id` integer NOT NULL,
    `created_at` datetime NOT NULL
)
;
CREATE TABLE `kwippy_beta_invite` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `email` varchar(75) NOT NULL,
    `sent_email_status` integer NOT NULL,
    `user_id` integer NULL,
    `ip` char(15) NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL
)
;
CREATE TABLE `kwippy_invite` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `invitee_email` varchar(75) NULL,
    `invite_type` integer NOT NULL,
    `unique_hash` varchar(20) NOT NULL UNIQUE,
    `converted_user_id` integer NULL,
    `status` integer NOT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL
)
;
-- The following references should be added but depend on non-existent tables:
-- ALTER TABLE `kwippy_account` ADD CONSTRAINT user_id_refs_id_3abf7e9a FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
-- ALTER TABLE `kwippy_page_setting` ADD CONSTRAINT user_id_refs_id_55ce68b8 FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
-- ALTER TABLE `kwippy_user_profile` ADD CONSTRAINT user_id_refs_id_25f406e3 FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
-- ALTER TABLE `kwippy_favourite` ADD CONSTRAINT user_id_refs_id_60ef4614 FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
-- ALTER TABLE `kwippy_forgotpassword` ADD CONSTRAINT user_id_refs_id_12ce73fc FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
-- ALTER TABLE `kwippy_follower` ADD CONSTRAINT follower_id_refs_id_7d519972 FOREIGN KEY (`follower_id`) REFERENCES `auth_user` (`id`);
-- ALTER TABLE `kwippy_follower` ADD CONSTRAINT followee_id_refs_id_7d519972 FOREIGN KEY (`followee_id`) REFERENCES `auth_user` (`id`);
-- ALTER TABLE `kwippy_beta_invite` ADD CONSTRAINT user_id_refs_id_5d34281b FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
-- ALTER TABLE `kwippy_invite` ADD CONSTRAINT user_id_refs_id_167fea41 FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
-- ALTER TABLE `kwippy_invite` ADD CONSTRAINT converted_user_id_refs_id_167fea41 FOREIGN KEY (`converted_user_id`) REFERENCES `auth_user` (`id`);
-- ALTER TABLE `kwippy_quip` ADD CONSTRAINT account_id_refs_id_6b79eb54 FOREIGN KEY (`account_id`) REFERENCES `kwippy_account` (`id`);
-- ALTER TABLE `kwippy_favourite` ADD CONSTRAINT quip_id_refs_id_32c05a78 FOREIGN KEY (`quip_id`) REFERENCES `kwippy_quip` (`id`);
CREATE INDEX `kwippy_account_user_id` ON `kwippy_account` (`user_id`);
CREATE UNIQUE INDEX `kwippy_page_setting_user_id` ON `kwippy_page_setting` (`user_id`);
CREATE INDEX `kwippy_quip_account_id` ON `kwippy_quip` (`account_id`);
CREATE UNIQUE INDEX `kwippy_user_profile_user_id` ON `kwippy_user_profile` (`user_id`);
CREATE INDEX `kwippy_favourite_quip_id` ON `kwippy_favourite` (`quip_id`);
CREATE INDEX `kwippy_favourite_user_id` ON `kwippy_favourite` (`user_id`);
CREATE INDEX `kwippy_forgotpassword_user_id` ON `kwippy_forgotpassword` (`user_id`);
CREATE INDEX `kwippy_follower_follower_id` ON `kwippy_follower` (`follower_id`);
CREATE INDEX `kwippy_follower_followee_id` ON `kwippy_follower` (`followee_id`);
CREATE INDEX `kwippy_beta_invite_user_id` ON `kwippy_beta_invite` (`user_id`);
CREATE INDEX `kwippy_invite_user_id` ON `kwippy_invite` (`user_id`);
CREATE INDEX `kwippy_invite_converted_user_id` ON `kwippy_invite` (`converted_user_id`);
COMMIT;
