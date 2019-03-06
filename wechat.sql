SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;
-- ----------------------------
-- Table structure for wechat_article
-- ----------------------------
DROP TABLE IF EXISTS `wechat_article`;

CREATE TABLE `wechat_article` (
	`id` INT (11) NOT NULL AUTO_INCREMENT COMMENT '主键',
	`search_name` VARCHAR (200) DEFAULT '' COMMENT '搜索名称',
	`title` VARCHAR (500) DEFAULT '' COMMENT '文章标题',
	`digest` VARCHAR (2550) DEFAULT '' COMMENT '文章摘要',
	`wechat_name` VARCHAR (200) DEFAULT NULL COMMENT '文章公众号名称',
	`url` VARCHAR (2550) DEFAULT '' COMMENT '文章URL',
	`article_html` LONGTEXT NOT NULL COMMENT '文章富文本内容',
	`content` LONGTEXT COMMENT '文章内容',
	`article_timestamp` VARCHAR (100) DEFAULT '' COMMENT '文章时间戳',
	`search_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP () COMMENT '搜索时间',
	`article_rich_media` LONGTEXT DEFAULT NULL COMMENT '文章富文本内容<div id="js_article" class="rich_media">',
	PRIMARY KEY (`id`) USING BTREE
) ENGINE = INNODB AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8mb4 ROW_FORMAT = COMPACT;

SET FOREIGN_KEY_CHECKS = 1;

-- alter table wechat_article add `article_rich_media` LONGTEXT DEFAULT NULL COMMENT '文章富文本内容<div id="js_article" class="rich_media">';