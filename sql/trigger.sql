CREATE TABLE user_log_before (
    user_id BIGINT,
    login VARCHAR(255),
    gravatar_id VARCHAR(255),
    url VARCHAR(255),
    avatar_url VARCHAR(255),
    status VARCHAR(255),
    log_timestamp TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP(3) PRIMARY KEY
);

CREATE TABLE user_log_after (
    user_id BIGINT,
    login VARCHAR(255),
    gravatar_id VARCHAR(255),
    url VARCHAR(255),
    avatar_url VARCHAR(255),
    status VARCHAR(255),
    log_timestamp TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP(3) PRIMARY KEY
);

DELIMITER //

CREATE TRIGGER before_inserted_users
BEFORE INSERT ON users
FOR EACH ROW
BEGIN
    INSERT INTO user_log_before(user_id, login, gravatar_id, url, avatar_url, status)
    VALUES(NEW.user_id, NEW.login, NEW.gravatar_id, NEW.url, NEW.avatar_url, 'INSERT');
END //

CREATE TRIGGER before_updated_users
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    INSERT INTO user_log_before(user_id, login, gravatar_id, url, avatar_url, status)
    VALUES(OLD.user_id, OLD.login, OLD.gravatar_id, OLD.url, OLD.avatar_url, 'UPDATE');
END //

CREATE TRIGGER before_deleted_users
BEFORE DELETE ON users
FOR EACH ROW
BEGIN
    INSERT INTO user_log_before(user_id, login, gravatar_id, url, avatar_url, status)
    VALUES(OLD.user_id, OLD.login, OLD.gravatar_id, OLD.url, OLD.avatar_url, 'DELETE');
END //

CREATE TRIGGER after_updated_users
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    INSERT INTO user_log_after(user_id, login, gravatar_id, url, avatar_url, status)
    VALUES(NEW.user_id, NEW.login, NEW.gravatar_id, NEW.url, NEW.avatar_url, 'UPDATE');
END //

CREATE TRIGGER after_inserted_users
AFTER INSERT ON users
FOR EACH ROW
BEGIN
    INSERT INTO user_log_after(user_id, login, gravatar_id, url, avatar_url, status)
    VALUES(NEW.user_id, NEW.login, NEW.gravatar_id, NEW.url, NEW.avatar_url, 'INSERT');
END //

CREATE TRIGGER after_deleted_users
AFTER DELETE ON users
FOR EACH ROW
BEGIN
    INSERT INTO user_log_after(user_id, login, gravatar_id, url, avatar_url, status)
    VALUES(OLD.user_id, OLD.login, OLD.gravatar_id, OLD.url, OLD.avatar_url, 'DELETE');
END //

DELIMITER ;



-- insert data
INSERT INTO users (user_id, login, gravatar_id, avatar_url, url) VALUES (1, 'user1', 'gravatar1', 'https://avatar.com/user1', 'https://api.user1.com');
INSERT INTO users (user_id, login, gravatar_id, avatar_url, url) VALUES (2, 'user2', 'gravatar2', 'https://avatar.com/user2', 'https://api.user2.com');
INSERT INTO users (user_id, login, gravatar_id, avatar_url) VALUES (3, 'user3', 'gravatar3', 'https://avatar.com/user3');
INSERT INTO users (user_id, login, gravatar_id) VALUES (4, 'user4', 'gravatar4');
INSERT INTO users (user_id, login, avatar_url, url) VALUES (5, 'user5', 'https://avatar.com/user5', 'https://api.user5.com');
INSERT INTO users (user_id, login) VALUES (6, 'user6');
INSERT INTO users (user_id, login, gravatar_id, avatar_url, url) VALUES (7, 'user7', 'gravatar7', 'https://avatar.com/user7', 'https://api.user7.com');
INSERT INTO users (user_id, login, avatar_url) VALUES (8, 'user8', 'https://avatar.com/user8');
INSERT INTO users (user_id, login, gravatar_id, url) VALUES (9, 'user9', 'gravatar9', 'https://api.user9.com');
INSERT INTO users (user_id, login, gravatar_id, avatar_url, url) VALUES (10, 'user10', 'gravatar10', 'https://avatar.com/user10', 'https://api.user10.com');



-- update data
UPDATE users SET login = 'new_user1' WHERE user_id = 1;
UPDATE users SET avatar_url = 'https://newavatar.com/user2' WHERE user_id = 2;
UPDATE users SET gravatar_id = 'new_gravatar3', url = 'https://newapi.user3.com' WHERE user_id = 3;
UPDATE users SET login = 'updated_user4', avatar_url = 'https://avatar.com/updated4' WHERE user_id = 4;
UPDATE users SET url = 'https://api.updated5.com' WHERE login = 'user5';
UPDATE users SET gravatar_id = NULL WHERE user_id = 6;
UPDATE users SET login = 'user7_updated', avatar_url = 'https://avatar.com/user7new' WHERE user_id = 7;
UPDATE users SET url = NULL, gravatar_id = 'gravatar8new' WHERE user_id = 8;
UPDATE users SET login = 'user9_new', avatar_url = 'https://avatar.com/user9new', url = 'https://api.user9new.com' WHERE user_id = 9;
UPDATE users SET gravatar_id = 'gravatar10_updated' WHERE login = 'user10';

-- delete data
DELETE FROM users WHERE user_id = 1;
DELETE FROM users WHERE login = 'user2';
DELETE FROM users WHERE gravatar_id = 'gravatar3';

-- Generating 100 random SQL queries for the users table
-- Schema: user_id (bigint), login (varchar(255)), gravatar_id (varchar(255)), url (varchar(255)), avatar_url (varchar(255))

-- INSERT Queries (60)
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (123456789, 'user_abc123', 'gravatar_abc123', 'https://api.abc123.com', 'https://avatar.com/abc123');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (987654321, 'john_doe', NULL, 'https://john.doe.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (456789123, 'jane_smith', 'gravatar_js789', NULL, 'https://avatar.com/js789');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (321654987, 'cool_user', 'gravatar_cu456', 'https://api.cooluser.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (789123456, 'test_user1', NULL, NULL, 'https://avatar.com/test1');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (147258369, 'random_guy', 'gravatar_rg147', 'https://api.randomguy.com', 'https://avatar.com/rg147');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (258369147, 'alice_w', NULL, 'https://alice.w.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (369147258, 'bob_m', 'gravatar_bm369', NULL, 'https://avatar.com/bm369');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (741852963, 'emma_k', 'gravatar_ek741', 'https://api.emmak.com', 'https://avatar.com/ek741');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (852963741, 'david_p', NULL, NULL, NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (963741852, 'sophia_l', 'gravatar_sl963', 'https://api.sophial.com', 'https://avatar.com/sl963');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (159753486, 'mike_t', NULL, 'https://mike.t.com', 'https://avatar.com/mt159');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (753159486, 'olivia_r', 'gravatar_or753', NULL, 'https://avatar.com/or753');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (486159753, 'liam_n', NULL, 'https://api.liamn.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (951357852, 'noah_b', 'gravatar_nb951', 'https://api.noahb.com', 'https://avatar.com/nb951');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (357852951, 'ava_c', NULL, NULL, 'https://avatar.com/ac357');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (258741963, 'william_h', 'gravatar_wh258', 'https://api.williamh.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (147963852, 'isabella_s', NULL, 'https://api.isabellas.com', 'https://avatar.com/is147');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (369852741, 'james_d', 'gravatar_jd369', NULL, NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (741369852, 'mia_f', NULL, 'https://api.miaf.com', 'https://avatar.com/mf741');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (852741369, 'charlotte_g', 'gravatar_cg852', 'https://api.charlotteg.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (963852741, 'benjamin_e', NULL, NULL, 'https://avatar.com/be963');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (123789456, 'amelia_v', 'gravatar_av123', 'https://api.ameliav.com', 'https://avatar.com/av123');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (456123789, 'harper_z', NULL, 'https://api.harperz.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (789456123, 'evelyn_q', 'gravatar_eq789', NULL, 'https://avatar.com/eq789');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (321789456, 'lucas_y', NULL, 'https://api.lucasy.com', 'https://avatar.com/ly321');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (654321789, 'aria_x', 'gravatar_ax654', NULL, NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (987123456, 'henry_u', NULL, 'https://api.henryu.com', 'https://avatar.com/hu987');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (147852369, 'ella_i', 'gravatar_ei147', 'https://api.ellai.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (258963741, 'alexander_o', NULL, NULL, 'https://avatar.com/ao258');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (369741852, 'sofia_p', 'gravatar_sp369', 'https://api.sofiap.com', 'https://avatar.com/sp369');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (741258963, 'daniel_k', NULL, 'https://api.danielk.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (852369741, 'grace_m', 'gravatar_gm852', NULL, 'https://avatar.com/gm852');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (963147258, 'jack_r', NULL, 'https://api.jackr.com', 'https://avatar.com/jr963');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (159852741, 'chloe_t', 'gravatar_ct159', NULL, NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (753951486, 'logan_w', NULL, 'https://api.loganw.com', 'https://avatar.com/lw753');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (486753951, 'lily_b', 'gravatar_lb486', 'https://api.lilyb.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (951486753, 'ethan_j', NULL, NULL, 'https://avatar.com/ej951');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (357951486, 'zoe_n', 'gravatar_zn357', 'https://api.zoen.com', 'https://avatar.com/zn357');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (258147963, 'mason_c', NULL, 'https://api.masonc.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (147369852, 'ava_k', 'gravatar_ak147', NULL, 'https://avatar.com/ak147');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (369852147, 'oliver_s', NULL, 'https://api.olivers.com', 'https://avatar.com/os369');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (741963258, 'emma_d', 'gravatar_ed741', NULL, NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (852741963, 'liam_p', NULL, 'https://api.liamp.com', 'https://avatar.com/lp852');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (963258741, 'sophia_m', 'gravatar_sm963', 'https://api.sophiam.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (123654789, 'noah_t', NULL, NULL, 'https://avatar.com/nt123');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (456987123, 'mia_r', 'gravatar_mr456', 'https://api.miar.com', 'https://avatar.com/mr456');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (789321456, 'james_l', NULL, 'https://api.jamesl.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (321456789, 'isabella_w', 'gravatar_iw321', NULL, 'https://avatar.com/iw321');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (654789123, 'william_z', NULL, 'https://api.williamz.com', 'https://avatar.com/wz654');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (987456321, 'charlotte_y', 'gravatar_cy987', NULL, NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (147123789, 'benjamin_u', NULL, 'https://api.benjaminu.com', 'https://avatar.com/bu147');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (258789456, 'amelia_q', 'gravatar_aq258', 'https://api.ameliaq.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (369456123, 'henry_i', NULL, NULL, 'https://avatar.com/hi369');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (741789456, 'ava_o', 'gravatar_ao741', 'https://api.avao.com', 'https://avatar.com/ao741');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (852123789, 'lucas_p', NULL, 'https://api.lucasp.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (963456789, 'harper_t', 'gravatar_ht963', NULL, 'https://avatar.com/ht963');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (123789654, 'evelyn_s', NULL, 'https://api.evelyns.com', 'https://avatar.com/es123');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (456123987, 'mason_r', 'gravatar_mr456', NULL, NULL);

-- UPDATE Queries (30)
UPDATE users SET login = 'new_john_doe', url = 'https://new.john.doe.com' WHERE user_id = 987654321;
UPDATE users SET gravatar_id = 'new_gravatar_js789', avatar_url = 'https://newavatar.com/js789' WHERE user_id = 456789123;
UPDATE users SET url = NULL, avatar_url = 'https://avatar.com/cu456' WHERE user_id = 321654987;
UPDATE users SET login = 'updated_test_user1', gravatar_id = NULL WHERE user_id = 789123456;
UPDATE users SET avatar_url = 'https://avatar.com/rg147_new' WHERE user_id = 147258369;
UPDATE users SET login = 'alice_w_updated', url = 'https://new.alice.w.com' WHERE user_id = 258369147;
UPDATE users SET gravatar_id = 'new_gravatar_bm369' WHERE user_id = 369147258;
UPDATE users SET url = 'https://new.emmak.com', avatar_url = NULL WHERE user_id = 741852963;
UPDATE users SET login = 'david_p_new' WHERE user_id = 852963741;
UPDATE users SET gravatar_id = NULL, url = 'https://new.sophial.com' WHERE user_id = 963741852;
UPDATE users SET avatar_url = 'https://avatar.com/mt159_new' WHERE user_id = 159753486;
UPDATE users SET login = 'olivia_r_updated', url = NULL WHERE user_id = 753159486;
UPDATE users SET gravatar_id = 'new_gravatar_nb951' WHERE user_id = 951357852;
UPDATE users SET url = 'https://new.avao.com', avatar_url = 'https://avatar.com/ao741_new' WHERE user_id = 741789456;
UPDATE users SET login = 'lucas_p_new' WHERE user_id = 852123789;
UPDATE users SET gravatar_id = NULL, avatar_url = 'https://avatar.com/ht963_new' WHERE user_id = 963456789;
UPDATE users SET url = 'https://new.evelyns.com' WHERE user_id = 123789654;
UPDATE users SET login = 'mason_r_updated', gravatar_id = 'new_gravatar_mr456' WHERE user_id = 456123987;
UPDATE users SET avatar_url = NULL WHERE user_id = 789321456;
UPDATE users SET login = 'isabella_w_new', url = 'https://new.isabellaw.com' WHERE user_id = 321456789;
UPDATE users SET gravatar_id = 'new_gravatar_wz654' WHERE user_id = 654789123;
UPDATE users SET url = NULL, avatar_url = 'https://avatar.com/cy987_new' WHERE user_id = 987456321;
UPDATE users SET login = 'benjamin_u_updated' WHERE user_id = 147123789;
UPDATE users SET gravatar_id = NULL, url = 'https://new.ameliaq.com' WHERE user_id = 258789456;
UPDATE users SET avatar_url = 'https://avatar.com/hi369_new' WHERE user_id = 369456123;
UPDATE users SET login = 'ava_o_new', url = 'https://new.avao.com' WHERE user_id = 741789456;
UPDATE users SET gravatar_id = 'new_gravatar_lp852' WHERE user_id = 852123789;
UPDATE users SET url = NULL, avatar_url = 'https://avatar.com/sm963_new' WHERE user_id = 963258741;
UPDATE users SET login = 'noah_t_updated' WHERE user_id = 123654789;
UPDATE users SET gravatar_id = NULL, url = 'https://new.miar.com' WHERE user_id = 456987123;

-- DELETE Queries (10)
DELETE FROM users WHERE user_id = 123456789;
DELETE FROM users WHERE user_id = 258369147;
DELETE FROM users WHERE user_id = 741852963;
DELETE FROM users WHERE user_id = 159753486;
DELETE FROM users WHERE user_id = 951357852;
DELETE FROM users WHERE user_id = 258147963;
DELETE FROM users WHERE user_id = 369852147;
DELETE FROM users WHERE user_id = 963456789;
DELETE FROM users WHERE user_id = 456123987;
DELETE FROM users WHERE user_id = 789321456;







-- Generating 200 random SQL queries for the users table
-- Schema: user_id (bigint), login (varchar(255)), gravatar_id (varchar(255)), url (varchar(255)), avatar_url (varchar(255))

-- INSERT Queries (120)
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000001, 'user_alpha1', 'gravatar_al1', 'https://api.alpha1.com', 'https://avatar.com/al1');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000002, 'emma_wilson', NULL, 'https://emma.wilson.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000003, 'liam_jones', 'gravatar_lj3', NULL, 'https://avatar.com/lj3');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000004, 'olivia_brown', 'gravatar_ob4', 'https://api.oliviab.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000005, 'noah_davis', NULL, NULL, 'https://avatar.com/nd5');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000006, 'ava_martin', 'gravatar_am6', 'https://api.avam.com', 'https://avatar.com/am6');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000007, 'sophia_garcia', NULL, 'https://sophia.garcia.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000008, 'mason_lee', 'gravatar_ml8', NULL, 'https://avatar.com/ml8');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000009, 'isabella_walker', 'gravatar_iw9', 'https://api.isabellaw.com', 'https://avatar.com/iw9');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000010, 'william_hall', NULL, NULL, NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000011, 'charlotte_moore', 'gravatar_cm11', 'https://api.charlottem.com', 'https://avatar.com/cm11');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000012, 'james_taylor', NULL, 'https://james.taylor.com', 'https://avatar.com/jt12');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000013, 'mia_anderson', 'gravatar_ma13', NULL, NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000014, 'benjamin_thomas', NULL, 'https://api.benjamint.com', 'https://avatar.com/bt14');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000015, 'harper_jackson', 'gravatar_hj15', 'https://api.harperj.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000016, 'evelyn_white', NULL, NULL, 'https://avatar.com/ew16');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000017, 'lucas_harris', 'gravatar_lh17', 'https://api.lucash.com', 'https://avatar.com/lh17');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000018, 'aria_clark', NULL, 'https://aria.clark.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000019, 'henry_lewis', 'gravatar_hl19', NULL, 'https://avatar.com/hl19');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000020, 'amelia_robinson', NULL, 'https://api.ameliar.com', 'https://avatar.com/ar20');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000021, 'alexander_wright', 'gravatar_aw21', NULL, NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000022, 'sofia_king', NULL, 'https://api.sofiak.com', 'https://avatar.com/sk22');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000023, 'daniel_scott', 'gravatar_ds23', 'https://api.daniels.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000024, 'grace_green', NULL, NULL, 'https://avatar.com/gg24');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000025, 'jack_adams', 'gravatar_ja25', 'https://api.jacka.com', 'https://avatar.com/ja25');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000026, 'chloe_baker', NULL, 'https://chloe.baker.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000027, 'logan_mitchell', 'gravatar_lm27', NULL, 'https://avatar.com/lm27');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000028, 'lily_carter', NULL, 'https://api.lilyc.com', 'https://avatar.com/lc28');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000029, 'ethan_perez', 'gravatar_ep29', NULL, NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000030, 'zoe_murphy', NULL, 'https://api.zoem.com', 'https://avatar.com/zm30');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000031, 'mason_rivera', 'gravatar_mr31', 'https://api.masonr.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000032, 'ella_cooper', NULL, NULL, 'https://avatar.com/ec32');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000033, 'oliver_bailey', 'gravatar_ob33', 'https://api.oliverb.com', 'https://avatar.com/ob33');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000034, 'ava_reed', NULL, 'https://ava.reed.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000035, 'lucas_cook', 'gravatar_lc35', NULL, 'https://avatar.com/lc35');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000036, 'mia_morgan', NULL, 'https://api.miam.com', 'https://avatar.com/mm36');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000037, 'james_bell', 'gravatar_jb37', NULL, NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000038, 'isabella_murphy', NULL, 'https://api.isabellam.com', 'https://avatar.com/im38');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000039, 'william_russell', 'gravatar_wr39', 'https://api.williamr.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000040, 'charlotte_ross', NULL, NULL, 'https://avatar.com/cr40');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000041, 'benjamin_howard', 'gravatar_bh41', 'https://api.benjaminh.com', 'https://avatar.com/bh41');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000042, 'mia_turner', NULL, 'https://mia.turner.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000043, 'henry_ward', 'gravatar_hw43', NULL, 'https://avatar.com/hw43');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000044, 'amelia_brooks', NULL, 'https://api.ameliab.com', 'https://avatar.com/ab44');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000045, 'alexander_hill', 'gravatar_ah45', NULL, NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000046, 'sofia_butler', NULL, 'https://api.sofiab.com', 'https://avatar.com/sb46');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000047, 'daniel_barnes', 'gravatar_db47', 'https://api.danielb.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000048, 'grace_foster', NULL, NULL, 'https://avatar.com/gf48');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000049, 'jack_kelly', 'gravatar_jk49', 'https://api.jackk.com', 'https://avatar.com/jk49');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000050, 'chloe_price', NULL, 'https://chloe.price.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000051, 'logan_gray', 'gravatar_lg51', NULL, 'https://avatar.com/lg51');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000052, 'lily_hughes', NULL, 'https://api.lilyh.com', 'https://avatar.com/lh52');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000053, 'ethan_long', 'gravatar_el53', NULL, NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000054, 'zoe_morris', NULL, 'https://api.zoem.com', 'https://avatar.com/zm54');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000055, 'mason_bennett', 'gravatar_mb55', 'https://api.masonb.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000056, 'ella_rogers', NULL, NULL, 'https://avatar.com/er56');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000057, 'oliver_simmons', 'gravatar_os57', 'https://api.olivers.com', 'https://avatar.com/os57');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000058, 'ava_cox', NULL, 'https://ava.cox.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000059, 'lucas_reynolds', 'gravatar_lr59', NULL, 'https://avatar.com/lr59');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000060, 'mia_sanders', NULL, 'https://api.mias.com', 'https://avatar.com/ms60');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000061, 'james_perry', 'gravatar_jp61', NULL, NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000062, 'isabella_butler', NULL, 'https://api.isabellab.com', 'https://avatar.com/ib62');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000063, 'william_coleman', 'gravatar_wc63', 'https://api.williamc.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000064, 'charlotte_jenkins', NULL, NULL, 'https://avatar.com/cj64');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000065, 'benjamin_griffin', 'gravatar_bg65', 'https://api.benjaming.com', 'https://avatar.com/bg65');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000066, 'mia_wallace', NULL, 'https://mia.wallace.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000067, 'henry_bishop', 'gravatar_hb67', NULL, 'https://avatar.com/hb67');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000068, 'amelia_campbell', NULL, 'https://api.ameliac.com', 'https://avatar.com/ac68');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000069, 'alexander_myers', 'gravatar_am69', NULL, NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000070, 'sofia_henderson', NULL, 'https://api.sofiah.com', 'https://avatar.com/sh70');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000071, 'daniel_ellis', 'gravatar_de71', 'https://api.daniele.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000072, 'grace_graham', NULL, NULL, 'https://avatar.com/gg72');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000073, 'jack_harrison', 'gravatar_jh73', 'https://api.jackh.com', 'https://avatar.com/jh73');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000074, 'chloe_stewart', NULL, 'https://chloe.stewart.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000075, 'logan_watson', 'gravatar_lw75', NULL, 'https://avatar.com/lw75');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000076, 'lily_hudson', NULL, 'https://api.lilyh.com', 'https://avatar.com/lh76');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000077, 'ethan_richards', 'gravatar_er77', NULL, NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000078, 'zoe_dixon', NULL, 'https://api.zoed.com', 'https://avatar.com/zd78');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000079, 'mason_hunt', 'gravatar_mh79', 'https://api.masonh.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000080, 'ella_murray', NULL, NULL, 'https://avatar.com/em80');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000081, 'user_beta81', 'gravatar_bt81', 'https://api.beta81.com', 'https://avatar.com/bt81');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000082, 'oliver_spencer', NULL, 'https://oliver.spencer.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000083, 'ava_fisher', 'gravatar_af83', NULL, 'https://avatar.com/af83');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000084, 'lucas_harper', NULL, 'https://api.lucash.com', 'https://avatar.com/lh84');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000085, 'mia_knight', 'gravatar_mk85', NULL, NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000086, 'james_owens', NULL, 'https://api.jameso.com', 'https://avatar.com/jo86');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000087, 'isabella_hart', 'gravatar_ih87', 'https://api.isabellah.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000088, 'william_larson', NULL, NULL, 'https://avatar.com/wl88');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000089, 'charlotte_mills', 'gravatar_cm89', 'https://api.charlottem.com', 'https://avatar.com/cm89');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000090, 'benjamin_carroll', NULL, 'https://benjamin.carroll.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000091, 'mia_hansen', 'gravatar_mh91', NULL, 'https://avatar.com/mh91');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000092, 'henry_gardner', NULL, 'https://api.henryg.com', 'https://avatar.com/hg92');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000093, 'amelia_wheeler', 'gravatar_aw93', NULL, NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000094, 'alexander_mason', NULL, 'https://api.alexanderm.com', 'https://avatar.com/am94');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000095, 'sofia_duncan', 'gravatar_sd95', 'https://api.sofiad.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000096, 'daniel_harvey', NULL, NULL, 'https://avatar.com/dh96');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000097, 'grace_ferguson', 'gravatar_gf97', 'https://api.gracef.com', 'https://avatar.com/gf97');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000098, 'jack_holmes', NULL, 'https://jack.holmes.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000099, 'chloe_gibson', 'gravatar_cg99', NULL, 'https://avatar.com/cg99');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000100, 'logan_welch', NULL, 'https://api.loganw.com', 'https://avatar.com/lw100');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000101, 'lily_burke', 'gravatar_lb101', NULL, NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000102, 'ethan_hunter', NULL, 'https://api.ethanh.com', 'https://avatar.com/eh102');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000103, 'zoe_mcdonald', 'gravatar_zm103', 'https://api.zoem.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000104, 'mason_sullivan', NULL, NULL, 'https://avatar.com/ms104');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000105, 'ella_rice', 'gravatar_er105', 'https://api.ellar.com', 'https://avatar.com/er105');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000106, 'oliver_schmidt', NULL, 'https://oliver.schmidt.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000107, 'ava_weaver', 'gravatar_aw107', NULL, 'https://avatar.com/aw107');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000108, 'lucas_hicks', NULL, 'https://api.lucash.com', 'https://avatar.com/lh108');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000109, 'mia_barrett', 'gravatar_mb109', NULL, NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000110, 'james_morrison', NULL, 'https://api.jamesm.com', 'https://avatar.com/jm110');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000111, 'isabella_hawkins', 'gravatar_ih111', 'https://api.isabellah.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000112, 'william_dunn', NULL, NULL, 'https://avatar.com/wd112');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000113, 'charlotte_lawson', 'gravatar_cl113', 'https://api.charlottel.com', 'https://avatar.com/cl113');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000114, 'benjamin_olson', NULL, 'https://benjamin.olson.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000115, 'mia_schneider', 'gravatar_ms115', NULL, 'https://avatar.com/ms115');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000116, 'henry_gordon', NULL, 'https://api.henryg.com', 'https://avatar.com/hg116');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000117, 'amelia_watts', 'gravatar_aw117', NULL, NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000118, 'alexander_bates', NULL, 'https://api.alexanderb.com', 'https://avatar.com/ab118');
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000119, 'sofia_ortiz', 'gravatar_so119', 'https://api.sofiao.com', NULL);
INSERT INTO users (user_id, login, gravatar_id, url, avatar_url) VALUES (100000120, 'daniel_silva', NULL, NULL, 'https://avatar.com/ds120');

-- UPDATE Queries (60)
UPDATE users SET login = 'new_emma_wilson', url = 'https://new.emma.wilson.com' WHERE user_id = 100000002;
UPDATE users SET gravatar_id = 'new_gravatar_lj3', avatar_url = 'https://newavatar.com/lj3' WHERE user_id = 100000003;
UPDATE users SET url = NULL, avatar_url = 'https://avatar.com/ob4_new' WHERE user_id = 100000004;
UPDATE users SET login = 'updated_noah_davis', gravatar_id = NULL WHERE user_id = 100000005;
UPDATE users SET avatar_url = 'https://avatar.com/am6_new' WHERE user_id = 100000006;
UPDATE users SET login = 'sophia_garcia_updated', url = 'https://new.sophia.garcia.com' WHERE user_id = 100000007;
UPDATE users SET gravatar_id = 'new_gravatar_ml8' WHERE user_id = 100000008;
UPDATE users SET url = 'https://new.isabellaw.com', avatar_url = NULL WHERE user_id = 100000009;
UPDATE users SET login = 'william_hall_new' WHERE user_id = 100000010;
UPDATE users SET gravatar_id = NULL, url = 'https://new.charlottem.com' WHERE user_id = 100000011;
UPDATE users SET avatar_url = 'https://avatar.com/jt12_new' WHERE user_id = 100000012;
UPDATE users SET login = 'mia_anderson_updated', url = NULL WHERE user_id = 100000013;
UPDATE users SET gravatar_id = 'new_gravatar_bt14' WHERE user_id = 100000014;
UPDATE users SET url = 'https://new.harperj.com', avatar_url = 'https://avatar.com/hj15_new' WHERE user_id = 100000015;
UPDATE users SET login = 'evelyn_white_new' WHERE user_id = 100000016;
UPDATE users SET gravatar_id = NULL, avatar_url = 'https://avatar.com/lh17_new' WHERE user_id = 100000017;
UPDATE users SET url = 'https://new.aria.clark.com' WHERE user_id = 100000018;
UPDATE users SET login = 'henry_lewis_updated', gravatar_id = 'new_gravatar_hl19' WHERE user_id = 100000019;
UPDATE users SET avatar_url = NULL WHERE user_id = 100000020;
UPDATE users SET login = 'alexander_wright_new', url = 'https://new.alexanderw.com' WHERE user_id = 100000021;
UPDATE users SET gravatar_id = 'new_gravatar_sk22' WHERE user_id = 100000022;
UPDATE users SET url = NULL, avatar_url = 'https://avatar.com/ds23_new' WHERE user_id = 100000023;
UPDATE users SET login = 'grace_green_updated' WHERE user_id = 100000024;
UPDATE users SET gravatar_id = NULL, url = 'https://new.jacka.com' WHERE user_id = 100000025;
UPDATE users SET avatar_url = 'https://avatar.com/cb26_new' WHERE user_id = 100000026;
UPDATE users SET login = 'logan_mitchell_new', url = 'https://new.loganm.com' WHERE user_id = 100000027;
UPDATE users SET gravatar_id = 'new_gravatar_lc28' WHERE user_id = 100000028;
UPDATE users SET url = NULL, avatar_url = 'https://avatar.com/ep29_new' WHERE user_id = 100000029;
UPDATE users SET login = 'zoe_murphy_updated' WHERE user_id = 100000030;
UPDATE users SET gravatar_id = NULL, url = 'https://new.masonr.com' WHERE user_id = 100000031;
UPDATE users SET avatar_url = 'https://avatar.com/ec32_new' WHERE user_id = 100000032;
UPDATE users SET login = 'oliver_bailey_new', url = 'https://new.oliverb.com' WHERE user_id = 100000033;
UPDATE users SET gravatar_id = 'new_gravatar_av34' WHERE user_id = 100000034;
UPDATE users SET url = NULL, avatar_url = 'https://avatar.com/lc35_new' WHERE user_id = 100000035;
UPDATE users SET login = 'mia_morgan_updated' WHERE user_id = 100000036;
UPDATE users SET gravatar_id = NULL, url = 'https://new.jamesb.com' WHERE user_id = 100000037;
UPDATE users SET avatar_url = 'https://avatar.com/im38_new' WHERE user_id = 100000038;
UPDATE users SET login = 'william_russell_new', url = 'https://new.williamr.com' WHERE user_id = 100000039;
UPDATE users SET gravatar_id = 'new_gravatar_cr40' WHERE user_id = 100000040;
UPDATE users SET url = NULL, avatar_url = 'https://avatar.com/bh41_new' WHERE user_id = 100000041;
UPDATE users SET login = 'mia_turner_updated' WHERE user_id = 100000042;
UPDATE users SET gravatar_id = NULL, url = 'https://new.henryw.com' WHERE user_id = 100000043;
UPDATE users SET avatar_url = 'https://avatar.com/ab44_new' WHERE user_id = 100000044;
UPDATE users SET login = 'alexander_hill_new', url = 'https://new.alexanderh.com' WHERE user_id = 100000045;
UPDATE users SET gravatar_id = 'new_gravatar_sb46' WHERE user_id = 100000046;
UPDATE users SET url = NULL, avatar_url = 'https://avatar.com/db47_new' WHERE user_id = 100000047;
UPDATE users SET login = 'grace_foster_updated' WHERE user_id = 100000048;
UPDATE users SET gravatar_id = NULL, url = 'https://new.jackk.com' WHERE user_id = 100000049;
UPDATE users SET avatar_url = 'https://avatar.com/cp50_new' WHERE user_id = 100000050;
UPDATE users SET login = 'logan_gray_new', url = 'https://new.logang.com' WHERE user_id = 100000051;
UPDATE users SET gravatar_id = 'new_gravatar_lh52' WHERE user_id = 100000052;
UPDATE users SET url = NULL, avatar_url = 'https://avatar.com/el53_new' WHERE user_id = 100000053;
UPDATE users SET login = 'zoe_morris_updated' WHERE user_id = 100000054;
UPDATE users SET gravatar_id = NULL, url = 'https://new.masonb.com' WHERE user_id = 100000055;
UPDATE users SET avatar_url = 'https://avatar.com/er56_new' WHERE user_id = 100000056;
UPDATE users SET login = 'oliver_simmons_new', url = 'https://new.olivers.com' WHERE user_id = 100000057;
UPDATE users SET gravatar_id = 'new_gravatar_ac58' WHERE user_id = 100000058;
UPDATE users SET url = NULL, avatar_url = 'https://avatar.com/lr59_new' WHERE user_id = 100000059;
UPDATE users SET login = 'mia_sanders_updated' WHERE user_id = 100000060;

-- DELETE Queries (20)
DELETE FROM users WHERE user_id = 100000001;
DELETE FROM users WHERE user_id = 100000006;
DELETE FROM users WHERE user_id = 100000011;
DELETE FROM users WHERE user_id = 100000016;
DELETE FROM users WHERE user_id = 100000021;
DELETE FROM users WHERE user_id = 100000026;
DELETE FROM users WHERE user_id = 100000031;
DELETE FROM users WHERE user_id = 100000036;
DELETE FROM users WHERE user_id = 100000041;
DELETE FROM users WHERE user_id = 100000046;
DELETE FROM users WHERE user_id = 100000051;
DELETE FROM users WHERE user_id = 100000056;
DELETE FROM users WHERE user_id = 100000061;
DELETE FROM users WHERE user_id = 100000066;
DELETE FROM users WHERE user_id = 100000071;
DELETE FROM users WHERE user_id = 100000076;
DELETE FROM users WHERE user_id = 100000081;
DELETE FROM users WHERE user_id = 100000086;
DELETE FROM users WHERE user_id = 100000091;
DELETE FROM users WHERE user_id = 100000096;