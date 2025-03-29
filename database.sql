-- Tạo database nếu chưa có
CREATE DATABASE IF NOT EXISTS discordbot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Sử dụng database vừa tạo
USE discordbot;

-- Tạo bảng lưu thông tin kênh được chỉ định cho từng guild
CREATE TABLE IF NOT EXISTS guild_settings (
    guild_id BIGINT PRIMARY KEY,
    channel_id BIGINT NOT NULL
);
