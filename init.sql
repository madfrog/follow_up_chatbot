use chatbot;

/* 模型服务表 */
DROP TABLE IF EXISTS `chatbot_history`;
CREATE TABLE `chatbot_history` (
        `id` BIGINT(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
        `user_id` VARCHAR(128) NOT NULL COMMENT '用户标识',
        `session_id` VARCHAR(128) NOT NULL COMMENT '会话session',
        `type` TINYINT NOT NULL COMMENT '消息类型：0-AI 1-Human',
        `message` TEXT NOT NULL COMMENT '消息内容',
        `gmt_create` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
        PRIMARY KEY (`id`),
        KEY (`user_id`),
        KEY (`gmt_create`),
        KEY (`type`),
        KEY (`session_id`)
) ENGINE = InnoDB AUTO_INCREMENT = 100 CHARSET = utf8 COMMENT '消息历史表';