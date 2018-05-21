#创建数据表
create database networkip;

#创建数据表
CREATE TABLE IF NOT EXISTS `networkip_tbl`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `ip` VARCHAR(100) DEFAULT NULL,
   `prefix` INT DEFAULT 0,
   `asNumber` INT DEFAULT NULL,
   `asName` VARCHAR(500) DEFAULT NULL,
   `asOrg` VARCHAR(500) DEFAULT NULL,
   `usage` VARCHAR(500) DEFAULT NULL,
   PRIMARY KEY ( `id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

#插入测试数据
INSERT INTO networkip_tbl(ip) VALUES ('1.1.2.4');
INSERT INTO networkip_tbl(`ip`,`usage`,`prefix`) VALUES('25.0.0.0','NET','10')

#删除数据表
drop tabel networkip_tbl;